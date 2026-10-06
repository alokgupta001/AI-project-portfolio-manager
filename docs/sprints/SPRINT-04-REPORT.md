# Sprint 04 implementation report

## Status and scope

2026-10-06. Complete locally, subject to the explicit limits below. Git main has no commit/remote; pre-existing and new files remain untracked. Source sections: WD/WP/W3/W4/W7/W8 and S4.2, mapped by coverage. Implemented the portfolio and delivery system of record on the existing identity and enterprise UI baseline. This makes project plans, work, financials and history persistent, scoped inputs for later capacity, assessment and intelligence modules.

## What was built

- Nineteen typed delivery resources, scoped membership grants, revisions, archive/restore, immutable audit and idempotent writes. This prevents hidden-tenant access, accidental retries and lost edits.
- Portfolio/program/project hierarchy; departments, teams, goals and owners; work/sprints/milestones/blockers/dependencies; reported status, versioned plan baselines and decimal budgets/expenditure. Forecast changes preserve approved historical plans.
- Organization setup, portfolio/project lists, project overview, work board, timeline/date table, named dependency relationships, budget summary, alignment editor and readable history, using the Sprint 03 shell/components.
- Migration 0003 extends unchanged earlier migrations. Generated API/TypeScript DTOs provide supported dashboard inputs. Demo v1 creates two isolated tenants with healthy/troubled projects and INR/USD examples; repeat seed preserves existing records.

Coverage: F-005/006/007/009/010/011/012 implemented for local Sprint 04. F-002/003 permission/isolation evidence extended. F-008 remains Sprint 05: dated login-backed teams exist, but independent resources/capacity do not.

## Verification evidence

| Acceptance | Result | Evidence |
| --- | --- | --- |
| Persistent hierarchy, work, spending, plan history, archive and security negatives | 38 backend tests passed; migration lifecycle passed | [Backend transcript](../verification/sprint-04-backend.txt) |
| Real UI lifecycle and identity/shell regression | 5 Chromium tests passed, 20.8s | [Browser transcript](../verification/sprint-04-browser.txt) |
| Runtime, typed contracts, source preservation and demo isolation | Passed locally; detailed limits recorded | [Checks](../verification/SPRINT-04-CHECKS.md) |

See [actual checks](../verification/SPRINT-04-CHECKS.md). Backend acceptance: 38 passed including existing identity tests; migration upgrade/downgrade/re-upgrade/drift checks passed. Browser regression and runtime results are recorded there. No paid service, external email, production deployment or later domain module was implemented.

[ADR 010](../architecture/adr/010-delivery-system-of-record.md) records deliberate restrictions: Admin-only cross-project dependency writes, organization-serialized mutations, immutable ledger corrections, explicit incomplete metrics and initial paged timeline/board. Computed health, working-day variance, resource capacity and executive dashboards remain future work. Automated accessibility coverage is not full certification. Git still has no initial commit/remote, so no hosted CI result is claimed.

## Why it was built

Later dashboards and AI need authoritative, permission-scoped records instead of illustrative cards. This sprint establishes the project hierarchy, measurable delivery data and historical evidence required by capacity (05), assessment (06) and dashboard (07) work. [ADR 010](../architecture/adr/010-delivery-system-of-record.md) records correctness and UI tradeoffs.

## How it works

An authorized user saves a typed project/work form through the existing same-origin transport. The API checks the live session, selected organization and CSRF, then validates scope, references, status and revision under an organization lock. PostgreSQL enforces tenant/project policies and composite references. The transaction writes the record, audit and retry receipt; the UI reloads scoped records/summary. A stale write asks the user to reload rather than overwriting another edit. Repeated creates reuse an idempotency key. Baselines capture immutable snapshots; expenses are corrected by exact reversals. See [delivery contract](../contracts/delivery.md) for endpoints, decimal units, formulas and unknown states. No AI or new background domain job participates.

## How to use and demonstrate it

Start the existing stack with `docker compose up --build -d --wait`; sign in using [identity setup](../IDENTITY-DEVELOPMENT.md). As Admin, open `/organization`, configure timezone/currency and create goals/departments/teams. Create a portfolio (optional program), then a project. On its overview, add work, milestones and budget/expenditure; save an initial baseline, change a forecast and save a second baseline. Both plans remain visible. Archive through the confirmation dialog; reload to see the preserved read-only project. Grant PM edit/manage or Viewer read to demonstrate scoped access. The [demo guide](../DEMO-DEVELOPMENT.md) provides exact isolated seed/activation commands without shared passwords. Screenshots are in ignored `artifacts/local/sprint04-project-desktop.png` and `sprint04-project-mobile.png`.

## Implementation record

[Handoff implementation map](../handoffs/SPRINT-04-HANDOFF.md) lists changed schema, API, UI, generated clients and tests. Migration 0003 expands schema without altering 0001/0002. Existing rows need no backfill; new delivery tables start empty. No package or paid service was added. Existing identity/session transport, theme and primitives are retained; server-paged tables opt out of internal table pagination. Demo port/origin overrides are documented separately. Future modules stay visibly unavailable rather than mocked.

## Operational and security behavior

Writes retain request-correlated, tenant-scoped audit history and sanitized errors. No credential/CSRF/token values are placed in reports. RLS and live grants apply to summaries as well as records. Demo mailbox remains private local storage; no external notification or provider cost. No new alerting or retention scheduler was introduced. Expand/recovery: back up the database, apply 0003 with the migration owner, verify head/readiness and generated contracts. No contraction/backfill is needed. Downgrade removes all delivery data and is destructive: only exercised on the isolated test database. For recovery with user data, restore a backup or use a forward repair; never downgrade the user's database as routine troubleshooting.

## Remaining work and decisions

See [delivery limitations](../contracts/delivery.md) and [checks](../verification/SPRINT-04-CHECKS.md): paged board/timeline, no working-calendar calculations, no FX conversion, Admin-only cross-project dependency mutations, latest-100 audit and unbenchmarked portfolio query scaling. These are explicit scope/authorization choices. Hosted CI, production and full accessibility/performance certification remain unverified. Existing mypy migration annotations and Starlette deprecation are recorded in the handoff; they do not fail the established CI check scope.

## Next sprint readiness

Sprint 05 prerequisites are locally verified. Next: independent resource profiles, working calendars and capacity allocations, preserving identity and project grants. Read [handoff](../handoffs/SPRINT-04-HANDOFF.md) and [coverage](../requirements/coverage.md). Sprint 05 has not started.
