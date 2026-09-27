# Audit — A/B/C Token Cache Benchmark
 
Controlled A/B/C benchmark of prompt caching behavior in the tested Anthropic API environment across three configurations. Run with a real API key and a fresh cache state. The included script can be used to reproduce the test methodology, although exact results may vary by model version, prompt size, and pricing.
 
**Date:** June 6, 2026
**Model:** `claude-sonnet-4-6`
**Script:** [`test-sonnet-cache.py`](./test-sonnet-cache.py)
 
---
 
## Results

| Config | Description | Input Tokens | Cached Tokens | Cost | Cost change vs A |
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
| `claude-sonnet-4-6` | Confirmed | Cache activity observed |
| `claude-haiku-4-5` | **0.0%** | No cache activity observed |
 
In this benchmark environment, Claude Haiku 4.5 showed 0.0% cache activity with the tested `cache_control: ephemeral` configuration, while Claude Sonnet 4.6 showed cache activity. This result is specific to the tested model versions and environment and should not be generalized beyond this benchmark without further verification. 
 
---
 
## What the Day 1 Number Understates
 
The 36.7% figure is the observed cost difference between Config A and Config B in this controlled benchmark. Config C represents the subsequent steady-state cache-hit request and was 35.9% below Config A. Production-scale evidence and modeled longer-term behavior are documented separately.
 
| Mechanism | Effect |
|-----------|--------|
| Write amortization across more reads | Cost per request falls as the same write serves more reads |
| Context architecture refinement | Cached content shrinks over time, hit rate rises |
| Model routing | Eliminates zero-return caching spend on non-supporting models |
 
**May 2026 developer-account evidence:** 97.6% cache read ratio on the May 16 peak day. Across May, 144,011,625 input tokens corresponded to $89.40 in observed token cost versus a $432.03 same-volume uncached input-cost baseline, placing observed cost 79.3% below that calculated baseline.
 
The controlled benchmark isolates the cache-behavior mechanism under the tested conditions. The [case study](../case-study/) documents separate May–June 2026 developer-account evidence.
 
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
 
The comparison among Configs A, B, and C reflects the observed relative behavior in this controlled run. Exact token counts and costs may vary with prompt size, model version, pricing, and API behavior.
 
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
 
- [../case-study/](../case-study/) — Developer-account console evidence (May–June 2026) with screenshots
- [../compounding-model/](../compounding-model/) — Modeled 12-month trajectory using stated assumptions; not observed production evidence
- [../white-paper.md](../white-paper.md) — Broader methodology, analysis, and contextual discussion
