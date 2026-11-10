# Assessment structure cleanup — step 5

10 November 2026. User-authorized incremental refactor following
[step 4](ASSESSMENT_STRUCTURE_STEP_4.md). Shared assessment workflow/data helpers
now live in [service.py](../../services/api/ppm_api/modules/assessments/service.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
explains the current responsibilities and remaining endpoint-specific work.

## Extraction

Seven existing async helper bodies move unchanged:

| Helpers | Responsibility |
| --- | --- |
| `bump`, `event` | Invalidate saved results/advance revision and append lifecycle events |
| `answer_map` | Load saved answers and released evidence indicators |
| `scoring` | Load the frozen framework, answers and reviewer adjustments for deterministic scoring |
| `fw_view`, `a_view` | Build existing framework/assessment response views and action flags |
| `finalize_check` | Require completed mandatory answers and computable dimensions before finalization |

The router falls from 838 to 744 lines. Agents now import the service for answer
loading and have no assessment HTTP-router dependency. The service reuses the
existing authenticated principal, scoped transaction and permission/scoring helpers;
it opens no new database sessions and adds no commit/rollback behavior. Decorators,
route registration, endpoint-specific SQL and lifecycle transitions stay in place.
Framework operations are the next separate extraction.

## Compatibility and preservation

AST comparison confirms all seven helper bodies and the remaining router logic are
unchanged apart from imports. The agent caller changes only its service import and
the answer-loader's module qualifier. Complete OpenAPI JSON, including all 113
paths, component names and operation IDs, and all 83 table/index definitions match
the current pre-step snapshot exactly. No schema or generated contract changes are
required.

Existing access/mutation/scoring/validation modules, schemas, examples, applied
migrations, local `.env`, tracked provider configuration, earlier evidence, tests
and unrelated local edits are preserved. Normal provider authorization and stopped
pilot state are not changed. The source index updates only router/agent sections
and adds the service; the scoring learning chapter points to the new data loader.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format and
  API/worker typing, preserved source manifest, generated contracts, ESLint,
  frontend/browser TypeScript, Prettier and all three tooling tests. Offline
  backend: **416 passed, 1 skipped, 166 integration cases deselected**, in 39.41
  seconds, with the inherited Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **8 focused tests** in 27.01 seconds:
  all 5 assessment tests, both parameterized semantic-review cases (read/edit grant)
  and the document/assessment bridge privacy case. These cover 6 database-backed
  cases plus 2 unit cases overlapping the offline run. The checks exercise saved
  result views, weighting/coverage and overrides, completion, lifecycle histories,
  revision/replay, immutable versions, tenant scope and private assessment sources.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: all 7 moved helper bodies, remaining router logic, expected agent import/
  qualifier change, full API JSON and table/index DDL match the pre-step snapshot.
  No unrelated existing file changed among 1,650 captured files.
- PASS: documentation checker, 415 Markdown files and 5,979 local links/anchors,
  no missing targets and retained historical requirement/status boundaries.
- PASS: the only assessment HTTP-router import left in API/scripts/tests is the
  application entry point registering its router. Agent data loading uses the service.

Only the established `enterprise-ppm-identity-test` Docker project was used, on
PostgreSQL/Redis test ports 15433/16380. The check script refuses any environment
other than app environment `test`, database `ppm_test` for both roles and Redis
database 1. Real provider execution remained disabled; selected provider/scanner
interactions used mocks. Temporary test containers and network were removed,
retaining named volumes. No normal/demo database or ordinary application container
was started, rebuilt or reset.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; the guarded test
container's `python -m alembic upgrade head`, `python -m alembic check`, and the
same assessment/semantic-review/document-bridge test selectors as the preceding
step; and `python scripts/check_documentation.py`. Scratch checks compare ASTs,
complete OpenAPI JSON, table/index DDL and preserved file hashes.

Other integration cases, browser/worker regressions, production deployment and
live-provider quality were not rerun or newly certified. The UI and normal schema
**0020** are unchanged. This is an initial shared-helper service; endpoint-specific
operations still need the separate extraction described below.

## Next step

Move framework operations behind thin route handlers, preserving current permission
and mutation boundaries, frozen published versions and the existing request/response
contract. Do not combine this with changes to scoring or other features.
