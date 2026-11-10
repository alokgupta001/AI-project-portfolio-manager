# Assessment structure cleanup — step 3

10 November 2026. User-authorized incremental refactor following
[step 2](ASSESSMENT_STRUCTURE_STEP_2.md). Assessment access rules now have one
owner: [access.py](../../services/api/ppm_api/modules/assessments/access.py).
The [feature guide](../../services/api/ppm_api/modules/assessments/README.md)
describes the current responsibilities.

## Extraction

Nine existing helper bodies move unchanged from the router:

| Helpers | Responsibility |
| --- | --- |
| `oid`, `get` | Active organization and organization-scoped record lookup |
| `grant`, `can_edit` | Active per-user framework grants and editing authority |
| `eligible`, `respondent`, `reviewer` | Eligible roles, named respondent and independent named reviewer |
| `evidence_access` | Private answer/evidence authority, separate from result-only access |
| `command_access` | Live path-specific authorization before writes and idempotent replay |

The router falls from 985 to 908 lines. Its mutation wrapper still obtains the
existing lock, checks current access, and then processes idempotency/replay, writes
and audit records in the same order. Identity/session authentication remains with
the existing principal. Agents and document evidence links import permission
helpers from the new module; the agent's workflow-data read still uses the existing
router helper pending a later workflow extraction.

## Compatibility and preservation

AST comparison confirms all nine helper bodies and the remaining router workflow
are unchanged. Agent consumer differences are the module qualifier on permission
calls; document consumer differences are imports only. The full OpenAPI JSON,
including all 113 paths, component names and operation IDs, is identical to the
pre-step snapshot. All 83 table/index definitions also match.

Applied migrations, schemas, examples, scoring/validation, the local `.env`,
tracked provider configuration, earlier verification evidence and unrelated local
edits retain their pre-step hashes. Provider authorization and stopped normal pilot
state are not modified. No contract regeneration or migration source
change is needed. Source navigation is updated only for the router, agent and
document sections plus the new access-module section.

## Verification

- PASS: the full existing `npm run check` workflow: Python lint/format and
  API/worker typing, preserved source manifest, generated contracts, ESLint,
  frontend/browser TypeScript, Prettier, all three tooling tests and backend unit
  tests. Offline backend: **416 passed, 1 skipped, 166 integration cases deselected**
  in 44.16 seconds, with the inherited Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux test image and **8 focused tests** in 28.89 seconds:
  all 5 assessment tests, both parameterized semantic-review tests (read/edit grant)
  and the document/assessment bridge privacy test. These cover 6 database-backed
  cases plus 2 scoring/validation unit cases that overlap the offline run.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: all 113 API paths/component definitions and all 83 table/index definitions
  match the pre-step snapshot exactly. All 9 moved helper bodies, the remaining
  router workflow and existing unrelated files match their expected pre-step
  content among 1,646 captured files.
- PASS: documentation checker, 413 Markdown files and 5,959 local links/anchors,
  no missing targets and retained historical requirement/status boundaries.

The Docker check refused any environment other than app environment `test`,
database `ppm_test` for both application and migration roles, and Redis database 1.
Only the existing `enterprise-ppm-identity-test` project was used, on PostgreSQL/
Redis test ports 15433/16380. Provider/scanner interactions in the selected tests
used mocks; real provider execution stayed disabled. Test containers and network
were removed afterward, retaining named volumes. Normal/demo databases and ordinary
application containers were not started, rebuilt or reset.

Commands: `npm run check`; the established isolated Compose configuration with
`--profile test build test` and `up -d --wait postgres redis`; a guarded test
container running `python -m alembic upgrade head`, `python -m alembic check`, and
`python -m pytest -q tests/test_assessment.py
tests/test_agents.py::test_semantic_review_scores_rejection_immutable_history_and_stale_answers
tests/test_documents.py::test_assessment_bridge_preserves_completed_scores_and_private_grants`;
and `python scripts/check_documentation.py`. Scratch checks compared original/new
ASTs, complete OpenAPI JSON, table/index DDL and existing file hashes.

The remaining integration suite, browser/worker regressions, production deployment
and live-provider quality were not rerun or newly certified by this step. The UI
was not changed; applied migrations and the normal schema **0020** are unchanged.

## Next step

Extract assessment write safeguards (idempotency/replay, revision preconditions and
audit handling) while retaining their current order and authorization boundaries.
Do not combine that next step with changes to business behavior or other features.
