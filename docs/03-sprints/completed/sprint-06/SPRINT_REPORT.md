# Sprint 06 implementation report

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

## Status and scope
2026-10-06. Enterprise maturity assessment engine: **complete locally after repair**, within the evidence-format limits below. Requirements F-016–F-022, W1/Features; metrics M11/M12. Base commit `f53d771`; implementation and repairs remain uncommitted. The earlier completion report is superseded. Local acceptance gates passed; hosted CI and production acceptance were not run.

## What was built
`/assessments` provides a typed framework builder, weighted dimensions, boolean/rubric/text questions, immutable publishing and four editable, labelled examples (PMO, Agile, governance, delivery). Admins assign a published version to an organization, department or team with distinct respondent and reviewer. Respondents autosave drafts and submit; reviewers start review, return with reasons, apply reasoned adjustments and complete. Results show dimension bars, accessible tables, evidence coverage, history and comparisons of completed assessments on the exact same version. Scoped editor/result grants are managed through the API.

## Why it was built
The approved maturity requirements need reproducible departmental assessments with traceable evidence and independent review. Published snapshots preserve historical scores when frameworks change. See [ADR 012](../../../architecture/adr/012-assessment-engine.md) and the [assessment contract](../../../contracts/assessment.md).

## How it works
An authenticated Admin defines and publishes a validated rubric, then assigns its immutable version. Tenant/role policies and live assignment checks authorize each operation. Draft answers use debounced autosave; revision conflicts preserve unsaved input and block submission until resolved. Writes require CSRF protection, `If-Match` where applicable and an idempotency key. Replays recheck current access.

Numeric answers normalize to 0–1; dimension scores are `100 * sum(question_weight * normalized_answer) / sum(answered_numeric_weights)`. Overall maturity sums dimension scores times dimension weights (which must total 1). Missing data is explicit, all-missing results are unknown, and required text affects completeness without pretending to be a numeric score. Completion requires computable dimensions and all required answers. The fixture yields Engineering 87.5 versus Operations 0; a documented reviewer adjustment yields Engineering 75. Weighted answer coverage is distinct from evidence question coverage. Full arithmetic is in the contract.

Evidence is quarantined on upload. The independent reviewer previews escaped text and releases it with a reason before completion/download. Completed results and published versions remain unchanged on later republishing; changes and reasons have append-only history.

## How to use and demonstrate it
Use the established ignored `.env` and activated accounts described in [identity setup](../../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md); do not bootstrap existing data again. Run `docker compose up --build -d --wait`, then open http://localhost:3000/assessments. As Admin, create or load an example, edit and publish, then assign distinct active respondent/reviewer accounts. As respondent, enter answers, wait for autosave, optionally attach a small UTF-8 `.txt` and submit. As reviewer, start review, preview/release evidence with a reason, adjust or return answers, then complete. Assign the same version to another department to compare. Publish an edited version and confirm the old result remains unchanged. Automated demonstrations use isolated fixtures; examples were not silently seeded into normal user data.

## Implementation record
- `assessment.py`, `assessment_schemas.py`, `assessment_tables.py`: domain, typed contracts, tenant entities, workflow, scoring, grants and evidence authorization.
- `0005_assessment`: additive successor, eight RLS-protected tables and immutable version/event grants. Original migrations 0001–0004 remain unchanged.
- `assessments.tsx`, route, identity shell and API proxy: responsive UI, generated DTOs, autosave and bounded evidence transport.
- `tests/test_assessment.py`, `tests/browser/assessment.spec.ts`: arithmetic, security, lifecycle and real browser coverage. Test runner credential fallbacks removed.
- No new dependencies, external scoring calls, AI functionality or background jobs introduced.

## Verification evidence
| Acceptance | Result | Evidence |
| --- | --- | --- |
| Workflow, two departments, arithmetic, missing/invalid inputs, immutable republish | Pass; full backend 49 tests | [Backend log](../../../verification/sprint-06-backend.txt) |
| RLS, roles, self-review denial, cross-assessment adjustment denial, CSRF, revisions/replay | Pass | Same backend log and test source |
| Clean/prior migration, guarded downgrade/re-upgrade, repeat upgrade, drift | Pass on disposable DB only | Same backend log |
| Real UI creation through independent review/completion | Pass, 1 targeted browser test | [Browser log](../../../verification/sprint-06-assessment-browser.txt) |
| Existing browser regression coverage | 6 passed in earlier combined run; assessment failure subsequently fixed | [Original run](../../../verification/sprint-06-browser.txt) |
| Responsive/axe/keyboard table access | Pass at 1440/768/360; screenshots inspected | [Checks and images](../../../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| Contracts, types, lint, formatting, source hashes, dependency audit | Pass | [Static](../../../verification/sprint-06-static.txt), [final web](../../../verification/sprint-06-final-web.txt) |
| Normal forward upgrade, preserved data, readiness, worker and restart/storage | Pass | [Preservation](../../../verification/sprint-06-preservation.txt), [persistence](../../../verification/sprint-06-persistence.txt), [worker](../../../verification/sprint-06-worker.txt) |

## Operational and security behavior
Local PostgreSQL, Redis, Linux worker and filesystem object storage are retained. All eight assessment tables enforce RLS. App role cannot update/delete published versions or events. Uploads have body/size/type/content checks, generated tenant storage keys and digest records. Private evidence is not exposed by result-only grants. Download rechecks authorization and sets attachment/nosniff headers. Backups/checkpoint baseline are ignored under `artifacts/local`; no credentials are included in evidence.

## Remaining work and decisions
Accepted local boundaries: only UTF-8 `.txt` evidence up to 512 KiB, at most 50 attachments per assessment; manual quarantine release is not antivirus. Broader file formats and automated scanning are not enabled. Removed evidence bytes are retained as inaccessible orphans pending a future retention process. Lists show the first 100 records; access-grant administration is API-only. These limits are documented in the contract and decision register. One inherited Starlette/httpx deprecation warning remains; all 49 tests pass. No known failing Sprint 06 acceptance check remains within this scope.

## Next sprint readiness
Sprint 07 portfolio command center dependencies are verified locally. It requires separate user authorization and has not started. Read the [technical handoff](HANDOFF.md), [checks](../../../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) and [coverage matrix](../../../requirements/coverage.md).

## Subsequent verification — 9 October 2026

The original checkpoint claims above are retained. Fresh Sprint 00–08 checks, the connector mapping repair, current runtime evidence and remaining live-provider blockers are recorded in the [sprint verification report](../../../04-testing/SPRINT_VERIFICATION_REPORT.md).
