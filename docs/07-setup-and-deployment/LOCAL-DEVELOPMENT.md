# Local development and foundation checks

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13. Existing installation setup retains the
approved Compose overlays, private environment, database and object volumes.
Use [the latest handoff](../handoffs/LATEST.md) for exact restart commands and
[document processing](DOCUMENT-PROCESSING.md) for scanner/source limits.

This is a local development stack with identity and organization authorization. Assessment evidence supports bounded UTF-8 text with manual quarantine release; the separate document library now supports bounded PDF/DOCX/TXT/CSV/XLSX/image intake, English OCR and keyword citations. Guided AI and CPU baseline controls are implemented locally; unrestricted model
quality and forecast serving remain unverified/planned. Jira/GitHub live sync requires operator credentials and remains unverified. The API rejects `PPM_APP_ENV=production`. Compose binds published ports to `127.0.0.1`; production acceptance is not established.

## Start with Docker

Requirements: Docker Desktop with its Linux engine running, Compose v2, and Python 3.12 for the bootstrap helper. All application dependencies are installed from committed locks during image builds; host Node/Python application installs are optional for this path.

Run from the project root:

```powershell
# Fresh setup only; preserve an established .env and database.
python scripts/bootstrap.py
docker compose config --quiet
docker compose up --build -d --wait
```

If Python is not on PATH, use an installed Python 3.12 executable. On the current host the project virtual environment is already present:

```powershell
.\.venv\Scripts\python.exe scripts/bootstrap.py
```

