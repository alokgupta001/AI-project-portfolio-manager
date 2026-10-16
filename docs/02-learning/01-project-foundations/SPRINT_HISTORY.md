# How the project grew

[Learning roadmap](../00-getting-started/README.md) Â· Next: [read and change code](../07-testing-and-debugging/DEVELOPER_GUIDE.md)

The history below uses current source, frozen migrations, `docs/03-sprints/completed/sprint-00/SPRINT_REPORT.md` through `SPRINT-07-REPORT.md`, corresponding handoffs/checks and Git. Git has broad checkpoints through Sprint 05 (`f53d771`) and Sprint 07 (`ef196c9`), followed by the transaction fix (`14f1eea`) and its verification record (`9056440`). It does not provide a separate implementation commit for every early sprint. Exact per-person authorship is not established.

## Sprint 00: decide what to build

**Objective:** turn the supplied requirements into an ordered plan. **Before:** no implementation baseline. **Changed:** preserved source documents, product scope, permission/metric contracts and sprint order. **Files:** `docs/source/INDEX.md`, `requirements/coverage.md`, `architecture/overview.md` explain source origin, scope and component responsibilities. **Database:** none.

**Verify:** read [the report](../../03-sprints/completed/sprint-00/SPRINT_REPORT.md) and [checks](../../04-testing/sprint-based/sprint-00/TESTING_REPORT.md); `scripts/check_sources.py` compares preserved copies against recorded hashes. **Learn:** a specification explains intended behavior; it does not demonstrate working behavior.

## Sprint 01: run the local services

**Objective:** make a repeatable local application foundation. **Before:** planning only. **Changed:** Next.js, FastAPI, PostgreSQL, Redis, local object storage and a Linux Celery worker with a checkpoint task. **Files:** `main.py`, `database.py` under `services/api/ppm_api`, `services/worker/ppm_worker/app.py`, `compose.yaml`. **Database:** `0001_foundation` creates installation metadata.

**Verify:** inspect `/api/v1/health/live`, `/health/ready` and `/foundation`; follow [`LOCAL-DEVELOPMENT.md`](../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) and [recorded checks](../../04-testing/sprint-based/sprint-01/TESTING_REPORT.md). **Learn:** process health differs from dependency readiness; container volumes preserve data; a worker is a separate process.

## Sprint 02: identify users and organizations

**Objective:** protect records using real identity and membership. **Before:** public foundation diagnostics. **Changed:** activation/invitations/reset, login cookies, live sessions, switching organizations and membership administration. **Files:** `identity.py`, `identity_tables.py`, `identity_schemas.py`, and `apps/web/app/account/identity-client.tsx`. **Database:** `0002_identity` adds identity and organization tables/policies.

**Verify:** follow [`IDENTITY-DEVELOPMENT.md`](../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md); inspect `tests/test_identity.py` and [checks](../../04-testing/sprint-based/sprint-02/TESTING_REPORT.md). **Learn:** authentication, authorization, CSRF, password hashes and transaction-local database context.

## Sprint 03: provide a shared workspace

**Objective:** make existing account functionality usable within common navigation. **Before:** working identity screens. **Changed:** authenticated layout, themes, reusable tables/dialogs, gallery and responsive navigation; diagnostics moved to `/system`. **Files:** `apps/web/components/shell.tsx`, `ui.tsx`, `gallery.tsx`, `app/globals.css`. **Database:** no new migration.

**Verify:** browse the workspace/gallery with a test account; read `tests/browser/shell.spec.ts` and [checks](../../04-testing/sprint-based/sprint-03/TESTING_REPORT.md). **Learn:** component reuse, state, focus handling and why visible buttons are not security checks.

## Sprint 04: store project delivery facts

**Objective:** create the project records needed by later reporting. **Before:** identity and navigation without persisted delivery facts. **Changed:** hierarchy, work, sprints, gates, dependencies, budgets/spend, baselines and audited/retry-safe writes. **Files:** `delivery.py`, `ppm_tables.py`, `ppm_schemas.py`, `apps/web/components/delivery.tsx`. **Database:** `0003_delivery` adds delivery tables, grants, audit and receipts.

**Verify:** follow [project creation](../02-backend/REQUEST_LIFECYCLE.md); inspect `test_delivery.py` and [checks](../../04-testing/sprint-based/sprint-04/TESTING_REPORT.md). **Learn:** references, SQLAlchemy Core, transactions, revisions, append-only history and duplicate-request handling.

## Sprint 05: calculate resource capacity

**Objective:** compare planned work with available hours. **Before:** delivery facts existed. **Changed:** profiles, calendars, skills, availability, leave, allocations, effort/coverage and saved planning snapshots. **Files:** `capacity.py`, `capacity_schemas.py`, extensions in `ppm_tables.py`, `apps/web/components/capacity.tsx`. **Database:** `0004_capacity` adds eleven resource-related kinds and private-effort policies.

