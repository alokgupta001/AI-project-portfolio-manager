# Backend structure cleanup — step 14: revision and fingerprints

10 November 2026. Following [step 13](BACKEND_STRUCTURE_STEP_13.md), the existing
`revision` and `request_identity` helpers now live in
[mutations.py](../../services/api/ppm_api/modules/documents/mutations.py).
The [file map](../../services/api/ppm_api/modules/documents/README.md) describes
the current ownership and remaining workflow/data responsibilities.

Both complete definitions move unchanged. Revision checks retain If-Match parsing,
428/412 responses and messages. Request identity retains UUID key validation,
the request-path plus `str(jsonable_encoder(body))` canonical input and SHA-256.
No hash serialization or error behavior changes. Document routes import these
helpers; AI submissions and agent reviews call the new module directly. AI no
longer imports the document router. Existing caller body selection, additional
agent fingerprint binding, authorization, locking and replay order are preserved.

The router falls from 730 to 713 lines. AST comparisons verify both definitions,
all remaining router logic and both AI/agent callers, allowing only their explicit
request-identity target redirection and imports. The new module does not import
document HTTP routes. Complete OpenAPI JSON (113 paths and all components) and
all 83 table/index definitions match exactly; no generated contracts or migrations
change. Tests, worker/parser/access behavior and unrelated work among 1,666 captured
files are preserved by hash. Only the mutation module and this report are new.

## Verification

- PASS: existing `npm run check`, including Python lint/format/API+worker typing,
  source preservation, generated contracts, ESLint, frontend/browser TypeScript,
  Prettier and all three tooling tests. Offline backend: **416 passed, 1 skipped,
  166 integration cases deselected** in 41.35 seconds; inherited Starlette/httpx warning.
- PASS: rebuilt isolated Linux image, **43 passed, zero skipped, 1 deselected** in
  91.90 seconds: 8 document workflows, 24 parser tests, 5 assessment tests, 2 selected
  AI source-runtime cases, 3 agent review/source cases and cohort paging/result grants.
  The 26 parser/unit cases overlap the Windows run; counts are not additive unique tests.
- PASS: revision/replay/conflicting-input workflows, direct AI/agent fingerprint
  callers, document access/storage/worker boundaries and real scanned-PDF/PNG/JPEG
  OCR, using existing fixtures. JUnit verifies the real OCR case ran and no selected
  cases skipped. Exact parser/OCR package locks passed during build and execution.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`, with
  no new upgrade operations. No applied migration changed or downgrade ran.
- PASS: exact helper/router/caller comparisons, full API/table snapshots and
  preservation of unrelated source/configuration/history, including `.env`.
- PASS: documentation checker, 424 Markdown files and 6,066 local links/anchors,
  zero missing targets; `git diff --check` reported no whitespace errors.

The live ClamAV acceptance case was explicitly deselected; scanner/provider calls
use existing doubles. No live scanner/signature or model-quality certification.
The Windows OCR skip remains an accurate environment-specific result, covered
separately by the successful Linux OCR execution. Existing tests are unchanged.

Only the established `enterprise-ppm-identity-test` project is used, PostgreSQL/
Redis ports 15433/16380, environment `test`, both databases `ppm_test` and Redis
database 1. Real model providers stay disabled. The isolated database/broker remain
running for the user's authorized sequential continuation; remove temporary services
and network at the end, retaining named volumes. No normal/demo database is reset.

Commands: `npm run check`; established isolated Compose build/test setup;
`python scripts/verify_document_runtime.py`; guarded Alembic upgrade/drift and
`python -m pytest -q -rs` on document/parser/assessment and selected AI/agent/cohort
cases with `-k 'not test_real_clamd_and_processing_job'`.
Other integrations, browser/broker-service journeys, deployment and live providers
were not rerun. UI, normal schema **0020**, provider authorization and stopped pilots
are preserved.

## Authorized continuation

The user requested automatic sequential continuation after this step. Next move
shared document response/replay/enqueue helpers into a service, then continue the
remaining document operations in reviewable increments. This authorization does
not advance sprints or authorize commits, publication, deployment or provider calls.
