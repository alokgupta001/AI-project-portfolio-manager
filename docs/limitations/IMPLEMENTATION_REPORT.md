# Sprint 11.1 limited guided review implementation report

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. Sprint 12 closeout checkpoint: schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13. The subsequent financial selection pilot at schema 0019 is recorded in [the latest handoff](../handoffs/LATEST.md).

Use the local history/dataset/baseline walkthrough linked from the closeout and
`/integrations` for authority/conflict review. Synthetic results are not real accuracy;
existing guided-provider quotas, access and $0 controls remain unchanged.

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
