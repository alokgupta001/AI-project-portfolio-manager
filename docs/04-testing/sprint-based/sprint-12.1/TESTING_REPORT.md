# Sprint 12.1 testing report

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../../../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. **Local controls verified; actual live fixture acceptance unmet.**
The owner-approved automated run stopped at f02 TIMEOUT. Human review is false.
Software tests use disposable databases and mocked inference/attestations; actual
provider results are reported separately.

## Fresh automated-mode validation

| Check | Actual result |
| --- | --- |
| Full guarded backend | **562 passed, 1 skipped, 1 inherited Starlette warning; 852.16 seconds** |
| Disposable migration lifecycle/drift | 0019 → 0006 → 0019 → base → 0019 → 0019; no upgrade operations detected |
| Focused arithmetic/pilot/access/runtime | **24 passed; 139.62 seconds**; overlaps full suite |
| Browser | **2 passed; 26.6 seconds**: existing human/fallback flow plus explicitly mocked automated provenance/download |
| Accessibility/responsive | Existing human journey checks zero Axe violations/overflow at 1440/768/360 |
| Static/contracts/inventories/links/preservation | Exact commands/results in [validation receipt](../../../verification/sprint12_1/automated-validation.json) |
| Locked Node audit | `npm audit --audit-level=high`: no vulnerabilities reported |

Focused coverage includes pinned corpus/strategy and exact Fraction arithmetic;
tampered labels/facts/splits/lineage; default-denied/local-only/one-pilot review;
wrong hashes, stale revisions, human-provenance injection, replay/immutability;
cross-tenant/Viewer/explicit-grant denial; twelve-case mocked measurements;
duplicates/order/pacing; queued allowlist revocation; unchanged human approval
and generic AI creation bypass rejection.

The automated browser case mocks only its presentation/API reply; its isolated
server record remains unapproved. It verifies the machine label, absence of
personal attestation, next action and downloaded human=false fields. API tests
separately verify durable automated review writes and authorization. Neither
provides real-model accuracy evidence.

## Actual normal-app experiment

After focused and isolated browser checks passed, the operator-approved single-ID
local overlay was applied. Ashu recorded the audit through the UI, measured f01
and f02 and downloaded the report. No migration was added.

- Arithmetic audit: 12/12 original synthetic labels checked, zero inference,
  `kind=automated_rule_audit`, **human_reviewed=false**.
- f01: accepted o1 matches; 21,437 ms, 101 input / 18 output tokens.
- f02: `TIMEOUT`, call/quota/provider outcome unknown, usage unknown;
  unavailable rather than accepted abstention. No retry/reset.
- Starts 88.659 seconds apart; one attempt each, 128-token output reservation,
  existing shared 50/day/provider, one/minute and $0 policy unchanged.
- State: `insufficient_data`, **1 measured, 1 unavailable, 10 unattempted,
  0 held-out measured**. f03 disabled. Actual report downloaded through the UI.
- Precision/recall are 1/1 on the one measured case only; no abstention quality
  estimate. Measured-only p95=21,437 ms from one call exceeds the 20,000 ms gate.
  Twelve valid matches are absent. **Fixture gate not met**.
- Both calls record $0 app charge; external billing was not inspected and timeout
  usage was not inferred. No tuning, alternate provider or new data scope.

[Downloaded report](../../../verification/sprint12_1/live-pilot-report.json),
[call/usage evidence](../../../verification/sprint12_1/live-evidence.json),
[visible stopped UI](../../../verification/sprint12_1/live-pilot-stopped.png),
[full run](../../../03-sprints/active/sprint-12.1/RUN_RECORD.md).
All evidence is synthetic, added interpretations=0, no genuine outcome/training
labels, semantic-qualified classes empty, **AT17 BLOCKED**.

## Preservation and decision history

Starting diff/schema and private fingerprints were captured before edits.
Applied 0001–0019, original prompts/source/provider files and all 40 protected
files (including 21 older unrelated artifacts) remain unchanged. Normal schema
stays 0019 and runtime is ready. Memberships/project/guided grants remain unchanged
since the separately approved four demo grants. Provider scope settings match;
only normal Gemini failure_count changed 0→1 on TIMEOUT. Its raw checksum changed
as expected; normalizing only that counter reproduces the pre-audit checksum.
Do not claim the whole raw scope table stayed identical. Ledger counts grew 4→6,
retaining unknown usage/outcome without reset.

Automatic approval review earlier rejected removing the explicit grant gate.
The patch did not apply. The owner approved four demo-only grants instead, then
separately approved the scoped automated audit. The grant gate remains; no human
identity/attestation was fabricated and no direct DB review write occurred.

## Historical checkpoints, retained separately

Before automated mode, the implementation passed 552 backend tests/one skip/one
inherited warning (793.48s), lifecycle/drift and three browser journeys.
[Original receipts](../../../verification/financial-selection-pilot/README.md)
retain those dates. One ordinary Gemini connectivity call succeeded in 18.477s;
it was not this pilot. Naming-only checks later passed 22 focused tests (113.96s)
and one browser journey (20.4s). Counts overlap and must not be added.

The earlier [offline audit](../../../verification/sprint12_1/automated-label-check.json)
recorded no app review/inference at that timestamp. The later approved automated
app review is a distinct event. Earlier preparation receipts are historical.
