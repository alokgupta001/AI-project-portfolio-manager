# Backend structure cleanup — step 12: document access

10 November 2026. User-authorized incremental refactor following the
[document folder move](BACKEND_STRUCTURE_STEP_11.md). Scoped lookup and write
eligibility now live in [access.py](../../services/api/ppm_api/modules/documents/access.py).
The [feature guide](../../services/api/ppm_api/modules/documents/README.md)
explains the current owners and remaining combined responsibilities.

## Access boundary

Three existing helpers move unchanged from the router:

| Helper | Preserved behavior |
| --- | --- |
| `document` | Tenant-scoped source lookup, deleted-source rejection unless explicitly requested, live project-read check and sanitized unavailable error |
| `version` | Version lookup followed by authorized document resolution, forwarding the existing deleted-source flag |
| `writable` | Viewer denial, project edit eligibility for non-Admins, Admin requirement for organization-wide policy changes |

The document router falls from **897 to 859 lines**. It imports these helpers for
its existing HTTP and worker operations. Agent version reads use `document_access`
directly; AI retrieval imports `version` from the access module. AI retrieval's
search/citation and agents' other operations retain their existing owners.

The three function definitions, annotations, defaults, statements and internal
calls are identical. The module reuses the established principal, transaction,
tenant-ID helper and delivery project-access checks. It imports no HTTP router,
creates no sessions/commits and adds no compatibility wrapper. Endpoint-specific
and worker authority checks remain in their original order in the router.

## Compatibility and preservation

AST comparisons verify all three complete functions, remaining router logic and
AI/agent caller statements, allowing only import changes and the two explicit
agent `documents.version` to `document_access.version` redirections. Route metadata,
permission responses, optional deleted-source handling, replay order and worker
fencing are preserved. The access module's independence from HTTP routes is checked.

Complete OpenAPI JSON, including **113 paths** and all components, matches the
pre-step snapshot exactly. All **83 table/index definitions** match. Generated
contracts, schemas, tables, parser, retrieval types, tests and applied migrations
need no changes.

Hashes preserve unrelated work among **1,662 captured files**, including the
assessment feature, `.env`, provider configuration, earlier verification and
dependency locks. New files are limited to the access module and this report.
Current documentation changes cover the file map, root guide, contract, tutorial,
handoff/checkpoints and the four affected router/access/AI/agent source-index entries.

## Verification

- PASS: complete existing `npm run check` workflow: Python lint/format, API/worker
  typing, source preservation, generated contracts, ESLint, frontend/browser
  TypeScript, Prettier and all three tooling tests. Offline backend: **416 passed,
  1 skipped, 166 integration cases deselected** in 43.16 seconds, with the inherited
  Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **42 focused tests, zero skipped,
  1 deselected**, in 91.67 seconds. This includes 8 document workflows, all 24 parser
  tests, all 5 assessment tests, 2 selected AI source-runtime cases, both semantic
  review grant cases and full-cohort paging/result grants. There are 16
  database-backed cases and 26 parser/unit cases; parser/unit cases overlap the
  Windows run, so these are not additive unique-test totals.
- PASS: an additional existing agent source/replay/independent-review journey,
  **1 passed, zero skipped**, in 9.84 seconds, exercising direct document-version
  inputs in the changed agent caller. It is distinct from the first run: **43
  selected Linux cases passed across the two invocations**.
- PASS: JUnit explicitly verifies real scanned-PDF/PNG/JPEG OCR passed and none of
  the 42 selected cases skipped. Exact parser/OCR package lock checks passed during
  build and execution. The Windows OCR skip remains an accurate local result.
- PASS: document tenant/project/role boundaries, revoked reads, worker authority,
  cancellation/deletion during extraction, retention/deleted-source handling,
  signed downloads, private assessment links and selected AI source invalidation,
  using existing tests and fixtures.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No applied migration changed or downgrade ran.
- PASS: identical access functions, remaining router/caller comparisons, complete
  API/table snapshots and unrelated-file hashes. Existing tests were reused unchanged.
- PASS: documentation checker, **422 Markdown files and 6,046 local links/anchors**,
  zero missing targets and retained historical requirement/status boundaries;
  `git diff --check` reported no whitespace errors.

The live ClamAV acceptance case was explicitly deselected; scanner transport uses
existing doubles. This run does not certify live scanner/signature readiness.
Real OCR executed. Real model providers remained disabled and selected provider
calls use existing mocks.

Only the established `enterprise-ppm-identity-test` Compose project was used,
with PostgreSQL/Redis on test ports 15433/16380. Guards require environment `test`,
application/migration databases `ppm_test` and Redis database 1. Temporary test
containers/network were removed with named volumes retained. No normal/demo
database was reset or ordinary application service started.

Commands: `npm run check`; the established isolated Compose files with
`--profile test build test`, `up -d --wait postgres redis` and guarded `run --rm -T
--no-deps test python -`. The container runs the locked document runtime verifier,
`python -m alembic upgrade head`, `python -m alembic check` and `python -m pytest -q
-rs` on document/parser/assessment suites and selected AI/agent/cohort cases, with
`-k 'not test_real_clamd_and_processing_job'`. The additional agent case is
`tests/test_agents.py::test_hidden_risk_disabled_replay_independent_review_and_preservation`.
Cleanup used Compose `down` without volume removal.
Documentation was checked with `python scripts/check_documentation.py`.

Other integration cases, browser/worker-service regressions, production deployment
and live-provider quality are not rerun or newly certified. UI, normal schema
**0020**, provider authorization, existing assessment rules and stopped pilots
are preserved.

## Next structural step

Separate `document_worker` from the HTTP router into its own worker module and
update dispatch/recovery/test callers. Preserve lease fencing, persisted/live
authority, cancellation/deletion and scanner/parser/storage boundaries. Perform
that as a separate authorized step.
