# Backend structure cleanup — step 13: document worker

10 November 2026. User-authorized incremental refactor following the
[document access extraction](BACKEND_STRUCTURE_STEP_12.md). The processing handler
now lives in [worker.py](../../services/api/ppm_api/modules/documents/worker.py).
The [feature guide](../../services/api/ppm_api/modules/documents/README.md)
explains its role in the existing job/Celery dispatcher.

## Worker boundary

The complete `document_worker` definition moves from the HTTP router, including
its signature, docstring, annotations and nested `principal` authorization helper.
All statements and their order are identical. The router falls from **859 to 730
lines**; the new worker module is **149 lines**. Worker-only asyncio, session/context,
object-store and scanner/extraction imports leave the router.

The handler preserves persisted/live actor/session/tenant authority resolution,
job row locking, terminal/running checks, cancellation and three-attempt bound,
120-second lease/token fencing, original-byte SHA-256 checks and storage keys.
Validation, scanner transport and bounded extraction still run outside database
transactions. The publication transaction rechecks authority and the lease before
replacing derived chunks, setting ready/quarantined state and recording progress.
Diagnostics, exception handling, return values and outbox/job updates are unchanged.

The existing `jobs.run_job` imports the worker from its new owner; its ML → AI →
document → integration dispatch order is preserved. The restore script imports the
same handler directly. Existing tests update their worker import and scanner/parser
patch/dynamic-import targets. Test assertions, fixture behavior, queue/task
configuration and retry policy are preserved. The worker imports shared access, parser,
storage, identity and job helpers and does not import the document HTTP router.
The router exposes no worker compatibility wrapper or re-export.

## Compatibility and preservation

AST comparisons verify the complete moved function, including its nested helper,
all remaining router logic and all job/recovery/test statements. Only imports and
the explicit test patch-module strings differ. Source inspection confirms the
dispatcher, recovery tool and tests import the new worker owner.

Complete OpenAPI JSON, including **113 paths** and all components, matches the
pre-step snapshot exactly. All **83 table/index definitions** match. Generated
contracts, schemas, tables, access rules, parser and applied migrations need no
changes. Router signatures/decorators, request limits, revision/replay handling,
HTTP errors, retention and evidence rules are preserved.

Hashes preserve unrelated work among **1,664 captured files**, including the
assessment feature, `.env`, provider configuration, dependency locks and earlier
verification. New files are limited to the worker module and this report. Current
documentation changes cover the file map, root guide, contract, code trace,
handoff/checkpoints and affected existing source-index entries.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, source preservation, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 41.07 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **43 focused tests, zero skipped,
  1 deselected**, in 91.57 seconds. This includes 8 document workflows, all 24 parser
  tests, all 5 assessment tests, 2 selected AI source-runtime cases, both semantic
  review grant cases, the document-source agent/replay/review journey and full-cohort
  paging/result grants. There are 17 database-backed cases and 26 parser/unit cases;
  parser/unit cases overlap the Windows run and are not additive unique-test totals.
- PASS: moved worker execution and updated scanner/parser patch targets, including
  quarantine failure, broker-redelivery behavior, cancellation/deletion during
  extraction, revoked authority, retention/private links and selected AI/agent
  source-version/review boundaries, using existing tests and fixtures.
- PASS: JUnit explicitly verifies real scanned-PDF/PNG/JPEG OCR passed and none of
  the selected 43 cases skipped. Exact parser/OCR package lock checks passed at
  build and execution. The Windows OCR skip remains an accurate local result.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No applied migration changed or downgrade ran.
- PASS: exact function/nested-helper preservation, remaining router/caller source
  comparisons, complete API/table snapshots and unrelated-file hashes.
- PASS: documentation checker, **423 Markdown files and 6,056 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  `git diff --check` reported no whitespace errors.

The live ClamAV acceptance case was explicitly deselected; scanner transport uses
existing doubles. This run does not certify live scanner/signature readiness.
Real OCR executed. Real model providers remained disabled; selected provider calls
use existing mocks. Tests retain their existing assertions and fixtures, changing
only module imports/patch targets. The restore tool's statements/import are checked;
the restore procedure itself was not executed.

Only the established `enterprise-ppm-identity-test` Compose project was used,
with PostgreSQL/Redis on test ports 15433/16380. Guards require environment `test`,
application/migration databases `ppm_test` and Redis database 1. Temporary test
containers/network were removed with named volumes retained. No normal/demo
database was reset or ordinary application service started.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test`, `up -d --wait postgres redis`, guarded `run --rm -T
--no-deps test python -` and `down` without volume removal. The test container runs
the locked document runtime verifier, `python -m alembic upgrade head`,
`python -m alembic check` and `python -m pytest -q -rs` on document/parser/assessment
suites and selected AI/agent/cohort cases, with
`-k 'not test_real_clamd_and_processing_job'`.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, broker/worker-service/browser journeys, production
deployment and live-provider quality were not rerun or newly certified. UI, normal
schema **0020**, provider authorization, assessment rules and stopped pilots are
preserved.

## Next structural step

Separate document revision preconditions and request-fingerprint helpers from
the remaining HTTP/workflow code. Preserve If-Match/key validation, fingerprint
inputs, error responses and the existing authorization/lock/replay ordering.
Perform that as a separate authorized step.
