# Sprint 12.1 — Current API financial selection pilot

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. **Workflow locally verified; approved automated run stopped on
TIMEOUT with insufficient_data. Live fixture acceptance unmet; human review false.** This is
the existing financial selection work after merged Sprint 12, now formally named
Sprint 12.1. It does not start Sprint 13 or close broad AT17.

- [Implementation report](SPRINT_REPORT.md): actual scope, evidence and open gates.
- [Technical handoff](HANDOFF.md): exact checkpoint and next safe action.
- [Actual saved pilot record](RUN_RECORD.md): creation, approved access and remaining gate.
- [User guide](USER_GUIDE.md): prepare, independently review, measure and export.
- [Reviewed execution plan](../../../09-planning/sprint-12.1/README.md).
- [Twelve-case label-review packet](../../../09-planning/sprint-12.1/LABEL_REVIEW_PACKET.md).
- [Test report](../../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md).
- [Practical code trace](../../../02-learning/06-ai-and-analytics/API_SELECTION_PILOT.md).

Normal schema is **0019_selection_pilot**. All applied migrations are frozen.
The branch is `financial-api-qualification-pilot`, based on merged main `5d5ce87`;
implementation/docs remain uncommitted alongside 21 preserved unrelated artifacts.

The live access mismatch was resolved through the owner's explicit approval of
four demo-only grants. Automatic approval review had rejected removing the grant
check; that patch did not apply and the check remains intact. Ashu then prepared
pilot `ce874a14` through the app. A separately approved automated audit checked
12/12 labels with human=false. Actual f01 matched; f02 timed out and stopped the
run. Software tests remain separate evidence; the live fixture gate is not met.
