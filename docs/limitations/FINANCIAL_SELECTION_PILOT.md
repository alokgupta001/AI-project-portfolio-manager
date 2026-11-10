# Sprint 12.1 — Financial API selection pilot

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

This is the canonical practical guide for [Sprint 12.1](../03-sprints/active/sprint-12.1/README.md).
[Exact twelve-label packet](../09-planning/sprint-12.1/LABEL_REVIEW_PACKET.md) ·
[Named report](../03-sprints/active/sprint-12.1/SPRINT_REPORT.md).

The live demo exposed an access prerequisite: Admin membership alone does not
satisfy this pilot's extra explicit guided-grant check. The
[demo-only access decision](../09-planning/sprint-12.1/ACCESS_PROPOSAL.md)
is approved for all four existing demo Admins. The grants are applied and Ashu
prepared pilot ce874a14. The check remains intact; no role promotion, access bypass
or personal human label approval is implied by granting access.

26 October 2026. This is the owner-authorized next step after Sprint 12 was merged
to main in PR 7. It uses the existing Gemini route, with no additional key, paid
service, Ollama process or model training. It is **closed-choice fixture evaluation**;
it cannot establish broad semantic quality or pass AT17. Sprint 13 serving and
forecast promotion remain out of scope.

## Use it locally

1. Sign in to an existing approved organization as Admin. In **Agents & recommendation
   center** (`/agents`), choose a project for which you already have an explicit guided
   grant. The existing two approved project scopes are unchanged.
2. Open **Evaluate financial API selection**, then **Prepare selection pilot**.
   Preparing, reading, refreshing and downloading make **zero model calls**.
3. For the owner-approved saved pilot **ce874a14**, choose **Run approved automated
   check**. The exact Fraction audit checks the original frozen numeric labels
   without inference and records `human_reviewed=false`. This exception is local,
   defaults off and is allowlisted for this one pilot only. Other pilots use the
   following human path: a different person with Admin access and an existing guided grant opens the same
   project and saved pilot. Review each of the 12 observations/expected labels,
   check each label, enter a reason and attest to personal review. Choose
   **Freeze reviewed labels**. Reject a bad label by leaving it unapproved; a protocol
   correction requires a new version/pilot. The coding agent does not impersonate
   an independent human or approve these labels for you.
4. Choose **Measure case f01**, wait for its existing durable job, then continue in
   order. The first six cases are calibration; six are reserved from prompt tuning.
   Wait at least one minute between requests. There is no automatic inference loop,
   retry or fallback to another provider. Each pilot contains at most 12 case runs.
5. Inspect expected IDs versus selected IDs, mismatches and abstentions. Open
   **Measured counts and limitations** or **Download pilot report**. Reopening a saved
   result makes no model call. An unavailable/ambiguous attempt stops that pilot;
   retain it and diagnose the cause instead of resetting history.

For personal review, use an existing second authorized human account. This flow does not create users,
promote roles or add grants. Existing non-Admin guided access remains available
for ordinary reviews; the experiment requires Admin.

## What is measured

The explicit rule is: select every usage observation at least 100%, or marked
partial; otherwise abstain. Inputs contain only fixture numbers, units, partial
labels and local aliases. Python owns all displayed facts/actions and validates
the returned IDs; the model cannot supply prose, scores or evidence labels.

The twelve original numeric fixtures carry CC0-1.0 and `synthetic` lineage. They
are separate from real project metrics, genuine outcome labels, the rejected
Sprint 11.1 measurements and the frozen 108-case semantic corpus. No source records
are edited to construct these cases. Project IDs, documents, assessments, personal
notes, names and keys are absent from the provider payload. Source IDs remain local.

The report freezes the corpus, strategy, provider policy and requested model, plus
the review kind, executing actor/time/reason, and human-review flag. An automated
record also includes method, per-case arithmetic checks and evidence hash. Cases link to ordinary AI run IDs,
call records and accepted sections. Counts are reconstructed from those records;
manual fallback cards are never counted as API success. Schema **0019** adds only
`ai_selection_pilots`; applied 0001–0018 are unchanged.

The small fixture gate requires all 12 exact expected selections/abstentions and
p95 call latency at most 20 seconds. Counts and denominators are shown even on
failure. An exact-match requirement is appropriate for this deterministic closed
choice rule; it does not replace or lower the separate semantic qualification rubric.
The deterministic rule itself already solves these fixtures: there is **no
demonstrated added interpretation**, genuine outcome prediction or real-world
accuracy. A configured model ID is the requested service identity; this is not
proof of a permanently pinned provider implementation.

## States and constraints

| State | Meaning / next action |
| --- | --- |
| `awaiting_label_review` | No eligible label check yet. Measurement is disabled; use personal review or the explicitly allowlisted automated path. |
| `insufficient_data` | Fewer than 12 valid measured cases; inspect counts and remaining cases. |
| `fixture_passed` | Only the 12 synthetic exact-match and latency gates passed. AT17 stays BLOCKED. |
| `fixture_failed` | All cases measured, but an exact-match or latency gate failed. Retain the results. |
| `binding_changed` | Policy, model, corpus, prompt, runtime, reviewer authority or automated allowlist changed. No further measurements; inspect the saved evidence. |
| Case `unavailable` | Quota, disabled provider, transport, cancellation, invalid output or revoked access. No success inferred; the pilot stops. |

Existing account admission enforces the shared **50/day/provider**, **one/minute**,
single concurrent generation and **$0** policy. The pilot uses the same SQL ledger
as guided runs, including failures and unknown outcomes. It does not use historical
benchmark scripts' separate ledgers or reset any usage/quarantine. Other traffic
can exhaust the shared allowance. Puter and Groq configuration/routes are unchanged.

Software tests supply no real-provider measurement or human approval.
Test doubles show pipeline behavior only. Current live results belong in the
[Sprint 12.1 run record](../03-sprints/active/sprint-12.1/RUN_RECORD.md); the
[earlier verification](../verification/financial-selection-pilot/README.md)
and [the API contract](../contracts/selection-pilot.md). Broader semantic prompts
still need an approved data scope and independently reviewed labels/output ratings
before their original task-class gates can be assessed.
