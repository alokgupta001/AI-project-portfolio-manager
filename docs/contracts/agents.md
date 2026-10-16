# Specialist analysis and independent review — specialists-rubric-v1

Sprint 11 implements PPM-11-001/002/003 at `/agents` and `/api/v1/agents`.
OpenAPI/generated TypeScript is authoritative. Real-provider semantic quality is
**UNVERIFIED/BLOCKED**. Deterministic doubles establish control behavior only.

## Authority and persistence

Admin alone starts/cancels analyses, through the existing AI ledger and durable
jobs/outbox. Reads require current project scope. An analysis containing an
assessment additionally requires private assessment evidence authority; completed
result-only grants do not suffice. Independent project editors can review ordinary
recommendations. Assessment-linked runs require the named independent reviewer,
an eligible Admin/PM role and current project scope. The initiating human cannot
review their own run. Agents have no mutation or approval tool.

Additive `0013_specialist_reviews` follows verified `0012_ai_runtime`, adding
`agent_analyses` and append-only `agent_reviews`. Composite tenant references,
app-role RLS, parent binding and immutable snapshot/result triggers apply. The
AI run, analysis, job, audit and outbox are one transaction. Existing score,
answer, project, migration and object records are not rewritten. There is no
backfill, new broker or automatic action. Accepted means reviewed only.

## API

| Operation | Contract |
| --- | --- |
| GET `/definitions` | Nine specialist allowlists, tools, output schema, timeout, fallback and evaluation cases |
| POST `/runs` | Project, up to five distinct ready source-version IDs, optional private assessment; UUID Idempotency-Key; 202 |
| GET `/runs?offset=0` | Stable latest 25 lightweight summaries (`run.id`, `run.status`, `run.created_at`, stored `semantic_status`), offset capped at 10000, permission-filtered; no evidence or review history |
| GET `/runs/{id}` | Execution, per-agent outcome, missing agents, score separation, current evidence, discrepancies, stages and review history |
| POST `/runs/{id}/reviews/{item_key}` | Accepted/rejected, required reason, optional maturity override 0–100; UUID Idempotency-Key and item review revision If-Match |
| Existing `/ai/runs/{id}/cancel`, `/events`, `/stages` | Same cancellation, fenced leases, current authorization and safe persistent progress |

Missing/stale revisions return 428/412; conflicting replay 409; inaccessible IDs
404/403. Review replay rechecks current authority and returns current evidence
availability/history without duplicating a decision. Rejection can be recorded
against stale evidence; acceptance requires currently supported evidence. Review
comments are escaped data, never future model instructions.

## Nine read-only specialists

`agent_engine.INPUTS` and GET `/definitions` are the executable registry. Each
specialist emits strict `SpecialistOutput`, source spans and an explicit status.
Permitted tools are `read_authorized_snapshot` and `cite_exact_span` only.

| Agent | Permitted inputs | Honest fallback |
| --- | --- | --- |
| Financial | Shared budget, spend, usage and financial-risk metrics with currency | Deterministic over-budget/overrun finding, or unavailable |
| Schedule | Shared variance, schedule risk, critical milestones and scoped dependencies | Overdue/late metric finding, or unavailable |
| Sentiment | Server-created team blocker summary after existing minimum-five resource/day check | Unavailable; no raw workforce notes or emotional/individual labels |
| Risk | Shared risk, risk/blocker records and chosen project document chunks | Deterministic risk finding, or unavailable |
| Resource | Shared capacity-risk aggregate; no individual effort notes | Aggregate capacity finding, or unavailable |
| Governance | Chosen policy chunks, permitted assessment text and frozen published rubric | Unavailable for semantic interpretation |
| Agile Coach | Scoped sprint records, chosen sprint reports and permitted assessment text/rubric | Unavailable for semantic interpretation |
| PMO | Authorized portfolio subset of risk, critical/financial metrics and dependencies | Cited deterministic indicators; no hidden-project totals |
| Executive | Authorized portfolio risk, health, critical and budget-use metrics | Cited deterministic indicators; no invented summary facts |

One bounded structured completion batches all nine specialists and rubric matches.
All share the existing completion deadline (Gemini 22 seconds, optional existing
OpenAI adapter 12 seconds), at most two attempts, 512 output tokens, the existing
90-second run deadline, 75-second lease, circuit, cancellation, concurrency,
four-attempt/run and rolling tenant request controls. No embedding request is
needed. Batching does not raise any ceiling. Long outputs may fail/truncate or
omit specialists: those remain unavailable/partial. No provider/model switch,
paid failover or daily confirmation expiry is introduced.

## Support, scores and revocation

Sources are bound to IDs, immutable version/hash, location and exact character
spans. Metrics come from `command.snapshot`, not reimplemented formulas; unknown
values and stale sources are ineligible supports. Project documents must match
the run project; organization policy sources retain their existing authority.
Inputs are bounded to five versions, twenty chunks/version, fifty sprint records,
70 KB source text and 90 KB complete snapshot. Oversize inputs fail explicitly.

Model output cannot select scope, tools, prose, commands or mutations. Fixed
candidate categories are risks, blockers, dependencies, compliance gaps and
maturity evidence, with severity, uncalibrated confidence and spans. This support
gate proves attribution, not that a model interpreted a source correctly.

Same category, signal and source set merges deterministically. Provenance unions;
highest severity and lowest confidence survive. Opposing signals with overlapping
sources remain separate, symmetrically linked conflicts. Shared reported-health
discrepancies survive independently of model opinion. Missing/failed specialist
states are explicit and do not imply health.

Semantic matches must select an exact published numeric question level and cite
permitted text from that dimension. `assessment.compute_scores` computes suggested
dimension scores using the unchanged published weights/rubric. Every numeric
question in a dimension needs a valid match; otherwise suggestion is unknown.
Original scores are independently recomputed without reviewer overrides and frozen
in the analysis snapshot. AI suggestions and append-only reviewer-approved scores
are distinct. An override needs a reason; rejection removes current approval
without deleting its history. Confidence 0–1 is never presented as maturity 0–100.
Framework, assessment revision, model, prompt/schema hashes, source versions and
rule versions are retained. Existing completed assessment results stay untouched.

Forward `0014_specialist_reviewer` preserves 0013 and extends its analysis read
policy to independently eligible assessment reviewers with a current project
read grant. Reviewer identity, assignee/submitter separation, actor separation,
role, tenant and project scope still apply. The ordinary edit requirement for
reviewing non-assessment analyses is unchanged.

Capture and citation authority are repeated before inference, publication, detail reads
and acceptance. Source change/revocation, assessment revision change, workforce
group suppression or scope loss withholds unsupported excerpts/suggestions and
marks unavailable findings. Sensitive old review comments/approved values are
withheld when their evidence is no longer available. Historic execution status
stays distinct from current evidence availability. No saved provider prose is
served. All nine agent contracts have supported/missing/conflicting/malicious
fixtures; see [testing](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md).
List summaries expose historical execution metadata only; they do not claim
current source support. Single-run detail and acceptance retain full evidence
revalidation. Citation offsets use Unicode code points on both server and client.
