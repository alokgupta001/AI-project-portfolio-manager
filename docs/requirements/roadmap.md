# Implementation roadmap

Execute one numbered sprint at a time using [ordered prompts](../prompts/02-ORDERED-SPRINT-PROMPTS.md). This is a dependency order, not a delivery-date promise. Only Sprint 00 is authorized and completed in the current request. Split large sprints into sub-sprints with separate reports/handoffs; do not close a parent until all acceptance criteria pass.

| Sprint | Deliverable | Principal prerequisites | Exit demonstration |
| --- | --- | --- | --- |
| 00 | Requirements, architecture, contracts, source preservation | Both specifications | Source traceability and complete continuity documents |
| 01 | Reproducible web/API/worker development foundation | 00 | Fresh checkout runs health and database/client contract checks |
| 02 | Identity, organization scopes, permissions | 01 | Three roles and two tenants pass positive/negative tests |
| 03 | Design system and application shell | 02 | Responsive keyboard-accessible authenticated navigation |
| 04 | Portfolio/program/project/work/budget system of record | 02,03 | Create/update/baseline/archive project with consistent hierarchy |
| 05 | Capacity, skills, allocation and effort | 04 | Part-time/leave/cross-project allocation arithmetic reconciles |
| 06 | Versioned assessments and deterministic scoring | 04 | Publish rubric, complete/review assessment, preserve history |
| 07 | Four dashboards, risk register and shared metrics | 04,05,06 | Source facts reconcile and hidden-risk fixture is visible |
| 08 | Durable jobs, integrations and SSE | 07 | Worker crash/replay/import recovery without duplicate effects |
| 09 | Documents, OCR, retrieval and extraction contracts | 08 | Scoped evidence retrieval and deletion checks; semantic client deferred |
| 10 | AI gateway, budgets, typed tools and evaluation | 08,09 | Invalid/timeout/provider failures yield truthful results |
| 11 | Nine agents and semantic assessment/document integration | 06,07,09,10 | Supported findings and partial-agent failure with citations |
| 12 | Historical features, labels, baseline models and lineage | 05,08,11 | Reproducible temporal split; no false synthetic accuracy claims |
| 13 | Forecast serving, eligibility and fallback views | 12 | Feature parity, model rollback and uncertainty states |
| 14 | Copilot and natural language analytics | 09,10,11,13 | Deterministic query fixtures and permission-safe cited answers |
| 15 | General workflows, approvals and SLAs | 08,11 | Authorized version-safe execution and restart-safe timers |
| 16 | Transformation roadmaps, KPIs and decisions | 06,11,15 | Approved evidence-linked initiative creates project once |
| 17 | Time Machine resource/budget scenarios | 05,07,13,15 | Conservation, baseline isolation and stale-apply rejection |
| 18 | Neo4j knowledge projection and impact paths | 04,05,09,11 | Rebuild, access isolation and deletion propagation |
| 19 | Comparable internal benchmarks | 06,07,13 | Cohort compatibility and small-group suppression |
| 20 | Meeting audio/transcripts and action intelligence | 09,10,15 | Ambiguities flagged and approved actions not duplicated |
| 21 | Weekly reports, alerts and daily briefing audio | 08,11,13,15 | Schedule/recipient/retry behavior and rendered exports verified |
| 22 | Passkeys and end-to-end access hardening | 02,21 | Challenge/recovery/revocation and all-surface isolation tests |
| 23 | Release integration, recovery, deployment artifacts | 01–22 | Full traceability plus measured performance and recovery evidence |

## Milestones and gates

After 07: operational PPM MVP, not AI-complete. After 14: evidence-backed intelligence, with experimental models clearly labeled. After 22: functional scope candidate. After 23: release readiness depends on actual acceptance, provider and environment evidence, not just completion of prompt execution.

All core source capabilities remain in scope even if later sprints require real data or external access. Missing training labels can block model promotion without blocking UI/fallback work. Missing deployment credentials permit IaC preparation but not verified live deployment. Track these distinctions in coverage and each report.

## Per sprint operating procedure

Read master, latest handoff, requirement IDs, contracts and actual git status. Implement the owning module's vertical slice. Run relevant tests and update evidence paths. Demonstrate user behavior and failures. Complete report and handoff, update LATEST, coverage and changelog. Preserve a reviewed Git checkpoint when appropriate; never claim a commit exists without its hash. Do not advance dependent work past failed prerequisites or weaken acceptance to hide gaps.

Application runtime commands are intentionally absent at Sprint 00; Sprint 01 must derive and verify them from installed supported versions. No sprint duration is estimated before the environment and first implementation slice are measured.
