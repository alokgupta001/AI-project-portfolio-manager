# AI runtime operator guide

## 11 November 2026 — source-bound benchmark approvals

Cloud benchmark reviews and independent approvals bind to the current strategy's
source-file hashes. The feature-module refactor changes those bytes and paths, so
older review/approval files cannot authorize scoring of the changed strategy.
Preserve historical artifacts. Any newly authorized benchmark must regenerate its
review packet and obtain fresh independent approval through the documented flow;
do not bypass the hash check or restart a stopped pilot as part of this cleanup.

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

26 October 2026. Sprint 12 closeout checkpoint: schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13. The subsequent financial selection pilot at schema 0019 is recorded in [the latest handoff](../handoffs/LATEST.md).

Sprint 11 operators: [specialist contract](../contracts/agents.md), [handoff](../03-sprints/completed/sprint-11/HANDOFF.md) and [test commands](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md). Model allowlist, confirmation, budget/request/retry/output/cancellation limits remain unchanged. One batch serves nine agents; no paid failover. Normal data remains 0012; forward 0013 adoption is not deployed by this task. No live provider call is made in Sprint 11 acceptance.

## Historical checkpoints before Sprint 11

As of 16 October 2026, the user authorizes Gemini on a confirmed Free Tier project
with no linked Cloud Billing account and a maximum spend of **$0**. The bounded
synthetic completion/embedding smoke passed. Full provider-quality acceptance
remains unverified. Original Sprint 10 disabled-provider evidence is historical.
See [Gemini free-tier setup and acceptance](GEMINI-FREE-TIER.md). Keep credentials
in the ignored provider file; never paste secrets into reports or screenshots.

## Start and verify

Use the existing .env and volumes; never rerun bootstrap on established data.
From repository root, after private backup and isolated acceptance:

```text
docker compose -f compose.yaml -f compose.documents.yaml up -d --build
python scripts/evaluate_ai.py
node scripts/check-identity-browser.mjs tests/browser/ai.spec.ts
```

Use the existing .venv Python on Windows. Normal web/API stay 3000/8000, scanner
private, pgAdmin 5050. The browser runner uses independent 3001/8001 and volumes.
Normal head and actually executed commands/results are in the Sprint 10 handoff;
never infer an upgrade from source code or this instruction. The test lifecycle
script refuses databases other than test/ppm_test before destructive downgrades.

## Configuration and spending

Settings are validated by config.Settings. Optional private Compose env_file is
artifacts/local/ai-provider.env; it is ignored and is not created by this execution.
API, worker and dispatcher must receive identical configuration. Isolated Compose
test/browser services explicitly force disabled provider, false authorization and
empty key. Production app_env remains rejected by the existing foundation.

| Variable | Required meaning |
| --- | --- |
| PPM_AI_PROVIDER | disabled by default; gemini free-tier adapter or separately authorized openai adapter |
| PPM_AI_REAL_CALLS_AUTHORIZED | false by default; true only after separate explicit authorization |
| PPM_AI_API_KEY | SecretStr; never browser-visible or logged |
| PPM_AI_COMPLETION_MODEL | explicit supported completion model ID, no default |
| PPM_AI_EMBEDDING_MODEL | explicit dimensions-compatible embedding model ID, no default |
| PPM_AI_SPEND_LIMIT_USD | operator ceiling, default 0; not a purchase authorization |
| PPM_AI_INPUT_USD_PER_MILLION | reviewed conservative upper input tariff; default 0 |
| PPM_AI_OUTPUT_USD_PER_MILLION | reviewed conservative upper output tariff; default 0 |
| PPM_AI_EMBEDDING_USD_PER_MILLION | reviewed conservative upper embedding tariff; default 0 |
| PPM_AI_GEMINI_FREE_TIER_PROJECT | confirmed unbilled key's project ID/number; empty by default |
| PPM_AI_GEMINI_FREE_TIER_CONFIRMED_AT | timezone-aware one-time confirmation timestamp; no daily expiry |
| PPM_AI_GEMINI_FREE_TIER_KEY_SHA256 | private key binding written by the setup helper; never publish it |
| PPM_AI_GEMINI_DAILY_CALL_LIMIT | default 20 persisted attempts per tenant for runs created within 24 hours; valid 1–100 |

