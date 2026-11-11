# Assessment structure cleanup — step 9

10 November 2026. User-authorized incremental refactor following
[step 8](ASSESSMENT_STRUCTURE_STEP_8.md). Grant management and private event-history
operations now live in [service.py](../../services/api/ppm_api/modules/assessments/service.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
explains the file responsibilities.

## HTTP boundary

| Existing route handler | Service operation |
| --- | --- |
| `set_access` | `set_access_grant` |
| `history` | `list_assessment_events` |
| `access_list` | `list_access_grants` |

The router falls from 282 to 219 lines. All **21 endpoint bodies** now contain one
awaited operation call. SQLAlchemy, table/access helpers, membership/user tables,
UUID generation and timestamp imports are no longer needed in the router.
It owns HTTP metadata/validation, the unchanged 2 MiB request bound and mutation
decorators; evidence storage operations remain in their dedicated module.

The three operation statement bodies move unchanged. Grant writes still require
the route's live authorization/idempotency boundary, active tenant membership and
the appropriate recipient role; completed-result grants still require completion.
Replacing a grant retains the original deactivate-then-insert statements. Grant
listing still requires Admin, exactly one target, tenant-scoped lookup and active
records ordered by ID. Event history still checks private-evidence access and
orders by creation time then ID. Result-only access exposes no private history.

Service operations reuse the existing principal and transaction. The grant-write
service omits the unused request parameter; the HTTP signature and `@mutation`
remain unchanged. No sessions, commits, re-exports or duplicate decorators are added.

## Compatibility and preservation

AST comparisons verify three identical operation bodies, original route metadata,
direct delegation, all 19 previous service functions and the remaining router
logic. All 21 endpoint bodies are checked as single awaited delegates. Complete
OpenAPI JSON, including all 113 paths/components, and all 83 table/index definitions
match the pre-step snapshot exactly. Contracts and migrations need no changes.

The existing workflow tests gain public grant-list success/filter checks,
missing/both-target validation, non-Admin denial, cross-tenant target denial,
private-history denial for a completed-result reader and chronological event
ordering. Existing assertions remain. No new test file or framework is introduced.

Unrelated files among 1,656 captured files are preserved by hash, including
evidence/access/mutation/scoring/validation modules, schemas/examples, applied
migrations, `.env`, provider configuration and earlier verification. Only the
router, service, assessment test and named current documentation are edited.
This report is the only new repository file. Source-index updates are limited to
the router, service and assessment-test entries.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, source preservation, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 55.71 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **33 focused tests, zero skipped**, in
  68.39 seconds: all 5 assessment tests, both parameterized semantic-review cases,
  document/assessment bridge privacy, full-cohort paging/result grants/equal
  timestamps, and all 24 document-parser tests. This includes the extended public
  grant/history assertions. The 9 assessment/caller cases contain 7 database-backed
  cases and 2 unit cases; unit/parser cases overlap the Windows run.
- PASS: JUnit output explicitly verifies real scanned-PDF/PNG/JPEG OCR passed and
  none of the 33 cases skipped. Exact parser/OCR package lock checks passed during
  image build and execution. The Windows OCR skip remains an accurate local result.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: exact operation-body/route comparisons, all 19 prior service functions,
  all 21 thin handlers, complete API JSON, table/index DDL and unrelated file hashes.
- PASS: documentation checker, **419 Markdown files and 6,013 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  `git diff --check` reported no whitespace errors.

The isolated run uses the established `enterprise-ppm-identity-test` Compose
project and PostgreSQL/Redis on test ports 15433/16380. Its guard requires
environment `test`, application/migration databases `ppm_test`, and Redis database
1. Real providers remain disabled; selected provider/scanner calls use existing
mocks. Temporary test containers/network were removed, retaining named volumes.
No normal/demo database was reset and no ordinary application service started.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; a guarded container
running `python scripts/verify_document_runtime.py`, `python -m alembic upgrade head`,
`python -m alembic check` and `python -m pytest -q -rs` with all assessment tests,
selected semantic-review/document-bridge/cohort tests and all document-parser tests.
Scratch checks compare operation ASTs, delegates, route metadata, existing service
functions, complete OpenAPI JSON, table/index DDL and preserved file hashes.
Cleanup used Compose `down` without volume removal.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, browser/worker regressions, production deployment and
live-provider quality are not rerun or newly certified. The UI, normal schema
**0020**, provider authorization and stopped pilot state are preserved.

## Next structural step

The assessment router extraction is complete. Separate framework authoring/version
operations from the growing shared service module, keeping dependency direction
clear and preserving transactions and the existing HTTP contract. Perform that
as a separate user-authorized step.
