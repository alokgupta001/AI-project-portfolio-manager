# Sprint 03 technical handoff

## Checkpoint

2026-10-05: enterprise shell/design system implemented, local only. Branch main has no commit/remote; all existing/new files remain uncommitted. Migration head stays `0002_identity`; no backfill/schema changes. [Report](SPRINT_REPORT.md), [checks](../../../04-testing/sprint-based/sprint-03/TESTING_REPORT.md), [coverage](../../../requirements/coverage.md). N-004/N-005/E-004 accepted in shell scope; N-013 core checks accepted, release-wide review remains ongoing. T-001 still partial.

## Read and preserve

Read MASTER and the selected ordered sprint, [reuse/screen plan](../../../planning/PRODUCT-REUSE-AND-SCREEN-PLAN.md), [frontend contract](../../../contracts/frontend.md), [ADR 009](../../../architecture/adr/009-enterprise-shell.md), [ADR 008](../../../architecture/adr/008-identity-implementation.md), architecture/data model, permissions, API/events and metrics contracts. Original specifications/prompts are hash-preserved.

Shell and primitives live in `apps/web/components`. `app/globals.css` is the semantic token/style authority. Existing identity client owns typed API requests, CSRF, refresh coalescing and organization state. Keep live membership checks, Secure/HttpOnly cookies, no credential localStorage, stale organization header, member revision and final-Admin protections. Modal confirmation is UX, never server authority.

Routes: `/` overview; `/account` account/member controls; existing login/reset/complete; `/design-system` authenticated illustrative gallery; `/system` local diagnostic status (old root behavior). Future navigation is noninteractive. Search is page navigation only. Notifications are explicitly unavailable. Real role, organization and latest-session counts are the only overview metrics.

Shared DataTable filters/sorts/pages loaded rows, explicitly labeled; server cursor load-more stays separate. Tenant table state uses organization key. Theme preference is `ppm-theme` only. Native dialogs provide modality/Escape/focus return; CSS reduced-motion applies globally. No new production dependencies; shadcn/Motion/Zustand/query/chart runtime deliberately deferred with ADR.

## Reproduce

Use existing `.env` without printing or replacing its credentials. Runtime: Node 24.20.0/npm 11.19.0/Python 3.12.14; Docker Linux, web3000/API8000/PG15432/Redis16379. Docker on this host: `%LOCALAPPDATA%/Programs/DockerDesktop/resources/bin/docker.exe`. Then:

```powershell
$env:PATH = "C:\Program Files\nodejs;$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
docker compose up --build -d --wait
npm run lint
npm run typecheck
npm run format:check
npm run contracts:check
npm audit --audit-level=high
node scripts/check-identity-browser.mjs
```

Fresh install uses `npm ci`; `npx playwright install chromium` supplies the browser. Exact dev dependency `@axe-core/playwright` 4.13.0, MPL-2.0; license inventory updated. Browser runner uses a separate test project and random credentials, four tests including full identity flow; fixture JSON removed afterward. Do not run concurrent instances on fixed test ports. See check record for actual results and unrun checks. Backend's 28-test result is historical Sprint 02, not newly executed here.

Local Demo organization/Admin identity and volumes are retained. Do not downgrade/reset local data to troubleshoot. No old GitHub code imported; its reuse map is a reference for later modules. No AI providers, project metrics or simulated business results are active.

## Limits and next work

Core Chromium axe/keyboard/contrast checks passed; full screen-reader, cross-browser and release-wide accessibility remain unverified. No FCP/60fps/load measurement or hosted CI run. Domain tables and saved views need server-scoped querying when implemented. Existing host sandbox ACL issue may require reviewed execution escalation; use exact per-command Git safe-directory for ownership, not global trust.

Next Sprint 04: portfolios/programs/projects, goals, work, milestones, budget/actuals, baselines and dependencies under existing tenant/project contracts. Reuse components; extend the migration chain; keep exact decimal/currency handling and explicit demo boundaries. Run domain integration/migration/negative-permission checks plus shell/identity regression.

## Next prompt (requires separate authorization)

```text
Execute Sprint 04 only. Read docs/prompts/MASTER.md and Sprint 04 in the
ordered prompts; recover context from docs/handoffs/LATEST.md. Read the
Sprint 03 frontend contract, reuse plan and relevant domain/permission/metric
contracts. Verify actual runtime, Git state, migration head and generated
contracts. Implement the portfolio and delivery system of record, preserving
identity controls and shared components. Extend migrations, seed isolated
business demo data, run required acceptance, update report/handoff/coverage
and changelog, then stop. Work economically without skipping required checks.
```
