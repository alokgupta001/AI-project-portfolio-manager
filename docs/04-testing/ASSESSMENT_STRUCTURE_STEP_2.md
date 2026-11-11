# Assessment structure cleanup — step 2

10 November 2026. User-authorized incremental local refactor following
[step 1](ASSESSMENT_STRUCTURE_STEP_1.md). The feature is still one backend module;
there is no deployment or database architecture change.

## Responsibilities

| File under `services/api/ppm_api/modules/assessments` | Responsibility |
| --- | --- |
| [scoring.py](../../services/api/ppm_api/modules/assessments/scoring.py) | `_normalize_rubric` and `compute_scores`: deterministic scores, weighted coverage and reviewer adjustments |
| [validation.py](../../services/api/ppm_api/modules/assessments/validation.py) | `questions`, `validate_definition` and `valid_answer`: framework structure, question lookup and acceptable answers |
| [router.py](../../services/api/ppm_api/modules/assessments/router.py) | Existing HTTP endpoints, authenticated state transitions, database access and evidence handling |

The five functions are moved with their bodies unchanged. Router size falls from
1,086 to 985 lines. Calculation-only agent consumers import the owning rule
modules directly; the planner and test support code also stop reaching through
the agent engine's imported assessment routes. No wrapper implementations or
duplicate copies of the rules are introduced.

## Compatibility and preservation

- The complete OpenAPI JSON, including all 113 paths, component names and operation
  IDs, matches the current pre-step snapshot exactly. No contract regeneration is
  required for this step.
- All 83 table/index definitions match. Schemas, examples, applied migrations,
  environment/configuration, provider policy, stopped pilot history and existing
  unrelated local edits are preserved.
- AST comparison confirms unchanged rule bodies and unchanged remaining router
  workflow. Consumer changes are direct imports and the corresponding function
  references.
- Current learning links, the feature README and seven affected source-index
  sections are updated. Earlier reports and dated verification evidence retain
  their original results.

## Verification

- PASS: focused assessment unit tests, 2 passed and 3 integration cases deselected.
- PASS: the full existing `npm run check` workflow. Python lint/format, API/worker
  typing, source-manifest preservation, generated contracts, ESLint, frontend and
  browser TypeScript, Prettier and all three tooling tests passed. Offline backend:
  **416 passed, 1 skipped, 166 integration cases deselected**, in 87.33 seconds.
  One inherited Starlette/httpx deprecation warning remains. Windows asyncio used
  the granted local network access; the runner supplied a fresh writable TEMP.
- PASS: a rebuilt isolated Linux test image and all **5 assessment tests** in
  13.96 seconds. These include the 2 scoring/validation unit tests and 3 real
  PostgreSQL/Redis workflow cases covering independent review, published-version
  isolation, evidence handling, retries, tenant/RLS access and invalid definitions.
  The unit cases overlap the offline run and are not counted as additional coverage.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: pre/post snapshots of all 113 API paths, all 83 table/index definitions,
  the 5 moved rule bodies and the remaining router workflow. Among 1,643 captured
  files, no unrelated existing file changed; protected environment, migration,
  schema/example, provider and historical evidence files retain their hashes.
- PASS: documentation checker, 412 Markdown files and 5,950 local links/anchors,
  with no missing targets and the established historical status boundaries retained.

The Docker run used only the established `enterprise-ppm-identity-test` project,
PostgreSQL/Redis on test ports 15433/16380, database `ppm_test` and Redis database 1.
The check script refused any other application/database environment. Real model
providers remained disabled. Temporary test containers/network were removed with
the existing Compose configuration; named volumes were retained. Normal/demo
databases and ordinary application containers were not started, rebuilt or reset.

Commands: `npm run check`; the existing isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; a guarded test
container running `python -m alembic upgrade head`, `python -m alembic check` and
`python -m pytest -q tests/test_assessment.py`; and
`python scripts/check_documentation.py`. Scratch checks compared function ASTs,
full OpenAPI JSON, table/index DDL and existing file hashes. The affected source
index and learning links were refreshed without regenerating unrelated inventories.

This step does not claim the other 163 database integration cases, worker/browser
regression, production deployment or live-provider quality were reverified. The UI
was not changed. Applied migrations and the normal schema **0020** remain unchanged.

## Next step

Extract assessment access checks into a dedicated module while retaining live
membership, named respondent/reviewer, tenant and evidence-access enforcement.
Other backend features and frontend restructuring remain separate later steps.
