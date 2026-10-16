# Testing strategy and current commands

Sprint 11 [actual testing report](sprint-based/sprint-11/TESTING_REPORT.md) adds 36 per-agent input cases plus real database review/privacy/revocation/budget/cancellation/lease/replay fixtures, migration lifecycle and persistent browser journeys. All use offline doubles/intercepts with provider transports denied. Keep real-model quality UNVERIFIED/BLOCKED; destructive lifecycle is guarded to `test/ppm_test`.

## Historical checkpoints before Sprint 11

This is strategy/run guidance, not an executed full application report. Historical evidence: [sprint checks](sprint-based/README.md) and [8.1 report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md). Future acceptance: [gap plan](GAP_ACCEPTANCE_TEST_PLAN.md).

| Category / purpose | Real infrastructure and run command | Scope / limits |
| --- | --- | --- |
| Backend unit tests: deterministic input/arithmetic/config | Windows `.\.venv\Scripts\python.exe -B -m pytest tests/test_ingestion_mapping.py tests/test_config_storage.py -q -p no:cacheprovider --basetemp=artifacts/documentation-audit/pytest-focused-20261009` | Explicit pure mapping/config/storage tests; no normal DB. The broad marker-selected run hit sandbox temporary-directory errors and was interrupted; the focused command passed with a workspace basetemp. Use guarded Compose for integration acceptance. |
| API/database integration: stored behavior and transaction boundaries | `docker compose --profile test run --build --rm test` | `scripts/test_backend.py` guards `ppm_test`; identity/delivery/capacity/assessment/command/jobs/pilot/transaction tests; lifecycle/drift on disposable test DB only |
| Frontend/end-to-end: real role-specific browser journeys | `npx playwright install chromium`; `node scripts/check-identity-browser.mjs` | Playwright `tests/browser`; isolated identity-test project, independent volumes/origins; fixture scripts can mutate only that disposable environment |
| API/schema contract drift | `npm run contracts:check` | Compares generated OpenAPI/TypeScript; no planned endpoint may be listed as current |
| UI static checks | `npm run typecheck`; `npm run lint`; `npm run format:check` | Type/error/format checks are not interactive user acceptance |
| Security/tenant isolation | Full guarded backend and browser suites; focus `test_identity.py`, `test_pilot.py`, assessment/capacity cases | Two tenants, ID substitution, revocation, CSRF, changed scope and sensitive effort; check negative cases rather than relying on UI hiding |
| Worker/persistence | `docker compose exec -T api python scripts/smoke_worker.py`; `node scripts/check-persistence.mjs` | Specific worker round trip/restart fixture; writes/restarts require intended local acceptance scope and are not run during a docs-only audit |
| Source preservation | `.\.venv\Scripts\python.exe scripts/check_sources.py` | Frozen source hashes; separate from application regression |
| Source/keyword grounding | Sprint 09 isolated backend/parser and document browser checks; [executed report](sprint-based/sprint-09/TESTING_REPORT.md) | Scope/citations/tickets, real scanner/OCR, hostile text and synthetic keyword baseline verified locally. Model inference/semantic quality remain planned 10–14. |
| Performance/recovery/release smoke | PLANNED TEST — NOT YET EXECUTED | 22/23 documented workload/device/profile and restore/rollback exercises; historical tiny-fixture timings do not prove targets |

## Test environment and interpreting results

Follow [local environment instructions](../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) for locked tools/services and [identity tests](../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md). Keep `ppm_local`, `ppm_demo` and guarded `ppm_test` distinct. Do not run lifecycle/reset/seed against the normal database. Existing tests contain integration/worker markers; a collected definition is not a pass. Static checks and fixture success cannot close live provider gates.

For a regression, record expected/actual, command, environment, fixtures, code revision and retained output. Preserve old successful reports even when a current run fails; add the current defect separately. Cover empty/invalid/stale/network/unavailable-provider cases, totals/relationships/periods and permissions. Run only checks relevant to changed behavior; documentation-only link/source checks do not require resetting application data.

Final release acceptance remains [the existing release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md); no gate is weakened by this strategy.

## Sprint 09 scanner-aware acceptance

Use `docker compose -f compose.yaml -f compose.documents.yaml --profile test run --build --rm test`
with a healthy scanner; the runner guards the disposable database. Browser runner:
`node scripts/check-identity-browser.mjs documents.spec.ts`. Real commands, log names,
123 full backend passes and separately accepted browser runs are in [Sprint 09 checks](sprint-based/sprint-09/TESTING_REPORT.md).
This docs-only follow-up does not rerun application/migration suites. Documentation
gates are `python scripts/documentation_inventory.py --check`,
`python scripts/check_documentation.py`, source hashes and `git diff --check`.

## Sprint 10 current closure

[Sprint 10 runtime and evidence](sprint-based/sprint-10/TESTING_REPORT.md). Retain prior coverage and original thresholds. Gemini free-tier completion/embedding smoke passed; general model-quality, hosted CI and archived Word visual gates remain open. Current evidence is in the Sprint 10 Gemini follow-up.
