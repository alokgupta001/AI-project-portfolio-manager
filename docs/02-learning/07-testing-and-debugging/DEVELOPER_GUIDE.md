# Read a real flow, then make a change

[Learning roadmap](../00-getting-started/README.md) Â· Next: [interview preparation](../01-project-foundations/INTERVIEW_PREPARATION.md)

The steps below teach how future changes fit the project. This documentation rewrite makes none of those application changes.

## Important files and what to read next

| File / symbol | Responsibility and why it exists | Caller, dependencies and next stop |
| --- | --- | --- |
| `apps/web/app/projects/page.tsx` | Selects the project workspace page | Next.js routing â†’ `IdentityClient` â†’ `Delivery` |
| `apps/web/components/delivery.tsx:RecordEditor.save` | Converts fields into a command and handles its result | Form submit; depends on fields/client â†’ shared transport |
| `apps/web/app/account/identity-client.tsx:transport` | Adds CSRF/organization context and refreshes credentials | Generated client or local API wrappers â†’ proxy |
| `apps/web/app/api/v1/[...path]/route.ts:proxy` | Forwards browser calls to the fixed API | Next route; depends on `API_ORIGIN` â†’ FastAPI route |
| `services/api/ppm_api/main.py:create_app` | Registers routes, resources, middleware and error handlers | uvicorn/import; depends on settings/engine/routers â†’ owning router |
| `services/api/ppm_api/identity.py:principal` | Supplies live user/session/role and transaction connection | FastAPI `Auth`; depends on identity tables/context â†’ domain handler |
| `services/api/ppm_api/delivery.py:create`, `write`, `get`, `view` | Creates, checks, reads and shapes domain records | Routes; depends on schemas, table map, grants and referenced rows â†’ table definitions |
| `services/api/ppm_api/ppm_schemas.py:ProjectInput`, `RecordView` | Defines public request and response data | FastAPI/adapter; depends on Pydantic â†’ route and validation tests |
| `services/api/ppm_api/ppm_tables.py:TABLES` | Maps typed record kinds to database tables | Domain handlers; depends on shared metadata â†’ migration and dictionary |
| `services/api/ppm_api/database.py:make_engine` | Creates reusable async database connections | App lifespan and worker â†’ `principal` transaction |
| `services/api/ppm_api/assessment.py:compute_scores` | Calculates frozen-rubric scores | `scoring`, submission/review â†’ result schemas and assessment UI |
| `services/api/ppm_api/capacity.py:calculate` | Calculates daily hours from explicit sources | `summary`, planning snapshots â†’ capacity UI |
| `services/api/ppm_api/command.py:snapshot` | Loads permitted facts and produces metrics | Snapshot route; depends on delivery/capacity/shared math â†’ `CommandCenter` |
| `services/api/migrations/versions/*.py` | Applies frozen database changes | Alembic; depends on previous revision â†’ app-role and lifecycle tests |

## Three walkthroughs

**Project:** `RecordEditor.save` â†’ typed POST â†’ `transport` â†’ `proxy` â†’ `delivery.create` with `Auth` â†’ `write`/`authorize`/`refs` â†’ INSERT `ppm_projects` plus audit/receipt â†’ `view`/`RecordView` â†’ commit â†’ `onSaved` â†’ list reload. The [line-by-line walkthrough](../02-backend/REQUEST_LIFECYCLE.md) teaches this path.

**Assessment:** `Assessments` autosave callback â†’ PUT `/assessment/assessments/{assessment_id}/answers` â†’ `save_answers` with mutation wrapper and `Auth` â†’ validate question against frozen snapshot â†’ insert/update `ppm_answers`, append event, clear results and increase revision â†’ `detail`/`scoring`/`compute_scores` â†’ response â†’ UI updates saved state. See [feature flow](../01-project-foundations/FEATURE_WORKFLOWS.md) and [scoring excerpt](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md).

**Dashboard:** `CommandCenter.refresh` â†’ GET `/command/snapshot` â†’ `snapshot` with `Auth` â†’ `delivery.lock` â†’ scoped source SELECTs â†’ capacity/shared math/`combined` â†’ `CommandSnapshot` â†’ UI state â†’ cards/tables/source drawer. Read the missing-input branch in `combined` before investigating an Unknown card.

For each walk, find one failure branch, predict what the caller sees, then find the matching test. Use `rg -n 'async def create|async def write' services/api/ppm_api/delivery.py` from the repository root to jump to symbols. Follow function calls rather than reading every file from top to bottom.

## Add an API endpoint

1. Choose the module that owns the behavior: delivery, capacity, assessment, command or identity. Add strict request/response schemas in that module's schema file.
2. Add a route on its existing router. Protected handlers use `p: Auth`; stored work uses `p.conn`. Do not create a separate connection that accidentally splits the operation's transaction.
3. Put the actual rule checks in the owning helper. Mutations need live authorization, the existing organization-lock pattern, and appropriate revision/retry rules. Reuse the assessment mutation wrapper when working in that module.
4. Return public data through the response schema. Add a frontend caller using shared transport; show loading, denial and failure states.
5. Run `npm run contracts:generate` after schema changes, then `npm run contracts:check`. Test permitted actions, wrong organization, wrong role, invalid input and relevant stale/retry cases.

## Add a database table

1. Add a Core table to the owning `*tables.py`, with organization scope, keys, relevant composite references and constraints. Do not register an internal history table as public CRUD merely because it appears in metadata.
2. Add a **new** Alembic revision after the current head. Include creation, indexes, RLS and only the necessary database privileges. Immutable records should also omit app-role UPDATE/DELETE grants.
3. Add API schemas and code that explicitly authorizes/queries/writes it. Extend `Kind`, `Input` and `TABLES` only when the generic delivery workflow fits.
4. Add form fields or a specialized UI, regenerate contracts and test direct app-role access as well as HTTP behavior.
5. Use the guarded test database for migration lifecycle/drift checks. Do not edit an already applied migration or downgrade normal user data as a shortcut.

