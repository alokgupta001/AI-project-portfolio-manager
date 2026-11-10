# Backend structure cleanup — step 26: agents feature folder

10 November 2026. User-authorized automatic sequential continuation. The feature's
purpose is read-only specialists, bounded task planning/execution and independent analysis review. Files now live together in
[agents](../../services/api/ppm_api/modules/agents/README.md).

| Previous path | Current owner |
| --- | --- |
| `services/api/ppm_api/agents.py` | [services/api/ppm_api/modules/agents/router.py](../../services/api/ppm_api/modules/agents/router.py) |
| `services/api/ppm_api/agent_engine.py` | [services/api/ppm_api/modules/agents/engine.py](../../services/api/ppm_api/modules/agents/engine.py) |
| `services/api/ppm_api/agent_schemas.py` | [services/api/ppm_api/modules/agents/schemas.py](../../services/api/ppm_api/modules/agents/schemas.py) |
| `services/api/ppm_api/agent_tables.py` | [services/api/ppm_api/modules/agents/tables.py](../../services/api/ppm_api/modules/agents/tables.py) |
| `services/api/ppm_api/agent_task_tables.py` | [services/api/ppm_api/modules/agents/task_tables.py](../../services/api/ppm_api/modules/agents/task_tables.py) |
| `services/api/ppm_api/agent_runtime.py` | [services/api/ppm_api/modules/agents/runtime.py](../../services/api/ppm_api/modules/agents/runtime.py) |
| `services/api/ppm_api/agent_registry.py` | [services/api/ppm_api/modules/agents/registry.py](../../services/api/ppm_api/modules/agents/registry.py) |
| `services/api/ppm_api/agent_planner.py` | [services/api/ppm_api/modules/agents/planner.py](../../services/api/ppm_api/modules/agents/planner.py) |
| `services/api/ppm_api/agent_context.py` | [services/api/ppm_api/modules/agents/context.py](../../services/api/ppm_api/modules/agents/context.py) |
| `services/api/ppm_api/agent_validation.py` | [services/api/ppm_api/modules/agents/validation.py](../../services/api/ppm_api/modules/agents/validation.py) |
| `services/api/ppm_api/agent_prompts.py` | [services/api/ppm_api/modules/agents/prompts.py](../../services/api/ppm_api/modules/agents/prompts.py) |
| `services/api/ppm_api/agent_examples.py` | [services/api/ppm_api/modules/agents/examples.py](../../services/api/ppm_api/modules/agents/examples.py) |
| `services/api/ppm_api/agent_batch.py` | [services/api/ppm_api/modules/agents/batch.py](../../services/api/ppm_api/modules/agents/batch.py) |
| `services/api/ppm_api/agent_critique.py` | [services/api/ppm_api/modules/agents/critique.py](../../services/api/ppm_api/modules/agents/critique.py) |
| `services/api/ppm_api/agent_provider.py` | [services/api/ppm_api/modules/agents/provider.py](../../services/api/ppm_api/modules/agents/provider.py) |
| `services/api/ppm_api/agent_recovery.py` | [services/api/ppm_api/modules/agents/recovery.py](../../services/api/ppm_api/modules/agents/recovery.py) |
| `services/api/ppm_api/guided_review.py` | [services/api/ppm_api/modules/agents/guided_review.py](../../services/api/ppm_api/modules/agents/guided_review.py) |

30 Python callers/generators follow the new owners, in addition to the moved Python
files. Statement ASTs match after explicit import/module/resource-path relocation.
Old files are absent; the initializer contains only a package description.
Historical Markdown source-link destinations are retargeted, with historical labels,
outcomes and line numbers retained. Current source-index entries use the new paths.

OpenAPI preserves all 113 paths and wire schemas after normalizing only the moved Python module namespace. The duplicate ReviewInput component identifier follows its new module. OpenAPI and TypeScript contracts were regenerated and compared to their originals after that exact identifier normalization; no other contract/type changes occurred.
All 83
table/index definitions match exactly. Unrelated files among
1,698 captured files, including applied migrations, .env,
dependency locks, earlier feature steps and verification evidence, are preserved.

## Verification

- PASS: complete npm run check: Python lint/format/API+worker typing, source
  preservation, contracts, frontend/browser typing, ESLint, Prettier and tooling.
  Backend **416 passed, 1 skipped, 166 integration cases
  deselected** in 44.73 seconds; inherited Starlette/httpx warning.
- PASS: **225 focused Linux cases passed, zero skips**, in 341.88 seconds.
  Agent API/review, graph runtime, planning, batches, evidence/validation and benchmark regressions run with real OCR and fixture model transports.
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

Group personal workspace/discovery and guided-review support, then isolate financial-selection research files and finish the architecture map.
Proceed sequentially without another “next”. Existing no-commit/publication/deployment,
provider and sprint boundaries still apply.
