# The Token Hygiene Imperative
 
## An Engineering Approach to Context Architecture, Prompt Caching, Model Routing, and AI Cost Observability
 
Lionfish7777 | White Paper | June 2026
 
---
 
## Executive Summary

AI application costs can increase even as per-token prices decline when workloads repeatedly process large, unchanged, or unnecessary context.

In May 2026, Lionfish7777 analyzed token usage within our own Claude developer account and developed the Token Hygiene System, an engineering methodology centered on context architecture, prompt caching, model routing, and cost observability.

This white paper documents the problem, the system architecture, developer-account evidence from May 2026, and a controlled A/B/C benchmark conducted in June 2026.

During May 2026, the Lionfish7777 developer account recorded **144,011,625 input tokens** and **$89.40 in observed token cost**. A same-volume uncached input-cost baseline calculated at $3.00 per million input tokens is **$432.03**, placing the observed May cost **79.3% below that calculated baseline**.

On May 16, the account recorded **60,776,845 total tokens**, with **97.6% represented by prompt cache reads**.

Separately, the June 6 controlled benchmark compared three configurations using the same model and content. Config B recorded a **36.7% lower total cost than Config A**, while the steady-state Config C request recorded a **35.9% lower total cost than Config A**. Raw input decreased from **1,506 tokens to 3 tokens** in the Config A-to-C comparison.

These results represent different conditions and should be interpreted separately. They are not a universal savings guarantee. Results depend on model support, request patterns, cache reuse, context structure, model routing, pricing, and workload characteristics.

The next stage of validation is to evaluate the methodology across additional external workloads and environments.
 
---
 
## Section 1: The Problem — Why AI Bills Are Spiraling
 
### 1.1 The Pricing Paradox

Lower per-token pricing does not necessarily produce lower total AI application cost.

Total cost depends on both unit pricing and consumption. As workloads make more model calls, carry larger context windows, or repeatedly process the same or similar information, aggregate token usage can increase even when the price of an individual token declines.

For engineering teams, the relevant question is therefore not only how much a token costs, but how many tokens each workflow processes, how often unchanged context is resent, whether reusable context is cached effectively, and whether workloads are routed appropriately.

This is where token hygiene becomes an architectural concern rather than simply a pricing concern.
 
### 1.2 The Agentic Multiplier

Traditional AI interactions are often relatively bounded: a user sends a prompt, the model responds, and the interaction ends or continues through a limited conversation.

Agentic workflows can change that consumption pattern. Depending on their architecture, agents may:

- make multiple model calls to complete a single task
- carry or reconstruct context across multiple steps
- invoke tools and incorporate their results into subsequent requests
- coordinate multi-step or parallel workflows
- continue operating across longer-running sessions

Each additional model call creates another opportunity for context to be processed. If large amounts of unchanged or unnecessary information are repeatedly included, token consumption can compound across the workflow.

This does not mean agentic systems are inherently inefficient. It means that as AI workflows become longer-running and more autonomous, context architecture, caching behavior, model routing, and cost observability become increasingly important engineering concerns.
 
### 1.3 A Key Engineering Cause: Context Bloat

One controllable source of unnecessary token consumption is context bloat: processing more context than a particular model request requires.

Context bloat can occur when:

- large instruction sets, background material, or documentation are included in requests regardless of whether each element is needed
- unchanged information is repeatedly sent across multiple turns or workflow steps
- reusable context is not structured to take advantage of supported caching mechanisms
- context accumulates across longer-running sessions without sufficient pruning or separation
- teams lack visibility into token composition, cache behavior, model routing, and request-level cost

These patterns do not affect every workload equally. Their impact depends on the application architecture, model behavior, request pattern, context size, cache reuse, and pricing.

Token hygiene treats context as an engineering resource to be measured and deliberately managed rather than an unlimited container for everything a workflow might need.
 
---
 
## Section 2: The Lionfish7777 Investigation — May 2026

### 2.1 Peak-Day Evidence

In May 2026, Lionfish7777 analyzed token consumption across our Claude developer account after observing high aggregate usage. On May 16, the account recorded **60,776,845 total tokens**.

The composition of that activity mattered more than the headline total:

