# Backend structure cleanup — step 29: completed organization pass

10 November 2026. User-authorized sequential continuation completed the current
backend feature-folder pass. Start with the [project map](../01-architecture/PROJECT_MAP.md)
and [feature file guides](../../services/api/ppm_api/modules/README.md).

## Result

The API package root went from **67 Python files to 7** during steps 19–28.
There are **12 feature packages**: agents, ai, assessments, capacity, command,
delivery, documents, identity, integrations, ml, selection and workspace. Each has
an explicit file guide. main/config/database/errors/health schemas/storage remain
shared at the API root. Existing web/API/worker deployments and task names remain.

The root README is now a short entrypoint. Current architecture and documentation
landing pages explain the implemented layout. Three prior landing pages are
preserved under docs/10-reference/history; only archive notes and relative-link
destinations change. Current API/database/symbol inventories were refreshed with
the existing generator, and its --check passes. The dictionary remains unchanged.
The documentation checker now includes services/README files and feature guides.

## Compatibility and preservation

All **113 API paths** and wire schemas match the step-19 baseline after normalizing
one generated component identifier: ppm_api__agent_schemas__ReviewInput became
ppm_api__modules__agents__schemas__ReviewInput. Step 26 regenerated OpenAPI and
TypeScript; normalized JSON and complete generated-type text match their originals.
There were no other contract changes. All **83 table/index DDL definitions** match
exactly, cumulatively and after the final documentation changes.

Per-step AST checks preserve definitions/statements after explicit import, module
and reviewed source/resource-path relocation. Caller imports and patch targets
follow their owners. Final static resolution checked **782 imports**;
the legacy module/source-path sweep found none in current executable/tooling code.
All **21 frozen migration/private-config files** match the
step-19 hashes. Unrelated files match each step's captured baseline, and final
documentation edits preserve the remaining source tree. Source prompts, private
provider configuration, dependency locks, existing artifacts and earlier evidence
remain preserved. No applied migration, normal/demo data, commit or deployment changed.

## Actual checks

- PASS: last complete npm run check: Python lint/format/typing, source preservation,
  generated contracts, frontend/browser typing, ESLint, Prettier and three tooling
  tests; **416 backend passed, 1 Windows OCR skip, 166 integration cases
  deselected**, in 45.08 seconds; one inherited Starlette/httpx warning.
- PASS: final npm run check:static after all source/documentation-tool changes.
- PASS: final **65 cross-feature Linux cases**, **zero skipped**, **one live-ClamAV
  case explicitly deselected**, in 130.18 seconds. This covers source processing,
  assessments, delivery, capacity, command metrics, real readiness/app-role checks,
  AI snapshots/replay, specialist review and ML artifact access after all moves.
  Real scanned-PDF/PNG/JPEG OCR executed and is checked in JUnit.
- PASS: locked parser/OCR runtime, guarded Alembic upgrade head/check, final API/DDL
  snapshots, static imports and unrelated/frozen-file preservation.
- PASS: current documentation inventories and the expanded link/anchor checker;
  final checker/whitespace results are recorded below.

Focused Linux checks at their feature checkpoints:

| Step | Feature | Passed, zero skips | Time |
| --- | --- | --- | --- |
| [19](BACKEND_STRUCTURE_STEP_19.md) | capacity | 35 | 31.15 s |
| [20](BACKEND_STRUCTURE_STEP_20.md) | command | 35 | 35.81 s |
| [21](BACKEND_STRUCTURE_STEP_21.md) | delivery | 45 | 49.54 s |
| [22](BACKEND_STRUCTURE_STEP_22.md) | identity | 69 | 57.81 s |
| [23](BACKEND_STRUCTURE_STEP_23.md) | integrations | 60 | 183.00 s |
| [24](BACKEND_STRUCTURE_STEP_24.md) | ml | 50 | 61.81 s |
| [25](BACKEND_STRUCTURE_STEP_25.md) | ai | 103 | 177.42 s |
| [26](BACKEND_STRUCTURE_STEP_26.md) | agents | 225 | 341.88 s |
| [27](BACKEND_STRUCTURE_STEP_27.md) | workspace | 49 | 28.06 s |
| [28](BACKEND_STRUCTURE_STEP_28.md) | selection | 51 | 136.55 s |

Counts overlap one another and offline checks; they are not additive unique totals.
Step 23 includes the existing real Celery crash/restart/lease-recovery case. Other
model/remote connector behavior uses fixtures or disabled providers. Live ClamAV,
live-model quality, browser journeys, restore and deployment are not certified by
this pass. The complete 583-case suite was not rerun as one final batch.

## Environment findings and cleanup

Step 19 first found a retained isolated database whose resource-update policy
lacked the current migration's archive guard. The failure reproduced using all
original pre-move service code. Verification moved to a separate fresh project,
where the existing migration chain and unchanged assertion passed. The old volume
was preserved; no normal/demo database or applied migration was repaired/reset.
Alembic table drift checks do not compare live RLS policy text.

Step 22's first Windows offline run hit WinError 5 replacing an unchanged benchmark
temporary ledger. The complete unchanged suite passed on rerun. Initial logs were
retained; no assertion or benchmark behavior was weakened.

Final checks used only enterprise-ppm-structure-20261110, environment test, both
database URLs ppm_test, Redis database 1 and ports 15435/16382. Both temporary test
projects' containers/networks are stopped/removed; named volumes are retained.
Ordinary application/demo services were not started. Live provider/pilot execution
and successor sprint work remain outside this structural pass.

## Remaining architecture seams

Several large routers still expose their established domain helpers. Delivery
retains shared workforce schemas/tables, ML retains connector authority/conflict
tables, and workspace retains the private account-mail outbox table. These are
documented in the project map and local guides. This completes feature grouping
and navigability; further domain extraction is a separate refactoring pass.

## Final navigation checks

- PASS: 458 Markdown files and 6,473 local links/anchors, zero missing targets;
  this includes API/worker and all feature guides. Requirement counts and retained
  sprint-status boundaries pass the existing checker.
- PASS: git diff --check reports no whitespace errors.
