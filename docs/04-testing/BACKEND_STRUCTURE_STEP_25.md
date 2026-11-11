# Backend structure cleanup — step 25: ai feature folder

10 November 2026. User-authorized automatic sequential continuation. The feature's
purpose is evidence-grounded assistance, retrieval/indexing and policy-controlled model execution. Files now live together in
[ai](../../services/api/ppm_api/modules/ai/README.md).

| Previous path | Current owner |
| --- | --- |
| `services/api/ppm_api/ai.py` | [services/api/ppm_api/modules/ai/router.py](../../services/api/ppm_api/modules/ai/router.py) |
| `services/api/ppm_api/ai_schemas.py` | [services/api/ppm_api/modules/ai/schemas.py](../../services/api/ppm_api/modules/ai/schemas.py) |
| `services/api/ppm_api/ai_tables.py` | [services/api/ppm_api/modules/ai/tables.py](../../services/api/ppm_api/modules/ai/tables.py) |
| `services/api/ppm_api/ai_retrieval.py` | [services/api/ppm_api/modules/ai/retrieval.py](../../services/api/ppm_api/modules/ai/retrieval.py) |
| `services/api/ppm_api/ai_provider.py` | [services/api/ppm_api/modules/ai/provider.py](../../services/api/ppm_api/modules/ai/provider.py) |
| `services/api/ppm_api/ai_evaluation.py` | [services/api/ppm_api/modules/ai/evaluation.py](../../services/api/ppm_api/modules/ai/evaluation.py) |
| `services/api/ppm_api/model_adapters.py` | [services/api/ppm_api/modules/ai/adapters.py](../../services/api/ppm_api/modules/ai/adapters.py) |
| `services/api/ppm_api/model_contracts.py` | [services/api/ppm_api/modules/ai/contracts.py](../../services/api/ppm_api/modules/ai/contracts.py) |
| `services/api/ppm_api/model_deadlines.py` | [services/api/ppm_api/modules/ai/deadlines.py](../../services/api/ppm_api/modules/ai/deadlines.py) |
| `services/api/ppm_api/model_qualification.py` | [services/api/ppm_api/modules/ai/qualification.py](../../services/api/ppm_api/modules/ai/qualification.py) |
| `services/api/ppm_api/model_registry.py` | [services/api/ppm_api/modules/ai/registry.py](../../services/api/ppm_api/modules/ai/registry.py) |
| `services/api/ppm_api/model_router.py` | [services/api/ppm_api/modules/ai/model_router.py](../../services/api/ppm_api/modules/ai/model_router.py) |
| `services/api/ppm_api/model_timing.py` | [services/api/ppm_api/modules/ai/timing.py](../../services/api/ppm_api/modules/ai/timing.py) |
| `services/api/ppm_api/local_model_readiness.py` | [services/api/ppm_api/modules/ai/readiness.py](../../services/api/ppm_api/modules/ai/readiness.py) |
| `services/api/ppm_api/ollama_provider.py` | [services/api/ppm_api/modules/ai/ollama_provider.py](../../services/api/ppm_api/modules/ai/ollama_provider.py) |
| `services/api/ppm_api/ai_evaluation_v1.json` | [services/api/ppm_api/modules/ai/ai_evaluation_v1.json](../../services/api/ppm_api/modules/ai/ai_evaluation_v1.json) |

59 Python callers/generators follow the new owners, in addition to the moved Python
files. Statement ASTs match after explicit import/module/resource-path relocation.
Old files are absent; the initializer contains only a package description.
Historical Markdown source-link destinations are retargeted, with historical labels,
outcomes and line numbers retained. Current source-index entries use the new paths.

Complete OpenAPI JSON is identical: 113 paths and all components, with no schema-name changes or contract regeneration.
All 83
table/index definitions match exactly. Unrelated files among
1,695 captured files, including applied migrations, .env,
dependency locks, earlier feature steps and verification evidence, are preserved.

## Verification

- PASS: complete npm run check: Python lint/format/API+worker typing, source
  preservation, contracts, frontend/browser typing, ESLint, Prettier and tooling.
  Backend **416 passed, 1 skipped, 166 integration cases
  deselected** in 46.53 seconds; inherited Starlette/httpx warning.
- PASS: **103 focused Linux cases passed, zero skips**, in 177.42 seconds.
  AI retrieval/indexing, immutable snapshots, authorization, model policy/routing and parser/OCR regressions run with model providers mocked or disabled.
  Real scanned-PDF/PNG/JPEG OCR executed and JUnit checks no selected case skipped;
  the Windows OCR skip remains an accurate environment-specific result.
- PASS: locked parser/OCR runtime verifier, guarded Alembic upgrade head/check
  against ppm_test, with no new upgrade operations and no migration edit/downgrade.
- PASS: reviewed source relocation, full API/table snapshots and unrelated-file hashes.

Tests are reused, changing imports/patch targets only if required by relocation.

No real provider execution: existing model/scanner fixtures remain. Live ClamAV,
Other integrations, browser/broker-service, restore and deployment are not certified.
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

Group agent planning, execution, validation, reviews and task-table definitions with a clear local file guide.
Proceed sequentially without another “next”. Existing no-commit/publication/deployment,
provider and sprint boundaries still apply.
