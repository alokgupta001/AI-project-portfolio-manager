# Sprint 11.1 limited guided review implementation report

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

24 October 2026. Local implementation and rules-only deployment verified; after
explicit synthetic-demo approval, all three live API requests succeeded.
See [the activation receipt](LIVE_API_VERIFICATION.md). Base commit `e3bf8a3`; changes
remain uncommitted on `sprint-11-1-review-closeout`. Existing unrelated artifact
changes are preserved. Broad accuracy acceptance AT17 remains blocked.

## Working capability and rationale

The owner requested something usable with the existing three API accounts and
limited RAM. The Agents page now defaults to guided review when enabled. One role
can receive an optional API selection from up to eight application observations;
the response contains at most two IDs, never generated business claims. Nine
manual role checklists remain available on failure. The exact workflow and review
findings are in [the design review](REVIEW_AND_SOLUTION.md).

This solves output size and useful fallback without representing failed general
reasoning tests as a pass. No fine-tuning, new provider or Ollama is required.

## Implementation record

- `guided_review.py`: typed closed-choice response, structured observations, fixed
  actions, source-bound context, selected-project restriction and read-time checks.
- Planner/runtime/router/native adapters: one optional 128-token request, separate
  guided permission, existing quota/admission/credential/egress/cancellation gates.
  Broad task qualification is unchanged; no retries or cross-provider substitution.
- Agent DTOs/OpenAPI/TypeScript and Agents UI: guided control, result panel, fallback
  reason and nine expandable checklists alongside existing evidence/coverage.
- `compose.guided.yaml`: local guided mode enabled, cloud and Ollama disabled.
- Demo setup/smoke helpers: additive synthetic tenant, private login, normal
  authentication, CSRF, durable jobs, persistence and logout. Setup is idempotent.
- No new schema migration or dependency. Existing additive 0013–0015 were applied
  to the backed-up local 0012 database after disposable migration validation.

## Verification evidence

All receipts below are under ignored `artifacts/local/guided-review/` unless noted.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Full backend and guarded migration lifecycle/drift | 509 passed, one skipped; inherited Starlette TestClient warning | `backend-full.log` |
| Closed-choice validation and real DB admission | Invalid IDs, extra prose, revoked source, shared quota, timeout, disabled mode and broad-qualification isolation tested | `tests/test_guided_review.py`, `tests/test_guided_runtime.py` |
| Browser regression | Two journeys passed: existing v2 modes and guided fallback/reopen; axe and overflow checks at 1440/768/360 | `browser.log`, `test-results/guided-review-*.png` |
| Static checks | Full backend mypy, Ruff, frontend typecheck/lint/format, generated contracts and source manifest passed | Commands in handoff |
| Normal deployment | API/web/Postgres/Redis/worker/dispatcher healthy; schema 0015 | `start-local-final.log` |
| Actual normal queued runs | Financial/executive facts and nine checklists; risk evidence correctly unavailable; no provider requests, recorded $0 | `fallback-output.log` |
| Actual localhost UI | Private demo login, guided default, agile sprint fact, nine checklists and Account logout passed; screenshot visually inspected | `local-browser.log`, `local-demo.png` |
| Approved live API workflow | One successful request each to Gemini/Puter/Groq; three saved UI results reopened without new calls; other project scopes blocked | `live-output.log`, `live-browser.log`, [receipt](LIVE_API_VERIFICATION.md) |
| Established data | 67 old tables identical; three identity tables contain only one added login row each; every original identity row verified unchanged against backup | `database-before.json`, `database-after.json`, `identity-preservation.json` |
| Files and objects | 25 frozen configuration/source/migration hashes and all five original object hashes matched before synthetic demo setup | Private preservation backups/receipts |

The first browser attempt failed because the test used a label locator for a
control named through its accessible role; correcting the locator passed the same
UI. The first demo setup rolled back atomically on a missing risk-table import;
the corrected setup succeeded without partial demo rows.

The architecture decision and API contract additions are recorded in
[ADR 018](../architecture/adr/018-limited-guided-review.md).

## Operational boundary and next steps

Use [the local walkthrough](TRY_IT_NOW.md). Keys stay in ignored local files;
browser responses do not contain keys. The normal tenant's original records and
the rejected evaluation evidence remain preserved. API selections are withdrawn
if source access/hashes change. No write action or score change is introduced.

The approved API scope is documented [here](API_DATA_SCOPE.md). Automatic approval
review required explicit approval before persistent external calls. The operator
approved synthetic demo only; that scope is active. Original account identities,
historical usage and failure/quarantine state were preserved. One bounded request
per provider succeeded; business projects and broad interpretation remain blocked.

All known material limitations and future solutions are consolidated in
[the requested register](LIMITS_AND_FUTURE_SOLUTIONS.md). This review is by the
coding assistant, not an independent human or a new CodeRabbit review. No hosted
CI, production readiness, held-out accuracy pass or Sprint 12 implementation is
claimed. Sprint 12 can address its documented independent data/connector work;
any dependency on qualified unrestricted specialists remains unmet.
