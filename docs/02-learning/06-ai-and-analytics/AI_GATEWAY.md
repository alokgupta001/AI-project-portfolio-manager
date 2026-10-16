# Practical trace: the Sprint 10 AI gateway

This chapter explains actual code. The default is disabled/fallback; the current local configuration enables operator-confirmed Gemini free tier at $0 with no daily renewal. The bounded real completion/embedding smoke passed; broad model/retrieval quality remains unverified. Full [contract](../../contracts/ai.md)
and [operator recovery](../../07-setup-and-deployment/AI-RUNTIME.md) define limits.

## Follow one query

AI in apps/web/components/ai.tsx receives the existing authenticated transport from
IdentityClient. It loads /ai/status, /ai/runs and Admin /ai/operations/evaluation.
No credentials live in component storage. A project selector comes from the existing
RecordSelect. Retrieve evidence preview sends AIRunInput plus UUID idempotency key.

ai.create calls delivery.lock, which shares the tenant advisory lock with membership
edits and rechecks the session. Admin is required because there is no separate
costly-analysis grant for PM. Project reads still pass the existing RLS service.
A replay validates scope and the canonical input SHA-256 before returning its old
run. budget locks ai_budgets and reserves the maximum four provider attempts.
ai_runs stores the immutable input, versions, prompt/schema/tool hashes and deadline.
The same transaction stores durable_jobs, job_outbox, queued stage and identity audit.
A 202 is acceptance into the queue, not completion or a successful provider response.

The existing Celery dispatcher calls pipeline.run, then jobs.run_job routes AI
references to ai_worker. ppm_ai_job validates the exact tenant/actor/job tuple,
live verified identity, session, Admin membership and active project. The task
claims a fenced 75-second lease. Work happens outside long database transactions.
Two typed Branch values run with asyncio.gather: keyword_branch calls the existing
documents.search; hybrid_branch embeds the query then reads current permitted
projections. Each opens its own connection/transaction so concurrent SQL does not
share one async connection. merge uses reciprocal ranks, not sums of incompatible
keyword and cosine units. More than 200 semantic candidates fails honestly to
keyword retrieval. SourceTool allowlists names and rejects a changed project.

Before completion, validate_snapshot checks every chunk through documents.citation,
latest ready version, original SHA-256 and text SHA-256. The evidence reference
snapshot commits before the provider call. Runtime.call precharges an ai_calls
attempt, then invokes the injected provider interface. DisabledProvider makes no
network request; source excerpts are returned with source_fallback and limitations.
An optional OpenAIProvider has fixed HTTPS origin, rejects redirects, caps JSON
request/response bytes and omits tools. Its response text must parse as AIOutput.

## Configured Gemini free-tier path

`ai_provider.provider` selects `GeminiProvider` only when `gemini_block_reason`
accepts explicit authorization, the saved key's confirmation binding, a valid
recorded project, zero tariffs/ceiling and the reviewed model IDs. The one-time
confirmation does not expire; replacing the key invalidates its SHA256 binding
until the operator records the replacement. The API key cannot verify Google
billing state; the no-billing project confirmation is an external precondition.

`GeminiProvider.post` rechecks those gates before every fixed-origin request,
rejects redirects and bounds bytes. Completion uses `generateContent`, one
candidate, 512 output tokens and structured `AIOutput`. Opaque text-part signatures
are discarded; thought/tool parts and incomplete output are rejected. Embeddings
use text-only `batchEmbedContents` with 256 dimensions. Missing embedding token
usage remains unknown. Provider error bodies and keys are never stored in results.

For Gemini, `call_cap` returns zero; no positive tenant USD budget is needed.
`Runtime.call` still locks the tenant budget before counting persisted attempts:
four per run and 20 per tenant for runs created within 24 hours. This is a request
window, not confirmation expiry. `PROVIDER_QUOTA` stops that operation without
paid/model switching; a retrieval quota failure also skips completion. Other
transient failures retain the bounded retry/circuit behavior. The existing output
and publication authority/citation checks apply equally to Gemini and doubles.

See [operator setup](../../07-setup-and-deployment/GEMINI-FREE-TIER.md) and
[recorded Gemini checks](../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).
The real smoke verifies only a narrow connection/exact excerpt/vector shape.

ai_retrieval.evaluate requires each statement to be the entire exact known source
chunk. An invented number, foreign ID, truncated quote, duplicate citation or extra
reasoning/tool field fails. References alone are persisted. At publication the worker
rechecks the lease, cancellation, live authority and every citation; settle transfers
only conservative used charges from reserved to spent and releases the balance.
The UI loads each completed result through view, which reauthorizes citations again.
Deleting a source can therefore hide an old result without rewriting history.

## Index and invalidation

Runtime.index structurally implements EmbeddingBackend.index(EmbeddingRequest), the
Sprint 09 seam. index_chunks creates the tenant/project/version/hash/chunker/chunk-ID
request from authorized current data, bounded to 20 chunks. The worker checks it
before calling and again before writing. ai_embeddings stores model, source hash,
text hash and 256 finite dimensions. In this bounded pilot exact JSONB vectors are
used on the existing PostgreSQL image; pgvector is not installed (ADR 016).
Appending a source version or tombstoning a document triggers invalidation. Removing
derived chunks cascades to embeddings. Originals and legal holds stay with Sprint 09.

## Debug failures without disclosing content

Use run ID, version IDs, fixed diagnostic codes, accounting and stage timestamps.
GET /runs/{id}/diagnostics requires Admin and never returns raw provider bodies,
input queries, object keys or private reasoning. Source excerpts remain separately
live-authorized. SSE reuses jobs.stream/event_batch, which creates a fresh principal
on each poll; it emits stages, resync_required or access_revoked. The UI polls the
same authorized stage records and displays timestamps, not a model thought stream.

If quota/timeout occurs, inspect attempts: two attempts maximum per operation and
four total per query. Missing usage remains null. A precharged timeout retains its
full cap because billing is ambiguous. Three consecutive failures open a 30-second
circuit. A successful later probe resets it. Cancellation can stop publication
while an already-sent call completes; the precharge remains. A crashed task is
settled CALL_OUTCOME_UNKNOWN instead of silently spending again on broker redelivery.
These are conservative controls, not exactly-once billing guarantees.

## Read and reproduce the evidence

Run python scripts/evaluate_ai.py for twelve versioned support/citation/completion/
leakage gate fixtures; any unexpected acceptance fails the command. Thresholds are
100% support/citation/completion and zero leakage/unsupported numeric claims. These
static cases validate gates, not model performance. tests/test_ai.py uses labeled
injected doubles with real app-role PostgreSQL, two tenants, roles, concurrent
reservations, revocation, source tombstones, worker fencing, timeouts and circuits.
It blocks accidental external network provider access. test_ai_contracts.py tests
pure shapes and adapter payloads. tests/browser/ai.spec.ts drives real no-key source
processing and the connected UI, failures/recovery, mobile layouts and role denial.

Sprint 11 agents, semantic maturity findings, predictive models and automatic plan
edits are absent. Do not describe this extractive preview as an evaluated copilot.