- **59,288,619 prompt cache reads (97.6%)**
- **1,248,486 prompt cache writes (2.1%)**
- **212,153 output tokens (0.3%)**
- **27,587 raw input tokens (0.05%)**

Rather than treating the total as evidence of a single failure mode, we used the account data to investigate how the workload was consuming tokens:

- Which requests were generating raw input?
- How much reusable context was being served through cache reads?
- Where was unchanged or unnecessary context being processed repeatedly?
- How were cache writes, cache reads, raw input, and output contributing differently to cost?
- How could context structure, caching, model routing, and observability be improved?

That investigation helped formalize the Token Hygiene methodology around measuring token composition, structuring context deliberately, using supported caching mechanisms effectively, routing workloads appropriately, and observing cost at the request and workflow level.
 
### 2.2 The Insight

The investigation reinforced a practical engineering principle: repeated context should not automatically be treated the same as fresh input.

Where a model and workload support prompt caching, reusable context can be written once and referenced again under a different pricing structure than uncached input. The exact economics depend on the model, provider pricing, cache behavior, request pattern, and how effectively reusable context is structured.

That makes the architectural question broader than simply “cache more.” The useful questions are:

- Which context is stable enough to reuse?
- Which information should remain dynamic?
- How much context does each request actually need?
- Does the selected model support the intended caching behavior?
- How often is cached context reused before it expires or changes?
- What do cache writes, cache reads, raw input, and output contribute to total cost?

Token Hygiene treats caching as one component of a larger system that also includes context architecture, model routing, and cost observability.
---
 
### 3.1 Overview

The Lionfish7777 Token Hygiene System is an engineering methodology for measuring and improving how AI workloads consume context, use supported caching mechanisms, route requests across models, and expose cost behavior.

The methodology is organized around four complementary components:

1. **Context Architecture** — structure each request around the information it actually needs
2. **Caching Strategy** — identify reusable context and use supported caching mechanisms deliberately
3. **Model Routing** — route workloads to models that fit the task, capability requirements, and intended cache behavior
4. **Cost Observability** — measure token composition, cache activity, routing behavior, and cost so optimization decisions are based on evidence

The objective is not simply to minimize token usage. It is to reduce unnecessary processing while preserving the context, model capability, and output quality required by the workload.

These components are evaluated together because changes in one part of the system can affect the others.
 
### 3.2 Context Architecture

Context architecture determines what information enters each model request, how that information is organized, and how much of it is actually necessary for the task.

Without deliberate context design, a workflow may repeatedly include large instruction sets, background material, prior conversation history, or documentation that a particular request does not need.

Token Hygiene addresses this by separating stable, reusable, and task-specific information so each request can receive the context appropriate to its purpose.

The objective is not to minimize context indiscriminately. It is to reduce unnecessary processing while preserving the information required for model capability, accuracy, and useful output.
 
### 3.3 Caching Strategy

Caching strategy determines which reusable portions of context can be stored and referenced again when the selected model and workload support that behavior.

Repeated context may include system instructions, stable product information, documentation, reference material, or other information that remains unchanged across multiple requests. When that context is repeatedly sent as fresh input, the workload may incur unnecessary processing and cost.

Token Hygiene approaches caching deliberately by identifying stable context, separating it from dynamic information, and measuring whether supported caching mechanisms are behaving as intended.

The May 16 developer-account evidence recorded **59,288,619 prompt cache-read tokens**, representing **97.6% of the 60,776,845 total tokens** observed that day. This describes the composition of that developer-account activity and should not be interpreted as a universal savings rate.

Caching effectiveness depends on model support, context structure, cache reuse, request patterns, expiration behavior, and provider pricing.
 ### 3.4 Model Routing

Model routing determines which model handles a request based on the task, capability requirements, context characteristics, cost profile, and supported caching behavior.

Different models can have different capabilities, pricing structures, context limits, and cache behavior. A routing decision that is appropriate for one workload may not be appropriate for another.

Token Hygiene treats model selection as an engineering decision rather than a fixed default. The objective is to match each workload with a model that can satisfy the task while supporting the intended context and cost strategy.

Routing decisions should be evaluated using observed behavior, including output quality, token usage, cache activity, latency, and cost.

### 3.5 Cost Observability

