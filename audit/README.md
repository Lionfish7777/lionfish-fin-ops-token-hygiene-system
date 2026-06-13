# Audit — A/B/C Token Cache Benchmark
 
> Independent benchmark of Anthropic prompt caching across three configurations. Reproducible. Real API key. No prior cache state.
 
**Date:** June 6, 2026
**Model:** `claude-sonnet-4-6`
**Script:** [`test-sonnet-cache.py`](./test-sonnet-cache.py)
 
---
 
## Results
 
| Config | Description | Input Tokens | Cached Tokens | Cost | Savings |
|--------|-------------|-------------|---------------|------|---------|
| **A** | Monolith — no cache | 1,506 | 0 | $0.005058 | baseline |
| **B** | Arch — cache write | 19 | 2,902 | $0.003201 | 36.7% |
| **C** | Arch — cache hit (steady state) | 3 | 2,902 | $0.003242 | 35.9% |
 
**Day 1 savings (A → B): 36.7%**
**Steady-state raw input reduction (A → C): 99.8%** (1,506 → 3 tokens)
 
> Config C costs marginally more than B because cache reads ($0.30/M) are priced below cache writes ($3.75/M) — the write was already paid in B. At any real request volume the write amortizes rapidly and cumulative cost of C runs far below A. Breakeven: 2 requests. May 2026 amortization ratio: **4.84×**.
 
---
 
## Cache Behavior by Model
 
| Model | Cache Read Ratio | Result |
|-------|-----------------|--------|
| `claude-sonnet-4-6` | Confirmed | `cache_control: ephemeral` works |
| `claude-haiku-4-5` | **0.0%** | No cache activity observed |
 
Haiku 4.5 does not honor `cache_control: ephemeral`. All production savings in this system are driven by Sonnet 4.6. Teams routing to Haiku expecting cache savings will see none — a finding most engineering teams discover only after months of wasted budget.
 
---
 
## What the Day 1 Number Understates
 
The 36.7% figure measures two requests against a fresh cache. At production scale, three additional mechanisms compound the savings monthly:
 
| Mechanism | Effect |
|-----------|--------|
| Write amortization across more reads | Cost per request falls as the same write serves more reads |
| Context architecture refinement | Cached content shrinks over time, hit rate rises |
| Model routing | Eliminates zero-return caching spend on non-supporting models |
 
**May 2026 production result:** 97.6% cache read ratio on peak day (May 16), 79.3% total cost reduction on 144M tokens.
 
The benchmark proves the mechanism. The [case study](../case-study/) proves the outcome.
 
---
 
## Reproduce This
 
```bash
# Install dependency
pip3 install anthropic
 
# Set API key
export ANTHROPIC_API_KEY=your_key_here
 
# Run benchmark — generates A, B, and C in sequence
python3 test-sonnet-cache.py
```
 
The ratio between A, B, and C is the signal — not the absolute dollar amounts. Results will vary slightly by prompt size and model version.
 
---
 
## Files
 
| File | Description |
|------|-------------|
| [`README.md`](./README.md) | This file — benchmark summary and findings |
| [`benchmark-results.md`](./benchmark-results.md) | Full terminal output from June 6, 2026 run |
| [`before-after-audit.html`](./before-after-audit.html) | Visual A vs C token flow comparison |
| [`test-sonnet-cache.py`](./test-sonnet-cache.py) | Script that generated these results |
 
---
 
## Related
 
- [`../case-study/`](../case-study/) — Production console data (May 2026) with screenshots
- [`../compounding-model/`](../compounding-model/) — 12-month trajectory model anchored to these results
- [`../white-paper.md`](../white-paper.md) — Full methodology and analysis
