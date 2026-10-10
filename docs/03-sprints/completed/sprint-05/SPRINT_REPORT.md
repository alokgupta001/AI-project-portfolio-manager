# Sprint 05 implementation report

## Status and scope

2026-10-06. Complete locally within the limits below. F-008/013/014 implemented;
source WD/W3/W4/S4.2. F-036 dashboard and F-055/056 predictive/velocity extensions
remain later work. Git main has no commit/remote; all project files remain untracked.

## What was built and why

`/resources` provides independent resource profiles, skill filters, dated reporting
teams, immutable working calendars, availability, approved leave, project allocations,
actual effort and explicit timesheet coverage. Staffing matrices, daily heatmap/table,
weekly reconciliation and project/team views expose capacity shared across projects.
Audit history and immutable allocation snapshots supply future simulation/ML inputs.
Resource identity never implies login or project authority.

Admin configures resources/calendar versions and delegates resource capabilities.
PM allocation edits require resource manage plus project edit; Viewer is read-only.
Sensitive effort requires a separate grant even for Admin. Team support signals are
suppressed below five resources on any selected date. No diagnosis or ranking exists.

## How it works

Existing identity transport, CSRF, organization lock and live permissions protect
typed commands. Revision checks reject stale edits; idempotency protects retries;
record/audit/receipt commit together. RLS protects records, counts and sensitive audit.
Capacity uses local dates `[start,end)`: available = max(0, scheduled hours minus
leave), with zero on holidays. Planned hours add across projects. Utilization =
100 × hours / available, unknown at zero/missing capacity; excess sums daily positive
differences. DST does not change scheduled local-date hours. Actual utilization needs
explicit complete coverage, invalidated by effort amendments. Scoped views cannot
publish full-resource utilization. See [contract](../../../contracts/capacity.md).

## How to use and demonstrate it

Run `docker compose up --build -d --wait`, sign in with the existing identity setup,
and open `/resources`. Configure the organization if new. Create a resource without
a login, a Mon–Fri four-hour calendar and dated availability. Two three-hour project
allocations give 20 available/30 planned hours and 150% utilization for one week.
Two full days of leave reduce availability to 12 hours: 250% and 18 excess hours.
Capture a snapshot before editing the plan. Grant sensitive effort explicitly before
entering/attesting timesheets. Snapshot history preserves the captured plan.

Browser fixtures are synthetic and isolated. Reviewed screenshots:
`artifacts/local/sprint05-resources-desktop.png` and `sprint05-resources-mobile.png`.
Mobile tables scroll with intact dates/numbers. Demo v1 at port 3002 remains delivery-only.

## Implementation record

`capacity.py`/`capacity_schemas.py` own policy, daily/weekly/team metrics and DTOs.
`ppm_tables.py` adds eleven tenant-bound resources; delivery CRUD and generated
OpenAPI/TypeScript are extended. Frozen migration `0004_capacity` follows unchanged
0001–0003, without backfill. `components/capacity.tsx` reuses shared forms, shell and
IdentityClient. Tests cover API/SQL and browser behavior. No dependency/configuration
secret or domain background job was added. [ADR 011](../../../architecture/adr/011-resource-capacity.md)
records design and privacy decisions.

## Verification evidence

| Acceptance | Actual result | Evidence |
| --- | --- | --- |
| Split projects, leave across milestone, part time, zero/missing capacity, DST, weekly totals | Passed | [44-test backend run](../../../verification/sprint-05-backend.txt) |
| Permissions/RLS, sensitive audit revocation, concurrency/retry, snapshots and team privacy/overtime | Passed | Same backend run |
| Migration lifecycle and schema drift | Passed | Same backend run |
| Existing foundation/identity/shell/delivery browser scenarios | Five passed; new staffing selectors initially failed and were repaired | [Regression run](../../../verification/sprint-05-browser.txt) |
| Final staffing lifecycle, reload/snapshot, axe, keyboard Escape, 360px and tenant switch | 1 passed, 15.1s | [Final browser run](../../../verification/sprint-05-capacity-browser.txt) |
| Static, source integrity, dependency security and runtime | Passed, with exact scope and limitations | [Checks](../../../04-testing/sprint-based/sprint-05/TESTING_REPORT.md) |

## Operations, limits and next sprint

Normal stack is healthy at 0004; no user data was seeded. Audit stays sanitized and
request-correlated. No external email/provider/cloud call or production claim. Recovery
means forward repair/backup restore; destructive downgrade ran only in disposable test DB.

Selectors cap at 100 matches; per-resource reporting is unbenchmarked. Full totals
require Admin. Atomic transfers, automatic historical-as-of reconstruction, shift-clock
timesheets, predictive models, full WCAG certification and hosted CI remain outside this
acceptance. Future ML must select snapshots recorded at/before its prediction cutoff.

Next recommended: separately authorized Sprint 06 maturity assessment. See
[handoff](HANDOFF.md) and coverage. Stop after Sprint 05.

## Subsequent verification — 9 October 2026

The original checkpoint claims above are retained. Fresh Sprint 00–08 checks, the connector mapping repair, current runtime evidence and remaining live-provider blockers are recorded in the [sprint verification report](../../../04-testing/SPRINT_VERIFICATION_REPORT.md).
