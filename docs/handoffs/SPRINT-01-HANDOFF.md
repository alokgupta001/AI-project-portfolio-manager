# Sprint 01 technical handoff

## Verified checkpoint

2026-10-05: **Sprint 01 local foundation complete**. Branch `main`, no commit or remote. All files are uncommitted task work; preserve them. Workspace: `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm`. Matching [report](../sprints/SPRINT-01-REPORT.md) and [acceptance record](../verification/SPRINT-01-CHECKS.md) distinguish actual tests from unverified hosted/demo execution.

N-012 met for the initial foundation; N-018 met for Sprint 01 and ongoing. T-002/T-003 foundation accepted; T-001 and T-010 only partially implemented. All product/domain features remain planned. Sources and five canonical prompt files are preserved byte-for-byte.

Runtime: Windows host Node 24.20.0/npm 11.19.0/Python 3.12.14; Docker Linux engine 29.7.2, container Python 3.12.15. Services last verified running on loopback. Do not infer that they remain running after app/host restarts.

## Read these files first

1. [MASTER](../prompts/MASTER.md), [ordered Sprint 02 prompt](../prompts/02-ORDERED-SPRINT-PROMPTS.md), [source index](../source/INDEX.md), [coverage](../requirements/coverage.md) and [decisions](../requirements/decisions-and-assumptions.md).
2. [Architecture](../architecture/overview.md), [data model](../architecture/data-model.md), [ADR 002 identity](../architecture/adr/README.md) and [ADR 007 runtime](../architecture/adr/007-sprint-01-runtime.md).
3. [Permissions](../contracts/permissions.md), [API/events](../contracts/api-events.md), [metrics](../contracts/metrics.md). These retain future module contracts.
4. `services/api/ppm_api/main.py`, `config.py`, `database.py`, `storage.py`; `services/worker/ppm_worker/app.py`; `apps/web/app/page.tsx`.
5. `packages/contracts/openapi.json`, `src/schema.d.ts`, `src/client.ts`; `services/api/migrations/versions/0001_foundation.py`; `infra/postgres/init.sh`; `compose.yaml`.
6. [Local development guide](../LOCAL-DEVELOPMENT.md), tests/scripts and evidence transcripts linked from the acceptance record.

## Current implementation and contracts to preserve

- Web `/` reads real API status/checkpoint server-side; there are no dashboards, login or domain modules. No mocked providers or AI feature flags exist.
- GET `/api/v1/health/live`, `/api/v1/health/ready`, `/api/v1/foundation`; versioned API, UUID request IDs, sanitized error envelopes and no-store responses. OpenAPI is authoritative; regenerate types instead of hand-editing them.
- Celery's `foundation.database_checkpoint` task uses the real Redis broker and per-task async DB engine lifecycle. Durable outbox semantics are future Sprint 08 work.
- Migration head **0001_foundation** creates one non-tenant installation checkpoint. Do not rewrite this applied revision. Add subsequent revisions in one chain. Readiness currently checks that exact head in `main.py`, and the response schema exposes it: update both deliberately when adding migrations.
- Application DB role `ppm_app` is non-superuser/non-RLS-bypass and SELECT-only; `ppm_owner` owns migration objects. Sprint 02 must add the needed least-privilege grants and real RLS policies, not promote the app role to owner/superuser.
- Authentication/session/tenant resolution are not implemented. Preserve planned membership-derived scope, secure cookie sessions, CSRF protection, rotation/revocation and authorization tests from Sprint 00.
- Risk/maturity/KPI formulas are still proposed contracts, not implemented calculations. No provider, vector or graph index exists. Local object adapter has no upload/download route.
- Slate/teal CSS and semantic layout are a starter; the shared design system belongs to Sprint 03. Do not imply all shadcn/Motion/chart/state dependencies are installed.

## Reproduce the current state

From the project root, with Docker Linux engine running:

