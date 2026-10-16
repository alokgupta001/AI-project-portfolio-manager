# Sprint 04 technical handoff

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

## Verified checkpoint

Checkpoint: delivery system of record implemented, 2026-10-06. Stop after Sprint 04. Next module is Sprint 05 only on separate authorization.

Read [checks](../../../04-testing/sprint-based/sprint-04/TESTING_REPORT.md), [delivery contract](../../../contracts/delivery.md), [ADR 010](../../../architecture/adr/010-delivery-system-of-record.md), frontend/permissions/metrics contracts, then Sprint 05 in the ordered prompts. Preserve originals and migrations 0001/0002/0003.

## Current implementation

- `services/api/ppm_api/ppm_tables.py`: current SQLAlchemy Core delivery metadata (19 resources plus audit/receipts).
- `ppm_schemas.py`: strict discriminated DTOs; `delivery.py`: RLS-backed authorization, validated writes, summaries/history.
- `services/api/migrations/versions/0003_delivery.py`: frozen schema, policies, SQL privileges. Current required head `0003_delivery`.
- `apps/web/components/delivery.tsx`, `delivery-fields.ts`: shared typed UI; route wrappers under organization/portfolios/projects. Existing IdentityClient owns session, CSRF and organization transport.
- `packages/contracts/openapi.json`, `src/schema.d.ts`: generated; edit backend schemas then regenerate/check, never hand-edit generated types.
- `tests/test_delivery.py`: ten tests added to 28 existing; `tests/browser/delivery.spec.ts`: real lifecycle in isolated browser stack.
- `scripts/seed_delivery_demo.py`: deterministic, guarded, transactional demo; [demo guide](../../../05-demos/sprint-based/sprint-04/DEMO-DEVELOPMENT.md).

## Reproduce the current state

Node 24.20.0/npm 11.19.0, Python 3.12.14, existing locked Next/FastAPI/Celery/Postgres/Redis baseline; no new dependency. Local ports 3000/8000, demo 3002/8002; test ports 3001/8001. Browser fixtures and demo use separate databases/volumes. The original local Demo tenant is not business-seeded. Credentials stay in ignored .env/private mailbox. App role remains non-superuser/non-bypass; owner role only migrates/seeds. Original database checkpoint: `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`.

Git branch main has no commits or remote; all project files were already untracked. Preserve user's working files. Per-command safe.directory may be required; do not change global Git trust. Docker Desktop may need starting after a host interruption.

## Contracts and known issues

Organization metadata writes require Admin; PM create requires portfolio manage and auto-grants project manage. Project edit does not confer staffing authority. Owner identity and team member are login-backed references, not Sprint 05 resource profiles. Introduce resources as separate entities, extend migrations and DTOs, and retain historical team membership.

Date-only timeline uses calendar days and current page/first 100 work items. Do not infer holiday-aware variance, drag scheduling or velocity. Ledger completeness and alignment weights control unknown outputs. Never combine currencies. Baseline snapshots preserve exact decimal strings and calendar configuration. Computed health remains null. Portfolio summary uses per-project queries; benchmark/batch later. Cross-project dependency writes remain Admin-only to validate the full graph. Audit returns latest 100; non-Admins see their own changes only.

Known tooling caveats: full `mypy services` includes untyped historical Alembic functions and fails; established CI command checks `services/api/ppm_api services/worker/ppm_worker` and passes. A Starlette/httpx deprecation warning remains without failing tests. No external email, hosted CI, production verification, full WCAG certification or performance benchmark.

## Copy ready next prompt

Execute Sprint 05 only. Read MASTER, Sprint 05, LATEST, Sprint 04 report/checks and delivery/frontend/permission/metric contracts. Verify actual services, Git, migration head and generated contracts. Build resource capacity/workload foundations without conflating resource profiles and login identities; extend migrations and preserve tenant/session controls and plan history. Run required negative-permission, date/calendar, concurrency and capacity acceptance. Update report/handoff/coverage/changelog and stop.

## Read these files first

`docs/prompts/MASTER.md`, `docs/prompts/02-ORDERED-SPRINT-PROMPTS.md`, `docs/requirements/coverage.md`, `docs/contracts/delivery.md`, `permissions.md`, `metrics.md`, `frontend.md`, `docs/architecture/adr/010-delivery-system-of-record.md`, `services/api/migrations/versions/0003_delivery.py` and `packages/contracts/openapi.json`. These define scope, compatibility and the actual data boundary. Matching report: [Sprint 04](SPRINT_REPORT.md). Completed F-005/006/007/009/010/011/012; F-008 remains Sprint 05.

Reproduce with `docker compose up --build -d --wait`; then `docker compose run --rm migrate alembic current`. Existing `.env` supplies local owner/app credentials; use `scripts/bootstrap.py` only for a new workspace. Full commands and outcomes are in [checks](../../../04-testing/sprint-based/sprint-04/TESTING_REPORT.md), [local guide](../../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) and [demo guide](../../../05-demos/sprint-based/sprint-04/DEMO-DEVELOPMENT.md). No new AI/vector/graph/provider/event contract was activated.

## Data and migration state

0003 is additive; no prior-record backfill or contraction. Owner-role migration upgrade/downgrade/re-upgrade passed on test data. Downgrade deletes delivery tables/data; never use it on user records without deliberate backup/recovery authorization. Prefer forward repair or backup restore. Original local records/checkpoint are preserved; seed UUIDs derive from `enterprise-ppm/demo-v1` and fixed UTC date 2026-10-01. Normal data remains separate from demo/test. Next sprint should add 0004, not rewrite applied migration 0003.
