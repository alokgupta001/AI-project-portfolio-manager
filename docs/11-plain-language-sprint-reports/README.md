# Sprint reports in plain language

Current documentation closure for all Sprints 00–10 (including 8.1): [coverage, corrections, recorded evidence and remaining gates](../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

Prepared 16 October 2026 from the sprint records and current application source.

This folder explains what each sprint added, why it is useful, where you can find it, and how to check it yourself. The original technical reports stay in their existing folders.

**Start with [Getting access and checking features](START_HERE.md).** It explains accounts, permissions, local startup and how to record your checks. You do not need to understand the code to follow the reports. The file links at the end of each report are for anyone who wants to locate the implementation.

## Completed sprints

“Completed” means the recorded local scope was completed. It does not mean every planned product feature or production release is finished. Sprint 00 delivered plans and documents; Sprints 01 onward delivered working application parts.

| Sprint | What it added, in everyday language | Report |
| --- | --- | --- |
| 00 | A shared product plan and a record of all requested features | [Product plan](completed/SPRINT-00.md) |
| 01 | A working local application with service-health checks and saved data | [Running foundation](completed/SPRINT-01.md) |
| 02 | Accounts, sign-in, member roles and separation between organizations | [Accounts and access](completed/SPRINT-02.md) |
| 03 | Navigation, themes, mobile layout and consistent screens | [Workspace experience](completed/SPRINT-03.md) |
| 04 | Portfolios, projects, tasks, dates, spending and saved plan history | [Project planning and tracking](completed/SPRINT-04.md) |
| 05 | People, working hours, leave, allocations and workload checks | [Resource planning](completed/SPRINT-05.md) |
| 06 | Questionnaires with scoring, evidence and independent review | [Maturity assessments](completed/SPRINT-06.md) |
| 07 | Dashboards explaining project health, money, delivery, risk and capacity | [Command center](completed/SPRINT-07.md) |
| 08 | Imports from files/connectors and visible background-job progress | [Integrations and jobs](completed/SPRINT-08.md) |
| 09 | A versioned document library with previews, keyword search and source links | [Document library](completed/SPRINT-09.md) |

## Implemented work with acceptance still open

These are separate so their useful working features are explained without presenting the whole sprint as complete.

| Sprint | What you can inspect | Status and report |
| --- | --- | --- |
| 8.1, between 08 and 09 | Signup, setup guidance, access sharing, record search, My work, notifications and updates | [Pilot improvements](in-progress/SPRINT-8.1.md). Local implementation exists; parent acceptance remains open. Later account repairs are identified separately. |
| 10, after 09 | Controlled AI evidence previews, run history and budget controls | [AI evidence tools](in-progress/SPRINT-10.md). Local implementation is verified; full provider/model-quality acceptance remains open. Includes the 16 October Gemini follow-up. |

Sprint 11 onward is planned work and has no completed report here.

## Find a feature quickly

| I want to check… | Start here |
| --- | --- |
| Login, password recovery, invitations, organization switching | [Sprint 02](completed/SPRINT-02.md); [signup and later improvements](in-progress/SPRINT-8.1.md) |
| Organization setup, portfolios, project grants, tasks, budgets and plan history | [Sprint 04](completed/SPRINT-04.md) |
| Capacity, leave, staffing and private timesheet access | [Sprint 05](completed/SPRINT-05.md) |
| Frameworks, questionnaires, evidence, review and scores | [Sprint 06](completed/SPRINT-06.md) |
| Executive/Delivery/Risk/Resource dashboards and saved views | [Sprint 07](completed/SPRINT-07.md) |
| Imports, failed rows and background-job activity | [Sprint 08](completed/SPRINT-08.md) |
| Signup, shared assessment results, search and notifications | [Sprint 8.1](in-progress/SPRINT-8.1.md) |
| Uploads, versions, OCR, keyword search, policies and retention | [Sprint 09](completed/SPRINT-09.md) |
| AI evidence retrieval and its current limits | [Sprint 10](in-progress/SPRINT-10.md) |

## How to read the reports

Each report distinguishes the sprint's original contribution from later improvements. The check steps use today's menu names where possible. A website button may depend on your role, grants or record status; the prerequisites explain these conditions.

The expected results are instructions for your own review, not a claim that a fresh browser test ran while these reports were written. “Recorded checks” links to the existing acceptance evidence. Historical technical reports can contain “next sprint has not started” statements that describe their original date.

For a longer business example, use the existing [website walkthrough](../06-user-guides/WEBSITE_WALKTHROUGH.md). For original sprint records, use the [technical sprint index](../03-sprints/README.md).
