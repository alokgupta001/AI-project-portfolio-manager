# Repository discovery

Inspected 17 October 2026. Repository: `C:/Users/alokg/OneDrive/Documents/Codex/enterprise-ppm`; source HEAD `d0ebe32e691a3d63166ced669450911c63151127` (`fix: address Sprint 11 review findings and browser CI failures`). Initial working tree was clean. Parent directory is not a Git repository. Git required an exact per-command `safe.directory`; global trust was not changed. No AGENTS.md was found in the repository search. `ANTIGRAVITY.md`, latest handoff, master prompt, source Sprint 11 prompt, requirements and current contracts were read.

## Verified code facts

Paths below are repository-relative. Symbols are existing unless explicitly labeled proposed.

| Area | Evidence and observed behavior |
| --- | --- |
| Runtime | `pyproject.toml`: FastAPI, Pydantic settings, SQLAlchemy async, asyncpg, Celery/Redis; no LangChain/LangGraph. `services/worker/ppm_worker/app.py`: `pipeline_run`, late acknowledgement, worker-loss redelivery, dispatcher every 10 s. PostgreSQL job/outbox truth already exists. |
| Nine IDs | `agent_schemas.py:AGENTS`, `Agent`, `AgentBatch`; `agent_engine.py:INPUTS`, `definitions`: financial, schedule, sentiment, risk, resource, governance, agile_coach, pmo, executive. These are typed capability contracts, not nine autonomous workers. |
| Execution | `agents.py:execute` makes one `Runtime.call('completion', ...)` for all specialists/rubric matches. Nine subsequent stages record validation outcomes, not independent model calls. |
| Provider selection | `config.py:Settings.ai_provider` accepts disabled/openai/gemini only. `ai_provider.py:provider`, `enabled`, `gemini_block_reason`; one globally selected provider, configurable model strings with fixed Gemini IDs. No Ollama adapter, multi-provider registry or intelligent router found. |
| Gemini | `gemini-3.5-flash-lite`, `gemini-embedding-2` constants. Real calls require explicit boolean, key-bound non-expiring no-billing confirmation and zero price/spend fields. Every HTTP post repeats the guard; fixed origin and no redirects. |
| OpenAI | `OpenAIProvider` completion/embedding transports exist; enabled only with explicit authorization, key, models and positive price/spend settings. Not eligible for the proposed zero-spend mode. This sprint made no calls. |
| Transport | `ProviderResult(value,input_tokens,output_tokens)` and `ProviderError(code,retryable,http_status)` lose substantial completion metadata. Gemini STOP required; MAX_TOKENS becomes PROVIDER_MALFORMED. OpenAI parsing does not inspect finish_reason. Both use blocking urllib in `asyncio.to_thread`; coroutine cancellation need not stop the underlying HTTP request. |
| Prompt/context | `agents.py:capture`: current command snapshot, scoped portfolio subset, project records, sprints, selected document chunks, published framework/answers. Per-source permitted_agents. Limits: five distinct versions, at most 20 chunks/version, 50 sprints, 20,000 characters/source, 70 KB source text and 90 KB full snapshot. |
| Privacy | Sentiment receives only server-built blocker count with Admin access and minimum five team resources; no raw workforce notes. Other portfolio project metrics are restricted to PMO/Executive. All batch source text is nevertheless delivered in one shared model request; source-use separation is primarily prompt plus validation, not separate inference contexts. |
| Validation | Pydantic strict schemas, source/span membership and freshness, duplicates, conflict links, rubric checks. `supported_spans` checks authorization/offsets, not entailment. `semantic_suggestions` uses unchanged `assessment.compute_scores`; incomplete numeric-question matches make dimension suggestion unknown. |
| Aggregation | `aggregate` merges same kind/signal/source-set irrespective of claim identity or exact span. It takes highest severity and minimum confidence; differing signals on overlapping sources produce conflicts. Fixed title/improvement templates; no rich causal reasoning. Potentially distinct findings on the same source can merge (inference from key construction). |
| Retry/bounds | `ai.py:Runtime.call`: at most two attempts/operation, 50 ms first retry delay, provider timeouts 12/22 s; `create` reserves four calls and 90 s; Gemini attempt count capped at four and tenant rolling count defaults 20. Circuit opens 30 s after three failures at tenant-budget scope, not per provider. |
| Quota accounting | `ai_calls` stores conservative precharge, nullable token counts, attempt/status/code/latency. Gemini recent count joins run creation time (not call time); scope is tenant, not shared provider project/account. Model key multiplicity is not quota multiplicity. |
| Persistence/restart | `ai_runs`, `ai_calls`, `agent_analyses`, `agent_reviews`, `durable_jobs`, outbox and stages persist. `ai_worker` uses 75 s lease and rejects any previously attempted interrupted job with CALL_OUTCOME_UNKNOWN. Safe against silent replay spend, but not section-resumable. No separate persisted task graph or validated section checkpoints. |
| Concurrency | Existing worker concurrency 2; tenant budget concurrency 1–4. Query operation runs keyword/hybrid retrieval with `asyncio.gather`; specialist model work is one batch. No shared host-local model slot or cross-tenant provider quota admission. |
| Frontend | `apps/web/components/agents.tsx`: `/agents/definitions`, `/agents/runs`, detail/review; 1.5 s detail polling including terminal runs to reauthorize sources, live job stages/cancellation; exact Unicode code-point citation slicing. `ai.py` exposes SSE stages; no private reasoning is streamed. |
| Review | `agents.py:can_review`, `review`; independent review and append-only decisions. Original deterministic, suggested and approved scores separate. `0014_specialist_reviewer` allows scoped independent assessment reviewer reads. No automatic business-data mutations. |
| RAG | `ai_retrieval.py`: protected keyword tools, exact cosine over at most 200 JSONB vectors, rank fusion (k=60), top five, 256-dimensional vectors, embedding model/chunk version/source hash checks. `ai_embeddings` is unique by chunk, so simultaneous embedding-model projections are not supported. pgvector is not the current implementation. |
| Deployment/schema | Source readiness `schemas.py:SCHEMA_REVISION` is 0014. Compose has web/API/Postgres/Redis/worker/dispatcher and optional document/scanner services. No source/config changes or normal migration performed. |

