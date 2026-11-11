# Backend structure cleanup — step 19: capacity feature folder

10 November 2026. User-authorized automatic sequential continuation. The feature's
purpose is resource staffing, scoped workforce effort and reproducible capacity metrics. Files now live together in
[capacity](../../services/api/ppm_api/modules/capacity/README.md).

| Previous path | Current owner |
| --- | --- |
| `services/api/ppm_api/capacity.py` | [services/api/ppm_api/modules/capacity/router.py](../../services/api/ppm_api/modules/capacity/router.py) |
| `services/api/ppm_api/capacity_schemas.py` | [services/api/ppm_api/modules/capacity/schemas.py](../../services/api/ppm_api/modules/capacity/schemas.py) |

7 Python callers/generators follow the new owners, in addition to the moved Python
files. Statement ASTs match after explicit import/module/resource-path relocation.
Old files are absent; the initializer contains only a package description.
Historical Markdown source-link destinations are retargeted, with historical labels,
outcomes and line numbers retained. Current source-index entries use the new paths.

Complete OpenAPI JSON is identical: 113 paths and all components,
with no schema-name changes or contract regeneration. All 83
table/index definitions match exactly. Unrelated files among
1,676 captured files, including applied migrations, .env,
dependency locks, earlier feature steps and verification evidence, are preserved.

## Verification

- PASS: complete npm run check: Python lint/format/API+worker typing, source
  preservation, contracts, frontend/browser typing, ESLint, Prettier and tooling.
  Backend **416 passed, 1 skipped, 166 integration cases
  deselected** in 42.26 seconds; inherited Starlette/httpx warning.
- PASS: **35 focused Linux cases passed, zero skips**, in 31.15 seconds.
  Six capacity cases cover dates/DST, allocation concurrency, snapshot history, sensitive effort and resource/team privacy; four command cases and one all-agent/revocation case cover callers; 24 parser cases include real OCR.
  Real scanned-PDF/PNG/JPEG OCR executed and JUnit checks no selected case skipped;
  the Windows OCR skip remains an accurate environment-specific result.
- PASS: locked parser/OCR runtime verifier, guarded Alembic upgrade head/check
  against ppm_test, with no new upgrade operations and no migration edit/downgrade.
- PASS: reviewed source relocation, full API/table snapshots and unrelated-file hashes.

Tests are reused, changing imports/patch targets only if required by relocation.

The initial run against the retained enterprise-ppm-identity-test database failed
one capacity permission assertion (34 passed). A disposable container overlaid
with all seven original service source files reproduced the same failure before
this move. Read-only policy inspection showed its tenant_update resource policy
lacked the migration source's NOT archived guard; ppm_app remained nonsuperuser
and NOBYPASSRLS. Alembic table drift checking does not compare RLS policy text.
A separate project with new PostgreSQL/Redis volumes applied the existing migration
chain from empty state: all 35 cases passed, including the unchanged denial test.
No existing database policy/data was repaired or reset, and no test/migration
was edited. The original isolated test database was preserved for inspection.

No real provider execution: existing model/scanner fixtures remain. Live ClamAV,
other integrations, browser/broker-service, restore and deployment are not certified.
Test counts overlap previous/offline runs and are not additive unique-case totals.

Current verification uses fresh enterprise-ppm-structure-20261110: environment test,
application/migration databases ppm_test, Redis database 1 and test ports
15435/16382. Dependencies remain
running for the authorized continuation; remove temporary containers/network at
the end, retaining named volumes. No normal/demo database reset or ordinary app start.

Commands: npm run check; isolated Compose image build and guarded run --rm -T
--no-deps; locked document-runtime verifier; python -m alembic upgrade head/check;
python -m pytest -q -rs on the selected existing feature/caller/parser cases.
UI, schema **0020**, source prompts, provider authorization and stopped pilots remain.

## Authorized continuation

Group the command-center router, schemas and metric tables, checking caller imports before moving them.
Proceed sequentially without another “next”. Existing no-commit/publication/deployment,
provider and sprint boundaries still apply.
