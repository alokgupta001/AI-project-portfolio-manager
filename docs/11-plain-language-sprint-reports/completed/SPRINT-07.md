# Sprint 07 — Dashboards you can trace back to the facts

**Status:** Completed locally for the rule-based Command center.

## What was built and why it matters

The application now brings project facts into dashboards. You can inspect money, dates, risks and capacity without opening every source record separately. It also makes a mismatch visible when a project reports Green but the recorded evidence shows a problem.

Open **Command center** at [Command center](http://localhost:3000/command-center).

| Delivered function | Where to find it | How to check / expected result |
| --- | --- | --- |
| Executive view | **Executive** dashboard. | Compare its money, reported/evidence health, strategic alignment and benefits with the selected projects' saved records. Currency totals remain separate. |
| Delivery view | **Delivery** dashboard. | Inspect closed-sprint completed points, milestone/timeline facts, baseline/calendar variance, blockers and dependencies. Missing history remains unknown. |
| Risk view | **Risk** dashboard. | Inspect risk components, recorded risks and reported-versus-evidence discrepancies. These are rule-based calculations, not failure predictions. |
| Resource view | **Resource** dashboard. | Compare available/allocated hours with Resource planning for the same scope and period. Private effort and small-team protections still apply. |
| Risk register and lifecycle | Project **Risk register** or permitted dashboard controls. | Add an owned risk with severity, likelihood and review date; save mitigation/status. Closing or accepting requires the relevant reason. |
| Business benefits | Project **Business benefits** or permitted dashboard controls. | Enter a target, unit, period and optional realized amount. The dashboard keeps units and periods visible. |
| Calculation inputs and policy | Project **Metric plans**; Admin: **Organization setup → Metric policy**. | Select a frozen baseline and calendar, record forecast final cost, and inspect the resulting supported measures. |
| Date and portfolio filters | Filter area above the dashboards. | Change portfolio/period and refresh. Only authorized records in scope contribute; current-state measures remain labelled as such. |
| Personal saved views | **New view name → Save view**, then **Personal saved view**. | Save filters, reload and select them. Saved filters return but do not grant access to more records. |
| Explanation of each metric | Metric evidence/source drawer. | Open a metric's details. Inspect its inputs, dates, explanation and coverage before interpreting the number. |
| Data export | **Export metric DTO**. | Download and inspect the structured JSON file. It contains the authorized metric snapshot, not a formatted Word/PDF report. |

## A check with a clear expected result

**You need:** An authorized project with currency INR, budget INR 100,000 and a dated INR 25,000 expense. Use practice data. See [Getting access](../START_HERE.md).

1. Open Command center and choose dates that include the expense.
2. Choose the relevant portfolio and refresh.
3. Open Executive and inspect the budget/spend measures.
4. Open a metric's evidence drawer and compare it with the project's records.
5. Save a personal view and reload it.
6. For an additional check, give a practice project Green reported health and an overdue critical milestone, then refresh the dashboard.

**Expected result:** The recorded expense is 25% of the stated budget. The selected view persists. A Green report can show an evidence discrepancy for the overdue critical milestone even when there is insufficient data for a full health score.

Missing schedule, financial or capacity inputs can leave composite risk/health unknown. Do not enter invented facts just to turn an unknown value into a number.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Four dashboard views, filters, evidence and export | [Command center screen](../../../apps/web/components/command-center.tsx) |
| Authorized snapshot and calculations | [Command service](../../../services/api/ppm_api/command.py), [shared metric arithmetic](../../../services/api/ppm_api/metric_math.py) |
| Risk, benefit, plan, policy and saved-view storage | [Command tables](../../../services/api/ppm_api/command_tables.py), [command migration](../../../services/api/migrations/versions/0006_command_center.py) |
| Browser check | [Command center scenario](../../../tests/browser/command.spec.ts) |

## Recorded checks and limits

The sprint recorded 53 backend tests, focused metric/security checks and a final repaired dashboard-browser pass. The dashboard uses saved facts and defined rules; its health score is not a probability. Current-state values are not a reconstruction of the entire past. Periods are limited to 1–366 days, and snapshots have record-count bounds. Automated escalations, scheduled reports and AI forecasts were not delivered in this sprint.

[Original report](../../03-sprints/completed/sprint-07/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-07/TESTING_REPORT.md) · [Report index](../README.md)
