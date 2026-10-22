# Sprint 11.1 plan

## Problem and outcome

The existing implementation has nine typed domain names, one shared provider completion and sound deterministic safety controls. It does not yet offer local inference, dynamic provider routing or durable section-level recovery. Its 512-token batch can omit agents and assessment matches; exact citations establish source identity but do not establish semantic entailment. The outcome of this sprint is a repository-specific implementation specification addressing these gaps without replacing the application foundation.

## Goals, scope and non-goals

Discover code and executable baseline; evaluate alternatives; select distinct domain responsibilities; specify execution, provider, state, evidence, validation, security and recovery contracts; define small implementation tasks and verifiable acceptance criteria. Preserve intended F-023–025, F-040–049, F-066/067/070–072 capabilities and future seams for F-075–077.

Hybrid-role revision: all nine specialists may combine Python services with on-demand AI interpretation. Deterministic calculations and fallbacks must not be represented as a completed requested interpretation. Calls are selected by evidence and request goal under the existing limits, with separate coverage and deferred work. This replaces the earlier permanent role split; ADR 11.1-11 records the rationale and acceptance.

No application rewrite, dependency installation, normal database migration, model download, real inference, paid call, commit, push, merge or deployment occurs here. Conversational analytics, causal prediction, plan application, integrations and notification workflows remain their existing later sprint scopes. This package does not mark broader release requirements complete.

## Constraints and dependencies

- Windows, approximately 16 GB RAM, integrated graphics: user-supplied target, not measured capacity. One local generation at a time; no nine-model deployment.
- Existing FastAPI/Pydantic/SQLAlchemy, PostgreSQL RLS, Celery/Redis, Next.js and generated contracts; no LangChain/LangGraph dependency in the inspected lock/source.
- Existing business calculations and published assessment rubrics are authoritative. Independent human acceptance records a review, never applies a plan or replaces an original score.
- Preserve immutable 0001–0014 migration files. The source expects 0014; the latest historical normal-runtime checkpoint is 0012. Do not confuse a healthy old container with the source checkout's schema state.
- Preserve legacy limits: four model attempts/run, 512 generated tokens/attempt, 90-second run deadline, existing 12-second general and 22-second Gemini completion timeouts. Proposed local completion timeout is 22 seconds. No automatic budget escalation. Larger local profiles require measured follow-up decisions.
- Legacy provider enablement and non-expiring key/project-bound Gemini confirmation must remain backward compatible. New providers require their own authorization and data-egress policy.

## Phases

1. Discover: read canonical handoff/contracts, source, tests and runtime metadata; establish provenance and limitations.
2. Decide: compare simple extension, planner-executor, graph framework and independent services; select the least complex adequate design.
3. Specify: define nine capabilities, task plan, router, normalized transport, persistence and validation; reconcile failure behavior.
4. Handover: ordered tasks, requirement/test mapping, benchmark plan, setup and explicit unknowns.
5. Verify documentation: re-read, check local links and source inventories, confirm all tasks have evidence gates and proposed work remains unimplemented.

## Acceptance and definition of done

All 15 requested documents plus index and traceability exist in the existing planning tree. Verified claims identify source symbols or fresh test evidence; historical results and untested inferences are labeled. Each retained capability has the twenty requested contract elements. Critical requirements map to tasks and acceptance tests. Lifecycle includes restart, cancellation, unknown outcomes and seven-of-nine partial success. Every external dispatch has eligibility and zero-spend checks. Sol can start T01 without reconstructing conversation context.

Documentation completeness is necessary but insufficient: contracts, diagrams, database design, limits, API compatibility, task order and negative tests must agree. Planning may finish with explicit hardware/provider qualification gates; it may not label those gates verified. All future implementation tasks start NOT_STARTED.

## Risks and scope control

Primary risks: incomplete semantic quality, CPU latency exceeding existing deadlines, schema/normal-runtime mismatch, provider terms drift, quota sharing across tenants, overbroad aggregation and mistaken citation confidence. Owners, defaults and revisit conditions are in [the risk register](SPRINT_11_1_RISKS.md). A verified source conflict pauses only the affected task, not unrelated work, and requires a documented correction.
