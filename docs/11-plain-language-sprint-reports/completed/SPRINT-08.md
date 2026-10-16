# Sprint 08 — Bringing work in and showing its progress

**Status:** Completed locally within the documented connector limits. Real Jira/GitHub authentication and sync were not verified in the sprint.

## What was built and why it matters

An Admin can configure an import, preview how its fields map to project work, run it in the background and see what succeeded or failed. Long tasks can recover from interruptions instead of disappearing when the worker restarts.

Open **Integrations & jobs** at [Integrations](http://localhost:3000/integrations).

| Delivered function | Where to find it | How to check / expected result |
| --- | --- | --- |
| Project-bound connections | Admin: **Create connection**. | Choose an existing project and CSV, Jira or GitHub. The saved connection identifies its provider, mode and scope. |
| Field and status mapping | Connection form. | Inspect which source field supplies the local name, ID, date and status. Preview catches invalid/unmapped values. |
| Explicit sample-data mode | **Mode → Contract fixture (no provider calls)**. | Use labelled sample input. Results stay identified as fixture work; it does not prove a live provider connection. |
| Preview before importing | Selected connection preview controls. | Preview one valid and one invalid row. Read the mapping/validation results before starting a sync. |
| Background import | Selected connection sync controls. | Queue the practice batch and inspect **Job progress & data quality**. Valid rows appear in the selected project's work records. |
| Visible stages, attempts and failures | **Connections & sync history**, job details. | Open a run and inspect stage timestamps, attempts, heartbeat and rejected rows. An incomplete batch is visibly partial. |
| Repeat-import protection and source tracking | Connection sync history/provenance and imported project records. | Repeat unchanged input through the same connection. It should not create duplicate work for the same external identity. |
| Protect local edits | Imported work plus a later sync through the same connection. | Locally change a disposable imported record, then try conflicting input. The conflict should be reported rather than silently erasing the local edit. |
| Cancel, disable and renew authority | Connection/job controls available to Admin. | Cancel a suitable active practice run or disable a practice connection. Already committed rows remain; further work must respect the new state. |
| Live job progress and dashboard refresh | Open a job; watch Command center during completion. | Progress updates without a full manual reload, and the dashboard refreshes its stored facts after relevant completion/degradation. |
| Interrupted-job recovery | Background worker and dispatcher; operator/test surface. | Review the recorded interruption/restart tests linked below. A browser refresh alone does not test recovery from a worker crash. |

## A practical check

**You need:** Admin, an editable practice project and the running worker/dispatcher. See [Getting access](../START_HERE.md).

1. Create one CSV connection in fixture mode and keep its default mapping unless you intentionally change the source columns.
2. Select the connection and paste this into **CSV source**, keeping the supported column names `id,name,updated_at,status`:

```csv
id,name,updated_at,status
plain-report-001,Prepare launch checklist,2026-10-16T09:00:00Z,backlog
```

3. Click **Preview import**, then **Start sync**. Inspect its progress and open the target project's Work items.
4. Repeat the unchanged batch through the **same** connection.
5. For an error check, change the status to an unmapped value and inspect the reported validation error.

**Expected result:** The valid row becomes project work once, repeats do not create duplicates, and invalid rows are explained. A newly created second connection has a separate identity space; it is not a duplicate-protection test of the first connection.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Connections, previews and progress screen | [Integrations screen](../../../apps/web/components/integrations.tsx) |
| Job state, progress and import/provider rules | [Jobs service](../../../services/api/ppm_api/jobs.py), [ingestion](../../../services/api/ppm_api/ingestion.py) |
| Worker, dispatch and saved recovery state | [Worker](../../../services/worker/ppm_worker/app.py), [job tables](../../../services/api/ppm_api/job_tables.py), [jobs migration](../../../services/api/migrations/versions/0007_durable_jobs.py) |
| Live progress and browser check | [Live jobs client](../../../apps/web/components/live-jobs.ts), [integrations scenario](../../../tests/browser/integrations.spec.ts) |

## Recorded checks and limits

The sprint recorded 63 backend tests, eight focused job checks and nine browser tests. Its tests included actual worker interruption/recovery, duplicate delivery, cancellation and permissions. CSV batches are bounded to 500 rows; provider jobs also have page/size limits. Real connector use requires separately configured server credentials and provider access. No production webhook deployment, AI or external notification delivery was completed here.

[Original report](../../03-sprints/completed/sprint-08/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-08/TESTING_REPORT.md) · [Report index](../README.md)
