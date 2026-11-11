# Assessment structure cleanup — step 7

10 November 2026. User-authorized incremental refactor following
[step 6](ASSESSMENT_STRUCTURE_STEP_6.md). Assessment lifecycle HTTP handlers now
delegate to [service.py](../../services/api/ppm_api/modules/assessments/service.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
describes the current owners and remaining work.

## Service boundary

| Existing route handler | Service operation |
| --- | --- |
| `assign` | `assign_assessment` |
| `list_assessments` | `list_assessments` with validated pagination, framework-version and search parameters |
| `detail` | `get_assessment` |
| `save_answers` | `save_answers`, refreshing its result through `get_assessment` |
| `submit` | `submit_assessment` |
| `review` | `review_assessment` |

The router falls from 623 to 418 lines. Each lifecycle route body is one awaited
service call. Route names, parameters/defaults, decorators, response models and
operation IDs remain unchanged. Unused assignment request transport is omitted
from the service interface; revision-sensitive operations retain the request.

Operation statements are moved unchanged except for redirecting answer saving's
internal `detail(...)` call to the equivalent service `get_assessment(...)`.
Assignment eligibility/scope checks, notifications, answer validation/overrides,
completion checks, review independence, quarantine enforcement, revisions and
events retain their order. Services reuse the existing authenticated principal and
transaction; they add no sessions, commits or duplicate mutation decorators.

## Compatibility and preservation

AST comparison verifies all six operation statement bodies with that explicit
internal-call redirect, six original route signatures/decorators, all 13 prior
service functions and the remaining router logic. Complete OpenAPI JSON, including
all 113 paths/components, and all 83 table/index definitions match the pre-step
snapshot exactly. No schema or generated contract changes are needed.

Existing tests, access/mutations/scoring/validation, schemas/examples, applied
migrations, the local `.env`, tracked provider configuration, earlier verification
and unrelated edits are preserved. Provider authorization and stopped normal pilot
state are not changed. Source-index changes are limited to router and service.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format and API/worker
  typing, preserved source manifest, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 37.30 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **9 focused tests** in 28.63 seconds:
  all 5 assessment tests, both parameterized semantic-review cases (read/edit grant),
  document/assessment bridge privacy and full-cohort paging/result grants/equal
  timestamps. These cover 7 database-backed cases plus 2 unit cases overlapping
  the offline run. Coverage includes lifecycle transitions, independent review,
  answer/scoring revisions, immutable versions/history, private inputs, 125-record
  paging/filtering and scoped result-only visibility.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: six operation statement bodies with the explicit internal-read redirect,
  six original route signatures/decorators, 13 unchanged previous service functions,
  remaining router logic, complete API JSON and all table/index DDL. No unrelated
  existing file changed among 1,653 captured files.
- PASS: documentation checker, 417 Markdown files and 5,995 local links/anchors,
  no missing targets and retained historical requirement/status boundaries.

The existing tests were reused without additions or modifications. Only the
established `enterprise-ppm-identity-test` Docker project was used, with PostgreSQL/
Redis on test ports 15433/16380. Its guard refuses non-test application environments,
application/migration databases other than `ppm_test`, or a broker other than Redis
database 1. Real providers remained disabled and selected provider/scanner calls
used mocks. Temporary test containers/network were removed after validation,
retaining named volumes. No normal/demo database or ordinary application container
was started, rebuilt or reset.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; a guarded test
container running `python -m alembic upgrade head`, `python -m alembic check` and
`python -m pytest -q tests/test_assessment.py` with the existing semantic-review,
document-bridge and full-cohort selectors; and
`python scripts/check_documentation.py`. Scratch checks compared operation ASTs,
original route metadata and exact delegation, previous helper ASTs, complete API
JSON, table/index DDL and preserved file hashes.

Other integration cases, browser/worker regressions, production deployment and
live-provider quality were not rerun or newly certified. The UI and normal schema
**0020** are unchanged. Grant management, history and evidence/file handling remain
in the router for separate later cleanup.

## 10 November 2026 — real OCR verification follow-up

The owner requested execution of the OCR case skipped by the Windows offline run.
The existing Linux application test image already contains Tesseract **5.3.0**,
Poppler **22.12.0** and English OCR data. The runtime verifier confirmed exact
package versions from `infra/document-packages.lock`. Parser, test, verifier and
dependency-lock hashes inside the image matched the current checkout.

The complete `tests/test_document_parser.py` suite passed: **24 passed, 0 skipped**
in **6.02 seconds**. JUnit output explicitly confirmed
`test_real_scanned_pdf_and_image_ocr` executed successfully. Its assertions cover
recognized text from a rasterized scanned PDF, PNG and JPEG, the OCR method and
PDF page location, and an OCR confidence value within the required range.

Execution used a temporary existing-image container with `--rm --network none`,
no host mounts, no application services and real model execution disabled. No
database, code, dependency lock or Windows installation was changed. The container
was automatically removed. The earlier **416 passed, 1 skipped** result remains
the historical Windows run; this separate Linux verification closes that OCR
execution gap without relabeling the earlier run.

Reproduction in the existing built application test image:

```text
python scripts/verify_document_runtime.py
python -m pytest -q -rs -p no:cacheprovider tests/test_document_parser.py
```

## Next structural step

Separate evidence/file handling from HTTP adapters while preserving bounded intake,
private storage, access/revision rules, quarantine/release and lifecycle effects.
Grant management and history reads can remain a separate later cleanup.
