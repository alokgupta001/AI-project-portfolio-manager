# Product reuse and screen plan

**Historical/proposed reference:** Current availability is [CURRENT_STATUS](../00-overview/CURRENT_STATUS.md); current architecture is [SYSTEM_ARCHITECTURE](../01-architecture/SYSTEM_ARCHITECTURE.md); future execution order is [the revised roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md). Preserve dated decisions/scope below; proposed components are not implementation claims.


Prepared 2026-10-05 after the user compared the Sprint 02 application with their earlier project. This is a planning supplement, not implementation of Sprint 03 or a replacement for the original specifications. The user approved preparing this plan. Proposed design and reuse choices remain subject to implementation evidence.

## Product and present state

The product is an AI-powered enterprise PPM intelligence and transformation platform: assess maturity, track portfolios and delivery, explain risks, and support strategic decisions. Account administration alone does not deliver that outcome.

Current local implementation: reproducible web/API/worker, PostgreSQL/Redis, generated contracts, identity, organization memberships, secure sessions and tenant authorization. The homepage is a technical foundation screen; no portfolio dashboard, project workflow, maturity assessment or AI assistant is implemented locally. The 28 backend and three browser passing tests establish the foundation/identity scope only.

The subsequently created Demo organization and demo@example.com Admin identity are for local account access. Activation status is not asserted here. They contain no seeded PPM business data. No passwords or activation tokens belong in this document.

Requirements remain authoritative in the [source index](../source/INDEX.md), [coverage matrix](../requirements/coverage.md) and [ordered sprint prompts](../prompts/02-ORDERED-SPRINT-PROMPTS.md). Keep all source originals, original prompts and applied migrations unchanged.

## Earlier repository: reference, not a verified dependency

