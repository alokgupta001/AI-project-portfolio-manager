# Implementation guide for GPT-6.1 Sol

Start with T01. This is a sequence of future implementation tasks, not work completed by Sprint 11.1. Read handover and authoritative contracts before coding. All paths below are repository-relative; **new** means proposed, other files exist at the inspected baseline. Keep v2 disabled until migration, worker and API agree. Do not implement Sprint 12+ product features under this guide.

## Rules and reusable verification commands

For every task, update tracker to IN_PROGRESS before edits, IMPLEMENTED only when behavior exists, VERIFIED only when specified checks passed with observed exit status and saved evidence. A partial test selection must be labeled. A blocked external benchmark does not prevent mock/unit progress; it does prevent qualifying that profile. Each receipt must include commit/source hashes, changed files, commands, outputs, passed/skipped/deselected counts and remaining limitations. No automatic commit/push/deployment.

Commands C1–C6 are defined in the test plan; commands for new modules are runnable only after the corresponding test files exist. Use existing virtual environment; no unnecessary dependency upgrade. C2/C3 destroy or populate disposable fixture databases and are **future implementation-only** checks after isolation guards are verified. They were not run during this planning sprint.

Rollback common to all tasks: disable v2 admission, drain/fence active v2 work, preserve task/results/attempt history; revert only task-owned code changes if necessary. Do not reset unrelated work, downgrade normal DB, delete volumes or rewrite historical results. All tasks update this tracker plus their authoritative specification if verified code conflicts require correction. Do not silently broaden limits/permissions.

## T01 — Establish implementation baseline and preservation

- **Objective / requirements:** R01/R12/R16; reproduce source state and establish an isolated implementation baseline.
- **Prerequisites/dependencies:** user authorizes implementation; read this package, latest handoff and current source. This planning package does not itself deploy anything.
- **Inspect/modify:** `ANTIGRAVITY.md`, `docs/handoffs/LATEST.md`, current Git diff/head, `schemas.py`, `services/api/migrations`, `scripts/sprint11_preserve.py`, `scripts/test_backend.py`, `compose*.yaml`; create `docs/verification/sprint11_1/implementation-baseline.md` only. Inspect preservation script before use; avoid running its output writers against existing checkpoints.
- **Behavior:** record exact source/schema/deployed-image distinction; read normal DB revision without mutation; establish frozen migration/source hashes and non-sensitive preservation receipt; validate test guards/provider-disabled environment. Never bootstrap existing data.
- **Acceptance/unit:** current fresh offline baseline C1; reproduce negative tests, record inherited warnings and skipped case. No application implementation is claimed.
- **Integration/regression:** read-only health/revision; execute C2 only in proven disposable environment when implementation scope permits; compare historical 257/18 evidence without calling it fresh.
- **Commands:** C1, C4, `git -c safe.directory=<exact-repo> status --short`, read-only Docker inspection; guarded source tests.
- **Failure/rollback:** unexpected user changes, missing source or DB mismatch becomes documented affected-task blocker; no reset/upgrade. Continue pure contracts if safe.
- **Docs/evidence:** discovery addendum and tracker; exact baseline/limits/policy record. Completion evidence identifies whether source 0014 is deployed or merely present.

## T02 — Versioned capability and execution contracts

