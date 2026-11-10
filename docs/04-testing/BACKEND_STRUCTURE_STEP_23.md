# Backend structure cleanup — step 23: integrations feature folder

10 November 2026. User-authorized automatic sequential continuation. The feature's
purpose is durable ingestion jobs, connector authority, bounded adapters and source provenance. Files now live together in
[integrations](../../services/api/ppm_api/modules/integrations/README.md).

| Previous path | Current owner |
| --- | --- |
| `services/api/ppm_api/jobs.py` | [services/api/ppm_api/modules/integrations/jobs.py](../../services/api/ppm_api/modules/integrations/jobs.py) |
| `services/api/ppm_api/job_tables.py` | [services/api/ppm_api/modules/integrations/tables.py](../../services/api/ppm_api/modules/integrations/tables.py) |
| `services/api/ppm_api/job_limits.py` | [services/api/ppm_api/modules/integrations/limits.py](../../services/api/ppm_api/modules/integrations/limits.py) |
| `services/api/ppm_api/connectors.py` | [services/api/ppm_api/modules/integrations/connectors.py](../../services/api/ppm_api/modules/integrations/connectors.py) |
| `services/api/ppm_api/ingestion.py` | [services/api/ppm_api/modules/integrations/ingestion.py](../../services/api/ppm_api/modules/integrations/ingestion.py) |

24 Python callers/generators follow the new owners, in addition to the moved Python
files. Statement ASTs match after explicit import/module/resource-path relocation.
Old files are absent; the initializer contains only a package description.
Historical Markdown source-link destinations are retargeted, with historical labels,
outcomes and line numbers retained. Current source-index entries use the new paths.

Complete OpenAPI JSON is identical: 113 paths and all components, with no schema-name changes or contract regeneration.
All 83
table/index definitions match exactly. Unrelated files among
1,689 captured files, including applied migrations, .env,
dependency locks, earlier feature steps and verification evidence, are preserved.

## Verification

- PASS: complete npm run check: Python lint/format/API+worker typing, source
  preservation, contracts, frontend/browser typing, ESLint, Prettier and tooling.
  Backend **416 passed, 1 skipped, 166 integration cases
  deselected** in 45.54 seconds; inherited Starlette/httpx warning.
- PASS: **60 focused Linux cases passed, zero skips**, in 183.00 seconds.
  Jobs and Sprint 12 connector/ML acceptance run with real OCR. The existing Linux Celery crash/lease-recovery test is included; remote connectors and model providers use fixtures.
  Real scanned-PDF/PNG/JPEG OCR executed and JUnit checks no selected case skipped;
  the Windows OCR skip remains an accurate environment-specific result.
- PASS: locked parser/OCR runtime verifier, guarded Alembic upgrade head/check
  against ppm_test, with no new upgrade operations and no migration edit/downgrade.
- PASS: reviewed source relocation, full API/table snapshots and unrelated-file hashes.

Tests are reused, changing imports/patch targets only if required by relocation.

No real provider execution: existing model/scanner fixtures remain. Live ClamAV,
Live model/remote connector/scanner quality, browser flows, restore and deployment are not certified. The selected real Celery crash/restart regression does certify its narrow broker/worker recovery scenario.
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

Group ML dataset/history and evaluation code, then group AI/model routing, agent execution and pilot workflows.
Proceed sequentially without another “next”. Existing no-commit/publication/deployment,
provider and sprint boundaries still apply.
