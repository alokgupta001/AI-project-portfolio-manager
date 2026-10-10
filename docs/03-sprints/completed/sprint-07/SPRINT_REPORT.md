# Sprint 07 implementation report

## Status and scope
2026-10-08. Portfolio command center and metric consistency: **complete locally**. Previous base `f53d771`; the user-authorized savepoint commit `savepoint up to sprint 7` records Sprint 06–07 work. Scope: F-015, F-026–F-033, F-036–F-037, E-001–E-003; Word Module 3 and supplementary command center/watermelon effect. No Sprint 08, AI or production acceptance claim.

## What was built
`/command-center` supplies Executive, Delivery, Risk and Resource dashboards backed by stored, authorized records. Executive shows health/coverage, money by currency, alignment and target/realized benefits with units. Delivery shows frozen sprint velocity, baseline/calendar variance, critical milestones, blockers and dependency links. Risk shows deterministic components, reported-versus-evidence discrepancy and editable risk lifecycle/readiness. Resource uses the existing capacity service and privacy-preserving team workload indicators.

Date/portfolio filters, personal saved views, an accessible evidence drawer, charts with tables and JSON DTO download share one typed snapshot. Admins configure thresholds/reporting cadence; Admins and granted PMs maintain project facts. Viewers retain scoped reads and may save their own filters. Unknown, partial and stale data remain explicit.

## Why it was built
Executives need financial and delivery measures that reconcile with source records and expose unsupported status claims. A Green report with a missed critical milestone now displays a visible discrepancy even when the composite health is unknown. [ADR 013](../../../architecture/adr/013-command-center.md) records consistency, scope and baseline decisions; the [contract](../../../contracts/command-center.md) defines all units, periods and missing-data behavior.

## How it works
An authenticated snapshot request locks the organization transaction and rechecks live membership. Restricted app-role RLS limits source projects and dependency endpoints. Shared Decimal money/alignment helpers reconcile existing delivery summaries with dashboard/export DTOs; capacity-v1 preserves resource and sensitive-effort rules. A baseline/calendar plan supplies deterministic schedule/financial inputs. Risk requires all three components (40% schedule, 35% financial, 25% capacity), and health is 100 minus risk. This is a heuristic, never a probability.

Filters select period spend, fully contained benefits, closed sprints and capacity. Current budget/health remain clearly labelled current-state values rather than historical reconstruction. Source age is separate from computation time. Sprint closure snapshots freeze completed points; pre-existing closed sprints remain unknown. Risk mutations require valid lifecycle/owner/mitigation/resolution, live edit grants, CSRF, revision checks and audited idempotent creation. Saved views are personal filters, not access grants. JSON download revalidates authorization.

## How to use and demonstrate it
Use the established ignored `.env`; never bootstrap existing data again. Start the local stack with `docker compose up --build -d --wait`, sign in at http://localhost:3000 and open `/command-center`. Configure a project in `/projects`, approved budget/expenditure and goal alignment. Record benefits and risks from the dashboard or project tabs. Add an immutable working calendar in `/resources`, freeze a project baseline and select both in its Metric plans tab; record forecast final cost. Configure organization Metric policy when different thresholds/cadence are needed. Resources and explicit effort grants remain in the existing resource workspace.

For the discrepancy demo, use the isolated browser runner `node scripts/check-identity-browser.mjs command.spec.ts`. It creates a labelled Green project with an overdue critical gate, INR 100,000 budget and INR 25,000 spend: 25% usage and a visible discrepancy. The test opens the facts drawer, filters an empty portfolio, reloads a saved view, creates a risk, exports the typed snapshot and switches to a Viewer tenant. No demo projects are inserted into normal user data.