Cost observability provides the measurement layer required to understand whether the rest of the Token Hygiene system is behaving as intended.

Useful signals include:

- raw input tokens
- prompt cache writes
- prompt cache reads
- output tokens
- model and routing decisions
- request-level and workflow-level cost
- cache reuse behavior
- changes in token composition over time

These measurements allow teams to distinguish observed behavior from assumptions and identify where architectural changes may improve efficiency.

Token Hygiene uses cost observability to evaluate context architecture, caching strategy, and model routing together rather than optimizing any one component in isolation.
---
 
## Section 4: Developer-Account Evidence — May 2026

### 4.1 May 2026 Account Data

The following measurements were recorded in the Lionfish7777 Claude developer account during May 2026. They describe observed account activity and should be interpreted separately from the controlled June benchmark and from any calculated or modeled comparisons.
 
**Monthly Overview:**
 
| Metric | Value |
|--------|-------|
| Total tokens in | 144,011,625 |
| Total tokens out | 945,674 |
| Account | Lionfish7777 |
| Period | May 2026 |
 
**Peak Day Breakdown — May 16, 2026 (grouped by Token Type):**
 
| Token Type | Count | % of Total |
|------------|-------|------------|
| Prompt caching read | 59,288,619 | 97.6% |
| Prompt caching write | 1,248,486 | 2.1% |
| Output | 212,153 | 0.3% |
| Input | 27,587 | 0.05% |
| Total | 60,776,845 | 100% |
 
### 4.2 What This Data Shows

On May 16, 2026, the Lionfish7777 developer account recorded **60,776,845 total tokens**.

The composition of that activity was:

- **59,288,619 prompt cache-read tokens (97.6%)**
- **1,248,486 prompt cache-write tokens (2.1%)**
- **212,153 output tokens (0.3%)**
- **27,587 raw input tokens (0.05%)**

These measurements show that the headline token total alone does not describe the cost behavior of the workload. Token composition matters because raw input, cache creation or writes, cache reads, and output can have different pricing characteristics.

The May 16 account data therefore provides evidence about how the workload was consuming tokens and how heavily prompt caching was represented in that activity.

It does not, by itself, establish a universal savings rate or prove that a particular architectural change caused the observed composition. Cost comparisons and controlled benchmark results are evaluated separately in the sections that follow.
 
### 4.3 Controlled A/B/C Benchmark — June 6, 2026

To evaluate the caching mechanism under controlled conditions, Lionfish7777 ran an A/B/C benchmark on June 6, 2026 using the same model and content across three configurations.

| Scenario | Token Behavior | Cost |
|---|---|---:|
| A — Monolith, no explicit cache control | 1,506 input tokens | $0.005058 |
| B — Architecture, cache write | 19 input + 2,902 cached tokens | $0.003201 |
| C — Architecture, steady-state cache hit | 3 input + 2,902 cached tokens | $0.003242 |

Using the stored benchmark costs:

- **Config B recorded a 36.7% lower total cost than Config A**
- **Config C recorded a 35.9% lower total cost than Config A**
- raw input decreased from **1,506 tokens in Config A to 3 tokens in Config C**, a **99.8% reduction in raw input tokens** for the tested request

These measurements describe the observed relative behavior of this controlled benchmark. They should not be interpreted as universal production savings rates.

The exact economics of caching depend on model pricing, cache-write and cache-read pricing, output generation, request patterns, cache reuse, context structure, and workload characteristics.

The benchmark also showed model-specific differences in cache behavior. Under the tested configuration and environment, `claude-sonnet-4-6` showed cache activity, while `claude-haiku-4-5-20251001` recorded 0.0% cache activity across the tested scenarios. This observation is limited to the tested model versions, configuration, and environment and should not be generalized into a universal claim about Haiku prompt-caching support.

The benchmark files and reproduction instructions are documented in the repository's `audit/` directory. Exact token counts and costs may vary across runs, but the controlled comparison is intended to make the relative behavior measurable and inspectable.

### 4.4 June 3, 2026 — Developer-Account Session
 
On June 3, 2026, Lionfish7777 recorded a full Claude Code development session spanning repository work, documentation, and planning across multiple workstreams. The session provides an additional developer-account observation under conditions different from both the May monthly evidence and the June 6 controlled benchmark.
 