```powershell
.\.venv\Scripts\python.exe scripts/bootstrap.py
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
docker compose config --quiet
docker compose up --build -d --wait
docker compose --profile test run --rm test
docker compose exec -T api python scripts/smoke_worker.py
npm run contracts:check
npm run test:e2e
node scripts/check-persistence.mjs
```

For a fresh host, install Python 3.12/uv 0.11.15/Node 24/npm 11 or 12, run `uv sync --frozen`, `npm ci`, and `npx playwright install chromium`. Container-only startup does not need host npm packages. Full static commands and configuration names are in [LOCAL-DEVELOPMENT](../LOCAL-DEVELOPMENT.md) and `.env.example`.

Ports: web3000, API8000, PostgreSQL15432, Redis16379, all loopback. Ignored `.env` contains generated local-only secrets; do not print or copy it into reports. `PPM_PYTHON`, `PPM_DOCKER`, `PPM_WEB_URL` and `PPM_API_URL` can override test-tool paths/endpoints. Existing environment credentials must match initialized DB volumes.

Last check results: 16 backend tests with one deprecation warning, two browser tests, real worker task, all lint/types/contracts, source hashes and full-service persistence check passed. Screenshot artifacts are ignored under `artifacts/local`; transcripts in `docs/verification` are retained. Hosted Actions not run; demo override configuration validated but separate demo runtime not launched. No Python vulnerability audit result is claimed.

## Data and migration state

Local checkpoint ID: `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`; generated on first initialization, not a required hardcoded seed. A fresh installation gets its own UUID. The test runner only downgrades `ppm_test`, then restores head. No backfills, enterprise/demo seed data, vector/graph state or external providers exist. The restart test's storage fixture is removed after verification. Named volumes retain the local database and object directory. Avoid `down --volumes`; schema rollback is destructive to the checkpoint and is tested only on the isolated test DB.

## Known issues and unresolved choices

- Docker Desktop can fail startup after interruptions on stale Windows socket reparse points. The acceptance record documents reversible backups of runtime-only directories; volumes/settings were preserved. Inspect fresh diagnostics before any repair. No factory reset is authorized by this handoff.
- Starlette warns that httpx TestClient support is deprecated. Locked tests pass; evaluate migration when compatible tooling is needed, without mixing unrelated upgrades into identity work.
- No Git commit/remote means no immutable checkpoint or hosted CI evidence. Do not claim a commit or publish code without appropriate user authorization.
- Production provider/region/spend/retention and source ambiguities remain in the decision register. None blocks local Sprint 02.

## Next sprint instructions

Sprint 02: organizations, users, memberships, invitations, authentication, sessions and tenant authorization. Local runtime/migration prerequisites are verified. Likely changes: API modules, migrations, contracts/client, identity screens, app-role grants and negative integration/browser tests. Required checks include all roles, forged tenant IDs, ID guessing, expired/replayed tokens, logout/revocation, CSRF, role changes, cross-tenant reads/writes and pool-context cleanup. Keep foundation smoke checks passing and update the expected migration head. No project/portfolio/AI modules or paid cloud provisioning belong in this step.

## Copy-ready next prompt

```text
Execute Sprint 02 only in the enterprise-ppm workspace.
Read docs/prompts/MASTER.md and Sprint 02 in the ordered prompt file.
Read docs/handoffs/LATEST.md, the Sprint 01 report and acceptance record,
coverage, decisions, architecture and shared contracts. Verify actual services,
Git state, migration head and generated contracts before changing code.
Implement identity and organization authorization with the existing baseline.
Preserve source originals; extend rather than rewrite migration 0001_foundation.
Keep the application database role non-superuser and non-bypass, and implement
the full tenant/session/CSRF and negative-permission acceptance checks.
Do not provision paid services or implement later domain modules.
Run relevant checks, create the Sprint 02 report and handoff, update LATEST,
coverage and changelog, and stop after Sprint 02.
```

This is a prepared follow-up prompt, not authorization to begin Sprint 02.