## Implementation record
- `command.py`, `command_schemas.py`, `metric_math.py`: one authorized metric snapshot and reusable arithmetic; generated OpenAPI/TypeScript updated.
- `command_tables.py`, migration `0006_command_center`: six additive RLS tables; no changes to applied 0001–0005.
- Delivery CRUD and schemas: risk/benefit/plan/policy/view validation, live replay authorization and automatic immutable sprint closure snapshots.
- `command-center.tsx`, route and shell: responsive dashboards, filters, evidence drawer, native chart/table and existing record editor. Empty risk text fields retain empty strings.
- `test_command.py`, `command.spec.ts`: arithmetic/security/browser acceptance. An inherited assessment test selected a random first answer; it now selects the intended question ID, preserving the expected 87.5 →75 result without changing scoring.
- No new dependencies, worker jobs, external provider, AI or cloud service.

## Verification evidence
| Gate | Result | Evidence |
| --- | --- | --- |
| Full backend with guarded migration lifecycle/drift | 53 passed; one inherited Starlette/httpx warning | [backend accepted](../../../verification/sprint-07-backend-accepted.txt) |
| Final unknown-coverage display check and command security/arithmetic | 4 passed | [command final](../../../verification/sprint-07-command-final.txt) |
| Existing browser regressions | 7 passed; command scenario initially failed risk text serialization | [combined run](../../../verification/sprint-07-browser-final.txt) |
| Repaired command workflow, export and tenant switch | 1 passed | [command accepted](../../../verification/sprint-07-command-browser-accepted.txt) |
| Final mobile layout/axe/screenshots | Passed; three screenshots inspected | [layout run](../../../verification/sprint-07-browser-layout.txt) |
| Contracts/types/lint/format/Ruff/mypy/source hashes | Passed, with final changed-file follow-up | [checks](../../../04-testing/sprint-based/sprint-07/TESTING_REPORT.md) |
| npm security audit | 0 vulnerabilities | [audit](../../../verification/sprint-07-audit.txt) |
| Query baseline | 48 SQL statements, 79.92 ms compute, 2 projects/1 resource | [focused run](../../../verification/sprint-07-command-tests.txt) |
| Rendering baseline | Tiny local production-build fixture; actual values retained | [rendering JSON](../../../verification/sprint-07-rendering.json) |
| Normal forward upgrade, preservation, worker, restart/storage | Passed | [preservation](../../../verification/sprint-07-preservation.txt) |

Earlier failed logs are retained. Backend assessment failure was a nondeterministic test lookup, not changed scoring. Browser selector issues and empty risk text serialization were repaired before accepted evidence. Screenshots are inspected separately from axe; automated checks do not certify complete accessibility.

## Operational and security behavior
Tenant/project scope, live sessions, CSRF and audit remain mandatory. Six new tables use RLS; closure history has no app-role UPDATE/DELETE. An unchanged idempotent retry now also rechecks live mutation authority. Saved views cannot bypass project access. Full-resource utilization is never inferred from a PM's visible subset, and team cohorts below five are suppressed. DTO files remain local downloads; there is no external delivery.

Normal backup/checkpoint are ignored under `artifacts/local/sprint07-normal-before.*`. Normal forward migration is additive, with no historical backfill or destructive downgrade. Existing assessment scores and versions remain unchanged.

## Remaining work and decisions
Accepted local boundaries: current-state reporting; explicit baseline/calendar selection; unknown pre-existing closure history; first-100 filter selectors; snapshots reject over 200 projects, 100 assigned resources or 5,000 project-source rows per kind. Large data/throughput certification remains Sprint 23. Conservative source age may mark stable old baselines stale. No predictive failure model, automated escalation or medical inference. The inherited Starlette warning remains. No known failing Sprint 07 acceptance gate remains within this documented scope.

## Next sprint readiness
Prerequisites are verified locally; see the matching [handoff](HANDOFF.md). Sprint 08 durable jobs/integrations/live progress requires separate authorization; it has not been started.

## Subsequent verification — 9 October 2026

The original checkpoint claims above are retained. Fresh Sprint 00–08 checks, the connector mapping repair, current runtime evidence and remaining live-provider blockers are recorded in the [sprint verification report](../../../04-testing/SPRINT_VERIFICATION_REPORT.md).
