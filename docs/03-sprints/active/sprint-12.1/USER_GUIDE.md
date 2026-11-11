# Sprint 12.1 user guide

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## Timing repair follow-up

The [28 October repair record](REPAIR_FOLLOWUP.md) supersedes the operational
checkpoint below. Open `/agents`, select the existing Demo project, expand
**Evaluate financial API selection**, then choose the saved repair pilot.
The original stopped pilot remains in the selector as historical evidence.
Its current binding can be stale after a measurement-version/allowlist change;
that does not change its original downloaded result.

Each completed case shows either **Response latency**, **Unavailable attempt
elapsed … (excluded from p95)**, or **Elapsed time not recorded** for legacy
failures. A missing elapsed value is not a zero-duration call. Use **Download pilot
report** for the same timing kind/value and measured-count summary. Narrow-screen
tables scroll horizontally; timing text wraps within the result column.

The separately authorized repair experiment uses one new exact allowlisted ID,
the unchanged twelve synthetic cases and automated review with human review false.
It stops on the first unavailable/unknown attempt. No retry/reset or additional
experiment is authorized by that repair scope. Accepted-case p95 alone cannot
pass the gate without all twelve correct cases.

## Historical 26 October workflow checkpoint

Use the [canonical financial selection walkthrough](../../../limitations/FINANCIAL_SELECTION_PILOT.md).
It covers preparation, twelve-label independent review, ordered measurement,
saved history, download, unavailable states and the shared provider budget.

The [label-review packet](../../../09-planning/sprint-12.1/LABEL_REVIEW_PACKET.md)
contains the exact synthetic cases and fingerprints. Granting access does not
approve labels. For saved pilot ce874a14, the owner approved **Run approved
automated check**. It records an exact arithmetic audit with human review false;
it does not use another person's account or attestation. Other pilots retain
personal review by a different authorized Admin.

The owner has approved and enabled the additional guided grant for all four
existing demo Admins. The gate remains intact, and Ashu prepared pilot ce874a14.
The single-pilot automated button is available after the approved local activation.
Do not change business roles, keys, egress or usage history. [Actual state](RUN_RECORD.md).

Use [the run record](RUN_RECORD.md) for actual measured counts, failures and latency.
Synthetic results cannot establish real-world AI quality; broad **AT17 remains
BLOCKED**. [Software evidence](../../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md).