On this Windows host Docker's executable is not on PATH. For this terminal only:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
```

Open [the local application](http://localhost:3000). Use this exact configured origin for identity flows. API endpoints: [liveness](http://127.0.0.1:8000/api/v1/health/live), [readiness](http://127.0.0.1:8000/api/v1/health/ready), [foundation checkpoint](http://127.0.0.1:8000/api/v1/foundation) and [OpenAPI docs](http://127.0.0.1:8000/docs).

Default ports are web 3000, API 8000, PostgreSQL 15432 and Redis 16379. Change the corresponding `PPM_*_PORT` values in ignored `.env` if occupied. Inside Compose, services use internal names/ports, independent of the host port choices. Browser tests honor `PPM_WEB_URL` and `PPM_API_URL` for changed web/API ports.

Bootstrap creates random local database credentials and preserves an existing `.env`. Never copy generated values into documentation. `.env.example` is a field reference with placeholders. Do not replace the generated passwords while keeping an initialized database volume; changing environment strings does not automatically rotate existing database users.

## Service responsibilities

| Service | Behavior |
| --- | --- |
| postgres | Three separate local, test and demo databases; migration and application roles are non-superusers |
| redis | Local queue/result transport with AOF persistence; no public network listener outside loopback |
| migrate | One-shot Alembic upgrade before API startup |
| api | Validated configuration, live/ready endpoints, persisted installation checkpoint, sanitized errors and request IDs |
| worker | Linux Celery process for durable ingestion and the foundation checkpoint probe |
| dispatcher | Reconciles durable PostgreSQL outbox entries with Redis every ten seconds |
| web | Next.js server rendering through generated API types/client; no mocked checkpoint |
| test | Profile-gated isolated test runner, including migration lifecycle on `ppm_test` only |

Migrations `0001_foundation` through `0012_ai_runtime` implement foundation, identity, delivery, capacity, assessment, command center and durable ingestion. The application role has SELECT only on the non-tenant foundation checkpoint; domain tables use scoped policies. Applied migrations are frozen. See [jobs guarantees](../contracts/jobs-integrations.md) for outbox/retry and connector bounds.

## Backend integration and worker acceptance

```powershell
docker compose --profile test run --build --rm test
docker compose exec -T api python scripts/smoke_worker.py
```

The test runner checks its environment/database name, upgrades the isolated test DB, downgrades to base, re-upgrades, repeats upgrade idempotently, checks schema drift and runs pytest. It never downgrades `ppm_local` or `ppm_demo`. The real worker test dispatches through Redis and reads PostgreSQL in a separate Linux worker process. No eager-mode stand-in is used for that check.

## Host developer tools and generated contracts

Host tooling baseline: Node 24, npm 11 or 12, Python 3.12 and uv 0.11.15. On a fresh host install those prerequisites, then:

```powershell
python -m pip install uv==0.11.15
uv sync --frozen
npm ci
npm run contracts:check
npm run lint
npm run typecheck
npm run format:check
uv run --frozen ruff check services scripts tests
uv run --frozen ruff format --check services scripts tests
uv run --frozen mypy services/api/ppm_api services/worker/ppm_worker
uv run --frozen pytest -q -m 'not integration'
uv run --frozen python scripts/check_sources.py
```

`uv.lock` pins transitive Python packages for supported platforms; package-lock.json pins npm resolution. Direct dependencies use exact versions. Container base/service images are pinned by digest. Update versions intentionally and regenerate locks in a separate reviewed change.

After editing backend response contracts:

```powershell
npm run contracts:generate
npm run contracts:check
```

These commands export sorted OpenAPI without loading secrets or contacting services, generate TypeScript from it, and compare committed output byte-for-byte. `PPM_PYTHON` optionally selects another Python executable; default is the project `.venv`. Review contract changes; do not manually edit generated schema files. The typed client lives in `packages/contracts/src/client.ts` and uses openapi-fetch.

For frontend hot reload with Compose API already running:

```powershell
$env:API_ORIGIN = 'http://127.0.0.1:8000'
npm run dev -- --port 3001
```

If forwarding arguments through the root workspace script does not select the desired port, run `npm run dev --workspace @ppm/web -- --port 3001` directly. Backend host development requires explicit `PPM_APP_ENV`, `PPM_DATABASE_URL` using `ppm_app`, `PPM_REDIS_URL`, `PPM_STORAGE_ROOT`, and `PYTHONPATH=services/api;services/worker` on Windows. Use the migration role only through `PPM_MIGRATION_DATABASE_URL`. Prefer Compose to avoid manually exporting database passwords.

## Browser and restart acceptance

```powershell
npx playwright install chromium
node scripts/check-identity-browser.mjs
node scripts/check-persistence.mjs
```

Set `PPM_DOCKER` to the full Docker executable path if it is not on PATH. The restart script writes a reserved local storage fixture, remembers the DB instance ID, restarts only this Compose project's services, then checks the same record and object survived. It removes its own object fixture after verification. Browser screenshots/traces are ignored under `artifacts/local`, `playwright-report` and `test-results`.

## Separate demo mode

Use alternate host ports before running both stacks simultaneously. For example set `PPM_WEB_PORT=3002`, `PPM_API_PORT=8002`, `PPM_POSTGRES_PORT=15434`, `PPM_REDIS_PORT=16381` in the shell, then:

```powershell
docker compose -f compose.yaml -f compose.demo.yaml up --build -d --wait
```

The demo override selects project `enterprise-ppm-demo`, separate named volumes and `ppm_demo`. Sprint 04 now provides guarded business fixtures; follow [the demo guide](../05-demos/sprint-based/sprint-04/DEMO-DEVELOPMENT.md) to set separate ports/origin before this command and activate the demo account. Stop it with the identical two `-f` arguments and `down`. The demo stack and repeat seed were verified in Sprint 04.

## Stop and troubleshoot

For real account email, the operator follows [Gmail SMTP setup](GMAIL-SMTP-SETUP.md). Development signup, invitation and recovery are verified; users follow website and Gmail instructions. Retain local previews only for intentional test environments, and keep all test recipients explicitly authorized.

`docker compose stop` stops local services and preserves containers/volumes. `docker compose start` starts them again. `docker compose down` removes this project's containers/network while preserving named volumes. Do not add `--volumes` unless deliberately discarding local data. `docker compose ps` shows status; use `docker compose logs --tail 100 api migrate` for troubleshooting, treating output as potentially sensitive.

Liveness reports process health without dependencies. Readiness returns HTTP 503 for missing database migration, Redis or writable storage; credentials and driver errors never appear in its response. Web presents unavailable/setup states instead of fake green indicators. Missing configuration errors identify field names, not values.

The Sprint 00 verification script is a historical checkpoint validator and intentionally expects no application files. For ongoing source preservation use `scripts/check_sources.py`; do not rerun the old script to overwrite Sprint 00 evidence with current implementation results.

CI runs frozen installs, static checks, contract drift, unit/integration/browser/restart checks in GitHub Actions. [Sprint 07 CI evidence](../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) records the earlier hosted acceptance; current Sprint 8.1 local verification does not establish a new hosted run.


## Prepared website training data

Use [the guarded walkthrough provisioning guide](../05-demos/WALKTHROUGH_DATA.md). The full seed provisions four fictional accounts and 41 records in a separate Northstar Website Training organization without resetting existing data. Credentials are generated privately, never committed. `--empty` provisions only identities on first use, for practicing setup yourself. A fresh browser signup remains the best way to execute every setup step.

The additive `0009_account_repair` migration preserves established identities, memberships, invitations and delivery records. Its downgrade discards only organization-free sessions and their refresh credentials, which the prior schema cannot represent. Back up an established database before maintenance; never run the test runner's downgrade lifecycle against it.

## Enable document intake

Use `docker compose -f compose.yaml -f compose.documents.yaml up -d --build`, wait
for ClamAV health/signatures and follow [Document processing](DOCUMENT-PROCESSING.md).
Base Compose deliberately leaves scanning unconfigured and source intake quarantines.
Use the same override for guarded document tests; preserve existing `.env`/volumes.
