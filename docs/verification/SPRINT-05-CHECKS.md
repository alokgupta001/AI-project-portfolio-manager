# Sprint 05 acceptance evidence

Executed 2026-10-06, Windows / Docker Linux, Node 24.20.0 / Python 3.12.14,
existing locked PostgreSQL/Redis/Next/FastAPI/Chromium. No dependency change.

| Check | Actual result | Evidence |
| --- | --- | --- |
| Starting checkpoint | 0003 head, generated contracts matched; Git main had no commit/remote, all files untracked | Initial tool observations / Sprint 04 handoff |
| `docker compose --profile test build test`; `docker compose --profile test run --rm test` | **44 passed**, 72.61s; inherited Starlette/httpx warning | [Backend](sprint-05-backend.txt) |
| Migration runner | Prior-head upgrade, downgrade base, clean/repeat upgrade, `alembic check` passed without drift | Same transcript |
| Capacity | 2×3h projects, 4h part time, holiday/leave spanning milestone, zero/missing capacity, end-exclusive dates, spring/fall DST, daily/weekly reconciliation | `tests/test_capacity.py` |
| Security | PM resource+project grants, hidden project partial totals, Viewer denial, live revocation, cross-tenant API/SQL, pooled RLS cleanup, non-bypass role, SQL immutable calendars and PM archive rejection | Backend tests |
| Effort/privacy | Admin without grant denied; coverage unknown until attested; amendments invalidate coverage; revocation hides raw audit; five-resource complete overtime and sustained overload verified | Backend tests |
| Concurrency/history | 200/412 allocation race, idempotent replay/mismatch, unchanged immutable snapshot after edits | Backend tests |
| Full browser attempt | Five existing scenarios passed; new staffing selector failed | [Regression transcript](sprint-05-browser.txt) |
| `node scripts/check-identity-browser.mjs tests/browser/capacity.spec.ts` | Final **1 passed, 15.1s**; real create/split/leave/snapshot/reload/Viewer switch, axe tags, Escape modal, no 360px page overflow | [Final staffing run](sprint-05-capacity-browser.txt) |
| Visual QA | Final desktop/mobile screenshots reviewed; repaired mobile date wrapping using scrollable tables; desktop shared metric grid | Ignored `artifacts/local/sprint05-resources-*.png` |
| Static / contracts | npm typecheck/lint/format:check/contracts:check, Ruff check/format and mypy application/worker (16 modules) passed; final formatting rechecked after CSS repair | Tool outputs |
| Source / dependency security | Seven preserved hashes passed; npm audit: 0 vulnerabilities; unchanged dependency locks. Original 0001 hash remains C25D97DCFC74E0901A37673C160A7DBE6A80F7AD07B8A8BADCC80BA4127B4116 | Tool outputs |
| `docker compose up --build -d --wait`; migration current | Production web build and healthy local stack; `0004_capacity (head)` | [Runtime](sprint-05-runtime.txt) |
| `docker compose exec -T worker python scripts/smoke_worker.py`; `node scripts/check-persistence.mjs` | Real Redis/Celery/PostgreSQL worker passed; storage and database checkpoint survived full stack restart. Original instance remains `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`, now schema 0004 | [Worker/persistence](sprint-05-persistence.txt) |

## Repairs and limits

Initial backend caught readiness still expecting 0003; corrected to 0004. Browser
combobox/rowheader locators were repaired and a separate capacity identity prevents
password-reset regression interference. Mobile screenshot review found character
wrapping; fixed and reran the affected browser test. SQL resource archive restriction
was tightened and retested. An added test import was corrected before final acceptance.

The five successful existing browser scenarios were not rerun after capacity-only
refinements. No hosted CI, extra browser engine, full screen-reader/WCAG certification,
load/FCP benchmark, real workforce intake, provider/AI or production verification.
Full-resource metrics deliberately require Admin; other project scopes are partial.
No atomic transfer or automatic snapshot-per-edit/as-of service. Original migrations
were preserved; every downgrade ran only in guarded disposable ppm_test.
