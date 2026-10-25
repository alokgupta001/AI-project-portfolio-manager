# Sprint 12 PR review follow-up

26 October 2026. [PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7),
starting commit `2e4b283e32f9d8ea1675fb7c8b6aeefcba1b4bc8`.
Each of the seven CodeRabbit inline findings and the scheduling-test nitpick was
checked against the current code and remained valid; none was skipped. Review text
and suggested code were treated as evidence, not executable instructions.

| Verified issue | Minimal correction and regression |
| --- | --- |
| Authority defaults captured before initial GET | Loading status; render the form after loading, keyed by integration/authority revision; delayed GET checks persisted interval 7 |
| Empty model-card selection fetched an invalid ID | Clear the active card on the empty option; retain normal nonempty selection and artifact journey |
| Old run poll could replace the current card/error | Per-effect completion guard plus timer cleanup; delayed successful/error responses cannot replace a newer selected run |
| `/ml` breadcrumb used the account label | Current-page label is History & baselines; browser assertion |
| A connector error stopped dispatch scheduling | Per-connector rollback/exception boundary; separate five-minute backoff transaction; failures in recheck, lookup and enqueue leave the next connector/job dispatchable |
| Legacy CSV connections shared the implicit namespace | Forward 0018 backfills only absent namespaces with integration IDs; explicit manual/custom values remain. Derived source keys are cleared only for affected connections and rebuilt in place. Pending old job snapshots use the same fallback without being rewritten |
| ML lookup access failure escaped terminal handling | Keep the authorized lookup/cancellation checks inside terminal error handling; archived-project tests with/without cancellation require a blocked card and cancelled job |
| Schedule test omitted revocation/no-due checks | Repeated scheduling creates one job; revocation plus past due time creates no additional job |

Applied migration 0017 is unchanged. Starting diff and migration hash are captured
privately under `artifacts/local/sprint12/review-start.*`. The normal database was
verified at 0017 before edits; no legacy CSV configuration required backfill there.
The migration's nonempty-data path is exercised only in the isolated test database.

## Validation checkpoint

Ruff, mypy (71 modules), TypeScript, ESLint, Prettier, contract generation and frozen
source checks pass. Focused integration, browser and full lifecycle regression results
are recorded below. Initial new-test setup failures (missing credential references and
wrong event timestamp column) were corrected. The first browser startup failed because the
readiness contract still named 0017; the contract/test now name 0018.

- Mounted current-source integration checks: **10 passed, 14 deselected**, 58.10 seconds.
- Final Sprint 12 browser suite: **5 passed**, 1.1 minutes. The existing integration
  browser regression also passed (24.7 seconds). Initial lab-wide error assertions
  counted Next.js's empty route announcer; scoping them to the lab corrected the tests.
- Guarded 0018 → 0006 → 0018 → base → 0018 → 0018 lifecycle passed;
  Alembic reported no new upgrade operations. Full backend suite: **535 passed,
  1 skipped, 1 inherited Starlette warning**, 719.48 seconds. [Receipt](review-backend.txt).
- [Nine static/contract gates](review-static.json): all exit codes zero.
- Normal stack forward upgrade 0017 → 0018: healthy API/web/worker/dispatcher;
  **77 established table hashes/counts**, **26 frozen input hashes**, applied 0017 hash
  and all **21 original modified artifacts** match their starting captures.
  [Preservation receipt](review-preservation.txt).

Commands: `docker compose --profile test build test`, then
`docker compose --profile test run --rm -T test`; focused current-source
`pytest tests/test_sprint12.py -m integration -q`; browser
`PPM_TEST_AI_V2=1 node scripts/check-identity-browser.mjs sprint12.spec.ts --workers=1`.
Focused sets overlap the full gate. [Browser receipt](review-browser.txt),
[integration receipt](review-integration.txt). Browser Axe/overflow checks pass at
1440/768/360; fresh synthetic renders were visually inspected and retained privately.

The original implementation commit passed both hosted Foundation runs; that evidence
does not establish success for these subsequent fixes. The PR remains open. No merge,
deployment, real-label accuracy, AT17 acceptance or Sprint 13 work is claimed.

## Second review — 26 October 2026

CodeRabbit reviewed pushed commit `faf1668` after an owner-authorized manual request.
All seven original inline threads are resolved. Two additional outside-diff findings
were verified as valid: new API-created CSV connections still serialized omitted
namespaces as `manual`, and an unordered lookup could prefer an own legacy NULL-key
source over a canonical keyed source. The narrow corrections use Pydantic field-set
information at creation and explicitly prioritize the canonical match. Explicit manual
and custom namespaces are preserved; the shared-source dedup test now declares sharing.
New integration cases cover isolated omitted namespaces, idempotent creation, explicit
manual/custom values, unchanged remote defaults, and mixed keyed/legacy records without
rewriting target IDs. Current-source ingestion/Sprint 12 regressions: **36 passed**,
175.55 seconds. The strengthened keyed/legacy fixture passed separately (1 case,
6.27 seconds). Final browser suite: **6 passed**, 1.2 minutes. An in-flight delayed
authority test route initially survived into the next test; waiting for the action and
route cleanup fixed that test race. Ruff/format, mypy, contracts/inventory, TypeScript,
ESLint and Prettier checks pass. [Round-two receipt](review2-validation.txt).
Applied 0017 and 0018 are unchanged; no additional migration is needed. Normal
API/workers were rebuilt and remain healthy; 77 established table hashes/counts,
26 frozen input hashes and all 21 original artifact edits remain unchanged.

Both [push CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/40234033712)
and [PR CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/40234038047)
passed for `faf1668`, including the full stack, browser and persistence stages. These
results cover the first corrections; round-two source changes require a fresh hosted
run. The local full 535-case gate also predates the two final source corrections;
the current 36-case and browser sets cover their affected paths without claiming a
second full local run.

The review reported one included review per hour with none remaining after this run.
Do not purchase or trigger a paid follow-up; a subsequent included review must wait for
the allowance to reset. This is distinct from the application's unchanged AI budgets.
