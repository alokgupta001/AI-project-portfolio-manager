# Assessment structure cleanup — step 10

10 November 2026. User-authorized incremental refactor following
[step 9](ASSESSMENT_STRUCTURE_STEP_9.md). Framework operations now live in
[frameworks.py](../../services/api/ppm_api/modules/assessments/frameworks.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
explains the current file owners and call direction.

## Framework boundary

The new module owns the existing `list_frameworks`, `create_framework`,
`edit_framework`, `publish_framework`, `list_framework_versions` and `seed_examples`
operations, their `fw_view` response helper and `EXAMPLE_FRAMEWORKS` loader.
All seven functions and the loader move unchanged, retaining their signatures,
annotations, statements and internal calls. The four-example JSON resource stays
in the same package; the loader uses the same adjacent-file path and JSON decoding.

The shared assessment service falls from **591 to 423 lines**; the framework
module is **184 lines**. All 15 remaining service functions are unchanged. They
cover assessment workflows, grants, event history and shared assessment helpers.
Frameworks and the assessment service do not import each other or the HTTP router.
There are no forwarding aliases or compatibility re-exports.

Six HTTP handlers delegate to `assessment_frameworks` instead of
`assessment_service`. Names, parameters/defaults, response models, status codes,
mutation decorators and operation IDs are unchanged. All 21 endpoint bodies remain
single awaited delegates. No authorization boundary, transaction, session, commit,
request bound, revision rule or error handling is added or removed.

Framework pagination and editable flags, role/grant rules, frozen version snapshots,
publication/revision increments, archived-framework refusal, version-history order
and idempotent example seeding retain the same statements. Assessment lifecycle,
evidence storage, scoring, grants and private event-history operations are preserved.

## Compatibility and preservation

AST comparisons verify all seven extracted functions plus the resource loader,
the complete remaining service logic, and the router with only six delegate
targets redirected. All 21 thin HTTP bodies are checked. Complete OpenAPI JSON,
including all **113 paths** and components, and all **83 table/index definitions**
match the pre-step snapshots exactly. Generated contracts and migrations need no
changes. Direct imports between the two service modules or into the router are
explicitly checked as absent.

Hashes preserve all unrelated files among **1,657 captured files**, including
existing tests, evidence/access/mutation/scoring/validation modules, schemas,
examples, migrations, `.env`, provider configuration and earlier verification.
New repository files are limited to `frameworks.py` and this report. Current
documentation updates cover the file map, root guide, contract, handoff/checkpoints
and router/service/framework source-index entries.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, source preservation, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 54.30 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **33 focused tests, zero skipped**, in
  55.32 seconds: all 5 assessment tests, both parameterized semantic-review cases,
  document/assessment bridge privacy, full-cohort paging/result grants/equal
  timestamps, and all 24 document-parser tests. The 9 assessment/caller cases
  contain 7 database-backed cases and 2 unit cases; unit/parser cases overlap the
  Windows run and are not additive unique-test totals.
- PASS: JUnit output explicitly verifies real scanned-PDF/PNG/JPEG OCR passed and
  none of the 33 cases skipped. Exact parser/OCR package lock checks passed during
  build and execution. The Windows OCR skip remains an accurate local result.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: seven identical framework functions, identical example loader, 15
  remaining service functions and logic, six delegate redirections with original
  HTTP metadata, 21 thin endpoint bodies, complete API/table snapshots and
  preservation of unrelated files.
- PASS: documentation checker, **420 Markdown files and 6,022 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  affected tracked documentation passed `git diff --check`.

Existing tests are reused unchanged, including framework pagination and bounds,
published-version history and snapshot preservation, repeated example seeding,
delegated editing/publication denial, assessment lifecycle and grant/history cases.

The isolated run uses the established `enterprise-ppm-identity-test` Compose
project and PostgreSQL/Redis on test ports 15433/16380. Its guard requires
environment `test`, application/migration databases `ppm_test` and Redis database
1. Real providers remain disabled; selected provider/scanner calls use existing
mocks. Temporary test containers/network were removed, retaining named volumes.
No normal/demo database was reset and no ordinary application service started.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test`, `up -d --wait postgres redis` and a guarded test
container running `python scripts/verify_document_runtime.py`,
`python -m alembic upgrade head`, `python -m alembic check` and
`python -m pytest -q -rs` with all assessment tests, selected
semantic-review/document-bridge/cohort tests and all document-parser tests.
Scratch checks compare function/loader ASTs, remaining service logic, router
delegates/metadata, module imports, OpenAPI JSON, table/index DDL and file hashes.
Cleanup used Compose `down` without volume removal.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, browser/worker regressions, production deployment and
live-provider quality are not rerun or newly certified. The UI, normal schema
**0020**, provider authorization and stopped pilot state are preserved.

## Next structural step

Use the assessment feature's explicit HTTP, workflow, framework, evidence,
access, mutation, schema/table and pure-rule owners as the template for the next
backend feature. Inspect that feature's folder and callers before choosing a
small move; do not start another feature automatically in this step.
