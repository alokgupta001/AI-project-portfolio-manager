# Resource capacity contract — Sprint 05

Migration `0004_capacity`, metric version `capacity-v1`, immutable planning snapshot
`capacity-snapshot-v1`. Extends the existing delivery CRUD/API and session contracts.

## Authority and units

Eleven resources: independent `resources` with optional login membership reference;
immutable `calendars`; dated `availability`, `resource_teams`, approved `time_off`
and project `allocations`; `resource_skills`; `resource_access`; restricted daily
`effort` and `effort_coverage`; immutable `capacity_snapshots`. Composite tenant
foreign keys bind relationships. All mutable records have revisions, archive state,
audit before/after and idempotent creation. No resource profile implies login access.
Existing login-backed team membership remains distinct and unchanged.

Dates use resource-calendar local dates, `[start,end)`, with Monday-based weeks.
One active availability/calendar and one reporting team may apply per resource/day;
overlap is rejected under the organization lock. Calendar versions contain IANA
timezone, seven explicit daily decimal-hour values (0–24), and ISO holiday dates.
Part-time work uses those values directly. DST does not stretch scheduled hours:
these are local date capacities, not elapsed timestamp shifts. Shift-clock tracking
is outside this contract. Missing calendars produce unknown capacity, never 8 hours.

Available hours/day = max(0, scheduled hours minus approved leave); a holiday has
zero scheduled available hours. Overlapping leave hours add and clamp at zero.
Allocations are decimal hours **per scheduled weekday**, added across projects.
They remain planned on a normally working holiday/leave day, exposing zero-capacity
conflicts. On zero-hour weekdays allocations contribute zero. Without a calendar,
allocation hours count each date conservatively but utilization remains unknown.
Over-allocation is allowed and flagged, never silently clipped to capacity.

Full-resource planned utilization = 100 × allocated / available; zero denominator
is unknown, with excess hours still visible. Excess = sum of daily max(0, allocated
minus available), not max of interval net totals. Weekly totals use the same daily
rows and clip boundary weeks to the selected interval. Query intervals are 1–366 days.

Actual hours include overtime; overtime cannot exceed the entry's total. Effort is
editable with retained audit history. An explicit full-resource daily completeness
attestation is required for every date in an interval (including nonworking days)
before actual utilization is published. Missing entries alone never prove zero.
Every effort mutation invalidates affected dates' attestation and increments its
revision with audit. Only Admin with an explicit effort grant may attest completeness.
Admin writes reject recorded daily totals above 24; scoped entries cannot establish
full-resource completeness or totals. A later import must provide stronger cross-source
deduplication and approval rules before asserting accepted timesheet coverage.

## Authorization and privacy

Existing live membership/session, exact-origin CSRF, organization precondition,
transaction-local RLS and non-superuser/non-BYPASSRLS app role remain in force.
Admin creates resources/calendar versions and delegates resource-level `manage`
or `effort` capabilities. PM resource management requires `manage`; allocation
changes also require edit/manage on the affected project. Allocation resource/project
scope is immutable: end/archive the prior allocation and create a new one. There
is no atomic cross-project transfer command or automatic capacity optimizer.
Resource archive/restore requires Admin because hidden dependents may exist.
Viewer cannot mutate staffing even if a capability was mistakenly assigned.

Effort requires explicit `effort` even for Admin, plus project scope; Viewer never
reads sensitive effort. RLS applies to records, list counts and audit JSON as well
as capacity calculations. Revoking effort hides historical raw audit immediately.
Time off collects approved hours, not free-text reasons. Do not enter medical details
in labels. No workforce notes, sentiment inference or individual ranking is implemented.

Only Admin has proven full-organization allocation scope. PM/Viewer summaries show
authorized project hours, mark `visible_projects_only`, and leave full utilization/
excess unknown. Project-filtered Admin views use the same partial-scope rule; resource
capacity is a shared denominator, not a project-owned budget to add across projects.
No hidden project identifiers or names are returned. Resource profiles/calendars and
non-sensitive resource metadata are shared within the active organization.

Team support signals require full scope and at least five resources on **every**
date selected. Dated reporting-team membership controls inclusion, preventing double
counting on transfers. Sustained overload means aggregate allocated > available for
two consecutive complete Monday–Sunday weeks. Shorter windows yield unknown.
Overtime warning means recorded overtime >10% of available capacity and requires
complete, authorized effort for the whole group. These are support signals, not
medical diagnoses or validated predictive models. F-056's later velocity/model work
and the Sprint 07 executive dashboard remain open.

## APIs and historical reconstruction

Generated OpenAPI/TypeScript are authoritative. Existing `/api/v1/delivery/{kind}`
CRUD, history, revision and idempotency rules extend to the eleven kinds above.
`resource_id` filters resource-child lists. `skill` on resource lists is an exact,
case-insensitive skill match; ordinary name search, archive filtering and pagination
remain. GET `/api/v1/capacity/resources/{id}?start=&end=&project_id=` returns daily,
weekly and interval measures, capabilities, scope, completeness and freshness.
GET `/api/v1/capacity/teams/{id}?start=&end=` returns privacy-checked team totals/signals.

Admin POST of `capacity_snapshots` records the selected resource, effective source
records (including their IDs/revisions), immutable calendar versions, local period,
daily calculations and `recorded_at` in the same locked transaction. Snapshot GET
`/api/v1/capacity/snapshots/{id}` is Admin-only. Effort and coverage are deliberately
absent. Subsequent edits cannot update a snapshot through API or app SQL privileges.
Snapshots may contain future **plans known at capture time**; they do not contain
later observations. Simulations/ML must select snapshots whose `recorded_at` is no
later than the prediction cutoff, retain contract/calendar versions, and never use
today's mutable records as past truth. Audit retains amendments; snapshots are not
automatically taken for every edit and there is no historical-as-of query service.

## UI and operating limits

`/resources` reuses identity transport, shell, modal, form, metric and table primitives.
It provides resource profiles, exact skill search, staffing matrix, calendar/leave/
allocation editors, project slice, daily heatmap plus equivalent table, weekly
reconciliation, team signals, history and snapshot capture. Lists are server-paged;
selectors show at most 100 authorized matches. Large tenants need broader server-side
selector search and batched reporting before scale claims. Reports currently query
per resource and are not load-benchmarked. No new background job, external provider,
notification, paid dependency or production-readiness claim is introduced.

Apply 0004 forward with the existing migration owner; no backfill is required and
0001–0003 are unchanged. Recovery with user data means backup restore or forward
repair. Downgrade deletes Sprint 05 data and is tested only in disposable `ppm_test`.


## Website calendar navigation repair

`capacity.tsx` now exposes Working calendars, Resource profiles and Availability as direct buttons; Admin also sees Resource access. Planning records retains all existing categories. An empty calendar list remains empty until authorized creation; no hidden default schedule is fabricated. Versions remain immutable: create a new schedule and assign dated availability. Existing validation, timezone/date arithmetic, RLS and separate effort grants are unchanged. [Repair checks](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) cover save/reload and calculations.
