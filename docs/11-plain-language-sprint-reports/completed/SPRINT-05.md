# Sprint 05 — Seeing who has time for the work

**Status:** Completed for local resource and capacity planning.

## What was built and why it matters

You can describe people/resources, their working patterns and leave, and allocate their hours across projects. The application compares available hours with planned work so an overloaded person does not look fully available simply because their work is spread across different projects.

Open **Resource planning** at [Resources](http://localhost:3000/resources). Setup buttons and the **Planning records** selector expose the record types below.

| Delivered function | Where to find it inside Resource planning | How to check / expected result |
| --- | --- | --- |
| Resource profiles independent of login accounts | **Resource profiles**. | Create a fictional resource without a login member. It can be planned but gains no website access. |
| Skills and dated team membership | **Skills**, **Resource teams**. | Save a skill/team record and use the corresponding skill/team filters. |
| Working calendars | **Working calendars**. | Save a calendar with weekday hours. The saved version is preserved; changed hours require another version. |
| Dated availability | **Availability**. | Assign a calendar and dates to a resource. The matching period gains known available hours. |
| Holidays and approved leave | Calendar holidays and **Approved time off**. | Add practice leave and recheck the same period. Available hours decrease. |
| Work across projects | **Allocations** / staffing matrix. | Allocate hours to two projects for one resource. Both allocations contribute to the permitted full-resource totals. |
| Daily and weekly workload | Select a resource and date period in **Staffing scope**. | Inspect the heatmap, daily table and weekly totals. Planned hours above availability appear as excess. |
| Private actual effort and timesheet completeness | **Actual effort**, **Timesheet coverage**. | With an explicit sensitive-effort grant, record effort and complete coverage. Actual utilization requires that completeness; missing data remains unknown. |
| Resource and sensitive-data permissions | Admin: **Resource access**. | Compare a PM with resource management plus project edit against a read-only person. A separate effort grant is needed even for Admin. |
| Saved staffing plans | **Allocation snapshots**. | Capture a snapshot, change an allocation and reopen the snapshot. The captured values remain unchanged. |
| Team workload indicators | **Team workload support signals**. | Inspect an eligible team period. Signals are hidden when the team has fewer than five resources on any selected date. |

## A check with easy numbers

**You need:** An Admin with full capacity visibility, two practice projects and a fictional resource. A PM needs both resource-manage and project-edit permissions to make allocations. See [Getting access](../START_HERE.md).

1. Create a calendar with four hours Monday–Friday and zero on weekends.
2. Give the resource that calendar for **19–24 October 2026**, with 24 October as the excluded end. Use no holidays in this example.
3. Allocate three hours each weekday to Project A and three to Project B.
4. Select the same resource and period in Staffing scope.
5. Capture an allocation snapshot, then add two full working days of approved leave.

**Expected result before leave:** 20 available hours, 30 planned hours, 150% planned utilization and 10 excess hours.

**Expected result after leave:** 12 available hours, 30 planned hours, 250% planned utilization and 18 excess hours. The earlier snapshot retains the plan captured before the change.

If the result is Unknown, check availability/calendar dates and full-resource visibility. A partial project view is not allowed to claim the person's total utilization.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Staffing screen, heatmap and snapshots | [Capacity screen](../../../apps/web/components/capacity.tsx) |
| Available/planned/actual hours and privacy rules | [Capacity service](../../../services/api/ppm_api/capacity.py) |
| Saved capacity records | [Capacity migration](../../../services/api/migrations/versions/0004_capacity.py), [shared tables](../../../services/api/ppm_api/ppm_tables.py) |
| Browser check | [Capacity scenario](../../../tests/browser/capacity.spec.ts) |

## Recorded checks and limits

The sprint recorded a 44-test backend run, existing browser regressions and a final staffing-browser pass. It did not deliver automatic staffing recommendations, health diagnoses, employee rankings or predictive models. Missing or zero capacity does not produce a guessed utilization percentage.

[Original report](../../03-sprints/completed/sprint-05/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-05/TESTING_REPORT.md) · [Report index](../README.md)
