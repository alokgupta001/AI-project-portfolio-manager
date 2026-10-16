# Sprint 01 — Making the application run

**Status:** Completed for the local application foundation.

## What was built and why it matters

This sprint turned the plan into a running website, an application service, a database and a background worker. It proved that the parts could communicate and that saved installation data could survive a restart. Business features came in later sprints.

| Delivered function | What it does | Where you can access it | How to check / expected result |
| --- | --- | --- | --- |
| Website connected to the application service | Shows real service information rather than a sample picture. | Today: sidebar footer **Service diagnostics**, or [System](http://localhost:3000/system). | Open it and refresh. Available services should show their actual status; an unavailable dependency should be reported. |
| Process-health check | Answers whether the application service itself is running. | [Liveness endpoint](http://127.0.0.1:8000/api/v1/health/live). | Open it in a browser. A running service returns a successful health response. |
| Readiness check | Checks that required database, queue and storage dependencies are usable. | [Readiness endpoint](http://127.0.0.1:8000/api/v1/health/ready). | Open it. A healthy configured installation returns ready; missing dependencies produce unavailable status. |
| Saved installation checkpoint | Provides a persistent installation record. | [Foundation endpoint](http://127.0.0.1:8000/api/v1/foundation) and System diagnostics. | Compare the checkpoint identifier shown by both. Reloading should not create a new identifier. |
| Background-worker connection | Proves that a queued task can reach the worker and database. | Operator command below; no business-task screen existed in this sprint. | A successful probe returns the persisted checkpoint. |
| Repeatable startup and persistent storage | Starts the same services from the project configuration and retains their data. | Project [Compose configuration](../../../compose.yaml). | The operator can stop/start the existing installation and compare the checkpoint afterward. |

The health page originally occupied the home page. Later workspace improvements moved diagnostics to `/system`; today's home page is different.

## How to check it

**You need:** The local application running; see [Getting access](../START_HERE.md).

1. Open System and inspect the service states.
2. Open the foundation endpoint and note the installation identifier.
3. Reload and confirm it remains the same.
4. If checking the worker, the operator runs this from the project folder:

```powershell
docker compose exec -T api python scripts/smoke_worker.py
```

**Expected result:** The running services report their real state, and the worker reads the existing database checkpoint. A successful health result does not test every business feature.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Current diagnostics page | [System page](../../../apps/web/app/system/page.tsx) |
| Service endpoints and database access | [API entry point](../../../services/api/ppm_api/main.py), [database connection](../../../services/api/ppm_api/database.py), [storage](../../../services/api/ppm_api/storage.py) |
| Background processing | [Worker](../../../services/worker/ppm_worker/app.py), [worker probe](../../../scripts/smoke_worker.py) |
| Persistent checkpoint and startup | [First database migration](../../../services/api/migrations/versions/0001_foundation.py), [Compose](../../../compose.yaml) |

## Recorded checks and limits

The sprint recorded 16 backend tests and two browser tests, plus startup, worker and restart/storage checks. These are historical results. It did not deliver accounts, projects, AI or a production deployment.

[Original report](../../03-sprints/completed/sprint-01/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-01/TESTING_REPORT.md) · [Report index](../README.md)