| Metric | Value |
|---|---:|
| Total tokens consumed | 48,433,145 |
| Prompt cache reads | 47,352,314 |
| Prompt cache writes | 934,519 |
| Raw input | 32,982 |
| Output | 113,330 |
| Cache read ratio | 97.8% |
| Total cost | ~$19.50 |
 
This session provides an additional developer-account observation showing a high proportion of cache-read activity during a full development workflow.

It should not be interpreted as a controlled before-and-after comparison or as proof of a specific savings rate. The session was recorded under different conditions from both the May monthly evidence and the June 6 controlled benchmark.
 
### 4.5 Modeled Implications for Input-Heavy Workloads

The May 2026 developer-account evidence recorded **$89.40 in observed token cost** across **144,011,625 input tokens**. A same-volume uncached input-cost baseline calculated at **$3.00 per million input tokens** is **$432.03**, placing the observed May cost **79.3% below that calculated baseline**.

This comparison is not an observed before-and-after savings measurement and should not be generalized as a universal savings rate.

The potential value of Token Hygiene depends heavily on workload composition. Workloads that repeatedly process large amounts of stable or reusable input may present more opportunity for context architecture and supported caching strategies than workloads dominated by dynamic output or frequently changing context.

Relevant variables include:

- the ratio of reusable input to dynamic input
- output-token volume
- model and provider pricing
- cache-write and cache-read pricing
- frequency of cache reuse
- cache expiration behavior
- context structure
- request volume
- model routing
- workload-specific quality requirements

Input-heavy use cases may exist in areas such as enterprise knowledge systems, document analysis, research workflows, software-development tooling, legal workflows, financial analysis, and healthcare applications. These examples identify potential workload characteristics, not validated industry-specific savings outcomes.

Any projected cost difference should therefore be treated as a modeled scenario until it is tested against an actual workload.

The next validation stage for Token Hygiene is to evaluate these relationships across external workloads with different context sizes, request patterns, models, and reuse behavior.
---
 
## Section 5: Industry Context and Timing
 
### 5.1 Why This Matters Now

AI workloads are becoming longer-running, more agentic, and more deeply integrated into software and business processes. As that happens, token consumption becomes an increasingly important engineering and operational variable.

Several factors make token hygiene relevant:

- **Longer-running workflows:** Multi-step and agentic systems can make repeated model calls and carry context across longer sessions.
- **Larger context requirements:** Applications may process documentation, code, conversation history, tool output, and other reference material within the same workflow.
- **Repeated context:** Stable information may be processed repeatedly when it is not separated, reused, or cached effectively.
- **Model diversity:** Different models can vary in capability, pricing, context behavior, and support for caching mechanisms.
- **Cost accountability:** As AI usage grows, engineering and finance teams need clearer visibility into how token consumption translates into workload cost.
- **Need for measurable optimization:** Teams need ways to distinguish useful context from unnecessary processing and to evaluate architectural changes using observed data.

These conditions do not mean every AI workload has a token-efficiency problem. They do mean that context architecture, caching strategy, model routing, and cost observability become more important as AI systems scale in complexity and usage.

Token Hygiene provides a framework for evaluating those variables systematically rather than assuming that lower model pricing alone will control total application cost.
 
### 5.2 Enterprise Cost Context

As AI becomes embedded in more business workflows, organizations have to evaluate more than model capability alone. Architecture, usage patterns, model selection, observability, and total workload cost all become part of the operating decision.

Token Hygiene addresses one controllable part of that broader problem: how efficiently an application processes context and how clearly teams can measure the resulting token behavior and cost.

This does not assume that every organization should optimize for the lowest possible token spend. The objective is to make AI consumption measurable enough that engineering and business teams can understand the tradeoffs between capability, context, performance, and cost.
 
### 5.3 Healthcare as an Example of an Input-Heavy Workload

Healthcare illustrates why workload composition matters when evaluating Token Hygiene.

Some healthcare AI workflows may process large amounts of structured and unstructured context, including patient history, medications, laboratory results, clinical notes, insurance information, guidelines, or other reference material. When portions of that information remain stable across repeated requests, the workload may present opportunities for deliberate context architecture and supported caching strategies.