## Add a field to a project

For a future project field, start at `ProjectInput` in `ppm_schemas.py` and the `projects` table in `ppm_tables.py`. Decide its type, whether old rows can omit it and how old data gets a value. Add a new migration, including a reviewed update to existing rows if needed.

Update `delivery.write`/`refs` if the field introduces rules or references. `view` reconstructs typed input data from row columns, so check request and response compatibility together. Add the field in `delivery-fields.ts` and any display in `delivery.tsx`. Regenerate contracts; test old records, valid new values and invalid values. Check audit/export consumers too if their semantics change.

## Add a dashboard metric

1. Define exactly which permitted rows, date range and unit it uses. Define missing/zero denominator behavior before coding.
2. Add reusable pure arithmetic to `metric_math.py` if both delivery and command views need it. Load permitted inputs in `command.snapshot` using the existing connection.
3. Return value plus source facts, coverage and freshness using the existing command schema pattern. Preserve Unknown rather than replacing missing data with zero.
4. Display it in `command-center.tsx` with a readable table/source explanation. Keep export and screen formulas the same.
5. Test a hand-calculated fixture, missing data, hidden project sources, dates and currencies where relevant. A fixed threshold should be described as a rule.

## Add an AI feature later

First define a narrow user action and output. Reuse ai.py/ai_provider.py/ai_retrieval.py and the existing sources/jobs contracts. Deterministic support gates and disabled fallback exist; real provider and model-quality acceptance are blocked. Durable business recovery is the jobs/outbox protocol, not the foundation checkpoint.

Implement the planned durable job foundation before relying on background model work. A job needs persistent state and retry/failure handling. An outbox is a database record saved with a change so a worker can reliably discover work after commit; this is future work here. Calling a provider after commit without such handling can lose the action if the process crashes between the two steps.

Connect a provider behind an explicit backend function with permitted, versioned inputs, bounded cost/time and validated output. If retrieval is needed, ingestion must preserve tenant/project access and deletion behavior before search is added. A future agent must have an allowlisted tool set; it should use existing checked commands for proposed changes rather than arbitrary SQL.

Add UI states for queued/running/failed results, clear labeling of generated advice, and tests for quality, unsupported answers, provider failure and unauthorized data. Do not invent route/function names in the guide until that code exists.

## Testing: choose a check that proves the behavior

**What?** Tests run code with selected inputs and check expected outcomes. **Why here?** Permission, scoring and transaction failures are hard to assess from a screenshot. **Where?** `tests/test_*.py`, `tests/browser/*.spec.ts`, the guarded runners and `.github/workflows/ci.yml`.

**Real example:** `test_assessment.py:test_weighting_unknown_and_coverage` calls the actual scoring function with weighted answers. It checks the 87.5 example and missing/coverage behavior. The code excerpt and arithmetic are explained in [chapter 8](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md).

**Internally:** pytest runs backend assertions; Playwright drives the browser. Integration tests require PostgreSQL/Redis and the app role. The Compose test runner also checks migration lifecycle/drift; browser fixtures are isolated through `scripts/check-identity-browser.mjs`.

**Failure:** a unit calculation test cannot prove cookies, RLS or the UI wiring. A test definition is not proof that the test ran successfully. Use the corresponding recorded logs or run the correct isolated test workflow.

Remember:

- Run calculation tests for formulas and real database tests for SQL/RLS.
- Use browser tests for form, cookie and refresh wiring.
- Regenerate/check contracts when API shapes change.
- Report the command, scope and result actually observed.

Use [`LOCAL-DEVELOPMENT.md`](../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) for the existing commands. Application tests were not rerun merely to rewrite documentation; this change uses documentation/source-integrity checks.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Follow the feature-to-document map when changing code. Confirm the exact task/acceptance and owning contract; implement, test and record real results before changing availability labels. Search functions by name because generated older line numbers moved. Update affected learning, user/demo, API/database, sprint report, limitations, catalogue and tracker; unrelated guides need no edit. Existing legacy generators contain snapshots and must not overwrite reviewed canonical guides.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Use `tests/test_account_mail.py` for templates, SMTP/TLS/auth/refusals/configuration and `tests/test_identity.py`/`test_pilot.py` plus browser identity/pilot tests for lifecycle/permissions. Isolated services force local mail despite a real configured sender. The latest recovery regression checks reset heading, masked token, password reset, revoked old session and new-password login. Keep automated results, SMTP acceptance and actual Gmail receipt separate in the [email report](../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md); diagnose credentials with booleans, never raw values or private links.

## Sprint 09 extension

For source changes, preserve byte identity/history and live scope. Use `test_documents.py`, `test_document_parser.py` and `documents.spec.ts` in guarded isolated environments. Include scanner failure/EICAR, actual OCR, replay/revocation, stale citations/tickets and held archived references. [Executed results](../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md) and [bugs/fixes](../../04-testing/sprint-based/sprint-09/BUGS_AND_FIXES.md) distinguish failed runs from accepted evidence. Refresh/check source inventories with `python scripts/documentation_inventory.py --check`.
## Sprint 10 evidence runtime

Run scripts/evaluate_ai.py offline; tests/test_ai.py uses real app-role PostgreSQL with labeled provider doubles and network access forbidden. Browser ai.spec.ts drives the no-key flow. Keep provider/model acceptance separate.

Read [the practical trace](../06-ai-and-analytics/AI_GATEWAY.md) for actual symbols, flow, failures and debugging. No Sprint 11 semantic agents or automatic changes are implemented.
