# ADR 016 — Budgeted AI runtime and evidence-only orchestration

16 October 2026 addendum: user-authorized Gemini free-tier support uses zero-dollar
reservations and charges plus persistent attempt counts in the existing ledger.
The exact free-tier models and fixed Google origin are allowlisted. A one-time,
key-bound operator attestation records that the Google project has no billing
account; API-key authentication cannot independently establish billing state.
No paid/model/provider failover is implemented. The
[Gemini guide](../../07-setup-and-deployment/GEMINI-FREE-TIER.md) documents that
external precondition and the narrow successful synthetic smoke. No migration,
new domain authority or overall provider-quality acceptance follows. Original
15 October acceptance restrictions below describe the prior execution. The daily
confirmation expiry was removed at the user's explicit request on 16 October;
request limits, zero-dollar gates and key/project binding remain in force.

Status: accepted implementation boundary for Sprint 10; real-provider acceptance
BLOCKED by user instruction. Date: 15 October 2026. Extends ADRs 003, 004, 005, 014,
015 without changing domain authority, immutable assessments or shared formulas.

Use ai.py and the existing durable_jobs/outbox/Celery pipeline for one controlled
provider boundary. Keep a strict disabled default and test-only injected doubles.
A configured OpenAI HTTP adapter has fixed HTTPS origin, rejects redirects, bounds
request/response sizes, discards raw diagnostics, and never passes model tool calls.
Model IDs and upper tariffs require explicit operator selection; no model or price
is invented. No real provider calls are authorized in this sprint execution.

Reserve worst-case run spend atomically under the established tenant lock. Charge
attempts conservatively before sending, retain unknown charges, settle unused
reservation once and fail crashed runs without external replay. Store immutable
input/prompt/schema/tool/model/rate snapshots and hashed evidence references.
Typed source tools independently enforce project scope; there is no mutation tool.

Use two bounded branches (keyword and hybrid), truthful partial aggregation and
strict full-excerpt output validation. Store references instead of provider prose;
resolve citations on every read. This prevents unsupported numeric output being
presented as an accepted AI fact. It does not prove semantic relevance or model
accuracy, and does not implement any Sprint 11 domain agent or assessment scoring.

The baseline proposed pgvector, but the established PostgreSQL 18 image has no
pgvector extension. For this bounded pilot use rebuildable JSONB arrays with exact
cosine ranking and a hard 200-candidate fail-to-keyword limit. This is an explicit
implementation deviation, not a claim that pgvector is installed. Keeping the
existing database image avoids changing an established storage foundation. The
EmbeddingBackend seam, provenance and live source authorization remain swappable.
A future measured scale change must add a forward migration, extension-compatible
image, preservation/rebuild tests and evaluation; do not silently enable ANN.

Source append/deletion triggers and chunk-delete cascades invalidate embeddings
without modifying retained originals or holds. Do not cache raw evidence in runs.
Admin-only diagnostics are fixed codes and accounting, never source prompts,
provider bodies, secrets or private reasoning. Retain SSE stage-only semantics.

The versioned harness gates support/citation/completion at 100%, leakage/numeric
fabrication at zero on its declared fixtures. Those are validator fixtures, not
production-model scores. Required real-provider, hosted CI, archived Word visual
QA, production, capacity and full release gates stay open. See [contract](../../contracts/ai.md).
