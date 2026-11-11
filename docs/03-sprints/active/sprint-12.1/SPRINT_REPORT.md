# Sprint 12.1 implementation report

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

## Status and scope

26 October 2026. **Local workflow verified; authorized live experiment stopped
after TIMEOUT with insufficient evidence. Broad AT17 remains BLOCKED.**
The existing current-API financial selection pilot is formally named Sprint 12.1.
Base main `5d5ce87` includes merged PR 7. Branch `financial-api-qualification-pilot`
contains local uncommitted implementation/docs plus 21 preserved unrelated
artifacts. No new commit, PR, push, deployment or Sprint 13 work is claimed.

## Delivered behavior

The `/agents` UI prepares and reopens a frozen 12-case CC0 synthetic protocol,
records typed label-review provenance, measures cases through normal jobs and
shared SQL admission, compares accepted observation IDs, and downloads a saved
report with counts, latency and limitations. Python computes facts/actions;
model output supplies only bounded IDs. No extra key, RAM-heavy model, hosted
training, paid service or always-on infrastructure is required.

Default review requires another active Admin with an explicit guided grant.
After the owner explicitly approved an exception for saved pilot ce874a14,
the app gained a default-off, local-only, one-UUID automated arithmetic audit.
It checks pinned original labels with Fraction independently of Decimal label
generation. It stores `kind=automated_rule_audit`, method/checks/hash/actor/time
and **human_reviewed=false**. Other pilots retain the human gate. No personal
attestation was simulated and no review was written directly to the database.

Admin/project/grant, CSRF, RLS, binding/revision and immutable review controls
apply to both paths. Revocation of authority or the automated allowlist blocks
new/queued cases. Duplicate cases retain one run; unavailable/unknown attempts
stop the experiment. Generic AI creation cannot bypass the pilot case endpoint.
[Contract](../../../contracts/selection-pilot.md) · [code trace](../../../02-learning/06-ai-and-analytics/API_SELECTION_PILOT.md).

## Tracker and actual acceptance

| Package | Local disposition | Live evidence |
| --- | --- | --- |
| PPM-12.1-001 | Frozen protocol, scoped preparation/history/UI delivered | Ashu prepared ce874a14 in the synthetic Demo project |
| PPM-12.1-002 | Ordered single-case jobs, shared quotas, no retries/fallback success, saved report delivered | Two actual attempts; second timed out and stopped the pilot |
| PPM-12.1-003 | Separate human and owner-scoped automated provenance, measurement/eligibility controls delivered | Automated labels 12/12 checked; human review false; fixture gate not met |

[Acceptance matrix](../../../09-planning/sprint-12.1/README.md) separates tested
software from unmet real-provider fixture acceptance. Live f01 matched o1 in
21.437 seconds. f02 timed out with unknown usage/outcome. There are **1 measured,
1 unavailable, 10 unattempted and 0 held-out measured** cases. One-case precision/
recall ratios are not broad accuracy. Twelve valid matches and the p95 ≤20-second
gate are not established. [Full actual record](RUN_RECORD.md).

## Verification and preservation

Fresh automated-mode checks: **562 backend passed, one skipped, one inherited
Starlette warning (852.16 seconds)**; guarded disposable lifecycle/drift passed.
Focused arithmetic/pilot/access/runtime checks: 24 passed, overlapping the full
suite. Both pilot browser journeys passed (26.6 seconds): existing human/fallback
flow plus explicitly mocked automated provenance/download. The former also
checks Axe/overflow at 1440/768/360. Real UI audit, two attempts and report download
were then verified separately. [Testing report](../../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md).

Forward 0019 added one table in the preceding checkpoint; this continuation uses
its existing JSON review column and adds no migration/dependency. Applied
0001–0019, original prompts/source, provider files and 40 protected files remain
unchanged. Normal schema is 0019 and runtime is healthy. Existing 82 table hashes
matched after the preceding migration, before authorized new runs/grants; that
historical assertion is not reused for intentionally added current records.

At initial UI inspection all four demo Admins lacked the extra guided grant.
Automatic approval review rejected removing that check; the patch did not apply.
The owner instead approved exactly four demo-only grants, which were applied and
verified. The later automated-review authorization is separate and preserves
that gate. Memberships/business roles/other scopes remain unchanged. Normal
provider failure_count=1 from the timeout is retained, as are all six ledger rows.

## Boundaries and final disposition

Gemini/Puter/Groq, approved egress, shared 50/day/provider, one/minute, one
concurrency, 128-token output bound and $0 policy remain. Ollama stays off.
Both actual attempts have $0 app charge; provider billing was not independently
verified and timeout usage is unknown. No retries, resets, alternate providers,
held-out tuning, training labels, semantic qualification or forecast serving.

The deterministic rule already solves these fixtures; added interpretations=0.
The automated quality-check workflow is usable and reports failed/incomplete
evidence honestly. Its live fixture acceptance remains **unmet**, not passed by
mocked tests. The authorized run finished under its stop condition. Stop here;
future deployment concerns are [deferred](../../../limitations/FUTURE_DEPLOYMENT_POINTS.md).
