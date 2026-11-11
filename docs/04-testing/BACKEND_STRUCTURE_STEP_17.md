# Backend structure cleanup — step 17: document intake and downloads

10 November 2026. Automatic sequential continuation authorized by the user.
Following [step 16](BACKEND_STRUCTURE_STEP_16.md), current ownership is
documented in the [feature guide](../../services/api/ppm_api/modules/documents/README.md).

Four file handlers delegate to operations for upload, download tickets, private downloads and reprocessing. Existing statement bodies, storage/hash checks and transport responses are preserved.

The new owner is [files.py](../../services/api/ppm_api/modules/documents/files.py). The router changes from
484 to 301 lines. AST comparisons
verify 4 complete extracted functions and
4 thin handlers with original metadata,
plus all remaining router/caller logic. For extracted HTTP operations only,
service signatures use Principal and explicit parameters instead of Auth/Query
defaults; HTTP signatures/decorators/validation retain their original definitions.
The operation bodies are identical. No new transaction, commit or authorization
boundary is introduced. New owner modules do not import document HTTP routes.

Full OpenAPI JSON (113 paths and all components) and all 83 table/index definitions
match pre-step snapshots exactly. Contracts and migrations are unchanged.
Hashes preserve unrelated work among 1,672 captured files,
including earlier extraction results, tests, worker/parser/access/mutation rules,
applied migrations, .env, provider configuration and historical evidence.

## Verification

- PASS: complete existing npm run check: Python lint/format/API+worker typing,
  source preservation, contracts, ESLint, frontend/browser TypeScript, Prettier
  and all three tooling tests. Backend: **416 passed, 1 skipped, 166 integration
  cases deselected** in 43.00 seconds; inherited Starlette/httpx warning.
- PASS: rebuilt isolated image; **43 Linux cases passed, zero skipped, 1 deselected**
  in 90.64 seconds: 8 document workflows, 24 parser tests, 5 assessment tests,
  2 AI source-runtime cases, 3 agent source/review cases and cohort paging/result
  grants. The 26 parser/unit cases overlap the Windows run; totals are not additive.
- PASS: real scanned-PDF/PNG/JPEG OCR, explicitly checked in JUnit, and the locked
  parser/OCR runtime verifier. The Windows OCR skip remains environment-specific.
- PASS: guarded Alembic upgrade head/check against ppm_test; no new upgrade
  operations and no applied-migration edit/downgrade.
- PASS: function/body/route/caller, complete API/table and unrelated-file comparisons.
- PASS: documentation checker, 427 Markdown files and 6,094 local links/anchors,
  zero missing targets; git diff --check reported no whitespace errors.

The live ClamAV acceptance case is explicitly deselected; existing scanner/provider
fixtures are used and live model execution is disabled. No live scanner/signature
or model-quality claim. Existing tests and assertions are preserved. Other
integration, browser/broker-service, restore and deployment procedures were not run.

Only enterprise-ppm-identity-test is used: test environment, application/migration
databases ppm_test, Redis database 1, PostgreSQL/Redis test ports 15433/16380.
Dependencies remain running for the authorized continuation; remove temporary
containers/network at the end, retaining named volumes. No normal/demo reset.

Commands: npm run check; isolated Compose build and guarded run --rm -T --no-deps;
locked document-runtime verification; python -m alembic upgrade head/check;
python -m pytest -q -rs on document/parser/assessment and selected AI/agent/cohort
cases, excluding test_real_clamd_and_processing_job. UI, normal schema **0020**,
provider/pilot/sprint boundaries and the ban on publication/deployment are preserved.

## Authorized continuation

Separate governance, cancellation, deletion/purge, evidence linking and orphan retention operations. Continue sequentially without waiting for another “next”; the user explicitly
authorized this. No successor sprint, commit, publication, deployment or real
provider calls are authorized by the structural cleanup.
