# Assessment structure cleanup — step 6

10 November 2026. User-authorized incremental refactor following
[step 5](ASSESSMENT_STRUCTURE_STEP_5.md). Framework HTTP handlers now delegate to
[service.py](../../services/api/ppm_api/modules/assessments/service.py); the
[feature guide](../../services/api/ppm_api/modules/assessments/README.md) describes
the current owners and remaining work.

## Service boundary

| Existing HTTP handler | Service operation |
| --- | --- |
| `list_frameworks` | `list_frameworks` with the validated offset/limit |
| `create_framework` | `create_framework` with the validated framework and principal |
| `edit_framework` | `edit_framework`, retaining scoped lookup and revision check |
| `publish_framework` | `publish_framework`, retaining validation, immutable snapshot and revision advance |
| `versions` | `list_framework_versions`, retaining scoped lookup and newest-first ordering |
| `seed_examples` | `seed_examples`, retaining sample copies, validation and duplicate avoidance |

The router falls from 744 to 623 lines. Each of these six route bodies is one
awaited service call. Public function names, parameters/defaults, decorators,
response models and operation IDs stay unchanged. Payloads accepted but unused
by the previous operation remain accepted by the route; service interfaces omit
unused transport arguments. Edit/publish still receive the request for their
existing revision check, at the same point in their operation.

The mutation decorator remains only on HTTP write adapters, preserving live
authorization before replay, locking, fingerprints and audit names. Services reuse
the authenticated principal and transaction and add no sessions or commits. The
example loader moves unchanged to the same package as `examples.json`; sample
bytes and the seeding algorithm are unchanged.

## Compatibility and preservation

AST comparison confirms all six operation statement bodies, six original route
signatures/decorators, seven existing service helpers and the other router logic
are preserved. Complete OpenAPI JSON (all 113 paths/components) and all 83 table/
index definitions match the pre-step snapshot exactly. No schema or generated
contract changes are needed.

Existing access/mutations/scoring/validation, model definitions, examples, applied
migrations, local `.env`, tracked provider configuration, earlier evidence and
unrelated edits are preserved. Source navigation updates only router, service and
the affected assessment test section. No new compatibility wrapper layer is added.

## Verification

The existing two-department/republication workflow now also exercises successful
framework-list pagination and an empty next page, invalid list bounds, newest-first
version history and unchanged original published content. These public read paths
previously lacked explicit success assertions; the existing workflow/write/security
tests remain in place.

- PASS: complete existing `npm run check` workflow: Python lint/format and
  API/worker typing, preserved source manifest, generated contracts, ESLint,
  frontend/browser TypeScript, Prettier and all three tooling tests. Offline
  backend: **416 passed, 1 skipped, 166 integration cases deselected**, in 39.48
  seconds, with the inherited Starlette/httpx deprecation warning.
- PASS: rebuilt isolated Linux image and **8 focused tests** in 25.48 seconds:
  all 5 assessment tests, both parameterized semantic-review cases (read/edit grant)
  and the document/assessment bridge privacy case. These cover 6 database-backed
  cases and 2 unit cases overlapping the offline run. The augmented existing
  workflow successfully verifies paginated framework reads, the empty next page,
  invalid bounds, version ordering and the unchanged original snapshot, alongside
  create/edit/publish/seeding, replay, stale revisions and tenant/privacy rules.
- PASS: guarded `alembic upgrade head` and `alembic check` against `ppm_test`;
  no new upgrade operations detected. No migration source changed or downgrade ran.
- PASS: six unchanged operation statement bodies, six original route signatures/
  decorators, seven unchanged existing service helpers, the example loader and
  other router logic. Full API JSON and all table/index DDL are identical. No
  unrelated existing file changed among 1,652 captured files.
- PASS: documentation checker, 416 Markdown files and 5,987 local links/anchors,
  no missing targets and retained historical requirement/status boundaries.

Only the established `enterprise-ppm-identity-test` project was used, with
PostgreSQL/Redis on test ports 15433/16380. The check script refuses a non-test app
environment, a database other than `ppm_test` for either role, or a broker other
than Redis database 1. Real provider execution stayed disabled; selected provider/
scanner interactions used mocks. Test containers and network were removed after
validation, retaining named volumes. No normal/demo database or ordinary application
container was started, rebuilt or reset.

Commands: `npm run check`; the existing isolated Compose files with
`--profile test build test` and `up -d --wait postgres redis`; the guarded test
container's `python -m alembic upgrade head`, `python -m alembic check`, and the
assessment/semantic-review/document-bridge selectors used in the previous steps;
and `python scripts/check_documentation.py`. Scratch checks compared operation
statements, route metadata/delegation, existing helper ASTs, complete OpenAPI JSON,
table/index DDL and preserved file hashes.

Other integration cases, browser/worker regressions, production deployment and live
provider quality were not rerun or newly certified. The UI and normal schema
**0020** are unchanged. Assessment lifecycle, grant and evidence operations remain
in the router for separate later steps.

## Next step

Put assessment assignment, list/detail, answer-save, submission and review operations
behind thin route adapters. Retain state transitions, live authorization, revision/
idempotency checks, scoring and immutable results. Grant management and evidence
transport can remain separate later steps.
