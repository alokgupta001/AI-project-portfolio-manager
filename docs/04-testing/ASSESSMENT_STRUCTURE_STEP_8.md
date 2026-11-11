# Assessment structure cleanup — step 8

10 November 2026. User-authorized incremental refactor following
[step 7](ASSESSMENT_STRUCTURE_STEP_7.md). Six evidence operations now live in
[evidence.py](../../services/api/ppm_api/modules/assessments/evidence.py), behind
their existing HTTP adapters. The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
explains file responsibilities and the remaining work.

## Evidence boundary

| Existing route handler | Evidence operation |
| --- | --- |
| `evidence_list` | `list_evidence` |
| `upload` | `upload_evidence` |
| `download` | `download_evidence` |
| `delete_evidence` | `delete_evidence` |
| `preview_evidence` | `preview_evidence` |
| `release_evidence` | `release_evidence` |

The router falls from 418 to 282 lines. Each evidence handler contains one awaited
operation call. Route signatures, decorators, response models, status codes and
operation IDs are preserved. Operations accept the existing principal and, where
needed, request; file downloads still return the same response and headers.

All six operation statement bodies move unchanged. This retains tenant-scoped
lookups, evidence access, revision checks, draft/returned edit restrictions,
published-question validation, UTF-8/base64/plain-text checks, the 512 KiB/50-file
limits, server-generated private storage keys, thread-pool storage calls, SHA-256
checks, quarantine and independent reviewer release. Revision bumps, events,
attachment/nosniff headers and the existing metadata-only draft deletion behavior
are unchanged. This step adds no object cleanup or storage policy.

The 2 MiB request bound and write mutation decorators remain in the router.
Operations reuse the existing transaction, shared lifecycle helpers and access
module; they add no sessions, commits or duplicate authorization decorators.
Framework/lifecycle services, grants and history logic are untouched.

## Compatibility and preservation

AST comparisons verify six identical operation bodies, six direct delegates with
original route metadata, operation parameters with `Auth` replaced by `Principal`,
and all remaining router logic. Complete OpenAPI JSON, including all 113 paths and
components, matches the pre-step snapshot exactly. All 83 table/index definitions
also match. Generated contracts and migrations require no changes.

File hashes preserve all unrelated existing files among 1,654 captured files,
including existing services/tests, access/mutation/scoring/validation, schemas,
examples, applied migrations, `.env`, provider configuration and earlier evidence.
New repository files are limited to the evidence module and this report. Current
documentation changes are limited to the feature/root guides, contract note,
handoff/checkpoints and affected source-index entries.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, preserved source manifest, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 40.87 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **33 focused tests, zero skipped**, in
  35.34 seconds: all 5 assessment tests, both parameterized semantic-review cases,
  document/assessment bridge privacy, full-cohort paging/result grants/equal
  timestamps, and all 24 document-parser tests. The 9 assessment/caller cases
  include 7 database-backed cases and 2 unit cases. Parser and unit cases overlap
  the Windows run; these totals are not additive unique-test counts.
- PASS: real scanned-PDF, PNG and JPEG OCR executed in that Linux run. JUnit output
  explicitly verified the real OCR case passed and none of the 33 cases skipped.
  The image's exact parser/OCR package lock verification passed at build and run.
  The Windows OCR skip remains an accurate environment-specific result.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: exact operation-body/route comparisons, unchanged remaining router logic,
  complete API JSON, all table/index DDL and preservation of unrelated files.
- PASS: documentation checker, **418 Markdown files and 6,005 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  `git diff --check` reported no whitespace errors.

Existing tests were reused without additions or modifications. Runtime coverage
includes upload/quarantine, authorized preview, independent release/download,
rejected active markup, revisions/replay, lifecycle/immutable results and private
caller boundaries. Source comparisons cover all extracted statements, including
deletion; these checks do not imply every limit/error branch ran in the focused suite.

Only the established `enterprise-ppm-identity-test` Compose project was used,
with PostgreSQL/Redis on test ports 15433/16380. The test guard requires environment
`test`, application/migration databases `ppm_test`, and Redis database 1. Real
providers remained disabled; selected provider/scanner calls use existing mocks.
Temporary containers/network were removed, retaining named volumes. Normal/demo
databases and ordinary application services were not started or reset.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test`, `up -d --wait postgres redis`, a guarded test container
and `down` without volume removal. The container ran
`python scripts/verify_document_runtime.py`, `python -m alembic upgrade head`,
`python -m alembic check` and `python -m pytest -q -rs` with assessment, selected
semantic-review/document-bridge/cohort cases and `tests/test_document_parser.py`.
Scratch checks compare operation ASTs, direct delegation, original route metadata,
complete API JSON, table/index DDL and file hashes.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, browser/worker regressions, production deployment and
live-provider quality were not rerun or newly certified. The UI, normal schema
**0020**, provider authorization and stopped pilot state are preserved.

## Next structural step

Move grant management and event-history operations behind thin HTTP adapters.
Keep existing tenant/role/result-grant checks and chronological event ordering.
Perform that as a separate user-authorized step.