**Verify:** calculate a small week by hand using [chapter 8](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md); read `test_capacity.py` and [checks](../../04-testing/sprint-based/sprint-05/TESTING_REPORT.md). **Learn:** local-date windows, daily overload, incomplete scope and separate sensitive-data permissions.

## Sprint 06: publish, answer and review assessments

**Objective:** score assessments under stable question definitions. **Before:** delivery and resource workflows. **Changed:** framework builder, frozen publication, assignment, autosave, independent review, weighted arithmetic and private text evidence. **Files:** `assessment.py`, `assessment_tables.py`, `assessment_schemas.py`, `apps/web/components/assessments.tsx`. **Database:** `0005_assessment` adds eight related tables.

**Verify:** use distinct respondent/reviewer test accounts; inspect `test_assessment.py`, the browser assessment scenario and [checks](../../04-testing/sprint-based/sprint-06/TESTING_REPORT.md). **Learn:** JSONB snapshots, versioning, score versus coverage, review authority and file/database failure boundaries.

## Sprint 07: show explainable portfolio metrics

**Objective:** turn authorized facts into consistent dashboards. **Before:** source project/resource/assessment data. **Changed:** four views, risk/benefit records, metric plans/policies, saved filters, source drawer, JSON download and frozen sprint points. **Files:** `command.py`, `command_tables.py`, `command_schemas.py`, `metric_math.py`, `apps/web/components/command-center.tsx`; delivery closes sprints into snapshots. **Database:** `0006_command_center` adds six tables.

**Verify:** trace one snapshot metric using [chapter 8](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md); inspect `test_command.py`, browser command scenario and [checks](../../04-testing/sprint-based/sprint-07/TESTING_REPORT.md). **Learn:** fixed risk formulas, Unknown states, period filters, source age and reported versus computed health.

## Later correction: commit before returning success

Hosted checks of `ef196c9` exposed an assessment race: upload returned successfully, but the immediate reload still saw the old revision. `14f1eea` changed `Auth` to `Depends(principal, scope="function")`, so transaction cleanup finishes before sending the response. This adds no tables or migration.

The [CI correction record](../../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) records two regression cases, 55 local backend tests, migration lifecycle/drift checks and an isolated assessment browser pass. It also records successful hosted run 37754868462 confirmed on 9 October 2026. These are existing evidence, not tests run by this rewrite. `9056440` records that outcome.

**Learn:** a success response must correspond to a completed database commit; otherwise the UI's next request can observe old data. Inspect the commit-order tests in `tests/test_transaction_boundary.py`.

## Historical future boundary after Sprint 07

At the Sprint 07 checkpoint, Sprint 08 durable jobs/integrations and later work were plans. Sprint 08 and local Sprint 8.1 are now implemented; Sprint 09 versioned documents/OCR/keyword retrieval are locally verified; Sprint 10 now implements a shared disabled/fallback gateway with bounded Gemini smoke verified; broader model quality unverified; Sprint 11 agents/semantic features and later ML/copilot/release work remain plans in [`roadmap.md`](../../requirements/roadmap.md). A numbered future sprint is not an implementation claim. Older reports saying that a later sprint had not begun were accurate at their own dates.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Sprint 08 implemented durable jobs/outbox, CSV mapping, labeled connector fixtures and progress streams. Sprint 8.1 subsequently added signup/setup, browser grants, record discovery/paging, personal receipts, nullable metadata and authorized workspace refresh. Original reports and checks are preserved in completed/active sprint folders. The latest 8.1 report records 74 backend and 12 browser tests plus focused closure checks; this documentation audit did not repeat those suites. Mail/CI/Word gates remain open, so 8.1 is not moved to completed.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

The 10 October follow-up adds real Gmail acceptance evidence and fixes reset-page wording without adding a schema migration. SMTP authentication/configuration, templates, truthful sending status and expired invitation handling were improved, then signup, existing-account Viewer acceptance and recovery were completed. Earlier sprint reports retain their original evidence. See [the current learning chapter](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md).

## Sprint 10 shared runtime — 15 October 2026

ai.py/provider/retrieval/evaluation modules and /ai extend the existing source and
job contracts. Local deterministic gates and no-key browser evidence are recorded
in [the active report](../../03-sprints/completed/sprint-10/SPRINT_REPORT.md). Overall
acceptance OPEN; Gemini free-tier smoke verified; broader quality unverified. The later user authorization permits free-tier Gemini at $0 with no daily expiry. Normal
forward rollout is recorded separately. No Sprint 11 agent or plan-edit work.