Repository: [ai-enterprise-ppm](https://github.com/alokgupta001/ai-enterprise-ppm). Reference revision resolved during planning: `e0c335832cc65fcacab632cf7004a95d9e01fd38`. The initial source inspection used main; resolve and compare exact blobs at this revision before importing anything. Inspection covered representative frontend, routes, scoring, agent routing and query services; it did not execute the old application or validate all README claims. No old code, database or dependencies have been imported.

Path links below identify candidates. Reuse means preserve useful behavior or presentation, then adapt and verify it against current contracts; it does not mean copy a complete subsystem unchanged.

| Candidate in earlier repository | Evidence and reuse decision | Destination and conditions |
| --- | --- | --- |
| `frontend/app/assessments/` | Framework selection, questions and results UI exist. Retain the flow and terminology; rebuild with shared components and generated DTOs. | Sprint 06; F-016–F-022; versioned frameworks, autosave/review, incomplete states and tenant tests. |
| `frontend/app/assessments/[id]/results/page.tsx` | Radar chart, maturity/category scores and strength/gap/recommendation panels. Adapt visual concepts. | Sprint 06 deterministic results; semantic recommendations in 11. Provide a table alternative; do not show generic positive claims for every result. |
| `backend/app/routers/assessment.py`, models and assessment services | Routes cover framework/start/questions/submit/results and organization checks. Reference workflow logic; map into the current schema and permission boundary. | Sprint 06; immutable rubric versions, answer validation, revision checks, transaction tests and reproducible scoring. |
| `backend/app/services/scoring.py` | Averages scores, maps five maturity levels, defaults missing category responses to 1.0. Rework scoring to match the metric contract. | Sprint 06; missing evidence must be distinguishable from low performance; verify weights, denominators and rounding with fixtures. |
| `backend/app/routers/project.py`, project models and seed data | List and summary routes exist; they do not by themselves provide complete project management. Reuse field and scenario ideas. | Sprint 04/05/07; implement scoped CRUD, baselines, money, dependencies and allocations under current contracts. |
| `frontend/app/assistant/page.tsx` | Chat, conversation UI and specialist labels exist. Adapt interaction design after backend prerequisites. | Sprint 14; authorized history, evidence links, cancellation/error states, explicit AI availability. |
| `backend/app/agents/orchestrator.py`, specialist agents | Keyword routing to risk/resource/timeline agents exists. Treat routing as a candidate baseline, not validated reasoning quality. | Sprint 10 gateway/evaluations, then 11 agents; typed outputs, scoped evidence, limits and fallback labels. |
| `backend/app/services/root_cause.py`, context builder | LLM and rule-based analysis paths exist. Reuse diagnostic examples and domain concepts after scope review. | Sprint 11/14; every lookup must be tenant/project scoped, with grounded explanations and honest uncertainty. |
| `backend/app/services/nl_to_sql.py` | Generated SQL is checked for SELECT/restricted keywords; tenant restriction is partly entrusted to a model prompt. Do not import this execution path unchanged. | Sprint 14; typed allowlisted analytics tools or a separately constrained query layer, server-owned authorization and adversarial tests. |
| `backend/app/routers/assistant.py` | Conversation and streaming endpoints exist. Review semantics before reuse; streamed delivery alone does not establish incremental model execution. | Sprint 08/10/14; authorized events, failure/reconnect behavior and actual progress reporting. |
| `frontend/lib/api.ts`, old authentication | Uses browser localStorage bearer tokens and handwritten API calls. Preserve current secure cookie/session client instead. | No auth replacement; adapter work must use current generated contracts and CSRF handling. |
| Old Alembic chain and dependency files | Different schema lineage and runtime conventions. Use for reference only. | New changes extend current `0002_identity`; no concatenation of migration histories, old database restore or wholesale dependency replacement. |
| Old homepage | Source still contains the Next.js starter page. Not a product-home candidate. | Design the workspace home in Sprint 03, then the live command center in 07. |

Source directories: [frontend](https://github.com/alokgupta001/ai-enterprise-ppm/tree/e0c335832cc65fcacab632cf7004a95d9e01fd38/frontend), [backend](https://github.com/alokgupta001/ai-enterprise-ppm/tree/e0c335832cc65fcacab632cf7004a95d9e01fd38/backend). Broad features claimed by documentation, including OAuth, are not accepted without inspecting and testing their execution paths.

## Proposed enterprise screen structure

Retain Enterprise PPM as the working product name until a name is selected. Use a restrained slate/indigo palette, clear typography, consistent spacing, subtle borders and compact but readable data layouts. Borrow the earlier assessment presentation without copying inconsistent component styles. Support light/dark themes and reduced motion. Color never carries status alone.

Desktop: left navigation; top bar with organization switcher, breadcrumbs, command/search entry and account menu; central page content; optional right detail/evidence drawer. Mobile: collapsible navigation, stacked summaries and forms, controlled table scrolling. Verify approximately 360, 768 and 1440 pixels.

| Screen / proposed route | Main content and primary action | Data availability / target |
| --- | --- | --- |
| Workspace home `/` | Organization identity, usable actions, onboarding guidance and clearly labeled module availability. Move developer health details out of the primary product experience while keeping diagnostics accessible. | Sprint 03: real member/account data only; no invented portfolio metrics. |
| Account `/account` and organization members | Profile, active sessions, organization switcher, invitations, role changes and audit. Reuse existing APIs and permission semantics within the new shell. | Sprint 03 restyling; preserve Sprint 02 behavior. |
| Development component gallery | Tables, filter bars, dialogs, drawers, metric cards, chart frames, empty/error/loading states. | Sprint 03; isolated labeled examples, not business results. |
| Portfolios `/portfolios`, project list `/projects` | Goals, portfolios/programs, project filters, owner/status/health; create or open a project. | Sprint 04; persistent records and scoped demo fixtures. |
| Project detail `/projects/[id]` | Overview, work board, timeline, milestones, dependencies, baseline history, budget and actuals. | Sprint 04; resource views arrive in 05, computed health in 07. |
| Resources `/resources` | Staffing matrix, capacity heatmap, skills, allocation editing and overload indicators. | Sprint 05; calendar/capacity math and permissions. |
| Assessments `/assessments` | Framework/version selection, in-progress assessments, completion state; start or resume. | Sprint 06. |
| Assessment questions/results | Autosaving answers, evidence references, validation, submission/review; score/category table and radar chart. | Sprint 06 deterministic scores; AI interpretation in 11 distinctly labeled. |
| Command center `/dashboard` | Portfolio health, budget by currency, delivery variance, resources and risk drill-downs. | Sprint 07; values must reconcile to records and show freshness/coverage. |
| Documents `/documents` | Upload/processing status, document detail and evidence retrieval. | Sprint 09; quarantine, permissions and retrieval prerequisites. |
| Intelligence / forecasts | Grounded specialist findings and model-eligible forecasts with uncertainty. | Sprint 11 findings; Sprint 13 forecasts after historical pipeline in 12. |
| Copilot `/assistant` | Conversation, suggested questions, source links, scoped analytics and explanation of unavailable capabilities. | Sprint 14; depends on implemented data and evaluated AI services. |
| Decisions, workflows and advanced analysis | Approvals, transformation roadmaps, scenario comparison, graph views, benchmarks, meeting actions and reports. | Sprints 15–21; activate each destination only when its module is usable. |

Routes above are proposed new destinations; existing account routes stay compatible. In Sprint 03, future modules may appear in an informative availability section or disabled navigation with a clear reason. They must not lead to dead links or look operational. Search must state its actual scope: command/navigation initially, authorized domain search only when implemented. Notification shell must not fabricate alerts.

## What the user will see after each sprint

| Sprint | Observable outcome / demonstration |
| --- | --- |
| 00–02 complete | Technical runtime and working account/organization controls. No business PPM module yet. |
| 03 | Coherent enterprise shell, responsive navigation, themes and redesigned real account/member screens. This is a visual milestone, not a working portfolio dashboard. |
| 04 | Create a portfolio and project, edit work/milestones, track budget and inspect timeline/baseline history using real persistence. Seeded demo business data first becomes available here. |
| 05 | Allocate people/resources and see capacity, availability and workload conflicts. |
| 06 | Complete and review a maturity assessment; inspect reproducible category results and charts. First assessment-focused product milestone. |
| 07 | Use an actual portfolio command center with reconciled metrics and risk/resource/delivery drill-downs. First broad PPM dashboard milestone. |
| 08 | Observe real background job status and authorized live updates, with recovery/reconnect behavior. |
| 09 | Process supported documents and retrieve authorized evidence with visible failure states. |
| 10 | Inspect AI run status, provider/fallback state, usage and evaluated output handling. Not a complete conversational copilot yet. |
| 11 | Review grounded specialist findings and semantic assessment suggestions separately from approved scores. |
| 12 | Inspect historical data quality and model evaluation baselines; synthetic data is explicitly labeled. |
| 13 | View eligible delay/budget forecasts with horizon, uncertainty and evidence; ineligible models remain unavailable. |
| 14 | Ask scoped PPM questions in a working copilot and follow answers back to records/evidence. |
| 15 | Review and approve workflow actions; see escalation and execution outcomes. |
| 16 | Build transformation roadmaps and trace recommendations to decisions and goals. |
| 17 | Compare saved scenarios against a baseline without silently modifying live plans. |
| 18 | Explore dependency/impact relationships with authorized graph and table views. |
| 19 | Compare compatible cohorts with transparent eligibility and metrics. |
| 20 | Review meeting-derived actions and approve their creation. |
| 21 | Generate reports, receive configured alerts and inspect executive briefing/audio outputs. |
| 22 | Enroll/use passkeys and verify additional enterprise access controls. |
| 23 | Review integrated acceptance, release/runbooks and deployment readiness; actual paid deployment still requires its own authorization and configuration. |

This sequence retains the original scope and dependencies. Reusing the earlier repository can reduce work, but does not imply skipping migration, permission, integration or evaluation gates. No delivery dates or conflict-free guarantee are asserted.

## Reuse acceptance and continuity

Before importing a candidate, pin its source, inspect applicable repository instructions and provenance, and record a small explicit adaptation decision. Match entities and DTOs to current architecture; identify consumers before changing shared contracts. Keep current database role restrictions, live memberships, secure cookies, CSRF and tenant preconditions. Secrets, old default passwords and old environment files must not be copied.

Use new migrations, deterministic contract generation and module-specific tests. Adapted assessment scoring needs known-answer fixtures; AI/query paths need negative authorization and adversarial cases. Record original path/revision, changed behavior, why it changed and evidence in that sprint's report and handoff. Do not label a feature complete just because its route or component exists.

Every subsequent sprint report should include: what the user can now do; which screen demonstrates it; data source (real, seeded demo or labeled example); remaining unavailable behavior; checks actually letrun; and the next dependency. Continue using the existing report/handoff templates and coverage IDs.

## Next authorized implementation boundary

No runtime changes are made by this plan. Sprint 03 has not started. When instructed to execute Sprint 03, read this supplement with the original prompt and Sprint 02 handoff, implement the shell around existing identity, and verify accessibility/responsive behavior plus identity regression. Do not pull assessment or AI execution forward merely to populate a dashboard.
