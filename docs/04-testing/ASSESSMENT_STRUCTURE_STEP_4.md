# Assessment structure cleanup — step 4

10 November 2026. User-authorized incremental refactor following
[step 3](ASSESSMENT_STRUCTURE_STEP_3.md). Existing assessment write protection now
lives in [mutations.py](../../services/api/ppm_api/modules/assessments/mutations.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
describes the current file responsibilities.

## Extraction

Two existing top-level helpers move without changes to their bodies:

| Helper | Responsibility |
| --- | --- |
| `mutation` and its nested `wrapped` function | Lock and authorize the current request, validate its idempotency key/fingerprint, check scoped replay, invoke the handler, translate existing validation/conflict errors, cache the response and record its request audit |
| `revision` | Preserve the existing 428 response for missing `If-Match` and 412 for a stale revision |

The router falls from 908 to 838 lines and imports these helpers at its existing
decorator/check locations. Live access is still checked after the lock and before
the replay lookup. A valid replay returns the existing cached response at the same
point; a successful new write retains its existing response-cache and request-audit
order. Handler-level revision checks stay in their existing positions.

`functools.wraps` remains intact. Decorated handler names, signatures, annotations
and generated API definitions retain their existing meaning. Assessment lifecycle
events and workflow/data helpers remain in the router for a later service extraction;
they are distinct from request audit recording inside the mutation wrapper.

## Compatibility and preservation

AST comparison confirms the two helper bodies, nested wrapper and remaining router
workflow are unchanged except for imports. Full OpenAPI JSON, including all 113
paths, components and operation IDs, is identical to the pre-step snapshot; all 83
table/index definitions also match. No contract generation or migration is needed.

Existing access/scoring/validation modules, schemas, examples, applied migrations,
the local `.env`, tracked provider configuration, earlier verification and unrelated
local edits are preserved. Agent/document code and existing tests are untouched.
Provider authorization and stopped normal pilot state are not changed. Source-index
updates are limited to the router section and new mutations section.

## Verification

- PASS: the complete existing `npm run check` workflow: Python lint/format and
  API/worker typing, source-manifest preservation, generated contracts, ESLint,
  frontend/browser TypeScript, Prettier and all three tooling tests. Offline
  backend: **416 passed, 1 skipped, 166 integration cases deselected**, in 40.73
  seconds, with the inherited Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **8 focused tests** in 25.69 seconds:
  all 5 assessment tests, both parameterized semantic-review cases (read/edit grant)
  and the document/assessment bridge privacy case. These cover 6 database-backed
  cases plus 2 unit cases overlapping the offline run. Retry/replay, revision
  conflicts, independent review, immutable histories and private evidence remain
  covered by the existing assertions.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: all 113 API paths/components, all 83 table/index definitions, both moved
  helper bodies (including the nested wrapper), remaining router workflow and
  unrelated existing files match expected pre-step content among 1,648 snapshots.
- PASS: documentation checker, 414 Markdown files and 5,969 local links/anchors,
  no missing targets and retained historical requirement/status boundaries.

The Docker check used only `enterprise-ppm-identity-test`, PostgreSQL/Redis test
ports 15433/16380, database `ppm_test` and Redis database 1. Its guard refuses a
different app environment or application/migration database. Real provider
execution remained disabled; provider/scanner interactions in the selected tests
used mocks. Temporary test containers and network were removed after validation,
retaining named volumes. Normal/demo databases and ordinary application containers
were not started, rebuilt or reset.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; the guarded test
container running `python -m alembic upgrade head`, `python -m alembic check`, and
the same focused assessment/semantic-review/document-bridge selectors recorded in
[step 3](ASSESSMENT_STRUCTURE_STEP_3.md); and
`python scripts/check_documentation.py`. Scratch checks compared ASTs, full OpenAPI
JSON, table/index DDL and existing file hashes. No new implementation-mirroring
tests or compatibility wrapper copies were added.

Other integration cases, browser/worker regressions, production deployment and live
provider quality were not rerun or newly certified. The UI was not changed;
normal schema **0020** and applied migrations remain unchanged.

## Next step

Extract workflow/data helpers into a service module, including the helpers reused
by agents, while retaining lifecycle transitions, authorization and transaction
behavior. Keep that work separate from this write-safeguard extraction.
