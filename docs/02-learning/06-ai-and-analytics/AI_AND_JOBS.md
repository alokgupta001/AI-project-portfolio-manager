# AI runtime, sources and durable jobs

## Sprint 12 local foundations

[Source authority, outcome history and baseline trace](LOCAL_BASELINES.md) explains the implemented Connector principal, current conflict diff, immutable manifests and offline CPU evaluation. Broad AT17 stays BLOCKED and supplies no training labels.

Sprint 11 implementation: [trace specialist evidence to human review](SPECIALISTS_REVIEW.md), [contract](../../contracts/agents.md) and [tests](../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md). One bounded completion batches nine read-only agents; shared metrics/scoring/jobs/ledger remain authoritative. Original scores, suggestions and reviewer decisions are distinct. Real semantic quality remains UNVERIFIED/BLOCKED.

## Historical checkpoints before Sprint 11

The current implementation has versioned source intake, real English OCR, keyword
citations and a controlled Sprint 10 evidence runtime. New installations default to disabled; the configured local Gemini free tier is authorized at $0 with no daily expiry and passed its bounded completion/embedding smoke. Read [the practical gateway trace](AI_GATEWAY.md) for real
symbols and flows; [document sources](DOCUMENT_SOURCES.md) owns intake/OCR/retention.

jobs.py, durable_jobs/job_outbox/job_events and the existing Celery dispatcher own
connector, document and AI work. Redis transports IDs and supports rate limits;
PostgreSQL remains job/domain truth. Workers create their own database engine/event
loop and recheck live authority. account_mail handles identity mail separately;
verified development Gmail is not evidence that an AI provider is configured.

AIOutput accepts only supported/unavailable full exact source excerpts. No private
model reasoning, arbitrary tool choice, metric rewrite, assessment rescoring or plan
mutation exists. Query results disclose keyword/source fallback and unsupported/
missing evidence rather than inventing an answer. Twelve deterministic evaluation
gates validate boundaries, not production model quality or Sprint 11 agents.

The optional fixed-origin completion/embedding adapter, typed bounded orchestration,
budgets/reservations, retry/deadline/circuit and redacted Admin console are actual
source paths. JSONB exact vectors are bounded pilot projections; pgvector/ANN scale
is not installed or accepted. Broad model/retrieval-quality acceptance remains unverified. Read
[the contract](../../contracts/ai.md), [operator controls](../../07-setup-and-deployment/AI-RUNTIME.md)
and [current tests](../../04-testing/sprint-based/sprint-10/TESTING_REPORT.md).

Sprint 11 semantic agents, Sprint 12–13 eligible models, 14 copilot and later workflow/
report/audio features remain planned. The Celery foundation checkpoint still proves
connectivity only; durable business recovery comes from the existing job protocol.
