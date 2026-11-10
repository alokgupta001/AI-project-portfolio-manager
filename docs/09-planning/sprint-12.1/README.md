# Sprint 12.1 — Current API financial selection experiment

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. Owner-authorized continuation after merged Sprint 12, now
executed locally. The automated workflow is verified; **live fixture acceptance
is not met**. [Report](../../03-sprints/active/sprint-12.1/SPRINT_REPORT.md) ·
[actual run](../../03-sprints/active/sprint-12.1/RUN_RECORD.md).

## Fixed scope

Use the existing Gemini structured-ID route and normal jobs/SQL ledger. Python
owns calculations, facts and actions. Twelve original CC0 numeric fixtures use
six calibration and six reserved cases, with no prompt tuning on reserved cases.
Default review is a different authorized human. The owner separately approved
an exact arithmetic audit for saved pilot ce874a14 only, local/default-off and
explicitly **human_reviewed=false**. [Approved scope](AUTOMATED_AUDIT_PROPOSAL.md) ·
[fixed packet](LABEL_REVIEW_PACKET.md).

## Acceptance and traceability

| ID / package | Required evidence | Actual disposition |
| --- | --- | --- |
| S12.1-A1 / PPM-12.1-001 | Scoped preparation, frozen corpus/prompt/policy/model | Met locally; saved ce874a14 under Ashu |
| S12.1-A2 / PPM-12.1-003 | Valid explicit label-review provenance; human path remains distinct | Met for approved automated exception: 12/12 checked, human=false. Human path tested; no actual human review claimed |
| S12.1-A3 / PPM-12.1-002 | One durable run/case, shared admission, no duplicates/retries/fallback success | Software verified; real stop-on-timeout observed |
| S12.1-A4 / PPM-12.1-002 | Twelve valid exact matches and p95 ≤20 seconds | **Not met**: 1 measured/match at 21.437 seconds; f02 TIMEOUT; 10 unattempted; 0 reserved measured |
| S12.1-A5 / all | Saved history/download, lineage, denominators and access negatives | Met locally with actual downloaded report and isolated negative tests |
| S12.1-A6 / all | Preserved schema/data/artifacts/policy/limits, truthful evidence | Verified; 0019 frozen, roles/grants unchanged after approved grants, expected timeout health change retained |

## Completed execution

1. Owner approved all four existing demo Admins' demo-only grants; the rejected
   proposal to remove the grant check never applied.
2. Ashu prepared ce874a14 through the app and froze the exact original packet.
3. Owner explicitly approved automated checks. Implemented and tested a typed
   local one-ID audit, then recorded it through the normal UI, with no inference.
4. Measured f01 then f02, one attempt each, 88.659 seconds apart, shared limits
   intact. TIMEOUT/unknown stopped the pilot; no retry/reset or remaining calls.
5. Downloaded the actual report and recorded denominators/latency/limitations.

Local software acceptance does not imply the separate live fixture gate passed.
All results are synthetic, added interpretations=0, no genuine outcome/training
labels, no semantic-qualified class or promotion. Broad **AT17 remains BLOCKED**.
The approved run is finished under its stop rule. Stop before Sprint 13.