The potential economics depend on the actual workload. Relevant variables include:

- how much of the context is reusable
- how frequently that context is referenced
- model and provider pricing
- cache-write and cache-read behavior
- output-token volume
- latency and quality requirements
- privacy, security, and compliance constraints
- whether the selected model supports the intended caching behavior

Token Hygiene has not yet been externally validated against a production clinical workload. Healthcare examples in this white paper should therefore be treated as workload scenarios illustrating how input-heavy systems could be evaluated, not as demonstrated clinical savings or performance outcomes.

Any healthcare deployment would also require validation beyond cost efficiency, including accuracy, reliability, privacy, security, regulatory requirements, and the appropriateness of the AI system for the intended clinical or operational use.

The broader principle is that large-context workloads should be measured on their own terms. Token Hygiene provides a framework for determining how much context is necessary, what can be reused, how requests should be routed, and how the resulting token behavior and cost can be observed. those two realities.
 
---
 
## Section 6: Implementation Framework
The Token Hygiene implementation framework applies the four components described above — context architecture, caching strategy, model routing, and cost observability — to a defined AI workload.

The framework is designed to make token behavior measurable before and after architectural changes so that improvements can be evaluated against observed evidence rather than assumed.

The June 6 controlled benchmark recorded a **99.8% reduction in raw input tokens** between Config A and the steady-state Config C request, alongside a **35.9% lower total cost** for that tested request. Separately, the May 2026 developer-account cost was **79.3% below a calculated same-volume uncached input-cost baseline**. These results represent different conditions and should not be combined into a single universal savings claim.
 
---
 
## Section 7: Conclusion

Token Hygiene reframes AI cost as partly an architecture and observability problem. Total workload cost depends not only on per-token pricing, but also on how context is structured, how reusable information is handled, which models receive each request, and how clearly token behavior can be measured.

The evidence documented in this repository represents several distinct conditions.

During May 2026, the Lionfish7777 developer account recorded **144,011,625 input tokens** and **$89.40 in observed token cost**. A same-volume uncached input-cost baseline calculated at **$3.00 per million input tokens** is **$432.03**, placing the observed May cost **79.3% below that calculated baseline**.

On May 16, **97.6% of 60,776,845 total tokens** were represented by prompt cache reads.

Separately, the June 6 controlled A/B/C benchmark recorded a **36.7% lower total cost for Config B versus Config A**, a **35.9% lower total cost for the steady-state Config C request versus Config A**, and a **99.8% reduction in raw input tokens from Config A to Config C** for the tested request.

These results should not be combined into a single universal savings claim. They describe different workloads, conditions, and evidence classes.

What the evidence does support is a practical engineering principle: token composition can be measured, unnecessary context can be investigated, supported caching behavior can be tested, model-routing decisions can be evaluated, and cost can be observed rather than assumed.

The next stage for Token Hygiene is external validation across additional workloads, models, environments, and usage patterns.

The methodology, benchmark, developer-account evidence, and implementation framework are documented in this repository so the system can be inspected, reproduced where applicable, challenged, and improved.
 
---
 
## About Lionfish7777
 
Lionfish7777 is a founder-led software engineering team based in Bluffton, South Carolina, founded by Nicolas Petroff and Zacary Petroff.

We build production-minded software systems across AI infrastructure and FinOps, full-stack software, interactive systems, data platforms, and developer tooling.

The Token Hygiene System is part of our AI infrastructure and FinOps work. It was developed from direct analysis of our own developer-account token usage and expanded through controlled benchmarking, documentation, and ongoing validation.

Our engineering approach emphasizes measurable problems, clear architecture, inspectable evidence, explicit limitations, and progressive validation as systems mature.
| | |
| | |
|---|---|
| **Contact** | nicolas@lionfishbuilds.com |
|  | zacary@lionfishbuilds.com |
| **GitHub** | github.com/Lionfish7777 |
| **LinkedIn** | linkedin.com/in/nicolas-petroff |
|  | linkedin.com/in/zacary-petroff |
| **Website** | lionfishbuilds.com |
 
---
 
*Evidence includes Lionfish7777 developer-account data from May–June 2026 and a controlled benchmark conducted June 6, 2026. Calculated baselines and modeled scenarios are labeled separately.*
