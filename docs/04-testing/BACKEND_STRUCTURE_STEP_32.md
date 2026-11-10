# Backend structure cleanup — step 32: remaining work completed

10 November 2026. The user requested completion of the remaining structural work.
This follow-through closes the large-router and shared-table ownership work called
out at step 29. Start with the [project map](../01-architecture/PROJECT_MAP.md) and
[feature file guides](../../services/api/ppm_api/modules/README.md).

## Completed boundaries

- **129 feature HTTP handlers across 13 routing modules are thin adapters.**
  The remaining 90 handlers delegate to business operations; the earlier 39
  assessment/document handlers retain their established delegation. HTTP
  signatures, decorators, bounds, response models and descriptions are preserved.
  Routing modules have no SQL imports. Domain modules do not import HTTP routers.
- **Tables and record inputs live at their owners.** Capacity owns workforce
  tables; integrations owns connector principals/conflicts; identity owns private
  mail deliveries; ML/workspace retain only their own tables. Command owns metric/
  risk record inputs. Shared record fields and reusable constructors live in
  shared/record_schemas and table_base. table_registry explicitly assembles complete
  metadata for API, scripts, workers and migration checks. Table-group tuples follow
  their new owners. The generic record API intentionally composes feature types.
- **Schemas and operations have explicit files.** Existing inline integration,
  workspace and selection models move to schemas. Feature operations live in
  service.py, or the descriptive integrations/jobs.py and connectors.py modules.
  Worker callers and test patch targets follow those owners directly.
- **Current navigation is reconciled.** Every feature/shared/API/worker guide
  explains actual files. The root README, project map, architecture and documentation
  index use the completed layout. Current API/database/symbol inventories match the
  existing source generator. Historical reports, prompts and artifacts remain.

See [step 30 ownership proof](BACKEND_STRUCTURE_STEP_30.md) and
[step 31 route/operation proof](BACKEND_STRUCTURE_STEP_31.md).

## Preservation

Complete OpenAPI JSON is **identical** to the pre-follow-through snapshot: **113
paths and all components**. There is no new identifier rename or contract
regeneration in this pass. All **83 table/index DDL definitions** match exactly.
Applied migrations and normal schema **0020** remain frozen; this is a Python
ownership/composition change, with no new database migration.

AST comparisons preserve 37 moved declarations/helpers, operation body statements,
21 input/response classes plus the SearchKind alias, and complete HTTP adapter
metadata. Operation signatures use Principal and ordinary values rather than HTTP
parameter metadata; adapters pass all arguments explicitly. Existing operation
comments/string contents are retained. Caller changes relocate imports, module
references and reviewed source-path strings only. Existing tests keep their
assertions; only imports/patch targets move. All 21 migration/private-config files
match the captured hashes. Per-stage checks preserve unrelated uncommitted work,
dependency locks, source prompts, provider configuration and historical artifacts.

The API root retains seven shared Python files and twelve business feature
packages. The explicit shared record foundation is an intentional common module;
the existing web/API/worker deployment and JSON task envelopes are unchanged.

## Actual verification

- PASS: **all 583 backend tests in one Linux run**, **zero skipped, zero
  deselected**, in **963.18 seconds**; one inherited Starlette/httpx warning.
  JUnit checks every collected case and rejects failures/errors/skips.
- PASS: the previously excluded **live ClamAV processing test**. The pinned scanner
  was healthy on the isolated network and real virus/source-processing checks ran.
- PASS: **real scanned-PDF/PNG/JPEG OCR** and the locked parser/runtime verifier.
- PASS: **actual Celery process crash/restart and lease recovery**, including
  500 unique effects; existing job/connector revocation, retry and replay tests.
- PASS: identity/CSRF/RLS/tenant boundaries, delivery/capacity/command facts,
  assessments/private evidence, source retention, AI/agent scopes, independent
  review, budget/fencing/cancellation, workspace, selection and ML regressions.
  Model and remote connector transports retain their fixtures/disabled-provider scope.
- PASS: npm run check:static: Python lint/format, typing across 124 source files,
  preserved-source hashes, generated contracts, frontend/browser TypeScript,
  ESLint, Prettier and all three tooling tests.
- PASS: exact API/DDL snapshots, 129-handler/dependency/ownership structural checks,
  current documentation inventories, local link/anchor checking and whitespace.
  Final navigation counts are recorded below after the completed handoff is written.

Counts are for this one full backend run; earlier focused/offline totals overlap
and are not added to it. Browser journeys and production deployment were not run
in this backend-only structural task. Live-model accuracy and open product/sprint
acceptance gates retain their existing status.

## Test isolation and final state

Only enterprise-ppm-structure-20261110 was started: test environment, both database
URLs ppm_test, Redis database 1 and ports 15435/16382. The test service used no host
source/object volume. PostgreSQL, Redis and ClamAV temporary containers/network are
removed after verification; named database/Redis/signature volumes are retained.
The old isolated test volume is preserved. Normal/demo databases were neither
reset nor migrated, and ordinary app services were not started.

The reported remaining structural tasks are complete. Existing APIs, schema/data,
authorization, quotas, stopped pilots and provider settings remain. No live model
call, new pilot, successor sprint, commit, push or deployment occurred.

## Final navigation checks

- PASS: 462 Markdown files and 6,511 local links/anchors, zero missing targets.
- PASS: all three source inventories match; preserved requirement/gap counts and
  historical sprint-status boundaries pass their existing checks.
- PASS: git diff --check, with no whitespace errors.
