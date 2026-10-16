# Sprint 08 acceptance checks

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

Verified 2026-10-09 on Windows PowerShell with Linux Docker services, PostgreSQL 18, Redis 8, pinned local Python/Node dependencies. Fixtures use guarded `ppm_test` or the isolated browser Compose project (3001/8001). Normal stack stays on 3000/8000. No live connector credential was available. [Report](../../../03-sprints/completed/sprint-08/SPRINT_REPORT.md), [jobs-v1](../../../contracts/jobs-integrations.md).

| Gate / actual command | Observed result | Evidence |
| --- | --- | --- |
| `docker compose --profile test run --rm test` | 63 passed; 1 inherited Starlette/httpx deprecation warning; head -> 0006 -> head -> base -> head -> repeat and metadata drift checks passed on guarded test DB | [backend](../../../verification/sprint-08-backend-security-final.txt) |
| `docker compose --profile test run --rm test python -m pytest tests/test_jobs.py -q` | 8 passed in 73.04s; final additional forged broker/foreign secret reference assertions included | [jobs](../../../verification/sprint-08-jobs-accepted.txt) |
| `node scripts/check-identity-browser.mjs` with `PPM_VERIFICATION_PREFIX=sprint-08-command-final` | 9 passed (1.2m), full existing regressions plus integration acceptance | [browser](../../../verification/sprint-08-browser-final.txt) |
| `.venv/Scripts/python.exe scripts/verify_sprint08_static.py` | Ruff, Python format, mypy (27 files), contract drift, TypeScript, ESLint, Prettier, 7 source hashes: each exit 0 | [exact commands/exit codes](../../../verification/sprint-08-static-results.json) |
| `npm audit` | 0 vulnerabilities | [audit](../../../verification/sprint-08-audit.txt) |
| `docker compose up --build -d --wait` | Healthy normal stack, forward-only 0007 | [runtime](../../../verification/sprint-08-runtime.txt) |
| `.venv/Scripts/python.exe scripts/sprint08_preserve.py before` and `after` | Private binary dump retained; 54 old table counts/hashes identical after migration and final restart | [before](../../../verification/sprint-08-preservation-before.txt), [final](../../../verification/sprint-08-preservation-final.txt) |
| Final `GET /api/v1/health/ready` and `/integrations` | HTTP 200, database/Redis/storage ready | [final runtime](../../../verification/sprint-08-final-runtime.txt) |
| Normal Linux worker checkpoint probe | Real Redis/Celery result; unchanged checkpoint `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c` | [worker](../../../verification/sprint-08-worker.txt) |
| `node scripts/check-persistence.mjs` | Worker/API/web/dispatcher/PostgreSQL/Redis restart and stored objects/checkpoint survived | [persistence](../../../verification/sprint-08-persistence.txt) |

## Security and correctness acceptance
- Actual Linux Celery subprocess killed during 500-row import, lease expires, process restarted: two attempts, exactly 500 source/target effects. Tests exercise cancellation, max-attempt dead letter, rate/backoff and frozen page resume.
- Same import/job key and signed GitHub delivery replay reuse persisted results; changed-body key collision rejects. Per-connection source repeat deduplicates. Rejected rows recover without duplicate successful effects; local revision changes and timestamp collisions produce quality errors.
- Restricted app-role RLS, cross-tenant source/target constraints, forged broker tenant/actor, foreign tenant secret reference, Viewer access, revoked/expired Admin/session/project scope and SSE revocation/resume/gap/24-hour retention are covered.
- CSV/Jira issue/sprint/GitHub issue/PR contract fixtures cover mappings and timestamp semantics. Provider fixture simulations cover rate/auth/transport failures; they are not real network authentication proof. Native public GitHub HMAC route validates repository/type/signature/delivery and delegated scope; signed batch gateway retains CSRF.
- Bound request/page/row inputs; deny arbitrary/internal host URLs and redirects; incidental source notes discarded. Imported closed sprint historical coverage is unknown, preventing fabricated velocity.
- Browser previews one good and one invalid row, queues partial result, observes live stages, resumes terminal SSE, repeats without duplicates, inspects source evidence and refreshes a sibling command-center snapshot. Viewer tenant switch prevents hidden run subscription. Keyboard and axe serious/critical checks and no overflow passed at 1440/768/360; screenshots visually inspected.

## Run boundaries and retained failures
Earlier backend runs found migration/normalization/typing issues and were repaired; the final full suite passes. Initial browser runs exposed duplicate rendering and exact-label selector errors, repaired before the final nine-test run. All earlier logs remain under `sprint-08-*` for audit.

`sprint-08-jobs-final.txt` failed because the normal persistence restart interrupted the shared PostgreSQL process while focused tests were running. After restart the unchanged focused suite passed all eight in `sprint-08-jobs-accepted.txt`. The standalone Windows unit pytest invocation stalled and was terminated; its empty log is not passing evidence. Linux full-suite verification includes those unit cases. No separate Windows unit success is claimed.

No hosted CI, real Jira/GitHub credentials, externally reachable webhook, production load/latency/SLA, physical retention purge or full accessibility certification was verified. These do not prevent the explicitly permitted local fixture acceptance. Normal data was never seeded or downgraded. Applied migrations 0001–0006 have no changes; now-applied 0007 is frozen. Older tracked browser screenshots regenerated by regression tests were restored to their baseline bytes.