- **Objective / requirements:** R02/R03/R08/R12; make model-independent domain and transport types explicit.
- **Prerequisites:** T01.
- **Files:** inspect `agent_schemas.py`, `agent_engine.py:INPUTS`, `ai_schemas.py`, `document_schemas.py:Strict`; add `model_contracts.py`, `agent_registry.py`, tests `test_agent_v2_contracts.py`; extend DTOs additively behind flag.
- **Behavior:** nine exact hybrid_on_demand IDs, each with deterministic and interpretation handlers/task classes/triggers; SectionOutput modes findings/rubric/synthesis and basis aliases; separate baseline/semantic outcome and coverage; analysis_mode and ordered requested_agents; normalized execution/error contracts. Common provider request never contains credentials/scope-authority tokens in model text.
- **Acceptance/unit:** AT01, AT04, AT10; unknown fields/agent/predicate, mode/list mismatch, booleans as numbers, NaN, oversized lists and wrong section IDs rejected. All nine roles declare an interpretation path. Missing basis aliases and unsupported task classes fail. Baseline success cannot set semantic_outcome completed. V1 payloads/reviews still parse identically.
- **Integration/regression:** generate OpenAPI/client only if public schemas changed; existing agents/contracts tests pass. No migration needed yet.
- **Commands:** C1 focused `tests/test_agent_v2_contracts.py tests/test_agents.py tests/test_ai_contracts.py`; C4 contracts generation then check/typecheck.
- **Failure/rollback:** breaking old input fingerprints or enums fails task; keep facade and default-off flag, revert additive schema use if needed.
- **Docs/evidence:** technical contracts/catalog version and validated payload fixtures; source/type hashes.

## T03 — Durable task and provider-scope admission persistence

- **Objective / requirements:** R04/R06/R09; atomic counters, immutable sections and secure shared scope.
- **Prerequisites:** T02; isolated PostgreSQL available for verification.
- **Files:** new `agent_task_tables.py`, next successor migration proposed `0015_agent_task_runtime`; inspect/extend `ai_tables.py`, `job_tables.py`, `database.py`, `schemas.py`, migration 0012/0013/0014 patterns; tests `test_agent_task_storage.py`, `test_model_quota.py`.
- **Behavior:** implement exact tables/constraints/RLS/triggers/admission function from technical contracts; retain old UNIQUE(operation,attempt) via global v2 numbering; atomic run/tenant/provider/host locks, no network during transaction; add due-job recovery compatibility.
- **Acceptance/unit:** SQL helper inputs and deterministic scope mapping; AT05/06/09. Duplicate attempt/section fails; root attempts cannot reset via child.
- **Integration:** C2 lifecycle from base, 0012 and 0014; two tenants sharing provider scope cannot over-admit; direct app-role global table read/write and forged cross-tenant reference denied. Concurrent admissions produce exactly four max per run and one host generation slot.
- **Regression:** old query/index/jobs/review persistence, source immutable history and old schema upgrade preservation.
- **Commands:** C2; focused storage/quota integration tests; C4 mypy/ruff/Alembic drift/generated contracts after readiness update.
- **Failure/rollback:** deadlock/counter leak/global data leak/old-head incompatibility blocks activation; additive migration forward-fix. Do not normal-downgrade.
- **Docs/evidence:** actual revision ID, schema diff, SQL/RLS/lifecycle receipts, provider admission contract and tracker.

## T04 — Normalize existing cloud adapters without activating calls

- **Objective / requirements:** R03/R04/R05; completion metadata and controlled transport.
- **Prerequisites:** T02; T03 admission seam for integration.
- **Files:** `ai_provider.py`, `agent_provider.py`, new `model_adapters.py`, `model_contracts.py`; `tests/test_gemini.py`, `test_ai_contracts.py`, new `test_model_adapters.py`.
- **Behavior:** legacy facade delegates to normalized adapters; preserve Gemini key/project binding and exact models; classify finish/auth/quota/refusal/context/outage separately; nullable usage; fixed endpoints/no redirects; no nested retry. Use `httpx.AsyncClient` for v2 cancellation, promoting already locked httpx from dev to runtime dependency with justification and lock update under ADR 11.1-10; legacy path can stay urllib until migrated. This is a scoped dependency placement change, not a new framework.
- **Acceptance/unit:** AT04/05/14; intercepted complete/length/unknown/tool/thought/refusal/malformed/401/403/429/5xx/timeout cases; request never starts without permit. Gemini non-expiring-confirmation regressions pass.
- **Integration/regression:** fake slow transport cancelled, late output fenced, usage unknown retained; old query/index facade results unchanged. No credential read or real network in tests.
- **Commands:** C1 focused adapter/Gemini/AI contracts; C4 lock/lint/type checks; C2 affected AI tests when facade changes.
- **Failure/rollback:** lost metadata or relaxed zero-spend blocks merge; leave legacy facade active and v2 false.
- **Docs/evidence:** actual transport choice/cancellation limits and normalized response fixtures.

