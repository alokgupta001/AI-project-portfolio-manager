# Project limitations and practical next steps

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

The current-API pilot is now **Sprint 12.1**. Its [canonical package](../03-sprints/active/sprint-12.1/README.md)
records the explicit-grant prerequisite discovered in the live demo, the rejected
gate-removal proposal, four owner-approved demo-only grants and actual pilot
preparation. Independent review and measurement are still required.

New local work: [financial API selection pilot](FINANCIAL_SELECTION_PILOT.md),
with second-person label review and a reproducible synthetic fixture report.
This adds a narrower evaluation path; it cannot pass broad AT17.

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

Reviewed 24 October 2026. This folder is the current limitations register requested
by the project owner. Older sprint reports remain historical evidence. A working
local pilot does not mean every planned enterprise feature or AI accuracy gate passed.

- [Review and limited-mode design](REVIEW_AND_SOLUTION.md)
- [Exact API data scope](API_DATA_SCOPE.md)
- [Known limits and future solutions](LIMITS_AND_FUTURE_SOLUTIONS.md)
- [Use the local guided review](TRY_IT_NOW.md)
- [Successful live checks on the three supplied APIs](LIVE_API_VERIFICATION.md)
- [Named-user access and shared account limits](USER_ACCESS.md)
- [Feasibility of increasing the daily cap to 50](QUOTA_REVIEW.md)
- [Future deployment points — deferred while using the local sample](FUTURE_DEPLOYMENT_POINTS.md)

The project can remain useful with the existing Groq, Gemini and Puter accounts.
Deterministic calculations, evidence display and manual checklists provide the
baseline. Optional API selection is bounded and disposable: a failed, unavailable
or exhausted API leaves the baseline usable. No additional key, Ollama model,
fine-tuning job or paid service is required for this limited design.

Keep AT17 (broad semantic accuracy) open. The reviewed 108-case label set and
rejected model outputs remain unchanged. Closed-choice assistance neither trains
those models nor proves that the nine unrestricted specialists meet their goals.

See [the complete product release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md)
and [future sprint roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md) for the original
requirements. This register records limitations; it does not delete required scope.