## Existing agents: functional scope versus gaps

All nine have strict parsing, source allowlists, stage/status display and four parameterized supported/missing/contradictory/malicious fixture cases. That verifies plumbing, not model reasoning.

| ID | Actual implementation | Assessment |
| --- | --- | --- |
| financial | budget/spend/usage/financial-risk metrics, generic candidates | Functional deterministic fallback; LLM domain quality unverified; reuse calculations. |
| schedule | variance/schedule risk/critical metrics and dependencies | Functional fallback; distinct timing responsibility. |
| sentiment | fixed aggregate team blocker text | Intentionally limited support signal; a model adds little to a count. |
| risk | risks/blockers/project documents and risk metric | Semantic extraction owner; root-cause claims not implemented. |
| resource | capacity-risk metric | Fallback exists; richer staffing optimization remains later scope. |
| governance | policy/rubric/answers plus shared rubric matches | Useful semantic role; numerical scoring remains deterministic. |
| agile_coach | sprint records/reports and assessment text | Useful semantic role, overlaps governance on rubric; target makes governance sole match owner. |
| pmo | risk/critical/financial-risk/dependency context | Overlaps risk/executive in generic output; target assigns scoped roll-up. |
| executive | health/risk/critical/usage | Generic output rather than dependency-fed briefing; target derives validated summary. |

## Tests and environment

Fresh commands/results and output are authoritative in [verification](../../verification/sprint11_1/README.md). Full offline pytest completed with 148 passed, one skipped, 108 deselected and one existing warning; the overlapping focused AI set passed 85 tests. Sandbox attempts stalled and were interrupted; successful runs used the same application code outside the sandbox. Docker inventory initially hit sandbox pipe permission, then a read-only elevated `docker ps` succeeded: eight existing containers, web/API/Postgres/Redis/scanner healthy. This verifies container health labels only, not current checkout deployment or database revision. `Get-Command ollama` found no executable on PATH; installation elsewhere and running endpoint remain unverified.

Database migrations, full integration/browser suite, restart injection and live model benchmarks were not executed in this planning sprint. The existing lifecycle runner explicitly downgrades disposable `ppm_test`; this sprint's no-destructive-database scope excludes running it. Historical review record reports 257 backend and 18 browser passes at its own checkpoint; those are not new passes here. No credentials or private fixtures were printed.

## Documentation discrepancies and unresolved facts

1. Handoff original sections mention 0013 and earlier uncommitted branches; its review header and code show 0014. Use current code/head, keep historical records.
2. Normal runtime was historically 0012; current source expects 0014. Running containers cannot establish schema compatibility. Sol must inspect before any implementation deployment.
3. Older architecture/decision text mentions LangChain/pgvector direction; locked dependencies/current retrieval implement native typed orchestration and JSONB exact vectors.
4. Documentation calls this multi-agent orchestration; actual execution is one batch. Nine roles are valid product requirements, not evidence of nine separate model processes.
5. Semantic_status provider_supported and supported spans are not semantic proof; model_quality explicitly remains UNVERIFIED/BLOCKED.
6. Provider free-tier terms were checked publicly; this account's current billing/quotas, credentials, egress approval and availability were not inspected. Historical authorization is preserved but no cloud execution is needed for planning.

7. `semantic_suggestions` accepts an answer span from any question in the matched question's dimension, rather than requiring that question's own answer/explicit linked evidence. The proposed question-specific check is a tightening with a required negative test, not an already-existing guarantee.

Reasonable inferences: the batch is a bottleneck; role-conditioned inputs and reusable deterministic summaries reduce token demand; task checkpoints can reuse the job system. These are design judgments, not measured throughput or accuracy claims.

Planning revision after discovery: ADR 11.1-11 replaces the initial permanent role split with nine hybrid roles. Proposed financial/schedule/resource narrative inputs and PMO/Executive derived-context permissions are **target contracts**, not existing functionality or authority inferred from this report. Source findings and baseline test observations above remain unchanged.
