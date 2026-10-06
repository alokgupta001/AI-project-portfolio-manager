# Sprint 01 implementation report

## Status and scope

2026-10-05. **Complete for the local repository foundation.** The user authorized the proposed architecture as the local baseline and Sprint 01 only. Foundation acceptance passed; hosted CI and a separately running demo stack remain explicitly unverified. Branch `main` has no commit or remote; all project work remains uncommitted. Originals and the prompt pack match the Sprint 00 preservation hashes.

Requirements: N-012 accepted for the initial migration/contract baseline; N-018 fulfilled for this sprint and ongoing; T-002 and T-003 foundation acceptance met; T-001 partially implemented because the full design system/charts/state tooling belongs to later sprints. T-010 has local Compose and CI preparation only, not cloud deployment. Source sections WT/ST and the master/Sprint 01 prompt map through [coverage](../requirements/coverage.md). No functional product requirement is being closed by a health screen.

## What was built

A running Next.js frontend, FastAPI service, Linux Celery worker, PostgreSQL database, Redis broker and local filesystem object adapter. The root web page shows real dependency readiness and a persisted database checkpoint in a responsive slate/teal interface. Refresh works with pointer and keyboard. No placeholder portfolio metrics or fake AI findings are shown.

The API provides GET `/api/v1/health/live`, `/api/v1/health/ready` and `/api/v1/foundation`. A worker checkpoint task proves the actual broker/process/database connection. One non-tenant installation record is persisted; no users, organizations, projects, uploads or AI providers are implemented. The foundation is for local developers and has no user-role authentication yet.

## Why it was built

Later identity, PPM and intelligence modules need one reproducible runtime and one authoritative API schema. This sprint establishes that baseline before domain data arrives. Separate migration and application credentials reduce accidental data access; deterministic OpenAPI generation prevents frontend/backend model drift. Linux containers avoid Celery's unsupported Windows worker platform. [ADR 007](../architecture/adr/007-sprint-01-runtime.md) records runtime choices and their limits.

## How it works

Loading `/` runs a server-side request through the generated typed client. FastAPI queries the singleton checkpoint in PostgreSQL and separately checks database revision, Redis and writable storage. The page renders those actual results. Errors produce setup/unavailable states; responses and request logs carry UUID correlation IDs without raw driver errors, credentials or request bodies. No AI step is involved.

Compose starts PostgreSQL/Redis, applies the one-shot migration, then starts API, worker and web. The worker smoke command dispatches a JSON task through Redis; the worker creates and disposes its own async database engine and returns the checkpoint. This connectivity task is not the durable outbox/job system planned for Sprint 08. Restarting containers preserves PostgreSQL and object data in named volumes.

## How to use and demonstrate it

Full prerequisites, commands, configuration and troubleshooting are in [LOCAL-DEVELOPMENT](../LOCAL-DEVELOPMENT.md). From the project root, with Python 3.12 and Docker Linux engine available:

```powershell
python scripts/bootstrap.py
docker compose config --quiet
docker compose up --build -d --wait
```

On the current host use `.\.venv\Scripts\python.exe` if `python` is unavailable, and add `$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin` to PATH for Docker. Bootstrap creates an ignored `.env` with random local credentials and preserves an existing file. Configuration names and placeholders are in `.env.example`; no credential values are included in this report.

Open http://127.0.0.1:3000. Expect “Services ready”, three connected dependencies and the checkpoint. Refresh and compare the same ID against http://127.0.0.1:8000/api/v1/foundation. PostgreSQL and Redis host ports are 15432 and 16379. Local screenshots are under `artifacts/local`. Demo configuration is isolated under a separate project/database but contains no seeded enterprise records.

## Implementation record

| Files | Purpose |
| --- | --- |
| `apps/web/app/*` | Server-rendered live foundation status and responsive styling |
| `services/api/ppm_api/*` | Validated settings, SQLAlchemy lifecycle, storage adapter, typed responses and sanitized HTTP behavior |
| `services/worker/ppm_worker/app.py` | Linux Celery process and real database checkpoint task |
| `services/api/migrations/versions/0001_foundation.py` | Initial singleton table, UTC creation time and read-only app grant |
| `packages/contracts/openapi.json`, `src/schema.d.ts`, `src/client.ts` | Backend schema, generated TypeScript and shared transport |
| `pyproject.toml`, `uv.lock`, npm manifests/lock | Exact supported dependency baseline |
| `compose*.yaml`, `infra/*` | Local/demo services, pinned images, isolated test DB and non-root application containers |
| `scripts/*`, `tests/*`, `.github/workflows/ci.yml` | Reproducible setup, source/contract checks, migration/API/storage/worker/browser verification and CI |

Migration head is **0001_foundation**. There are no backfills or domain seed records. The application role is non-superuser and cannot bypass RLS; it only reads installation metadata. Actual tenant policies and session authorization remain Sprint 02. There are no product audit events yet; request logs are operational records. PostgreSQL remains authoritative and future object/vector/graph ownership contracts are unchanged. Basic semantic UI and focus behavior exist; the full design system and theme switcher remain Sprint 03.

## Verification evidence

The [acceptance record](../verification/SPRINT-01-CHECKS.md) lists actual commands, outcomes, transcripts and limits. All core foundation checks passed: container production build/start, deterministic contracts, Python/TypeScript checks, migration lifecycle and schema drift, **16 backend tests**, a real Redis/Celery/DB task, **two browser tests**, and database/object survival across full service restart. All seven preserved files match their original hashes. npm audit reported zero vulnerabilities at the time run.

The browser checks include real API-to-web data, reload, tab/Enter interaction and mobile overflow. Screenshots were visually inspected. No complete WCAG, tenant-isolation or load-test claim is made. Hosted Actions has not executed because the repository has no remote.

## Operational and security behavior

Published ports bind only to loopback. Environment validation permits local/test/demo and rejects production. Readiness distinguishes dependency failure from process liveness, uses bounded timeouts and returns sanitized status. Logs contain route templates and correlation IDs. Local object keys are validated against path escapes and writes are atomic. Application containers run without root. Named volumes preserve data; `docker compose stop` is the normal safe shutdown. The isolated test runner rejects unintended database/environment names before migration rollback.

No cloud resources, model calls, real notifications or external enterprise data were used. Runtime package downloads were required for the local build. This foundation must gain the planned identity and authorization controls before real enterprise data is introduced.

## Remaining work and decisions

Docker Desktop on this host exhibited stale Windows runtime sockets following interruptions. Reversible runtime-directory backups restored startup without deleting images/volumes; details are in the acceptance record. This host-specific issue may recur and is not fixed by application code. A Starlette test-client deprecation warning remains non-blocking. Python vulnerability scanning, production image hardening and cloud delivery remain later work; license inventories are recorded now.

The demo override passed configuration validation but was not launched as a second stack. A completely separate fresh Git checkout and hosted Actions run remain unverified; locked clean image installs/builds and migration resets were exercised locally. No immutable code commit exists yet.

## Next sprint readiness

Sprint 02's local runtime and migration prerequisites are verified. The next sprint is identity and organization authorization, and requires a separate user instruction. Read the [technical handoff](../handoffs/SPRINT-01-HANDOFF.md) before proceeding. **Sprint 02 has not started.**
