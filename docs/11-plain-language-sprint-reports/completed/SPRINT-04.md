# Sprint 04 — Planning and tracking real projects

**Status:** Completed for the local project-planning and delivery records.

## What was built and why it matters

This sprint added the information people need to run projects: portfolios, project plans, tasks, dates, owners, budgets and spending. Records are saved, access is controlled, and changes leave a history. A saved baseline preserves an earlier plan so later changes do not erase it.

| Delivered function | Where to access it | How to check / expected result |
| --- | --- | --- |
| Organization timezone/currency, departments, teams and membership | Admin: **Organization setup** at `/organization`. | Save configuration and a practice department/team, then reload. Saved values remain available to project forms. |
| Strategic goals, portfolios and programs | Goals in Organization setup; **Portfolios** at `/portfolios` for portfolios/programs. | Create a practice goal and portfolio, optionally a program. They become selectable in the corresponding project fields. |
| Projects, ownership and reported health | **Projects** at `/projects`, then open a project. | Create a project under the practice portfolio. Save and reload; the overview retains the entered facts. |
| Access for project and portfolio readers/editors | **Organization setup → Project & portfolio access**, or a project's access section. | Grant a practice member read access and compare with edit/manage access. A read-only person can read but cannot edit. |
| Sprints and work items | Open a project, then **Sprints** and **Work items**. | Add a sprint and task; set their permitted fields and save. The task appears in the list/work board. |
| Milestones and timeline | Project **Milestones**, with timeline/date views. | Add a dated milestone and check it appears with its saved date. |
| Blockers and dependencies | Project **Blockers** and **Dependencies**. | Record a blocker and a permitted dependency. The named relationship is visible; cross-project dependency changes require Admin. |
| Budget and expenditure | Project **Budget lines** and **Expenditure**. | Record a practice budget and expense in the project currency. The overview reflects those amounts. Corrections preserve the spending record. |
| Status updates | Project **Status updates**. | Save an update and reload. Its reported state and notes remain in the project records. |
| Saved plan baselines | Project **Plan baselines**. | Capture a baseline, change the current plan, then inspect the saved baseline. The captured plan retains its original values. |
| Goal alignment | Project **Goal alignment**. | Link the project to an existing goal and inspect the saved relationship. |
| Change history, archive and restore | Record **History**, project **Project history**, and permitted archive controls. | Edit a practice record and inspect the history. Archive only a disposable record and check the archive filter and read-only behavior. |

## A practical walkthrough

**You need:** An Admin, configured timezone/currency and a practice portfolio. A PM also needs the relevant portfolio/project grants. See [Getting access](../START_HERE.md).

1. Create **Sprint report practice** under the practice portfolio.
2. Add a task called **Prepare launch checklist** and a dated milestone called **Launch approval**.
3. Add a practice budget of INR 100,000 and expenditure of INR 25,000, using INR as the project's currency.
4. Save a plan baseline, then change the current milestone date.
5. Reload the project. Check the records, money summary, change history and original baseline.
6. Open the project as a granted Viewer in another browser profile.

**Expected result:** Records survive reload, the old baseline remains intact, and the Viewer can read the granted project without delivery-edit controls. Later dashboards can calculate 25% budget usage from these amounts; dashboard calculations arrived in Sprint 07.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Setup, portfolio and project screens, forms and history | [Delivery screens](../../../apps/web/components/delivery.tsx), [field definitions](../../../apps/web/components/delivery-fields.ts) |
| Save/access/archive/history rules | [Delivery service](../../../services/api/ppm_api/delivery.py) |
| Records and original database structure | [Project tables](../../../services/api/ppm_api/ppm_tables.py), [delivery migration](../../../services/api/migrations/versions/0003_delivery.py) |
| Browser check | [Delivery scenario](../../../tests/browser/delivery.spec.ts) |

## Recorded checks and limits

The sprint recorded 38 backend tests and five browser tests. It provided stored project facts and reported health; calculated dashboard health, capacity, risks/benefits and closed-sprint velocity were added later. Money in different currencies is not automatically converted. Boards and timelines are paged rather than unlimited.

[Original report](../../03-sprints/completed/sprint-04/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-04/TESTING_REPORT.md) · [Report index](../README.md)