## T05 — Ollama adapter and host resource gate

- **Objective / requirements:** R03/R10; useful local inference path with bounded memory/calls.
- **Prerequisites:** T03/T04; real Ollama unnecessary for mocked implementation.
- **Files:** new `ollama_provider.py`, `model_registry.py` local fields; `config.py`; optional new `compose.ollama.yaml` only if private-container profile is selected; tests `test_ollama_provider.py`.
- **Behavior:** fixed private origin, explicit enablement/digest, tags/show capability probe, chat schema, stream=false, think=false, 4096 context, ≤512 output, 22 s deadline, one global host slot and configured memory reservation; no pull/cloud/arbitrary API tools. Encode all prompt fields safely and reject redirects. Share slot with embeddings.
- **Acceptance/unit:** AT04/15; mock missing model, changed digest, OOM, timeout, unsupported schema, malformed done flag, usage and concurrent requests. No auto-download or external fallback in local_only.
- **Integration:** mock server plus DB slots; two workers/tenants prove one local inference. Real smoke deferred to T12.
- **Regression:** default legacy/disabled mode starts without Ollama; no local endpoint required by CI.
- **Commands:** C1 focused local tests; C2 slot tests; C4.
- **Failure/rollback:** unsafe bind/origin or duplicate slot means no activation; disable local profile, retain legacy provider behavior.
- **Docs/evidence:** setup endpoint choice, memory policy and mock payload/response receipts; no claimed tokens/s yet.

## T06 — Deterministic eligible-first router and zero-spend policy

- **Objective / requirements:** R03/R04; decouple capabilities from provider identity.
- **Prerequisites:** T03–T05.
- **Files:** new `model_router.py`, complete `model_registry.py`; `config.py`, `ai.py` policy/admission facade; tests `test_model_router.py`, `test_model_quota.py`.
- **Behavior:** implement ordered eligibility/ranking/preflight from routing; tenant + real provider project/account + host scopes; legacy config translator that does not auto-enable cloud; immutable policy hash; unknown price/tier/limits deny. Cloud egress policy default deny.
- **Acceptance/unit:** AT03/05; deterministic route replay; absent key/enablement/spend/egress/capability denies; eligible local after cloud quota; no paid fallback; same-scope second key cannot reset quota; change auth binding invalidates. Financial/schedule/resource/PMO/Executive and privacy-safe sentiment interpretation route when their own qualified task classes are selected, without role-based exclusion. An extraction-qualified profile cannot silently perform synthesis.
- **Integration/regression:** concurrent quota admission, retry-after and circuit scopes; existing Gemini daily limit preserved in addition to provider scope, using call timestamp for v2. V1 semantics unchanged.
- **Commands:** C1 router/quota; C2 quota integration; C4.
- **Failure/rollback:** any denied route making HTTP, race overspend or data leak is release blocker; v2 off, preserve quota ledger.
- **Docs/evidence:** policy truth table, exact route fixtures and redacted diagnostics examples.

## T07 — Deterministic planner and scoped context packing

