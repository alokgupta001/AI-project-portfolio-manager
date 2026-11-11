# Sprint 12.1 — Actual pilot run record

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. **Authorized local experiment executed and stopped on TIMEOUT;
fixture acceptance is not established.** This is actual provider evidence,
separate from mocked tests and the preceding ordinary connectivity call.

| Field | Actual observation |
| --- | --- |
| Pilot | `ce874a14-bbd0-50c5-b9b6-f7909a8bda8a` |
| Created | 26 October, 19:19:45 IST, by Ashu through the normal UI |
| Organization / project | Guided Review Demo · synthetic / Demo project |
| Requested service | Gemini / `gemini-3.5-flash-lite` |
| Label check | `automated_rule_audit`; exact Fraction check matched 12/12 original numeric labels |
| Personal human review | **False**; no second person was impersonated or attestation submitted |
| Actual state | `insufficient_data`; stopped after f02 became unavailable |
| Cases | 2 attempted; 1 measured/matching; 1 unavailable; 10 unattempted |
| Reserved cases measured | **0/6** |
| Observed p95 of valid measured calls | **21,437 ms**, based on only one call; exceeds the 20,000 ms gate |
| Fixture gate | **Not met**: twelve valid matches are absent and observed latency exceeds the threshold |
| Broad AT17 / qualification / serving | BLOCKED / none / none |

## Attempt history and denominators

| Case | Split | Expected | Accepted selection | Outcome | Run |
| --- | --- | --- | --- | --- | --- |
| f01 | calibration | o1 | o1 | Measured, matches; 21.437 seconds; 101 input / 18 output tokens | `baba6ccc-2d9e-4ac6-b692-5b1f7a401f87` |
| f02 | calibration | abstain | none measured | `TIMEOUT`, provider outcome/usage unknown; not an abstention success | `8860eeea-1557-4f7f-9df7-0c60f5d767fd` |
| f03–f06 | calibration | frozen packet | unmeasured | Not attempted after stop | none |
| f07–f12 | held_out | frozen packet | unmeasured | Not attempted after stop | none |

Among the **one valid measured case**, relevant/emitted/expected selections are
1/1/1, so the report's precision and recall are each 1.0. Those one-case ratios
do not estimate broad accuracy. No abstention or reserved case was measured.
The timeout's recorded call latency is zero because no provider result was
available; its local start-to-settlement interval was about 22.087 seconds.
It is excluded from measured-call p95 and retained as unavailable/unknown.

The calls started at 20:43:10 and 20:44:38 IST, **88.659 seconds apart**. Each had
one attempt and a 128-token output reservation, using normal SQL admission.
Both have $0 application charge; provider billing was not independently inspected,
and timeout token usage is unknown. There was no retry, quota reset, alternate
provider, prompt/corpus change or held-out tuning. The next case is disabled.

## Authorization, provenance and preservation

The owner first approved four existing demo Admins' demo-only guided grants
(Alok Gupta, Ashu, Blaze, Hement). The grant check remains intact. The owner then
explicitly authorized the one-pilot automated mode and up to twelve paced Gemini
cases, stopping on unavailable/unknown. See the
[approved scope](../../../09-planning/sprint-12.1/AUTOMATED_AUDIT_PROPOSAL.md).
Only this saved pilot is allowlisted in a private local overlay; defaults remain
empty and other pilots retain the different-person review gate.

The app's immutable review records `human_reviewed=false`, its executing account,
checked time, method, per-case checks and evidence hash. The original corpus,
strategy and policy binding stayed fixed. All cases remain original CC0 synthetic
fixtures, with no real outcome/training-label claim or extra data egress.

Normal schema remains **0019**. Memberships, project/guided grants and provider
scope configuration are unchanged from the pre-audit checkpoint. The normal
Gemini `failure_count` increased to 1 after TIMEOUT; this health-state change is
retained. Ledger rows grew from four to six calls/reservations, without reset.
All 40 protected files, including 21 older artifact edits, remain byte-identical.

## Evidence

- [Report downloaded through the normal app](../../../verification/sprint12_1/live-pilot-report.json).
- [Sanitized call/usage and preservation evidence](../../../verification/sprint12_1/live-evidence.json).
- [Visible stopped UI](../../../verification/sprint12_1/live-pilot-stopped.png),
  [automated provenance](../../../verification/sprint12_1/automated-audit-recorded.png).
- Historical preparation: [receipt](../../../verification/sprint12_1/prepared-pilot.json),
  [four grants](../../../verification/sprint12_1/demo-grants-approved.json),
  [offline label check](../../../verification/sprint12_1/automated-label-check.json).

The approved run is complete under its stop rule. Do not resume this pilot,
reset its history or infer a pass from synthetic tests. Any future experiment
needs a separately authorized scope; Sprint 13 remains out of scope.
