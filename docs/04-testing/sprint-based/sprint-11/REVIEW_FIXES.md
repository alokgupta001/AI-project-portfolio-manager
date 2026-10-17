# Sprint 11 PR #3 review fixes

16 October 2026. Base `e608a09`, dedicated branch `sprint-11-specialist-review`,
[PR #3](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/3).
Review text was treated as untrusted data and each of the five findings was
checked against current code. Four fixes are implemented. The output-budget
increase is deferred because the user explicitly required unchanged controls.
No CodeRabbit CLI, paid reviewer or live provider call was invoked.

## Verified findings and changes

| Finding | Disposition and validation |
| --- | --- |
| Citation slices used UTF-16 offsets | Fixed with code-point slicing and unchanged span bounds. The browser fixture includes a non-BMP character; the exact complete excerpt is asserted. |
| Backups preceded SQL/hash validation | Fixed: compute hashes and successfully write the JSON checkpoint before creating permanent backups. Offline tests simulate both query and JSON-write failure, verify no blocking files remain, retry successfully and reject overwriting an existing checkpoint. No real backups are touched by these tests. |
| Independent assessment reviewer with only a view grant could not read analyses | Fixed in forward migration `0014_specialist_reviewer`; published 0013 is unchanged. The existing independent-review criteria and current project scope apply. The API calls this grant `read`. Integration and browser fixtures exercise read-only project access, separate original/suggested/approved scores, acceptance/rejection and immutable history. |
| Specialist batches can exceed 512 tokens | Valid limitation; requested increase deferred. The user's explicit instruction to preserve limits controls over review text. Provider calls, persisted ceiling and replay controls remain at 512 with unchanged request/retry limits. An intercepted realistic nine-agent truncation fixture verifies `MAX_TOKENS` fails honestly and exposes missing/unavailable agents without retrying through another provider or increasing the ceiling. This does not establish actual tokenizer fit or real-model quality. |
| Listing revalidated every full analysis | Fixed: one bounded RLS-filtered query returns ID/status/time and stored semantic status only. Detail retains current evidence and review checks. A regression fails if listing invokes detail, capture, source revalidation or full AI view. Pagination and role/tenant denial remain covered; polling is unchanged. |

## Hosted CI diagnosis

The [original pull-request CI run](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38930286777)
passed static checks, backend regressions and migration lifecycle checks, then
failed browser acceptance: 16 passed, two failed. The two GitHub failure indicators
are workflow invocations for push and pull-request events.

The default browser runner seeded specialists only when the literal filename was
passed. Full-suite execution therefore tried to log in with an undefined email.
The runner now initializes specialist fixtures for both default and focused runs;
captured setup errors expose stderr for diagnosis. Its isolated test database,
disabled provider settings and volume-preserving cleanup are retained.

The shell contrast failure occurred during a theme switch: text changed immediately
while button backgrounds animated for 140 ms. Background theme changes are now
immediate; hover shadows retain their transition. The existing shell journey
checks automated accessibility in both themes at 360, 768 and 1440 px.

The first local follow-up used the review's word `view` as an API grant value;
the existing schema correctly rejected it (valid values are `read`, `edit`,
`manage`). The fixture was corrected to `read`. A subsequent browser run exposed
competing logout/login navigation; the test now awaits the actual logout redirect
before signing in again. These are test synchronization/setup corrections, not
permission-model changes. Earlier failed results are retained below.

## Fresh validation

Final full backend regression: **257 passed in 451.34s**, including 54 specialist
tests and two backup retry tests. One existing Starlette/httpx deprecation warning
remains. Command: `docker compose -f compose.yaml -f compose.documents.yaml
--profile test run --rm --no-deps` with read-only test/script mounts and private
JUnit mount, `PYTEST_ADDOPTS=--junitxml=/evidence/backend-final.xml`, then
`test python scripts/test_backend.py`. Clean/base/prior-head migration lifecycle,
repeated upgrade and Alembic drift checks pass. The dedicated
`test python scripts/check_agent_migration.py` also passes both 0013 and 0012
round trips to 0014. All destructive checks are guarded to `test/ppm_test`.

Final full browser command: `node scripts/check-identity-browser.mjs --workers=2`.
**18 passed in 4.3m**, including exact Unicode evidence, the independent read-only
reviewer, rejection/history/reload, disabled-provider durable execution, role
denial, keyboard scrolling and light/dark automated accessibility. A fresh mobile
render was visually inspected. Earlier completed follow-up runs recorded 256
backend passes with one invalid-fixture failure and 17 browser passes with one
navigation race; these are superseded by the final complete passing runs.

Ruff lint/format (131 files), mypy (47 modules), ESLint, TypeScript, Prettier,
OpenAPI/client drift and all three generated source inventories pass.
Documentation checks cover 315 Markdown files and 4945 local links/anchors with
zero missing links, 156 requirements, 36 gaps and 115 required artifacts across
13 sprint packages. Seven frozen source manifest entries and 22 original frozen
file hashes still match. Twenty-four historical regression artifacts were restored
byte-for-byte; fresh renders remain private. No provider configuration, allowlist,
budget/retry/cancellation logic, CI workflow or existing migration was changed.

See the [machine receipt](../../../verification/sprint11-review-fixes.json) for
commands, normalized code hashes, JUnit hash and the deferred finding. Hosted CI
for the upcoming revision is outside this local checkpoint; current results are
shown on PR #3.

## Preservation and remaining gates

Normal head was read as `0012_ai_runtime`; only disposable `ppm_test` databases
receive 0014 or destructive lifecycle checks. Existing 0001–0013 migrations,
configuration/keys, objects, records and named volumes are preserved. Original
[Sprint 11 evidence](../../../verification/sprint11/results.json) and
[PR #1's six-fix receipt](../../../verification/coderabbit-review-fixes.json)
remain historical evidence for their checkpoints. Fresh screenshots go to the
ignored `test-results/sprint11-review` folder; historical screenshots are preserved.

The full nine-specialist/semantic output may still exceed 512 tokens; partial or
unavailable output is explicit. Raising this limit needs a new authorized budget
decision. Real-provider semantic quality remains **UNVERIFIED/BLOCKED**. Branch
protection still requires a qualifying approving review. No merge, deployment,
normal migration or Sprint 12 work is performed by this follow-up.
