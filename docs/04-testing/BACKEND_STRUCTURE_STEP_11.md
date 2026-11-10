# Backend structure cleanup — step 11: documents

10 November 2026. User-authorized incremental refactor following the
[assessment separation](ASSESSMENT_STRUCTURE_STEP_10.md). The next cohesive feature
was the document-source library: five related files were scattered across the API
root. They now live in [modules/documents](../../services/api/ppm_api/modules/documents/README.md).
This step groups files and updates their callers; internal operation extraction
remains a separate step.

## File map

Paths below are relative to `services/api/ppm_api`.

| Previous file | Current file |
| --- | --- |
| `documents.py` | [modules/documents/router.py](../../services/api/ppm_api/modules/documents/router.py) |
| `document_schemas.py` | [modules/documents/schemas.py](../../services/api/ppm_api/modules/documents/schemas.py) |
| `document_tables.py` | [modules/documents/tables.py](../../services/api/ppm_api/modules/documents/tables.py) |
| `document_parser.py` | [modules/documents/parser.py](../../services/api/ppm_api/modules/documents/parser.py) |
| `document_retrieval.py` | [modules/documents/retrieval.py](../../services/api/ppm_api/modules/documents/retrieval.py) |

The package initializer contains only a description. The README explains file
responsibilities and remaining combined HTTP/access/worker logic. Old modules are
absent; callers use the new owners directly without compatibility shims.

Twenty-two Python caller files are updated in addition to the five moved files.
They include main router registration, durable-job dispatch, AI/retrieval/agent
consumers, shared model/schema/table imports, migration metadata registration,
restore tooling and tests. Test monkeypatch/dynamic-import targets follow the new
module. Test assertions, scanner/provider fixtures and workflow statements remain.
Applied migration files are untouched; only Alembic's current metadata imports move.

## Parser subprocess and compatibility

The child command now runs `python -m ppm_api.modules.documents.parser`.
The previous file's `parents[1]` pointed to `services/api`; the deeper file uses
`parents[3]` to preserve that exact effective `PYTHONPATH`. Process limits,
timeouts, file bounds, source locations, scanner transport and OCR behavior are
unchanged. This relative-root adjustment is required by the folder move.

AST comparison covers all **27 affected Python files**, normalizing only imports,
the explicit module-path strings and that parser-root expression. Schema/table
file bytes match exactly. Old Python module references are checked as absent from
current service/script/test sources. Complete OpenAPI JSON, including **113 paths**
and all components, matches exactly; there are no component renames or generated
contract changes. All **83 table/index definitions** also match.

File hashes preserve unrelated work among **1,659 captured files**, including the
assessment feature, frozen migrations, `.env`, provider configuration, historical
JSON/log evidence and dependency locks. Current tutorial links/names and affected
source-index entries are updated. The completed Sprint 09 plain-language report
retains its content/results with only source-link targets retargeted. Historical
logs and planning text retain their original paths as evidence of those checkpoints.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, source preservation, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 42.31 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **42 focused tests, zero skipped,
  1 deselected**, in 104.98 seconds. This includes 8 document workflow tests,
  all 24 parser tests, all 5 assessment tests, 2 selected AI source-runtime cases,
  both semantic-review grant cases and full-cohort paging/result grants. There are
  16 database-backed cases and 26 parser/unit cases; the latter overlap the Windows
  run and totals are not additive unique-test counts.
- PASS: real scanned-PDF/PNG/JPEG OCR and the moved parser subprocess executed.
  JUnit explicitly verifies the OCR case passed and none of the selected cases
  skipped. Exact parser/OCR package lock checks passed during build and execution.
  The Windows OCR skip remains an accurate environment-specific result.
- PASS: document upload/version/replay, worker delivery, retrieval/citations,
  signed downloads, revoked access, cancellation/deletion during extraction,
  policy/retention/hold/purge/orphans, paging, private assessment links and selected
  AI source-version invalidation/fallback workflows, using existing fixtures.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No applied migration changed or downgrade ran.
- PASS: source ASTs with the explicit relocation exceptions, schema/table bytes,
  parser child/root checks, complete API/table snapshots and unrelated-file hashes.
- PASS: documentation checker, **421 Markdown files and 6,036 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  `git diff --check` reported no whitespace errors.

`test_real_clamd_and_processing_job` was explicitly deselected: this folder-move
run uses scanner transport doubles and did not start a live ClamAV service. It does
not certify live scanner/signature readiness. Real OCR was executed. No test was
added or weakened; the three affected test files change only imports/module targets
and the resulting formatting.

Only the established `enterprise-ppm-identity-test` Compose project was used,
with PostgreSQL/Redis on test ports 15433/16380. The guard requires environment
`test`, application/migration databases `ppm_test` and Redis database 1. Real
providers remained disabled and selected provider/scanner calls use existing
mocks. Temporary containers/network were removed with named volumes retained.
No normal/demo database was reset or ordinary application service started.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test`, `up -d --wait postgres redis`, guarded `run --rm -T
--no-deps test python -` and `down` without volume removal. The container ran
`python scripts/verify_document_runtime.py`, `python -m alembic upgrade head`,
`python -m alembic check` and `python -m pytest -q -rs` on document/parser/assessment
suites plus selected AI/agent/cohort cases, with
`-k 'not test_real_clamd_and_processing_job'`.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, browser/worker-service regressions, production deployment
and live-provider quality were not rerun or newly certified. UI, normal schema
**0020**, provider authorization, existing assessment rules and stopped pilots are
preserved.

## Next structural step

Extract scoped document/version lookup and write-access helpers from the grouped
router into an access module. Preserve live tenant/project checks, deleted-version
handling and private-evidence boundaries. Perform that as a separate authorized step.
