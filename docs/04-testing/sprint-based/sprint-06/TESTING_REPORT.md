# Sprint 06 acceptance checks

Verified 2026-10-06 on the local Windows workspace with Docker Linux services. Status: passed locally after repair. See [report](../../../03-sprints/completed/sprint-06/SPRINT_REPORT.md) for scope and limits.

| Gate | Observed result | Evidence |
| --- | --- | --- |
| `docker compose --profile test run --rm test` | 49 passed, 1 inherited deprecation warning; migration clean/prior upgrade, guarded disposable downgrade/re-upgrade, repeat and drift passed | [backend](../../../verification/sprint-06-backend.txt) |
| Existing browser regression run | Six prior tests passed; new assessment initially failed account loading | [original combined run](../../../verification/sprint-06-browser.txt) |
| Final isolated assessment browser test | 1 passed after account-loading, responsive table and keyboard fixes; production build successful | [final assessment browser](../../../verification/sprint-06-assessment-browser.txt) |
| `npm run contracts:check`, typecheck/lint/format; Ruff check/format; mypy; `scripts/check_sources.py`; `npm audit --audit-level=high` | All passed; 7 source hashes intact; 0 npm vulnerabilities | [static](../../../verification/sprint-06-static.txt) |
| Final web typecheck/lint/format after accessibility markup | Passed | [final web](../../../verification/sprint-06-final-web.txt) |
| `docker compose up --build -d --wait` | All runtime services healthy, migration successful | [runtime](../../../verification/sprint-06-runtime.txt) |
| Read-only normal DB and HTTP assertions after restart | 0005; original checkpoint and projects/portfolios/resources/organizations/users counts preserved; 8 RLS tables and immutable grants; readiness and page 200 | [preservation](../../../verification/sprint-06-preservation.txt) |
| `docker compose exec -T worker python scripts/smoke_worker.py` | Real Redis/worker/PostgreSQL pass | [worker](../../../verification/sprint-06-worker.txt) |
| `node scripts/check-persistence.mjs` | Database checkpoint and stored object survived restart | [persistence](../../../verification/sprint-06-persistence.txt) |

The seven browser tests were not all rerun in a single final invocation. Six existing cases passed in the original run and the repaired assessment case passed in its final targeted run. Original failure evidence is retained rather than relabelled as passing.

The backend suite covers two departments, 87.5 versus 0 score arithmetic, adjustment to 75, all-missing/required-text behavior, invalid rubrics, old results after republishing, role/scoped grants, private evidence, cross-tenant RLS, CSRF, stale revisions, replay conflicts, self-review and wrong-assessment adjustments. See `tests/test_assessment.py` for assertions.

Browser acceptance exercises builder/publish/assign, autosave, evidence intake, submit, separate reviewer, release and completion. Axe finds no serious/critical violations at checked widths, with no page overflow. Scrollable score/comparison regions are keyboard focusable. Images were inspected: [desktop 1440](../../../verification/sprint-06-1440.png), [tablet 768](../../../verification/sprint-06-768.png), [mobile 360](../../../verification/sprint-06-360.png). Automated and visual checks do not constitute a complete accessibility certification.

Normal database forward-upgraded from 0004 to 0005 only, with a prior ignored pg_dump backup. No normal/demo downgrade, source-spec change or dependency addition. Historical review: [initial findings](SPRINT-06-REVIEW.md). Local evidence does not certify production deployment or broad-format malware scanning.
