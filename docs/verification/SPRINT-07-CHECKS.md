# Sprint 07 acceptance checks

Verified locally 2026-10-08 on Windows with Docker Linux services and Playwright
Chromium. **Passed within the documented local scope.** No production, hosted CI,
predictive-model or complete accessibility certification.

| Gate / actual command | Observed result | Evidence |
| --- | --- | --- |
| `docker compose --profile test build test` then `docker compose --profile test run --rm test` | 53 passed, one inherited Starlette/httpx warning; clean/prior upgrade, guarded disposable downgrade/re-upgrade, repeat upgrade and drift passed | [backend accepted](sprint-07-backend-accepted.txt), [build](sprint-07-build-final.txt) |
| Final coverage-display change: `docker compose --profile test run --rm test python -m pytest tests/test_command.py -q` | 4 passed; all Sprint 07 cases retained | [command final](sprint-07-command-final.txt) |
| `node scripts/check-identity-browser.mjs` | Seven existing scenarios passed; new command case failed blank risk text serialization, subsequently repaired | [combined regression](sprint-07-browser-final.txt) |
| `node scripts/check-identity-browser.mjs command.spec.ts` after repair | 1 passed, then final layout refinement also passed | [repaired workflow](sprint-07-command-browser-accepted.txt), [final layout](sprint-07-browser-layout.txt) |
| `npm run contracts:check` | OpenAPI and generated TypeScript match | [contracts](sprint-07-contracts.txt) |
| `npm run typecheck`, `npm run lint` | Passed; changed-form/layout files checked again after repairs | [types](sprint-07-layout-types.txt), [lint](sprint-07-lint-final.txt), [form lint](sprint-07-form-lint.txt), [layout lint](sprint-07-layout-lint.txt) |
| `npm run format:check` | Final full check passed after formatting the browser test | [format accepted](sprint-07-format-accepted.txt) |
| Ruff check/format and `.venv/Scripts/python.exe -m mypy services/api/ppm_api services/worker/ppm_worker` | Passed; 50 Python files formatted, mypy 23 source files | [Ruff](sprint-07-ruff-final.txt), [format](sprint-07-python-format.txt), [mypy](sprint-07-mypy.txt) |
| `.venv/Scripts/python.exe scripts/check_sources.py` | All seven source/prompt SHA256 entries intact | [sources](sprint-07-sources.txt) |
| `npm audit --audit-level=high` | Zero vulnerabilities; network sandbox retry required | [audit](sprint-07-audit.txt) |
| `docker compose up --build -d --wait` | Normal local forward upgrade from 0005 to 0006, services healthy | [runtime](sprint-07-runtime.txt) |
| Read-only pre/post SQL comparison, RLS/grant checks and HTTP probes | Checkpoint and project/portfolio/resource/organization/user/assessment/version counts preserved; six new RLS tables; closure UPDATE/DELETE denied to app role; readiness/page HTTP 200 | [preservation](sprint-07-preservation.txt) |
| `docker compose exec -T worker python scripts/smoke_worker.py` | Real broker/worker/database task passed | [worker](sprint-07-worker.txt) |
| `node scripts/check-persistence.mjs` | Checkpoint and stored object survived service restart | [persistence](sprint-07-persistence.txt) |

## Acceptance evidence

`tests/test_command.py` checks source/summary/dashboard money reconciliation,
separate INR/USD totals, period spend and full-period benefit filters, complete
and unknown health, configurable thresholds, freshness, resource scope, personal
views, cross-tenant app-role RLS, CSRF, optimistic concurrency, replay conflicts
and revocation, valid risk transitions and frozen velocity after task edits.
The frozen baseline/calendar gives five working days of delay over a 21-day
baseline; financial risk is 10 and capacity risk is 25. Combined risk is
`200/21 + 9.75 ≈ 19.27381`, with 100% required-input coverage. Removing sufficient
resource scope returns unknown combined risk, never a falsely healthy score.

The browser fixture is isolated and labelled DEMO: reported Green, overdue
critical security gate, INR 100,000 budget, INR 25,000 spend and 25% use. The
discrepancy and supporting date are visible in the keyboard-accessible drawer.
The test verifies portfolio/date controls, saved-view reload, risk creation,
four views, JSON DTO value reconciliation, and clearance after tenant switch.

Final screenshots were visually inspected at [1440](sprint-07-1440.png),
[768](sprint-07-768.png) and [360](sprint-07-360.png). No page overflow and no
serious/critical axe findings were observed. Tables scroll horizontally at
narrow widths and their regions are keyboard focusable; modal Escape returns
focus. This is targeted local accessibility evidence, not full WCAG certification.

## Measured baseline and limits

The two-project/one-resource API fixture issued **48 SQL statements** and measured
**79.92 ms** inside the snapshot service ([query baseline](sprint-07-command-tests.txt)).
The final one-project local browser fixture reached visible discrepancy in
**968 ms**, with **51.32 ms** server computation. Full browser navigation and
paint entries are in [rendering JSON](sprint-07-rendering.json); cached navigation,
tiny fixture size and local hardware make these observations unsuitable as a
production performance claim. Source reads are bounded and there is no load test.

The final 53-test backend run preceded only the unknown-coverage display change;
the four affected cases passed afterward. The seven older browser scenarios and
the final command case passed in separate invocations. Earlier failure logs remain
available: the assessment regression initially chose a randomly ordered answer,
fixed by question-ID lookup without changing scoring; command browser failures
identified a label selector, an incorrect test button name and blank-text/null
serialization. No unsuccessful run has been relabelled as passing.

Ignored normal backup/baselines are under `artifacts/local/sprint07-normal-before.*`
and `sprint07-normal-after.json`. No normal/demo downgrade or user-data seeding.
Checkpoint remains `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`. Migration 0006 is now
deployed locally and must not be rewritten.