- **Objective / requirements:** R02/R05/R08/R09; eliminate one enormous nine-role prompt.
- **Prerequisites:** T02/T06.
- **Files:** new `agent_planner.py`, `agent_context.py`; inspect `agents.py:capture/current_sources`, `ai_retrieval.py`, `document_retrieval.py`; tests `test_agent_planner.py`, `test_agent_context.py`.
- **Behavior:** implement analysis_mode, explicit requested priority, per-role interpretation triggers, three initial slots drawn from any eligible role, reserved requested PMO/Executive slots and 24-node manifest; metric-only mode has no inference. Role-isolated context includes the catalog's explicit target text allowlists and tightly scoped derived synthesis evidence. Preserve snapshot/offset/assessment revision rules. Baselines use no token budget; deferred requested interpretation has separate coverage.
- **Acceptance/unit:** AT02/09/11; same input stable DAG/hash, priority reorder changes fingerprint, duplicate selection rejected, metrics mode zero calls, absent required input unavailable, huge scope exact deferred IDs. Explicit financial/schedule/resource request can receive three initial slots; Executive-only reserves its call without forcing three other agents; both synthesis roles consume at most two reserved slots. Nine-role interpretation request cannot falsely complete all semantics. Code-point offsets/injection/suppression and derived-evidence scope tests pass.
- **Integration/regression:** private assessment/organization policy/cross-project/revoked source fixtures; legacy capture unaffected when v2 off.
- **Commands:** C1 planner/context; C2 source/security; C4.
- **Failure/rollback:** untracked omission or lost rubric answer pairing fails; keep old path and stop affected v2 request.
- **Docs/evidence:** plan fixtures for minimal, full, oversized, sparse and unauthorized scope.

## T08 — Checkpointed orchestrator, leases and restart

- **Objective / requirements:** R06/R07/R14; execute persisted graph within limits.
- **Prerequisites:** T03/T06/T07.
- **Files:** new `agent_runtime.py`; `ai.py:Runtime/ai_worker/settle`, `jobs.py`, `services/worker/ppm_worker/app.py`, due-job SQL seam; tests `test_agent_runtime.py`.
- **Behavior:** state table/compare-and-swap, 10 s heartbeat/30 s lease extension within 90 s deadline; serialized inference; task/attempt checkpoints; bounded retry_wait; cancellation/unknown-outcome fencing; exactly-once local finalization and conservative quota accounting.
- **Acceptance/unit:** AT06–08/14; virtual clock deadline and retry logic; invalid transitions rejected; per-root/global budgets never reset.
- **Integration:** crash before admission/after admission/after response/after section commit/before finalization; new worker reuses committed sections, never replays unknown cloud attempt; stale token cannot publish; revoked session stops work; lost Redis messages recover through DB dispatch.
- **Regression:** old crash behavior unchanged for v1, old query/index/cancellation and worker source processing pass.
- **Commands:** C1 runtime; C2 durable jobs/AI/runtime; existing worker smoke only in isolated test stack; C4.
- **Failure/rollback:** duplicate publication, stale lease writes or runaway retries block activation; disable v2, preserve pending tasks for forward recovery.
- **Docs/evidence:** transition trace and failure-injection receipts, not only happy-path assertions.

## T09 — Capability services and deterministic validation

- **Objective / requirements:** R02/R08/R11/R12; actual nine-domain v2 behavior.
- **Prerequisites:** T07/T08.
- **Files:** extend `agent_engine.py`, `agent_schemas.py`, `agents.py:execute/publish/detail`; new `agent_validation.py`; tests `test_agent_v2_capabilities.py`, `test_agent_validation.py`; existing metrics/assessment tests.
- **Behavior:** implement deterministic baselines plus qualified on-demand interpretation handlers for all nine roles. Financial/schedule/resource interpretation explains authorized narratives with unchanged canonical numbers; Sentiment advice retains current privacy-safe aggregate and does not become emotional analysis. PMO/Executive synthesis consumes accepted basis items and original permitted spans. Validate numbers/question support/synthesis provenance, separate baseline/semantic states, preserve conflicts and review/legacy keys.
- **Acceptance/unit:** AT01 per-role matrix, AT10/12/13; all twenty catalog fields realized; each role has positive interpretation, no-benefit/metric-only, unavailable model and malicious/missing-evidence cases. Financial rework, schedule approval delay, privacy-filtered resource constraint and cross-domain/Executive explanation fixtures show grounded added value. Exact math/conflicts/scoped no_findings/null incomplete score remain; synthesis cannot erase mandatory gaps or turn its upstream interpretation into fact.
- **Integration/regression:** nine outcomes with two failures yields partial; independent reviewer can read/accept current items, self/stale/foreign acceptance denied; no project/assessment score mutation. Existing agents/review tests remain.
- **Commands:** C1 capability/validation; C2 agents/assessment/security; C4 regenerate/check contracts and inventories.
- **Failure/rollback:** altered scores/privacy/review semantics block; v2 off; never remap old approvals.
- **Docs/evidence:** domain fixtures and table-hash comparisons of business records; updated catalog actual symbols.

