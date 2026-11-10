# Sprint 12.1 technical handoff

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

## Final local checkpoint

26 October 2026. **Authorized local work complete; live fixture acceptance unmet.**
Normal schema **0019_selection_pilot**, applied migrations frozen. Branch
`financial-api-qualification-pilot`, base `5d5ce87`; implementation/docs remain
uncommitted. Preserve all 21 older unrelated artifact edits. No new publication
or Sprint 13 authorization exists.

Read [report](SPRINT_REPORT.md), [actual run](RUN_RECORD.md),
[contract](../../../contracts/selection-pilot.md),
[tests](../../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md) and
[approved automated scope](../../../09-planning/sprint-12.1/AUTOMATED_AUDIT_PROPOSAL.md).

## Actual operational state

Pilot `ce874a14-bbd0-50c5-b9b6-f7909a8bda8a`, created by Ashu in Guided Review
Demo · synthetic / Demo project, has immutable `automated_rule_audit` provenance,
12/12 numeric labels checked, **human_reviewed=false**, revision 4. Only this ID
is allowlisted locally. Defaults are empty; other pilots retain personal review
by a different authorized Admin. No human identity/attestation was fabricated.

f01 matched o1, 21.437 seconds. f02 is unavailable `TIMEOUT`, call/quota outcome
unknown and usage unreported. State is `insufficient_data`; 1 measured, 1
unavailable, 10 unattempted, 0 reserved measured. Next case disabled. Calls were
88.659 seconds apart with one attempt each. App charge $0; external billing not
inspected. The observed one-case p95 exceeds the 20-second gate. No fixture pass,
broad AT17 pass, genuine outcome label or semantic qualification exists.

The owner authorized up to twelve cases with a stop on unavailable/unknown.
That stop was reached. **Do not retry, reset, start another pilot or tune prompts
to obtain a pass.** Any future experiment needs a separately authorized scope.
The app remains usable for existing authorized local flows and saved report access.

## Access and preservation

The owner approved four demo-only grants for the existing Demo Admins, then
separately approved automated checking for this one saved pilot. The explicit
grant check remains intact. Automatic approval review earlier rejected removing
it; the rejected patch did not apply. No further grant or role expansion occurred.

Memberships/project/guided grants match the pre-audit snapshot. Provider scope
configuration matches after accounting for only Gemini failure_count changing
from 0 to 1 on timeout; retain that health state. Quota/call rows grew from 4 to
6. No ledger reset, provider policy/key/egress change, migration edit or original
artifact change. Forty protected file fingerprints match.

## Validation and reproduction

- Full guarded ppm_test suite: **562 passed, one skipped, one inherited warning,
  852.16 seconds**; 0019→0006→0019→base→0019→0019 lifecycle and zero drift.
- Focused 24 tests overlap that suite; arithmetic mutation, tenant/role/grant,
  stale revision, provenance injection, replay and queued allowlist revocation.
- Two pilot browser journeys pass; human/fallback plus explicitly mocked
  automated provenance/download. No cloud/Ollama calls in disposable tests.
- Normal UI audit, real f01/f02 history, disabled f03 and downloaded report were
  separately observed. [Evidence](../../../verification/sprint12_1/README.md).

Private diff/baselines/logs/config are under ignored
`artifacts/local/sprint12_1/automated/`. The local runtime appends its separate
`allowlist.compose.yaml` to existing compose/guided/private-provider overlays.
Never publish private configuration/logs. Do not rerun preparation-only helpers
that assert empty review/cases. Final read-only evidence is public and sanitized.

No action remains within the approved run. Broad AT17 stays BLOCKED and Sprint 13
promotion/serving remains out of scope. Future deployment policy administration,
review ownership and API/worker config consistency belong in
[future deployment points](../../../limitations/FUTURE_DEPLOYMENT_POINTS.md).
