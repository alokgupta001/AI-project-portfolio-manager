# Sprint 02 technical handoff

## Verified checkpoint

2026-10-05: **Sprint 02 local identity complete**. Workspace `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm`; branch main, no commit/remote. All task files remain uncommitted. [Report](SPRINT_REPORT.md), [evidence](../../../04-testing/sprint-based/sprint-02/TESTING_REPORT.md), [coverage](../../../requirements/coverage.md). Accepted within implemented scope: F-001/F-002/F-003/N-001; N-012/N-018 ongoing. Original specifications, prompt pack and migration 0001 are unchanged. Sprint 03 is not authorized.

## Read first

1. [MASTER](../../../prompts/MASTER.md), Sprint 03 in [ordered prompts](../../../prompts/02-ORDERED-SPRINT-PROMPTS.md), [source index](../../../source/INDEX.md), [decisions](../../../requirements/decisions-and-assumptions.md).
2. [ADR 008](../../../architecture/adr/008-identity-implementation.md), [permissions](../../../contracts/permissions.md), [API/events](../../../contracts/api-events.md), [metrics](../../../contracts/metrics.md), [architecture](../../../architecture/overview.md), [data model](../../../architecture/data-model.md).
3. API `identity.py`, schemas/tables/config/main, both migrations; generated OpenAPI/TypeScript under `packages/contracts`.
4. Web account/login routes, `identity-client.tsx`, fixed API proxy, CSS; `tests/test_identity.py`, browser tests and acceptance scripts.
5. [Identity operation guide](../../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md) and linked acceptance transcripts.

## Current state and contracts

Web login/account/reset/completion and typed API sessions/CSRF/profile/switch/revocation/challenges/invitations/members/audit work locally. Head **0002_identity** adds seven tables after the unchanged foundation. No domain/backfill/vector/graph/AI/provider is implemented. Private local mailbox only; no simulated external delivery. No user-owned local Admin was created; the tested operator flow provisions the user's chosen identity.

- Access JWT: ten minutes; refresh: fixed seven days. HS256/issuer/audience/claims pinned; signing key in ignored `.env`.
- Secure/HttpOnly/SameSite=Strict cookies, no localStorage; exact configured localhost Origin, CSRF header/cookie and authenticated session binding. Do not weaken cookies to fix an origin mismatch.
- Live session/membership checks precede transaction-local RLS context. App role stays non-owner/non-super/non-bypass. Global credential lookup is a narrow auth-control-plane exception, not a future tenant data pattern.
- Unsafe organization calls require matching `X-Organization-ID`; authority stays server-side. Member changes require numeric `If-Match` revision, organization lock and final-admin protection. Preserve composite tenant references.
- One-use hashed challenges, bcrypt byte limits, strict refresh replay and reset-wide revocation are invariants. Concurrent refresh can require re-login; no grace window is implemented.
- FastAPI OpenAPI is authoritative. Regenerate client types after DTO changes. Browser transport handles CSRF/refresh; never add tokens to localStorage.
- Readiness/foundation DTO explicitly expect `0002_identity`; future migrations must update these together and extend the chain. Do not rewrite applied revisions.
- Project scopes and metric/AI contracts remain planned. Sprint 03 introduces shared components/theme/navigation around existing identity semantics.

## Reproduce

Host Node 24.20.0/npm 11.19.0/Python 3.12.14; Linux engine 29.7.2/container Python 3.12.15. From root:

```powershell
.\.venv\Scripts\python.exe scripts/bootstrap.py
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
docker compose up --build -d --wait
docker compose --profile test run --build --rm test
npm run contracts:check
node scripts/check-identity-browser.mjs
docker compose exec -T api python scripts/smoke_worker.py
node scripts/check-persistence.mjs
```

Fresh tooling: `uv sync --frozen`, `npm ci`, `npx playwright install chromium`; Python 3.12/Node 24/uv 0.11.15 baseline. Bootstrap preserves DB passwords and adds a missing random JWT key. `PPM_WEB_ORIGIN=http://localhost:3000` must match browser requests. Local ports: 3000/8000/15432/16379. `PPM_DOCKER` selects the full Docker path. The identity guide contains first-admin/private mailbox commands; never reuse acceptance credentials or expose links in reports.

Browser acceptance uses separate project `enterprise-ppm-identity-test`, ports 3001/8001/15433/16380 and random identities in ppm_test. It removes its fixture JSON, stops its containers/network and preserves named volumes. Plain `npm run test:e2e` without that fixture skips identity; use the runner. Do not run concurrent runners against its fixed project/ports.

## Evidence and data

28 backend tests, three Chromium tests, static/contract checks and production builds/start passed. Real worker/full restart retained original local checkpoint `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`. Source/migration hashes match; npm audit reported zero vulnerabilities. Hosted CI, SMTP, other browsers, full accessibility/penetration/load and Python vulnerability scanning are unverified. Screenshots/traces are ignored; traces may contain disposable credentials.

Only isolated ppm_test is downgraded by tests. Local identity rollback deletes accounts/sessions/memberships and requires explicit intent/backups. Normal stop preserves volumes; never factory-reset/delete volumes as routine recovery. Mailbox files persist until operator cleanup, although expired tokens cannot be reused.

## Known issues and next sprint

Docker can fail after interruption on stale zero-byte runtime socket reparse points. Verified runtime-only folders were preserved as `*-stale-ppm-sprint02` backups; no images/settings/volumes reset. Reinspect before repairing. Sandbox ACL startup sometimes fails; reviewed escalation was used. Exact per-command Git safe-directory trust resolves host/sandbox ownership for inspection without changing global trust.

Starlette's test-client deprecation warning is non-blocking. Session list caps at 100; reset revokes all. Production retention/key/edge policy remains later work. No new acceptance failures remain. Runtime was healthy after final regression; verify actual service availability after any later host restart.

Next: **Sprint 03 enterprise design system/application shell**. Authenticated sessions, live roles, active-org selection, typed transport and harness are verified. Likely changes are web layout/tokens/components/theme/navigation; retain identity/RLS/session semantics. Do not implement portfolio/project/AI modules or provision paid resources.

## Copy-ready next prompt

```text
Execute Sprint 03 only in the enterprise-ppm workspace.
Read docs/prompts/MASTER.md and Sprint 03 in the ordered prompt file.
Read docs/handoffs/LATEST.md, Sprint 02 report/checks, coverage, decisions,
architecture, ADR 008 and shared contracts. Verify actual runtime, Git state,
migration head and generated contracts. Implement the enterprise design system
and application shell around existing identity/session/organization controls.
Preserve secure cookies, CSRF, live roles, tenant preconditions, RLS and the
migration chain. Do not implement later domain modules or provision paid
services. Run relevant checks including full identity browser regression,
create the Sprint 03 report and handoff, update LATEST/coverage/changelog,
and stop after Sprint 03.
```

This prepared prompt does not authorize Sprint 03.
