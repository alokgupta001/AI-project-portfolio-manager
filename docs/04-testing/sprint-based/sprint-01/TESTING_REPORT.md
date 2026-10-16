# Sprint 01 acceptance evidence

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

Verified 2026-10-05 on Windows with Docker Desktop's Linux engine 29.7.2. Host: Node 24.20.0, npm 11.19.0, Python 3.12.14; container Python 3.12.15. Exact package versions, licenses and image digests are recorded in the lockfiles, Compose/Dockerfiles, dependency inventories and [ADR 007](../../../architecture/adr/007-sprint-01-runtime.md).

Commands below run from the repository root. On this host Docker is not on PATH: use `$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\docker.exe`, or add that directory to the terminal PATH. Node/npm are under `C:\Program Files\nodejs`. See [setup](../../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md).

| Acceptance | Executed check | Result and evidence |
| --- | --- | --- |
| Original specifications and prompts preserved | `.venv\Scripts\python.exe scripts/check_sources.py` | PASS, all seven SHA256 values match; [static transcript](../../../verification/sprint-01-static.txt) |
| Reproducible dependency installation and production build | Frozen uv install and npm ci in image builds; `docker compose up --build -d --wait` | PASS earlier in this Sprint 01 session; API/worker/web built and services healthy. Image build transcript was not retained as a repository artifact. A separate clean Git checkout was unavailable because there are no commits yet. |
| Valid local and separate demo configurations | `docker compose config --quiet`; `docker compose -f compose.yaml -f compose.demo.yaml config --quiet` | PASS. Demo configuration parsed; a second running demo stack was not launched. |
| Environment validation and secret-safe failures | Config/API tests in backend suite | PASS: missing fields, invalid environments, request IDs, validation/log redaction, process liveness versus unavailable dependencies |
| Python lint, format and types | `.venv\Scripts\ruff.exe check services scripts tests`; `ruff format --check services scripts tests`; `mypy services/api/ppm_api services/worker/ppm_worker` | PASS: 21 formatted files, eight typed source files; [static transcript](../../../verification/sprint-01-static.txt) |
| Frontend lint, types and format | `npm run lint`; `npm run typecheck`; `npm run format:check` | PASS. Transcript retains the formatting failure from adding keyboard assertions and the subsequent successful correction. |
| Deterministic generated contracts | `npm run contracts:check` | PASS: sorted OpenAPI and generated TypeScript match byte-for-byte |
| Clean test migration and round-trip | `docker compose --profile test run --rm test` | PASS: upgrade, downgrade to base, re-upgrade, repeated upgrade, Alembic schema check, then **16 tests passed**; [backend transcript](../../../verification/sprint-01-backend.txt) |
| Restricted application database role | Integration suite above | PASS: role is not superuser/RLS-bypass; unauthorized UPDATE denied. Tenant RLS tests are not applicable until Sprint 02 creates tenant data. |
| Real background process | `docker compose exec -T api python scripts/smoke_worker.py` | PASS: Redis → Linux Celery → PostgreSQL, no eager-mode substitution; [worker transcript](../../../verification/sprint-01-worker.txt) |
| API-to-web, keyboard and mobile behavior | `npm run test:e2e` | PASS: **two Chromium tests**, real checkpoint comparison, reload, brand/refresh tab order and Enter activation, no page errors, 360px no horizontal overflow; [browser transcript](../../../verification/sprint-01-browser.txt) |
| Visual inspection | Open generated desktop/mobile screenshots | PASS: readable headings, cards and wrapped checkpoint values. Local screenshots: `artifacts/local/foundation-desktop.png` and `foundation-mobile.png` (ignored artifacts). This is not a comprehensive WCAG audit. |
| Database and object persistence | `node scripts/check-persistence.mjs` with `PPM_DOCKER` full path | PASS: all five runtime services restarted; checkpoint `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c` unchanged; storage fixture verified and removed. Observed tool exit 0. |
| Dependency scan | `npm audit --audit-level=high` | PASS earlier in Sprint 01: zero reported npm vulnerabilities. Python license inventory exists; no Python vulnerability scan result is claimed. |
| CI definition | `.github/workflows/ci.yml` plus local executions of its checks | Workflow supplied; hosted GitHub Actions **not run**, no remote/push exists |
| Documentation and credential exclusion | Resolve repository Markdown targets with URL escapes decoded; compare generated password values against non-ignored Git file candidates; `git check-ignore` | PASS: links resolve, no generated password value appears in repository candidates, `.env`/dependencies/local screenshots ignored |

## Interruptions and resolved failures

Earlier browser runs failed with connection refused while Docker was stopped after interrupted turns. Docker startup also failed on stale zero-byte Windows socket reparse points (`sailor-ingest.sock`, then `engine.sock`). With Docker stopped, the inspected runtime directories were renamed to sibling backups and empty replacements created. Images, settings and named volumes were retained; no factory reset or volume deletion occurred. Latest recovery backups are `%LOCALAPPDATA%\Docker\run-stale-ppm-sprint01-third` and `%LOCALAPPDATA%\docker-secrets-engine-stale-ppm-sprint01-third`; earlier backups remain. Current startup, browser and restart checks passed after recovery. If this host issue recurs, inspect the actual error and contents before attempting recovery; do not automate deletion of Docker directories.

The initial keyboard test incorrectly assumed Refresh was the first tab target. The page's brand link precedes it. The corrected test verifies both links in their actual order and passed. This was a test expectation error, not a removed accessibility requirement.

## Limits

Backend tests emit one Starlette warning about future `httpx2` test-client support; tests currently pass using the locked httpx dependency. Playwright emits a harmless NO_COLOR/FORCE_COLOR warning. No external provider, paid cloud, identity flow, tenant RLS, load benchmark, full accessibility certification, domain module, or hosted deployment was tested or claimed. Original Sprint 00 evidence remains a historical checkpoint.
