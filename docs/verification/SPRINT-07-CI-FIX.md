# Sprint 07 hosted CI correction — 2026-10-08

Savepoint `ef196c9` was pushed successfully. Hosted run
[37723773986](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/37723773986)
passed static checks, backend tests and seven browser scenarios. Assessment submission
failed with HTTP 412: the trace shows evidence upload using revision 3 succeeded,
but the immediate reload still supplied revision 3 to submission.

The authenticated dependency committed its transaction during request-scope cleanup,
after sending the response. Set its dependency scope to `function` so transaction
commit completes before response transmission. Commit errors now also prevent false
success responses. Authorization, RLS, CSRF and revision checks remain enforced.

Acceptance:
- New ASGI regression: commit precedes response; failed commit returns 500, not 200
  (2 cases passed).
- Guarded Compose backend suite: **55 passed**, migration lifecycle and schema drift
  passed; one inherited Starlette/httpx deprecation warning.
- Isolated assessment browser scenario: **1 passed**, including independent review,
  evidence release, responsive layouts and accessibility assertions.
- Ruff lint/format and mypy passed.

Local command logs: ignored `artifacts/local/ci-fix-backend.log` and
`artifacts/local/ci-fix-browser.log`. Downloaded CI traces remain ignored because they
contain test-session data. No production data or migrations changed.

The correction will trigger a fresh hosted run on push. Its result must be checked;
local acceptance alone does not establish hosted success.
