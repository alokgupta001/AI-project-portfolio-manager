# Final product scope and release criteria

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

**Execution update 2026-10-09:** Sprint 8.1 local implementation is recorded in the [report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md); parent acceptance remains OPEN. The planning baseline below is historical. Future task scope and release criteria remain unchanged; no next sprint was started.

**Historical planning baseline (before Sprint 8.1 execution):** 9 October 2026. Documentation only; no feature work is authorized by this pack.** Sprint 08 is complete locally; Sprint 8.1 is proposed, not started. Numbers describe execution order, not dates or delivery promises. The frozen source specifications and original prompt pack remain intact. For future work, this pack supersedes the earlier gap review and the future sections of the original ordered prompts; those prompts remain historical scope evidence. Completed reports retain their original meaning.

Read the [audit](../09-planning/SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](../09-planning/SPRINT_8_1_PLAN.md), [future roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md), [traceability](../09-planning/FEATURE_GAP_TRACEABILITY.md), and [release criteria](FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) together. A later implementation session must read the latest handoff and current working tree before using these plans.

## Three scope levels

### Minimum complete operational product — pilot gate after 8.1 and safety prerequisites

A new user can sign up or accept an invitation, verify their address, set a password, create/join a named organization and understand Admin/PM/Viewer access. They can manage portfolios/programs/projects, work/sprints/milestones/dependencies/risks/budgets/benefits; manage capacity/resources; publish/complete/review maturity assessments; and reconcile the four dashboards with stored facts. They can find older permitted records, use browser grants, see personal work and basic in-app events, and follow an accurate guide with fictional sample data.

The core pilot includes local durable import/job recovery and safe configuration, a scratch backup/restore exercise and clear data-retention guidance before real data. Operational readiness is not implied solely by finishing UI tasks: actual mail delivery, relevant negative security tests, migrations and restore evidence must pass in the chosen pilot environment. Live Jira/GitHub capability remains unavailable/unverified until authorized credentials and real sync acceptance exist. Manual CSV and explicitly labeled fixture examples may support a pilot, but do not imply real external connector verification.

This level is useful on its own and may be released as a clearly described operational pilot. It does **not** fulfill the whole original AI-PPM specification. Document uploads require 09 security/retention acceptance before use; no unimplemented AI button may imply available intelligence.

### Recommended full product — original required scope plus adopted completion improvements

All original 109 functional requirements remain required, including safe documents/OCR/RAG, governed policy evidence, a shared AI gateway, all nine agents, suggested semantic assessment scoring, historical dataset/model pipeline and genuinely eligible forecasts, contextual cited copilot/analytics, configurable approvals/SLA/reminders, six transformation outputs/KPIs/decision log, resource/budget scenarios, Neo4j impact paths, fair internal benchmarks, meeting transcripts/audio/minutes/approved actions, weekly PDF/HTML/email/Slack reports, daily executive audio, passkeys, and integrated deployment/recovery artifacts. Adopted usability/account/discovery and operational controls in 8.1 and later follow-through remain part of this plan.

Forecasts can be truthfully unavailable while an operational pilot runs. For the **full original product**, disabled mode and synthetic model demos do not satisfy eligible-model acceptance. Real-data suitability and evaluation must pass or the release decision must explicitly say the full product is blocked. The same distinction applies to provider transcription, reporting delivery, embeddings and cloud deployment. Interface/fixture completion is a meaningful partial deliverable, not proof of externally verified service.

User outcomes include asking a project-specific question and tracing its answer to permitted sources; reviewing suggestions without silently changing live work; approving one accountable action; comparing a scenario with live baseline unchanged; tracing impact across teams/risks/dependencies; and receiving a permitted report or briefing whose numbers match the app.

### Optional additions

Task comments/checklists, SSO/SCIM/custom roles, cross-customer benchmarks, radar alongside existing assessment charts and extra providers/clouds/models require separate adoption. Existing bars/tables satisfy current chart visualization; a particular radar shape is not a blocker. None of these optional choices demotes original advanced scope. See OPT-001–005 in the roadmap.

## Full release checklist

Each unchecked item is a required gate; store evidence in the final report with exact revision and environment. The planning task intentionally leaves implementation gates unchecked.

