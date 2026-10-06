# Sprint 05 technical handoff

## Verified checkpoint

2026-10-06. Sprint 05 complete locally, migration `0004_capacity`; normal stack healthy
on 3000/8000. Main has no commit/remote and all files remain untracked. Preserve user
files. F-008/013/014 accepted; F-036/055/056 later dashboard/model scope remains open.
See [report](../sprints/SPRINT-05-REPORT.md) and [checks](../verification/SPRINT-05-CHECKS.md).

## Read first / implementation map

MASTER, authorized ordered sprint prompt, coverage, capacity/delivery/permissions/
frontend/metrics contracts, ADR 011 and migration 0004. `capacity.py` owns calculations
and policy; `capacity_schemas.py` DTOs; `ppm_tables.py` metadata; `delivery.py` shared
CRUD and coverage invalidation. `components/capacity.tsx` owns `/resources`; shared
editor and IdentityClient retain secure transport. OpenAPI/TypeScript are generated.

## Contracts to preserve

Independent resource UUIDs do not imply login/project access. Immutable calendars and
allocation snapshots, dated non-overlapping availability/reporting teams, local dates
`[start,end)`, decimal schedules, explicit holidays/leave. Weekly excess sums daily
excess. Missing/zero capacity stays unknown. Actual utilization needs full-date coverage,
invalidated on effort amendments. `capacity-v1` / `capacity-snapshot-v1` are the future
consumer contracts: enforce recorded-time cutoff, never train on today's amended plan.

Live session/CSRF/tenant checks and app-role RLS remain. PM allocation needs resource
manage plus project edit; Viewer never writes. Effort needs explicit grant even for
Admin; revocation hides audit. Full-resource totals and resource archive require Admin.
Scoped/project views are partial. Team signals require five resources each selected
day; no diagnosis or individual ranking. No new AI/vector/graph/provider/event contract.

## Reproduce / evidence

Reuse ignored `.env`, never rerun bootstrap on established data. `docker compose up
--build -d --wait`; `docker compose run --rm migrate alembic current`. Backend:
`docker compose --profile test build test`, then `docker compose --profile test run
--rm test` (44 passed, lifecycle/drift). Browser: `node scripts/check-identity-browser.mjs`;
optional spec filename selects affected tests. Five existing scenarios passed; final
capacity-only run passed 15.1s. Final desktop/mobile screenshots were reviewed.

Real worker and full-stack restart persistence passed; original instance remains
`44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`, now schema 0004. Evidence and exact commands:
`docs/verification/sprint-05-persistence.txt` and Sprint 05 checks.

Static command scope and actual runtime evidence are in checks. Python source edits
on Windows must use UTF-8. Sandbox launcher failed (`apply deny-read ACLs`); shell
commands used per-command reviewed escalation. Git trust used only per-command
safe.directory. Historical migrations remain outside established mypy app/worker scope.
Inherited Starlette/httpx deprecation persists without failing tests.

## Data, recovery and limits

0004 is additive, no backfill; unchanged 0001–0003. Never downgrade user data: recover
with backup restore/forward repair. Test lifecycle is guarded for ppm_test. Normal
tenant was not seeded. Separate delivery demo v1 remains 3002/8002; browser fixtures
use isolated 3001/8001 volumes/accounts and remove the private credential file on exit.

No new dependency/secret/background domain job. Selectors cap at 100 matches and
per-resource reports are unbenchmarked. Atomic transfers, historical-as-of service,
shift-clock timesheets and automated approvals are not implemented. Snapshots capture
known plans only; choose one recorded at/before the historical prediction cutoff.

## Next sprint / copy-ready prompt

Execute Sprint 06 only after authorization. Read MASTER, Sprint 06, LATEST, Sprint 05
report/checks, ADR 011 and delivery/capacity/frontend/permission/metric contracts. Verify
services, 0004 head and generated contracts. Implement enterprise maturity assessment,
preserving staffing/privacy/history. Add 0005 rather than rewriting applied migrations.
Run rubric/versioning/assignment/approval/scoring, negative-permission and browser
acceptance; update report/handoff/coverage/changelog and stop. Sprint 06 is not authorized
by the Sprint 05 request.
