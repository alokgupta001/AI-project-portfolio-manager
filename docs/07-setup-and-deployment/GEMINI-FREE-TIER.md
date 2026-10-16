# Gemini free-tier development

The user authorized Gemini on 16 October 2026 with **maximum spend $0**, and
confirmed that the key belongs to a Free Tier project with no Cloud Billing
account attached. Project identifiers and keys are separate values; a project ID
does not authenticate a request.

## Current behavior

- Completion: exact model ID `gemini-3.5-flash-lite`, structured extractive output,
  at most 512 output tokens, one candidate, minimal thinking, no returned thoughts.
- Optional embeddings: `gemini-embedding-2`, text only, 256 dimensions, at most 20
  chunks per index request. No full document uploads are sent to Google.
- Both models are explicitly listed as free-tier eligible on Google's
  [pricing page](https://ai.google.dev/gemini-api/docs/pricing), checked 16 October
  2026. Free quotas and availability remain controlled by Google.
- Zero tariffs, deployment ceiling, new reservations and new charges. Historical
  paid-provider ledger entries, if any, are preserved. This ledger is not a Google
  invoice and cannot establish the account's billing status.
- At most four attempts per run and 20 per tenant for runs created within the
  preceding 24 hours, including failed attempts. The tenant budget lock serializes
  admissions. Existing concurrency and circuit-breaker controls also apply.
- HTTP 429 is not retried; a query returns authorized source excerpts. A quota
  failure during retrieval also skips completion. Other transient failures allow
  at most two attempts per operation. No automatic model/provider fallback exists.
- Missing/changed keys, revoked authorization, nonzero price/ceiling, unknown model,
  missing confirmation, timeout, malformed/partial output or unsupported citations
  fail closed or use the existing explicit source fallback.
- The UI identifies the free tier, source transmission, Google's free-tier data
  treatment, and paused recovery. Use synthetic sources during development.

## Billing boundary

Gemini has no request parameter that forces a key to use the free tier. The same
model can incur charges on a paid project. Google's
[billing guide](https://ai.google.dev/gemini-api/docs/billing) identifies the project
tier and linked billing account as the controlling boundary.

The application records the operator's confirmation, project identifier and a
private SHA256 key binding. It does **not** verify billing through OAuth or assume
that an API key proves free-tier eligibility. At the user's request, confirmation
does not expire and requires no daily renewal. The recorded project/key binding,
authorization, zero-dollar settings and approved models are still checked before
each network attempt. Do not link this project to a billing
account. If its billing state changes, set `PPM_AI_REAL_CALLS_AUTHORIZED=false`
and recreate API, worker and dispatcher before further use. Counts and a $0
local ledger cannot prevent Google charges if the external billing precondition
is violated.

## Private setup

Save the API key locally as `PPM_AI_API_KEY` in
`artifacts/local/ai-provider.env`. This directory is ignored by Git and excluded
from Docker build contexts. Never put the key in browser code, command arguments,
chat, screenshots or reports. Do not overwrite the established root `.env`.

For initial setup, or after replacing the key/project, confirm in AI Studio that
the key's project has no billing account, then record it from repository root:

```powershell
.venv/Scripts/python.exe scripts/configure_gemini_free_tier.py --project YOUR_GOOGLE_PROJECT_ID --confirm-no-billing
docker compose -f compose.yaml -f compose.documents.yaml up -d --no-deps api worker dispatcher
```

The helper preserves a private dated backup and the original key, sets Gemini,
the exact reviewed models, all USD values to 0, and a 20-attempt tenant limit.
It makes no network calls. API, worker and dispatcher load the same private file.
Recreation is required after updates; `restart` does not reload environment files.
The existing verified key/project needs no configuration change or daily command.
Record a new confirmation if you replace the key/project; the application never
automatically asserts anything about Google's billing state. The rolling 24-hour
request-count limit is independent of confirmation and remains in place.

The generic disabled/OpenAI defaults remain unchanged for other installations.
Test and isolated browser services override provider, authorization and key so
they never use real credentials or call Google. No database migration is needed.

## Verification

The explicit real smoke sends only one synthetic source sentence and its UUID:

```powershell
$env:PYTHONPATH='services/api'
.venv/Scripts/python.exe scripts/smoke_gemini_free_tier.py --run
```

This opt-in helper makes at most two AI requests and has no retries or model
fallback. It never uses project source data. It records only redacted outcomes,
token counts when available and embedding dimensions. See the
[successful bounded smoke](../verification/gemini-free-tier-smoke.json).
Earlier attempts are preserved separately; they exposed timeout/server/model
availability failures and the need to discard an opaque text-part signature.
No raw thought text, signature or provider error body is persisted.

This establishes authentication, one supported exact excerpt and a finite
256-dimension embedding. It does not establish general reasoning quality,
retrieval quality, production scale, SLA or complete Sprint 10 acceptance.
The offline 12-case evaluation remains a fixture gate and continues reporting
real-provider acceptance as BLOCKED; it never infers acceptance from an external
smoke. The distinction is intentional.

Regression coverage: [offline adapter tests](../../tests/test_gemini.py),
[real-database runtime tests](../../tests/test_ai.py), and
[isolated UI tests](../../tests/browser/gemini.spec.ts). See the
[follow-up verification report](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).

Official references:

- [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Generation API](https://ai.google.dev/api/generate-content)
- [Text embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
- [API-key security](https://ai.google.dev/gemini-api/docs/api-key)