- [ ] **Scope:** all 156 original source/control/enhancement/technology/planning rows have their original criterion checked, justified alternatives recorded, and no required functionality silently removed. All 36 tracked findings have closed evidence or an explicit release-blocking status. Verify actual crosswalk counts if source scope changes.
- [ ] **New-user journey:** unaided signup/invite/verify/setup/reset/session/account lifecycle succeeds; expired/cancelled/replayed tokens and same-email concurrency tested. Real account mail reaches authorized test recipient; no public mailbox or secret diagnostics.
- [ ] **Roles and isolation:** two organizations × Admin/PM/Viewer across UI/API/search/counts/files/SSE/jobs/tools/RAG/graph/cache/exports/queued delivery. Existing sessions lose revoked access. Owners do not bypass grants; sensitive effort and small-group sentiment stay protected.
- [ ] **Data correctness:** project relationships, immutable baselines/frameworks/scores, decimal currencies and dated capacity/leave/allocation calculations reconcile. Unknown/stale/incomplete evidence is explained. Aggregates include the complete permitted cohort and disclose period/count/coverage.
- [ ] **Growing data:** at least 125-record list/selector checks; stable paging/sort/filter; bounded queries and measured indexes. Search results open the correct project even when names duplicate.
- [ ] **Core journeys:** project lifecycle/archive/restore, resources/leave, assessments/review/history, risk/mitigation and four dashboards/JSON exports pass with ordinary manual-change freshness and accessible detail views.
- [ ] **Documents:** required format/category matrix, corrupt/oversize/malware quarantine, OCR confidence, versioned source locations, safe downloads, retrieval quality, prompt injection, changed permissions, deletion/hold/purge and reprocessing tests. Embedding provider/hybrid search and reviewed extraction are verified, not only keyword fixtures.
- [ ] **AI agents:** all nine agents evaluated using predeclared support/citation/access/error thresholds; unsupported numeric assertions rejected; deterministic/suggested/approved scores distinct; missing agents shown; budgets/timeout/cancellation/tool boundaries pass with one real configured provider.
- [ ] **Models:** target/label/license/as-of origin established; temporal/entity split and leakage checks; baseline/calibration/error/sample context; tracked model/version/card, reproducible training, eligible promotion/rollback/serving parity and outcome monitoring. Production acceptance excludes synthetic accuracy claims.
- [ ] **Copilot/actions:** deterministic analytic answers reconcile, correct project/multi-project follow-ups, cited source access after revocation, bounded query tools and safe ambiguity. Recommendation acceptance is distinct from application; approved workflow actions are version-safe and replay-safe.
- [ ] **Enterprise capabilities:** six transformation outputs and KPI/decision histories; conserved isolated scenarios with approved application; graph rebuild/delete/access proof; compatible privacy-safe benchmarks; meeting consent/transcript/ambiguity/review/action deduplication.
- [ ] **Communication:** rendered PDF/HTML/CSV where specified reconcile; actual authorized email/Slack delivery, subscription removal, timezone schedules/cooldown/retry/ambiguous timeout tests; daily roughly two-minute audio aligns with its cited transcript and text fallback.
- [ ] **Passkeys/account safety:** origin/RP/challenge/credential/recovery tests with virtual authenticator and available real-device evidence; last-Admin/lifecycle protections and audit export access tested.
- [ ] **Reliability:** worker crash/restart/lease fencing/outbox/replay/cancellation; provider and dependency outage; narrow connector principal rotation/revocation/session-expiry behavior; authorized live connector sync and reviewed local/source conflicts.
- [ ] **Security/accessibility:** secrets/dependency scan, rate limits/upload abuse, keyboard/mobile/contrast/screen-reader checks proportionate to product; all errors offer useful recovery without confidential details.
- [ ] **Performance:** document hardware, data size, network, users and percentile; measure login under one second, FCP under two seconds and representative chart interaction toward 60fps. Record actual results and agreed p95 budgets; failure remains open, never assert target from screenshots or a tiny fixture.
- [ ] **Preservation/recovery:** forward upgrade from current stored data; migration/object manifests unchanged except authorized changes. Backup/restore to scratch reconciles database, files and rebuildable projections. Measure RTO/RPO (time to recover and possible data loss); do not promise untested targets.
- [ ] **Deployment:** production-safe config, least privilege/TLS/secrets, AWS Terraform/container/migration/rollback validation, Kubernetes profile status, hosted CI at reviewed revision. State prepared artifacts versus actual deployment; live deployment requires credentials, budget and authorization.
- [ ] **Availability:** monitor alert-worker availability/delivery/lag, define error budget for 99.9% target, record observation interval and actual result. Short local test results cannot establish achieved uptime.
- [ ] **Handoff:** simple user guide/sample organization/members/projects/rubric matrices; administrator/operations/incident/backup/rollback documentation; model/data cards, threat model, API docs, ten-minute demo and final exact-revision report. Independent reviewer can reproduce critical journeys.

## Release decision and open assumptions

Record one of: operational pilot accepted; full-product implementation accepted locally with named external gates still blocked; or full release accepted for a named deployment. Do not use "complete" without the scope/environment qualifier. Critical authorization/data loss defects block every level. Required functionality or real-provider/model evidence gaps block full release even when a pilot can proceed.

Provider accounts, live connector/cloud credentials, approved recipients/data rights, real historical labels, retention/hold decisions, metadata vocabulary, model thresholds and actual team capacity remain unresolved. They are owning-task entry decisions, not assumed purchases, dates or fabricated facts. Adopted public registration policy needs explicit product confirmation before implementation if organization onboarding is intentionally invitation-only.

## Safe implementation handoff

This planning request creates no new feature, migration or cloud deployment. A future session must be authorized for the intended sprint, inspect current uncommitted work, preserve unrelated changes and normal databases, and use task IDs/report evidence from this pack. Existing Sprint 08 is the implementation baseline; 8.1 is the next proposed work. Source specifications and frozen original prompts remain hash-identical.

## Sprint 09 local checkpoint — 15 October 2026

Source intake/OCR, scoped keyword citations, policy registry and document retention/pilot
scratch recovery now have [local evidence](../03-sprints/completed/sprint-09/SPRINT_REPORT.md).
This does not check off full release requirements: F-066/067/074 remain partial,
embeddings/semantic inference are pending 10/11, policy approvals pending 15, and
production backup erasure/all-surface recovery remain 22/23. Hosted CI at a reviewed
revision and archived Word visual acceptance remain open. Existing release criteria
above are unchanged; no production or complete-RAG acceptance is inferred.
## Sprint 10 execution boundary

Sprint 10 implementation and local verification are complete for the authorized mock/fallback slice under explicit
authorization. Required real-provider smoke is BLOCKED by user instruction; mocks
and fallback do not close full-product provider/embedding gates. No release checkbox
above is closed by a code path or fixture. Sprint 11 remains separately authorized.
