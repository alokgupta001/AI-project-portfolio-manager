# Assessment structure cleanup — step 1

5 November 2026. User-authorized local organization work, separate from sprint
feature execution. This step groups the assessment backend into one feature
package. It does not split the workflow or change its business rules.

## File map

All paths below are relative to `services/api/ppm_api`.

| Previous path | Current path |
| --- | --- |
| `assessment.py` | `modules/assessments/router.py` |
| `assessment_schemas.py` | `modules/assessments/schemas.py` |
| `assessment_tables.py` | `modules/assessments/tables.py` |
| `assessment_examples.json` | `modules/assessments/examples.json` |

The [feature README](../../services/api/ppm_api/modules/assessments/README.md)
explains each file. Imports in the API, agents, document helpers, migration metadata
loader, fixture scripts and existing tests point to the new package. Current
learning references, the code index and guide-generation source paths are updated.
Six older Markdown documents have only their source-link destinations repaired;
their historical prose, labels and results are preserved. Verification evidence
and historical plain-text paths remain unchanged.

## Compatibility

The pre-refactor API schema was captured from this existing local checkout.
All 113 API paths and all request/response definitions are equivalent after
normalizing one generated component name: `ppm_api__assessment_schemas__ReviewInput`
becomes `ppm_api__modules__assessments__schemas__ReviewInput`. This is Pydantic's
module-based disambiguation of two models named `ReviewInput`. Generated OpenAPI
and TypeScript references follow the new name; HTTP paths, operation IDs, fields,
validation and responses do not change. TypeScript consumers that explicitly name
the old component key must use the regenerated key.

The shared metadata is compared with a pre-refactor snapshot of all 83 table DDL
definitions and indexes. Applied migration files, local configuration and existing
unrelated edits are preserved. The normal application stack is not rebuilt or
restarted by this step; source changes take effect on its next ordinary rebuild.

## Verification

- PASS: Python lint/format and API/worker type checking; ESLint, frontend and browser
  TypeScript checks, Prettier and all three existing tooling tests.
- PASS: Generated OpenAPI and TypeScript contracts match the moved source.
- PASS: API definitions match the pre-refactor snapshot after the component-name normalization above.
- PASS: All 83 table/index definitions, example framework bytes and applied
  migrations match the pre-refactor snapshot. No unrelated existing file changed
  among the 1,639 captured files, including local environment and prior evidence.
  AST comparison confirms 16 affected Python source/fixture/test files differ only
  in imports or the moved resource/import path.
- PASS: Both focused assessment unit tests. The broad offline backend run selected
  417 tests: **406 passed, 10 failed, 1 skipped**, with 166 integration tests
  deselected and one inherited Starlette warning, in 75.97 seconds. All 10 failures
  were document-parser temp-directory permission errors under the Windows sandbox.
  A focused rerun using a fresh writable workspace TEMP/TMP/TMPDIR passed **10/10**
  in 2.98 seconds. Thus every one of the 416 non-skipped selected tests has a
  passing result across these runs; this is not a single all-green full-suite run.
- PASS: Documentation checker: 411 Markdown files, 5,939 local links/anchors,
  no missing targets, retained requirement and historical status boundaries.
- The existing `npm run check` runner completed its static/tooling phases but was
  interrupted during backend tests. A diagnostic located the stall in Windows
  asyncio's loopback socket-pair creation, before application code. After a network
  permission grant, the equivalent backend tests ran separately as recorded above.
  Real provider flags stayed disabled; mocked provider tests made no model calls.
- BLOCKED: Docker-backed integration, migration lifecycle and browser checks.
  The Docker named pipe is inaccessible in this chat; sandbox escalation was rejected.
  No such check is reported as passed, and normal/demo databases were not accessed.

Commands used: the static/tooling phases of `npm run check`,
`npm run contracts:generate`, `npm run contracts:check`,
`python -m pytest tests/test_assessment.py -q -m "not integration"`,
`python -m pytest -q --tb=short -m "not integration"`,
`python -m pytest tests/test_document_parser.py --last-failed -q`, and
`python scripts/check_documentation.py`. Pytest used a new disposable workspace
base directory; the parser rerun also set the three temporary-directory variables
to that writable workspace directory. The scratch snapshot checks additionally
compared API JSON, table/index DDL, normalized ASTs and preserved file hashes.

## Next step

Extract deterministic scoring and framework validation from the assessment router
while retaining their existing behavior and focused tests. Other backend features,
frontend restructuring and documentation archival are separate later steps.