For OpenAI, all required fields plus positive tariffs/ceiling must be present to enable calls.
The tenant Admin must additionally save a budget within the operator ceiling;
new tenants start at 0 USD. Lowering a tenant budget below spent plus reserved is
rejected. Operator ceiling is for the selected tenant/runtime configuration;
multiple independently authorized tenants need their own spending decisions. No
invoice reconciliation or global multi-tenant invoice cap is claimed. Do not
configure live secrets merely to test missing-key behavior.

Gemini instead requires zero tariffs and a zero ceiling, an exact reviewed model,
and an operator confirmation bound to the local key and Google project.
No positive tenant budget is needed. As requested by the user, this one-time
confirmation does not expire. A replacement key/project requires confirmation;
the existing verified setup requires no daily renewal.
Each run permits at most four attempts; each tenant permits 20 attempts for runs
created in the preceding 24 hours. These counts persist in the existing ledger.
Free quota exhaustion is terminal and returns source excerpts. Gemini completion
has a 20-second HTTP timeout (22-second outer bound); embedding remains 10/12
seconds. No search, tools, uploads, caching, batch jobs or provider/model switching
are enabled. A key alone cannot establish billing state; the operator must keep
the Google project unlinked from billing.

## Inspect and recover

1. Open /ai as Admin. Inspect disabled status, tenant usage, circuit and run history.
2. Open a run and redacted diagnostics. Precharged attempts, missing token usage and
   conservative USD charges are deliberately explicit; they are not provider bills.
3. Circuit opens after three consecutive failures for 30 seconds. Correct the
   dependency/configuration and wait for cooldown before a new bounded run.
4. Timeout/cancel/crash can already have incurred an external effect. Preserve the
   unknown precharge; do not zero spent usage or blindly replay the paid request.
5. Dispatcher discovers expired leases. Crashed AI work settles failed with
   CALL_OUTCOME_UNKNOWN. Inspect before creating a fresh run with a new key.
6. Stale/deleted citations require current source retrieval/reindex; permission
   revocation requires restored authority and a new authenticated authorized run.
7. Rebuild vectors by explicitly indexing a current ready version; source append,
   deletion and reprocessing invalidate old projections. Larger than 20 chunks or
   more than 200 candidates stays keyword-only with a stated limitation.
8. Keep private database/object backups and all applied migration bytes. Recovery
   uses forward repair, never downgrade of normal/demo databases. Scratch restore
   evidence from Sprint 09 remains historical; no new full restore SLA is claimed.

The fixed-origin adapter follows the official [completion API](https://developers.openai.com/api/reference/resources/chat)
and [embedding API](https://developers.openai.com/api/reference/resources/embeddings/methods/create),
consulted 15 October 2026. Account/model compatibility, actual tariffs and real smoke
are unverified. No production/provider acceptance, RTO/RPO or invoice claim follows
from deterministic fixture success.

## Sprint 12.1 local automated fixture audit

The operator-approved exception uses `PPM_AI_FIXTURE_AUTOMATED_PILOTS`, a JSON
list of at most one pilot UUID, default `[]`. It is effective only in the local
environment. Set the same approved value on API and worker; do not add it to
shared/deployment defaults or edit the existing provider policy to enable it.
The current local activation uses a separate ignored compose overlay for saved
pilot ce874a14 only. It grants no project/provider access and preserves explicit
guided grants, shared SQL admission and the different-person path for other pilots.

An automated audit records human_reviewed=false. Removing the allowlist prevents
new/queued automated cases; retain existing reports and attempts. The approved
run is already stopped after TIMEOUT and must not be retried/reset. See
[the exact current record](../03-sprints/active/sprint-12.1/RUN_RECORD.md) and
[contract](../contracts/selection-pilot.md). Broad AT17 remains BLOCKED.
