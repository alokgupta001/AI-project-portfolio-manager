# Sprint 07 technical handoff

## Verified checkpoint
**Sprint 07 complete locally**, 2026-10-08. Previous base commit `f53d771`; Sprint 06–07 work is recorded in the savepoint commit `savepoint up to sprint 7`. The user authorized this commit and GitHub push on 2026-10-08. Sprint 08 remains separately authorized work. Normal Docker web/API are healthy on 3000/8000, migration `0006_command_center`.

Completed: F-015, F-026–F-033, F-036–F-037, E-001–E-003 within [documented limits](../contracts/command-center.md). No known failing Sprint 07 acceptance gate remains. See [report](../sprints/SPRINT-07-REPORT.md) and [checks](../verification/SPRINT-07-CHECKS.md).

## Read these files first
1. `docs/prompts/MASTER.md`, the selected ordered sprint section, this handoff and decision register.
2. `docs/contracts/command-center.md`, `metrics.md`, `delivery.md`, `capacity.md` and ADR 013. Assessment contract/ADR 012 remain compatibility boundaries.
3. `services/api/ppm_api/command.py`, `command_schemas.py`, `metric_math.py`, `command_tables.py`; `delivery.py` owns mutations/closures. Frontend: `apps/web/components/command-center.tsx`.
4. `tests/test_command.py`, `tests/browser/command.spec.ts`, current generated OpenAPI/TypeScript by targeted lookup; do not dump generated files.

## Current implementation and contracts
`/command-center` provides Executive/Delivery/Risk/Resource views, current-state metrics with explicit period facts, source freshness/coverage, reported-versus-evidence discrepancy, native chart/table, personal saved views, keyboard evidence drawer and reauthorized JSON DTO download. Risk/benefit/metric-plan CRUD reuses the delivery editor; Admin thresholds/cadence live in Organization setup. API prefix `/api/v1/command`, contract `command-v1`, deterministic risk `risk-rule-v1`; capacity-v1 remains authoritative for staffing.

Shared Decimal budget/alignment helpers reconcile delivery summaries with dashboard/export consumers. No mixed-currency total. Health requires all three inputs; missed critical milestones can flag a Green discrepancy even when composite health is unknown. Baseline/calendar plans are explicit. Closed sprint points are frozen automatically; existing closed sprints are unknown rather than reconstructed from mutable work. No AI, new jobs, external notifications or provider calls.

Preserve live identity/organization/project scope, real app-role RLS, CSRF, revision/idempotency/audit behavior, sensitive effort grants and minimum-five team suppression. The snapshot uses the organization transaction lock; JSON download revalidates current read access. Personal saved views confer no access. Preserve completed assessment scores and frozen versions.

## Reproduction and evidence
Use the existing ignored `.env`; never bootstrap established normal data. No new dependencies. Locked Node/Python/Docker tools are retained. Docker/localhost/network checks require this environment's sandbox escalation. On Windows use `.venv/Scripts/python.exe -m mypy` (the executable trampoline failed).

- `docker compose --profile test build test` then `docker compose --profile test run --rm test`: **53 passed**, one inherited Starlette/httpx warning, guarded clean/prior/downgrade/re-upgrade/repeat/drift success. `sprint-07-backend-accepted.txt`.
- Final unknown-coverage display adjustment: `docker compose --profile test run --rm test python -m pytest tests/test_command.py -q`: **4 passed**, `sprint-07-command-final.txt`.
- `node scripts/check-identity-browser.mjs`: seven existing cases passed, new command case initially failed. Final `node scripts/check-identity-browser.mjs command.spec.ts`: **1 passed**, including 1440/768/360 no-overflow/axe and inspected screenshots. `sprint-07-browser-layout.txt`. These were separate passing invocations, not one final eight-test run.
- Contracts, typecheck/lint/format, Ruff, mypy, seven source hashes and npm audit passed. Final audit: zero vulnerabilities. Exact logs in checks.
- `docker compose up --build -d --wait`: normal forward upgrade, healthy services; baseline counts/checkpoint retained. Real worker and `node scripts/check-persistence.mjs` restart/storage checks passed. Post-restart readiness and `/command-center` HTTP 200 verified.
- Baseline only: two projects/one resource, 48 SQL statements and 79.92 ms snapshot compute; final one-project browser fixture 968 ms to visible discrepancy, 51.32 ms server compute. No scale/production compliance claim.

The inherited assessment test used an arbitrary first answer; changing lookup to question ID removed nondeterminism without modifying scoring. Earlier failed logs are preserved. Browser repairs covered selectors, empty risk text serialization and narrow-table layout.

## Data and migration state
Applied normal head: **0006_command_center**, six new RLS tables. It is now frozen; any subsequent schema repair needs a successor migration. Existing migrations 0001–0005 are unchanged. Normal checkpoint remains `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`; recorded project/portfolio/resource/organization/user/assessment/version counts match the pre-upgrade baseline. Ignored backup and JSON are `artifacts/local/sprint07-normal-before.dump`, `sprint07-normal-before.json`, `sprint07-normal-after.json`. Backups were not committed. No normal/demo downgrade or seeding. All fixtures used guarded test databases; browser stack used 3001/8001 and was stopped by its runner.

## Limits and next work
Current-state reporting is not historical reconstruction. Legacy closed sprints lack snapshots. Metric plans need explicit baseline/calendar inputs. Selector lists show first 100. Snapshots reject over 200 projects, 100 assigned resources or 5,000 project-source rows per kind; existing capacity reads remain capacity-v1 behavior. Conservative source age can mark stable old baselines stale. No automatic escalation, prediction, full accessibility certification, hosted CI or production load test. Starlette/httpx warning remains inherited.

**Next recommended sprint: 08 — durable jobs, integrations and live progress**, only when separately authorized. Metric DTOs are locally verified prerequisites. Preserve scope checks and distinguish source time from compute time when adding jobs/events. Do not rebuild completed delivery, capacity or assessment modules. Read only the selected Sprint 08 prompt and relevant job/event contracts.

Copy-ready prompt after authorization: Execute Sprint 08 only. Read MASTER, LATEST and the Sprint 07 handoff, then the Sprint 08 ordered prompt and required contracts. Preserve current data, applied migrations, scope/privacy and uncommitted work. Implement the vertical slice and required security/correctness gates, update report/checks/coverage/handoff, and stop before Sprint 09.
