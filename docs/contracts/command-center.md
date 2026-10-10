# Command center — Sprint 07

`GET /api/v1/command/snapshot?start=YYYY-MM-DD&end=YYYY-MM-DD&portfolio_id=UUID`
returns `CommandSnapshot`, contract `command-v1`, risk rule `risk-rule-v1`.
The authenticated active-organization header is mandatory. The service takes the
same transaction advisory lock as delivery/identity mutations and rechecks live
membership. SQL uses the restricted application role and project RLS, including
both ends of dependencies. Hidden projects are neither named nor counted. JSON
DTO download re-fetches this endpoint, revalidating current authorization; it is
a download of the dashboard response, not a scheduled report or external delivery.

## Time, scope and quality

This is a **current-state** snapshot, not historical reconstruction. Explicit
date filters apply to expenditure `spent_on`, sprint end date, fully contained
benefit periods and capacity intervals. They do not retrospectively change current
budget, reported health, risk or baseline selections. Timestamp compute time is
UTC; current-day overdue checks use organization timezone. Capacity uses its own
immutable resource calendars. Intervals are `[start,end)`, 1–366 days.

Every metric has value/unit/period/source, oldest source update, freshness,
coverage, status, explanation and evidence facts. Unknown remains null. Source
recomputation never makes an old fact fresh. Default manual reporting cadence is
seven days; Admin can persist a policy with 1–365 days. Old immutable records can
therefore conservatively mark a composite stale. Snapshot reads are bounded at
200 visible projects, 100 assigned resources and 5,000 rows per project-source kind;
exceeding the bounds fails explicitly rather than returning truncated totals.
Selectors and saved-view lists disclose their first-100 limit.

## Metric authority

`metric_math.py` shares budget-use and strategic-alignment arithmetic with existing
delivery project/portfolio DTOs. `command.py` orchestrates source facts and the
existing `capacity-v1` service; all dashboards and JSON DTO download use its one
snapshot. Money is Decimal, never implicit FX. Recorded cumulative spend includes
all ledger entries and reversals, consistent with delivery summaries. Period spend
is separately labelled. Usage is rounded to two decimals, unknown for zero budget
or incomplete ledger. Alignment requires weights exactly 1; portfolio alignment
is the equal-weight covered-project mean, with coverage.

Business benefits store a target, optional realized value, explicit unit and
period. Only wholly contained periods are selected. Units are displayed beside
each record; unlike units are never combined or converted into an AI score.

Metric plans select a frozen baseline and immutable working calendar, with an
optional forecast final cost in the project's currency. Schedule variance counts
scheduled working dates in `(baseline,finish]` (negative when early), excluding
calendar holidays. Actual finish replaces forecast only for completed projects.
Milestone variance compares actual/current planned date with its frozen milestone
date and stays unknown if the baseline/calendar is missing. The selected calendar
must be an explicit input; there is no assumed five-day week. Baseline duration
uses the same date difference, clamped to a denominator of one for risk.

Schedule risk is positive working-day delay / baseline duration ×100, financial
risk is positive forecast overrun / approved budget ×100, capacity risk is excess
/ available hours ×100 over the next 28 local dates for distinct assigned resources.
Each is clamped 0–100. Full-resource capacity is available only to Admin; insufficient
scope, missing calendars or zero capacity makes that component unknown. Combined
risk requires all three and equals 0.40 schedule + 0.35 financial + 0.25 capacity.
Health is 100 − risk; it is not a probability. Default Amber ≥30 and Red ≥60 are
configurable Admin policy thresholds, with policy revision in every snapshot.

Portfolio health averages covered active/on-hold projects, shows eligible coverage
and worst covered health; missing projects are never treated as healthy. Reported
health is preserved separately. Discrepancy means computed severity exceeds a known
reported severity **or** reported Green conflicts with an unfinished critical
milestone due before today, even if composite health is unknown. Evidence identifies
the missed milestone and its date.

## Persisted records and lifecycle

Migration `0006_command_center` adds six RLS-protected tables. Existing 0001–0005
remain unchanged. 0006 is now deployed locally; future schema edits require a successor. All editable resources use existing delivery CRUD, CSRF,
organization lock, live authorization, revision checks, idempotent creation and
append-only audit. Deletion is archival, not physical removal.

- `risks`: project, active member owner, severity/likelihood 1–5, mitigation,
  review date, resolution; open → mitigating/accepted/closed, mitigating →
  open/accepted/closed, accepted → open/closed, closed → open with reason.
  Mitigation requires owner/plan; acceptance/closure requires owner/resolution.
  Readiness is visible preparation, not an automated escalation workflow.
- `benefits`: project, unit, target/realized, explicit nonempty period.
- `metric_plans`: one per project, same-project baseline, immutable calendar,
  nonnegative forecast cost. Archived rows may be restored and revised.
- `metric_policies`: one per organization, Admin writes, all members read;
  0 < Amber < Red ≤100 and valid cadence; not archivable.
- `saved_views`: actor-owned date/portfolio/dashboard filters. Viewers may save
  their own views; nobody may access another user's saved view, including Admin.
  A saved filter never grants portfolio access; loads recheck live scope.
- `sprint_closures`: automatic, immutable snapshot on active → closed, including
  team, end date, completed items and points, rule `team-points-v1`. Missing
  completed points means unknown velocity with recorded subtotal retained.
  Closed sprint definitions cannot change. Later work edits do not rewrite velocity.
  Already-closed sprints have unknown velocity; no speculative historical backfill.

Resource figures reconcile directly with capacity-v1. Portfolio selection identifies
assigned resources, but capacity rows describe all of each resource's authorized
work and state full/subset scope. Team signals are whole-team, not portfolio slices,
suppressed below five resources on any selected day, and effort remains governed by
explicit sensitive grants. No individual ranking, diagnosis or sentiment prediction.

## Verification and limits

`tests/test_command.py` covers reconciliation, complete/unknown arithmetic,
currency separation, source age, date/portfolio filters, immutable closure,
thresholds, risks, personal views, CSRF, replay, revoked scope and app-role RLS.
`tests/browser/command.spec.ts` covers the visible discrepancy, evidence drawer,
filters, saved view reload, risk creation, dashboard tabs, DTO download, tenant
switch, responsive layout and axe checks. Actual outcomes are in Sprint 07 checks.
Query and rendering measurements use tiny local fixtures and do not certify
production performance. No new dependencies, AI, cloud or external notifications.


## Sprint 08 live sync consumers

The command center discovers authorized ingestion activity and refreshes the same
`command-v1` snapshot after persisted `completed`/`degraded` stages. SSE resumes by
sequence; missed/expired progress falls back to current snapshots. This adds no
metric formula or historical reconstruction. Imported historical sprint closures
have unknown coverage; original frozen closures remain untouched. [jobs-v1](jobs-integrations.md).
