# Sprint 12.1 — Testing one small task with the existing APIs

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

The app now checks one fixed financial selection rule through the existing
Gemini API. It prepares twelve synthetic examples, checks their arithmetic
labels, runs cases one at a time and saves a report. Automated checks are
clearly marked; they never pretend that another person reviewed the labels.
Only the one pilot approved by the owner can use this local automated option.
Other pilots retain the separate-person review requirement.

The actual run checked all twelve expected labels, then tried two API cases.
The first selected the correct ID but took 21.437 seconds, above the fixed
20-second threshold. The second timed out. The app stopped and retained both
attempts, leaving ten unattempted cases. There was no retry, quota reset or
prompt change. Both calls have $0 app charge; the timeout's usage is unknown.

This shows that automated quality checks can be useful: they can report a
correct answer, excessive latency and an incomplete experiment honestly.
It does **not** establish that this model meets the full fixture gate, and
one correct synthetic answer is insufficient to estimate real-world accuracy.
Broad AT17 remains BLOCKED. No training, model promotion or Sprint 13 serving
was performed. Existing accounts, access controls and shared limits are preserved.

[Actual case history](../../03-sprints/active/sprint-12.1/RUN_RECORD.md) ·
[Technical report](../../03-sprints/active/sprint-12.1/SPRINT_REPORT.md) ·
[Tests](../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md).
