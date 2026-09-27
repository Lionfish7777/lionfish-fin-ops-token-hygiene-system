# Benchmark Results
 
**Date:** June 6, 2026
**Model:** claude-sonnet-4-6
**Environment:** Fresh API key, no prior cache state
**Script:** `test-sonnet-cache.py`
 
---
 
## Terminal Output
 
```
╔══════════════════════════════════════════════════════════════════╗
║           LIONFISH A/B/C AUDIT TEST                              ║
║               Haiku 4.5 | default-claude-hygiene-audit           ║
║              Sonnet 4.6 | default-claude-hygiene-audit           ║
║         Testing: No Cache vs Cache Write vs Cache Hit            ║
╚══════════════════════════════════════════════════════════════════╝
 
┌─────────────────────────┬─────────────────────────┬───────────┐
│                         │         Tokens          │   Cost    │
├─────────────────────────┼─────────────────────────┼───────────┤
│ A — Monolith (no cache) │ 1,506 input             │ $0.005058 │
├─────────────────────────┼─────────────────────────┼───────────┤
│ B — Arch (cache write)  │ 19 input + 2,902 cached │ $0.003201 │
├─────────────────────────┼─────────────────────────┼───────────┤
│ C — Arch (cache hit)    │ 3 input + 2,902 cached  │ $0.003242 │
└─────────────────────────┴─────────────────────────┴───────────┘
 
36.3% savings on 2 requests.
At 2,000 requests/month that's $3.63/month saved, $130/year per 3 engineers.
```
> **Normalization note:** The terminal output above records 36.3% savings for that historical run. Using the stored Config A and Config B costs ($0.005058 and $0.003201), the recalculated A → B cost difference is 36.7%. The README uses the recalculated 36.7% figure while preserving the original terminal output above unchanged. 
---
 
## Key Findings
 
### Finding 1 — Cache write vs cache hit pricing
 
Config C costs $0.000041 more than Config B despite doing less work.
This is expected and documented Anthropic behavior: cache reads are priced at $0.30/M tokens,
cache writes at $3.75/M tokens. A fresh write costs more than a read.
At any real request volume (10+ calls per context), the cache write amortizes and the
cumulative cost of C runs far below A.
 
**Write amortization breakeven: 2 requests.**
**Write amortization at May 2026 scale (4.84×): significant.**
 
### Finding 2 — Haiku 4.5 cache behavior
 
`claude-haiku-4-5-20251001` returned **0% cache activity** across the configurations tested in this benchmark. The cache-control parameters were structured as intended. Under the same benchmark conditions, `claude-sonnet-4-6` showed cache activity.

These observations are specific to the tested model versions, configuration, and environment. They should not be interpreted as a universal claim about Haiku 4.5 prompt-caching support outside this benchmark.
 
### Finding 3 — Raw input reduction
 
| Metric | Config A | Config C | Change |
|--------|----------|----------|--------|
| Raw input tokens | 1,506 | 3 | **-99.8%** |
| Total cost | $0.005058 | $0.003242 | **-35.9%** |
 
The 99.8% raw input reduction is not the same as 99.8% cost reduction.
Output tokens are not cacheable and represent the dominant cost at steady state.
The correct claim: **99.8% reduction in raw input tokens and 35.9% lower total cost for the tested steady-state cache-hit request compared with Config A.**
 
---
 
## Context for the Controlled Benchmark Result
 
The 35.9% figure is the observed cost difference between Config A and the steady-state Config C request in this controlled benchmark. It should not be treated as a universal production savings rate. Production behavior depends on request volume, cache reuse, context structure, model routing, pricing, and workload characteristics.
 
Additional mechanisms considered in the broader system:
 
| Factor | Effect |
|--------|--------|
| Cache write amortized across more reads | Cost per request falls |
| Arch files refined over time | Cached context shrinks, hit rate rises |
| Model routing (Haiku → Sonnet where cache applies) | Eliminates zero-return caching spend |
| Session-level reuse across multiple users | Same write serves many readers |
 
Separate May 2026 developer-account evidence: the May 16 peak day recorded a 97.6% cache-read ratio. This production evidence is documented in the case study and should be considered separately from the controlled benchmark above.
 
---
 
## Reproduction Instructions
 
```bash
# Install dependency
pip3 install anthropic
 
# Set API key
export ANTHROPIC_API_KEY=your_key_here
 
# Run benchmark
python3 test-sonnet-cache.py
```

The comparison among Configs A, B, and C reflects the observed relative behavior in this controlled run. Exact token counts and costs may vary with prompt size, model version, pricing, and API behavior.
---
 
## Related Files
 
- [`test-sonnet-cache.py`](./test-sonnet-cache.py) — Script that generated these results
- [`before-after-audit.html`](./before-after-audit.html) — Visual token flow comparison
- [`../case-study/`](../case-study/) — Production console data (May 2026)
- [`../compounding-model/compounding-model.js`](../compounding-model/compounding-model.js) — Modeled 12-month trajectory using stated assumptions; not observed production evidence