## T10 — Bounded semantic review and output recovery

- **Objective / requirements:** R05/R07/R08; distinguish malformed, truncated and unsupported work.
- **Prerequisites:** T08/T09.
- **Files:** new `agent_recovery.py`, `agent_evaluator.py`; validation/runtime hooks; tests `test_agent_recovery.py`, `test_agent_evaluator.py`.
- **Behavior:** one repair/split under two-per-root/four-per-run; no JSON concatenation; original manifest/accepted sections persist; optional critique shares last slot; correlated judge labeled; no LLM-derived confidence gate.
- **Acceptance/unit:** AT11/13; truncated complete-looking object rejected, malformed repair bounded, repeated IDs cannot complete missing scope, failed continuation terminal, self-agreement cannot approve unsupported evidence, fourth attempt prevents fifth.
- **Integration/regression:** restart during repair doesn't reset counters; source revocation before critique/publish; partial result remains. Preserve v1 truncation test at 512.
- **Commands:** C1 recovery/evaluator; C2 runtime failure injection; C4.
- **Failure/rollback:** loop growth or accepted incomplete JSON blocks; evaluator can be disabled independently, deterministic validation remains mandatory.
- **Docs/evidence:** recovery traces for each failure matrix row and explicit unresolved outcomes.

## T11 — API and frontend truthful progress/review

- **Objective / requirements:** R12/R14; make new execution semantics usable.
- **Prerequisites:** T09/T10.
- **Files:** `agents.py`, `ai.py:diagnostics`, `agent_schemas.py`, `ai_schemas.py`, `apps/web/components/agents.tsx`, `ai.tsx`, `live-jobs.ts`, generated contracts; tests/browser/agents.spec.ts and new v2 fixtures.
- **Behavior:** additive analysis_mode and ordered role selection; task view shows base_outcome versus semantic_outcome and separate coverage per role. Legacy states preserved; show deferred interpretations, blocked reason, unreviewed synthesis and mixed routes; role-aware controls and terminal-source revalidation retained. Baseline-only fallback cannot be labeled completed AI reasoning. Stage events ≤40 characters; no token/thought streaming.
- **Acceptance/unit/integration:** AT14/16; API role/tenant denial, legacy replay, safe error redaction; old clients tolerate added fields; exact Unicode spans still correct.
- **Browser/regression:** C3 agents/ai/documents/assessment; all nine cards, zero calls in deterministic run, partial two failures, source revoked while drawer open, keyboard/reduced-motion/mobile/light/dark, review/reject/reload and no auto-apply.
- **Commands:** C4 contract generation/check/type/lint; C2 APIs; C3 focused then final full in T14.
- **Failure/rollback:** private text/error leaks or complete label on partial result blocks; disable new UI entry, keep legacy rendering of old runs.
- **Docs/evidence:** user/demo/operator guide additions and reviewed screenshots; preserve existing historical screenshots.

## T12 — Local hardware and semantic qualification

