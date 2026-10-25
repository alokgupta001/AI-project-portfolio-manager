# AI runtime operator guide

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

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
