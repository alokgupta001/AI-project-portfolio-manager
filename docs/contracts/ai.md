# AI runtime — ai-evidence-v1

Sprint 11 extends the runtime with the additive `agents` operation and [specialist contract](agents.md). It reuses calls/reservations/leases/cancellation; query/index replay hashes and all six PR #1 fixes remain. No model/ceiling/confirmation change.

Sprint 10 adds a bounded evidence runtime, not Sprint 11 domain agents. `/ai` uses
`/api/v1/ai`. OpenAPI/generated TypeScript remains authoritative. The default is
disabled. On 16 October the user authorized Gemini free-tier use at $0, confirmed
no billing account, and a bounded synthetic smoke passed. General real-provider
quality remains unverified. The optional OpenAI adapter remains separately gated.
See [Gemini limits and setup](../07-setup-and-deployment/GEMINI-FREE-TIER.md).

Gemini status reason is `FREE_TIER_OPERATOR_CONFIRMED` when eligible, otherwise
`PROVIDER_DISABLED`, `GEMINI_ZERO_SPEND_REQUIRED`, `GEMINI_FREE_MODEL_REQUIRED` or
`GEMINI_FREE_TIER_UNCONFIRMED`. Existing status fields and routes are unchanged.
`real_provider_acceptance` stays `not_verified`: a smoke is not a model evaluation.
Gemini runs snapshot the operator confirmation and count limit and use zero USD
reservation/charges. No positive tenant budget is required. `FREE_TIER_CALL_LIMIT`
and `PROVIDER_QUOTA` produce source fallback with no model/provider switch.

## Authority and API

Existing cookie/session, Origin/CSRF, organization selector and RLS apply. Admin
alone starts/cancels runs and changes budgets; current PM grants do not include an
explicit costly-analysis capability. PM/Viewer can read provider-disabled status
and use the existing permitted document keyword library. They cannot read Admin
usage, errors, budgets, evaluation or diagnostics. Run reads require actor or Admin
plus live project scope. Ownership does not bypass authority. Source tools read
only this run's project. Assessment answers, private attachments and workforce
notes are not tool inputs. Existing scores and metric formulas are unchanged.

POST `/runs` accepts project_id, operation (`query` or `index`), bounded query or
one ready version_id. It requires UUID Idempotency-Key. Replay rechecks scope and
canonical request hash; conflicting reuse is 409. Foreign/source-scope mismatch is
404. Budget/concurrency exhaustion is 429. GET `/runs` returns latest 25 with offset
(maximum 10000), stable created_at/id ordering and optional project filter.
Cancellation and PATCH `/budget` require If-Match; absent/stale is 428/412.
Budgets cannot exceed the operator ceiling or fall below spent plus reserved.

GET `/runs/{id}` reauthorizes all returned citations against current source version,
SHA-256 and chunk-text hash. Saved outputs contain references, never saved model
prose or source text. Deleted, superseded, reprocessed or revoked evidence is
withheld with EVIDENCE_UNAVAILABLE. A completed run's historic execution status
remains distinct from currently available evidence. `answer_status` differentiates
supported, source_fallback, unavailable, indexed and not_requested.

GET `/runs/{id}/events` reuses existing authorized SSE with retained cursors,
resync_required and access_revoked; fresh authentication on every poll. Stages and
timestamps contain no prompts, source text, reasoning, errors or credentials.
GET `/runs/{id}/stages` supports the UI's authorized polling. Admin diagnostics
contain version/hash references and fixed attempt codes; no raw provider bodies,
queries, object keys, credentials or private model reasoning. Returned source
excerpts are separately live-authorized public run data, not model diagnostics.

## Persistence, budget and worker behavior