- **Objective / requirements:** R10/R15; choose measured local profile.
- **Prerequisites:** T05/T09/T10; explicit local model setup/download available; no cloud required.
- **Files:** new `scripts/benchmark_agent_runtime.py` and synthetic `tests/fixtures/agent_v2_quality.json`; registry qualification record and `docs/verification/sprint11_1/benchmarks/`.
- **Behavior:** execute cold/warm context/model cases with rest of stack running; record RSS/available RAM/load/generation/end-to-end timing and accuracy/abstention/coverage. Qualify financial_interpretation, schedule_interpretation, team_support_advice, risk_extraction, resource_interpretation, governance_interpretation, agile_advice, portfolio_synthesis and executive_synthesis separately. A profile can activate only passing classes; universal nine-role quality requires all nine evaluated. No confidential input or estimates labeled measured.
- **Acceptance/unit:** harness refuses cloud absent specific profile authorization, caps calls and writes finite metrics; AT15/17.
- **Integration/benchmark:** real Ollama selected models, serialized chat/embedding if enabled, missing-model/OOM simulation; qualify each semantic class only against rubric thresholds. If 4B fails, benchmark smaller 1.7B; do not raise deadline automatically.
- **Regression:** C1 harness; mock tests stay passing without installed models. Real quality gate can remain BLOCKED while implementation passes.
- **Commands:** C5 exact bounded benchmark CLI after implemented; C4 script lint; `ollama --version/list/ps` read-only diagnostics.
- **Failure/rollback:** memory/latency/support failure leaves profile benchmark_only and disabled for user tasks; keyword/deterministic mode stays useful.
- **Docs/evidence:** model digest/Ollama version/hardware measured values, raw synthetic case scores, rubric reviewer, p50/p95 and retained failures. Update setup/risk/model registry with measured selection.

## T13 — Optional second free provider and local embeddings

- **Objective / requirements:** R03/R04/R10/R15; prove extension seams without mandatory cloud spend.
- **Prerequisites:** T06/T12; each sub-slice independently optional and feature-flagged.
- **Files:** optional new `groq_provider.py`; model adapter/router tests; `ai_retrieval.py`/`ai_tables.py` only if local embedding projection activated; setup/registry.
- **Behavior:** implement mock-contract Groq adapter with empty live allowlist; live profile only after exact model/free account/capability/egress authorization. For embedding, qualify 256-dimension support, truncate=false, exact model hash/query pairing; explicit reindex separate run, never automatic chat-time rebuild. Keyword fallback remains.
- **Acceptance/unit/integration:** AT03/04/05/18; keys share organization quota, paid tier denied, unsupported schema denied; mismatched embedding dimensions/model return keyword, no mixed-vector comparison.
- **Regression:** C1 mocks, C2 index/retrieval/scopes. Optional C6 only with recorded exact real free provider/model authorization; no paid requests.
- **Commands:** C1/C2/C4; C5 embedding fixture; C6 disabled by default.
- **Failure/rollback:** leave optional profiles disabled with reason, do not block local-only release. Existing embedding model remains until explicit rebuild; never delete original sources.
- **Docs/evidence:** optional sub-slice status and account verification metadata excluding keys, or explicit not-activated reason. No requirement to obtain a second key to finish core implementation.

## T14 — End-to-end regression, preservation and handover

- **Objective / requirements:** R01–R16; verify integrated runtime and close only proven gates.
- **Prerequisites:** T01–T11 implemented; T12 qualification result recorded; T13 either verified or explicitly deferred/disabled.
- **Files:** all affected source/tests; existing preservation/lifecycle/browser scripts read first; documentation, tracker, CHANGELOG, latest handoff and generated inventories.
- **Behavior:** run complete relevant regression once after integration; verify zero-spend on all dispatch paths, migration compatibility and immutable business history. No normal rollout implied; prepare concrete rollout/preservation recipe for separately authorized deployment.
- **Acceptance/unit/integration:** AT01–AT20 with receipts, failure injection, no unresolved correctness/security regressions; offline+mock mode works without keys/Ollama; local quality status truthful.
- **Regression/commands:** C1 full, C2 full guarded lifecycle/backend, C3 full browser, C4 complete static/contract/source/documentation; C5 measured record if available. Never replace missing live acceptance with mock success.
- **Failure/rollback:** keep v2 flag false for any hard-gate failure; restore app version through forward-compatible flag/code path while retaining new data. Record exact next failing test.
- **Docs/evidence:** final source hashes, matrix statuses, preservation receipt, test counts, benchmark limits, operational runbook and next action. Mark tasks VERIFIED individually; overall deployed/production readiness remains distinct.
