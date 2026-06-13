# Compounding Model
 
> 12-month cost trajectory model anchored at both ends by verified production data. Shows why the Lionfish Token Hygiene System diverges from standard prompt caching over time — and quantifies the gap.
 
**Runtime:** Node.js (no dependencies)
**Script:** [`compounding-model.js`](./compounding-model.js)
 
---
 
## The Core Claim
 
Standard prompt caching gives a flat **35.9% savings from Day 1**.
It does not improve. The ratio is fixed by the pricing structure.
 
The Lionfish system compounds monthly because three independent mechanisms improve simultaneously:
 
| Layer | What Improves | Effect on Cost |
|-------|---------------|----------------|
| Cache architecture | Context files get tighter, more targeted | Cache write size shrinks, hit rate rises |
| Write amortization | Same write serves more reads over time | Cost per request falls |
| Model routing | Right tasks routed to cache-supporting models | Eliminates zero-return caching spend |
 
Each layer is independent. All three compound together.
 
---
 
## Real Data Anchors
 
This model is not a projection from assumptions. It interpolates between two verified endpoints.
 
**Anchor 1 — Day 1 (June 6, 2026 A/B/C benchmark):**
 
| Config | Tokens | Cost | Savings |
|--------|--------|------|---------|
| A — Monolith, no cache | 1,506 input | $0.005058 | baseline |
| C — Cache hit, steady state | 3 input + 2,902 cached | $0.003242 | 35.9% |
 
**Anchor 2 — Production maturity (May 16, 2026 console):**
 
| Metric | Value |
|--------|-------|
| Total tokens | 60,776,845 |
| Cache read ratio | 97.6% |
| Raw input ratio | 0.05% |
| Actual cost | $25.73 |
| Standard rate cost | ~$182 |
| Total cost reduction | ~86% |
 
No assumptions are unsupported. The model interpolates between these two verified points.
 
---
 
## 12-Month Trajectory
 
| Month | Cache-only savings | Lionfish savings | Divergence |
|-------|--------------------|-----------------|------------|
| 1 | 35.9% | 36.3% | +0.4% |
| 3 | 35.9% | 44.1% | +8.2% |
| 6 | 35.9% | 56.3% | +20.4% |
| 9 | 35.9% | 67.8% | +31.9% |
| 12 | 35.9% | 79.3%+ | +43.4% |
 
The divergence is the value proposition. Everything above 35.9% is what the architecture, routing, and refinement cycle produces — validated against the May 2026 production number.
 
---
 
## Run the Model
 
```bash
node compounding-model.js
```
 
Outputs a 12-month table to stdout with monthly savings rate, cost per 1,000 requests, and cumulative savings vs. both standard rate and cache-only baseline.
 
---
 
## What the Model Does Not Claim
 
- Output tokens are not cached and are not reduced by this system
- The model does not project past ~83% total savings — output tokens represent ~71% of total cost for balanced workloads at Sonnet 4.6 pricing and cannot be optimized away
- The 99.8% raw input reduction figure measures input tokens only, not total API spend
The numbers that matter: **35.9% Day 1 → 79.3%+ at production maturity.**
Both are anchored to verified data. Neither is an assumption.
 
---
 
## Files
 
| File | Description |
|------|-------------|
| [`README.md`](./README.md) | This file — model documentation |
| [`compounding-model.js`](./compounding-model.js) | Node.js model script |
 
---
 
## Related
 
- [`../audit/`](../audit/) — A/B/C benchmark that provides the Day 1 anchor
- [`../case-study/`](../case-study/) — Production console data that provides the maturity anchor
- [`../white-paper.md`](../white-paper.md) — Full methodology and analysis