Additive migration 0012_ai_runtime follows frozen 0011. Four tenant tables:
ai_budgets (tenant ceiling/spent/reserved/concurrency/circuit), ai_runs (immutable
input/version provenance, evidence references, settlement), ai_calls (operation
attempt and conservative charge), ai_embeddings (rebuildable chunk projection).
Composite tenant foreign keys, app-role RLS and immutable snapshot trigger apply.
durable_jobs references exactly one connector, source version or AI run; existing
outbox, events, dispatcher and Celery workers dispatch it. There is no second queue.

A tenant transaction lock serializes membership edits and reservations. Creation
reserves four worst-case calls; each operation attempts at most twice. A call cap
uses 120000 conservative input tokens plus 512 completion tokens at operator-set
upper USD tariffs per million; actual serialized HTTP bodies are bounded to
110000 bytes. Charges are rounded upward to six decimal places. Every attempt is
precharged before dispatch, and retained on timeout/unknown outcome. Unused run
reservation is released exactly once at settlement. This is deliberately
conservative budget accounting, not an invoice or verified provider pricing.
Input/output tokens and measured latency are recorded when actually available;
missing usage is null. No configured tariff, key, model, explicit real-call flag or
positive operator ceiling means disabled, even if some other fields exist.

At most four active runs per tenant (default one). Runs have a 90-second deadline,
75-second fenced lease, 12-second attempt deadline and bounded 0.05/0.10-second
backoff. Three consecutive failed calls open a tenant circuit for 30 seconds;
a successful probe after cooldown resets it. Cancellation and live identity/session/
role/project rechecks occur before calls and publication. A matching tenant/actor/
job tuple is required even to reconcile revoked work. A crashed paid run is failed
with CALL_OUTCOME_UNKNOWN, retaining its precharge; whole-run broker replay never
silently purchases another attempt. Recovery is inspection then an explicit new run.

## Protected graph and retrieval

Fixed typed branches are keyword retrieval and budgeted query embedding/hybrid
retrieval. Fan-out is two via asyncio.gather, each with its own short transaction;
source indexing is a separate bounded operation. Model output cannot select tools,
IDs, scopes, mutations or commands. SourceTool's Literal allowlist is validated
independently, and every branch rechecks the project. Untrusted text stays data.

Runtime.index implements the Sprint 09 EmbeddingBackend/EmbeddingRequest seam.
It checks tenant/project/version/byte hash/chunk identities before embedding and
again before storing. One request supports 1–20 chunks, 256 finite nonzero vector
dimensions. Larger sources remain keyword searchable; partitioned large-source
indexing is a future scale extension. Active hybrid reads require latest ready
source, matching source/text hash, model and chunker. More than 200 permitted vector
candidates produces an explicit keyword fallback, not an undisclosed truncated
semantic cohort. Reciprocal rank fusion combines keyword and cosine ranks.

Projection storage uses bounded exact JSONB vectors on the established PostgreSQL
image, a documented interim alternative to the proposed pgvector extension (ADR
016). No database-image swap or new extension is applied to existing data. No ANN
scale/performance claim is made. Version append/deletion triggers invalidate
projections; chunk deletion cascades. Holds and retention still protect originals.
Citation reads always reauthorize, even for an existing successful run.

Completion returns strict AIOutput: supported/unavailable and at most five full,
exact source excerpts with known chunk IDs. Unsupported numbers, foreign citations,
partial quotations and extra tool/reasoning fields fail the support gate. This is
an extractive preview; it does not establish relevance, semantic scoring or a
free-form copilot. A failed completion/embedding branch exposes honest permitted
source fallback and limitations. No matching evidence stays unavailable.

## Evaluation and acceptance

ai_evaluation_v1.json and run_evaluation establish support/citation/completion 100%,
access leakage 0 and unsupported numeric claims 0 before Sprint 11. Twelve static
positive/adversarial cases test the validator, not real model quality. Admin GET
`/evaluation` and scripts/evaluate_ai.py expose counts, failures, fixture version,
thresholds and BLOCKED real-provider acceptance. Full adversarial database and
browser gates are recorded in the Sprint 10 testing report. A real model, broader
relevance dataset, pgvector scale and production evaluation remain unverified.
