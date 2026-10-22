# Configuration and setup guide

Runtime-v2 settings/adapters now exist behind a default-off flag. Normal deployment and real-model qualification remain open; the original planning instructions below are operational requirements, not evidence of an installed/qualified model. No credentials or normal data were changed.

Current [provider/local setup follow-up](../../03-sprints/active/sprint-11.1/PROVIDER_SETUP.md): Ollama 0.40.5 and Qwen3 4B are installed and private Docker inventory reachability is verified. Groq/OpenRouter/Mistral transports exist under the same qualification/zero-spend/egress gates. Keys are entered only in ignored `artifacts/local/ai-v2.env`. Current host RAM blocks local qualification; no model inference/activation or normal rollout has occurred. This supersedes historical absent-runtime/deferred-Groq observations below. Local embeddings remain deferred.

## Implemented configuration entry points

Use `config/model-policy.example.json` as a disabled candidate template; copy it into an ignored operator directory, outside uploaded-source storage. The optional `compose.ai-v2.yaml` overlay mounts `artifacts/local/ai-v2` read-only at `/etc/ppm-ai` for API/worker and reads optional private `artifacts/local/ai-v2.env`. Set `PPM_AI_MODEL_REGISTRY_PATH=/etc/ppm-ai/policy.json` only after placing the validated policy there. This overlay does not install Ollama, enable inference, change existing Gemini confirmation or run normal migrations.

The registry profile's model, installed digest, context and memory reservation are authoritative for v2 selection. Corresponding standalone candidate defaults in Settings do not install, qualify or override a registry profile. Keep timeout/attempt/output controls within their independent hard caps.

V2 execution mode controls v2 runs. A fully offline deployment must also keep the legacy selector `PPM_AI_PROVIDER=disabled`. V2 Gemini eligibility requires that disabled legacy selector, so legacy query/index/v1-agent traffic cannot bypass the new shared scope. Keep the existing key/project/no-billing confirmation fields intact; this is an intentional dispatch-mode switch during rollout, not key rotation or daily renewal. Its profile daily limit cannot exceed `PPM_AI_GEMINI_DAILY_CALL_LIMIT`. Quiesce legacy calls and verify remaining account quota before first activation; account traffic from the old ledger is not retroactively imported into v2 reservations. Leave cloud disabled until that transition and account/egress qualification are complete.

`scripts/sync_model_policy.py` validates the same trusted policy; `--apply` explicitly synchronizes provider scopes using `PPM_MIGRATION_DATABASE_URL` in an operator-owned environment with that policy mounted. It requires 0015 and owner privileges, preserves usage/failure/auth-disable/quarantine state, and never calls a provider. Do not run it against normal 0012. All Ollama aliases must share one host scope; shared credentials must share one account scope. The SQL boundary additionally serializes every local scope globally.

`scripts/check_model_qualification.py REPORT.json` checks an independently labeled measurement report against task-class and hardware gates without changing any profile. There is no completed local benchmark or automatic qualification runner. Missing reports/digests/memory qualification keep the profile disabled/benchmark-only. Before real activation, verify a current trustworthy host-memory envelope, private endpoint, one model residency and latency/quality measurements; the configured available-memory value is operator supplied, not a Windows monitor installed by this implementation.

`PPM_TEST_AI_V2=1` is used only by the isolated browser runner to select `compose.ai-v2-test.yaml`. It enables v2 controls while Ollama/cloud stay disabled. It is not a production setting.

## Existing environment to preserve

`config.py:Settings` uses `PPM_` prefix. Required existing fields: PPM_APP_ENV, PPM_DATABASE_URL, PPM_REDIS_URL, PPM_STORAGE_ROOT, PPM_JWT_SECRET. Keep existing `.env` and ignored `artifacts/local/ai-provider.env`; never print them. Compose already reads optional provider secret env-file. Existing AI fields: PPM_AI_PROVIDER, PPM_AI_REAL_CALLS_AUTHORIZED, PPM_AI_API_KEY, PPM_AI_COMPLETION_MODEL, PPM_AI_EMBEDDING_MODEL, PPM_AI_SPEND_LIMIT_USD, PPM_AI_INPUT_USD_PER_MILLION, PPM_AI_OUTPUT_USD_PER_MILLION, PPM_AI_EMBEDDING_USD_PER_MILLION, PPM_AI_GEMINI_FREE_TIER_PROJECT, PPM_AI_GEMINI_FREE_TIER_CONFIRMED_AT, PPM_AI_GEMINI_FREE_TIER_KEY_SHA256, PPM_AI_GEMINI_DAILY_CALL_LIMIT.

An existing Gemini binding remains non-expiring and must not be rewritten merely for v2. API key presence is not provider authorization. Legacy paid OpenAI remains blocked under zero spending. Exact credentials/account status are private operator data, not documentation examples.

## Implemented settings (T02–T06)

| Name | Default / validation |
| --- | --- |
| PPM_AI_RUNTIME_V2_ENABLED | false; new run admission only, legacy results readable |
| PPM_AI_EXECUTION_MODE | local_only; enum local_only/hybrid/disabled |
| PPM_AI_MODEL_REGISTRY_PATH | unset; local trusted operator config, outside uploaded-source roots; no network URL; missing registry disables v2 inference |
| PPM_AI_CLOUD_ENABLED | false; additionally requires existing real-call authorization and per-profile authorization |
| PPM_AI_SPEND_LIMIT_USD | existing zero default; zero mode rejects any paid/unknown profile |
| PPM_AI_OLLAMA_ENABLED | false; explicit local profile enablement required |
| PPM_AI_OLLAMA_BASE_URL | http://127.0.0.1:11434 for host process only; validate fixed private allowlist, no redirects/credentials/query |
| PPM_AI_OLLAMA_MODEL | qwen3:4b candidate, not automatically installed/qualified |
| PPM_AI_OLLAMA_MODEL_DIGEST | unset; must match installed model before dispatch |
| PPM_AI_OLLAMA_NUM_CTX | 4096; initial allowed values 2048/4096; larger profiles require design review/benchmark |
| PPM_AI_OLLAMA_KEEP_ALIVE | 60s; bounded 0–60s, avoid repeated cold starts when safe |
| PPM_AI_LOCAL_CONCURRENCY | 1 only for initial deployment; enforced globally, not per process |
| PPM_AI_LOCAL_MEMORY_RESERVATION_MB | profile-specific measured peak +25%; initial 4B envelope 4096, plus host headroom 2048; admission requires available ≥sum |
| PPM_AI_RUN_DEADLINE_SECONDS | 90 hard maximum; cannot raise through user API |
| PPM_AI_MAX_ATTEMPTS_PER_RUN | 4 hard maximum, including fallback/evaluator/embedding |
| PPM_AI_MAX_OUTPUT_TOKENS | 512 hard maximum |
| PPM_AI_MAX_ATTEMPTS_PER_SECTION | 2 hard maximum including replacement child |
| PPM_AI_MAX_TASKS_PER_RUN | 24 hard maximum |
| PPM_AI_LOCAL_COMPLETION_TIMEOUT_SECONDS | 22 max initial profile; effective bound also remaining deadline minus 5 |
| PPM_AI_EGRESS_POLICY_PATH | unset means deny cloud; operator-owned tenant/project/data-category policy |
| PPM_AI_LOCAL_EMBEDDING_MODEL | empty; keyword retrieval enabled without model |

Registry stores model capacities, quota scope and exact limits, qualified task classes, endpoint allowlist and credential references. Do not accept these policy settings from ordinary analysis requests. Bound profile counts/config bytes and use schema/hash validation. Changing config invalidates pending old policy work rather than silently switching it.

Hybrid-role revision: configure eligible task classes for all nine roles independently. Do not copy a fixed role exclusion list into provider settings. A profile qualified for risk_extraction does not automatically qualify financial_interpretation or executive_synthesis. Unqualified classes remain explicit unavailable/benchmark-only while their Python baselines work.

Proposed v2 per-request `analysis_mode` is auto/metrics/domain/assessment/portfolio/executive, not an environment variable or spending authorization. Use metrics for no-model numerical checks; domain with ordered requested_agents for focused investigation; assessment requires assessment_id; portfolio/executive reserve the requested synthesis slot(s) within the three initial model sections. Four attempts/512 tokens/90 seconds still apply. Requesting interpretation for all nine roles cannot guarantee all nine finish in one run; inspect baseline and semantic coverage separately.

## Local Ollama setup after implementation

Use the [official Windows installer](https://docs.ollama.com/windows); record installed version. No installation was attempted here. Configure process environment before restarting the Ollama application: `OLLAMA_NO_CLOUD=1`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_CONTEXT_LENGTH=4096`. These are Ollama settings, not application PPM settings. Default listener is loopback. Model download is an explicit operator operation; the backend must never pull models on a user request.

```powershell
ollama --version
ollama pull qwen3:4b
ollama list
ollama show qwen3:4b
ollama ps
```

Record full installed digest through `/api/tags` response; compare show metadata/schema support and license. The 4B download is about 2.5 GB as observed in official registry; runtime requires additional model/cache/context memory. Benchmark before user-data activation. Qwen3 1.7B (about 1.4 GB) is a smaller fallback candidate; Gemma3 4B (about 3.4 GB plus associated modality components in its package) a comparator. These download figures are not RAM promises. See [sources](SPRINT_11_1_SOURCES.md).

Host loopback is not the container's loopback. A worker in Docker must use a deliberately configured private endpoint, often a verified `host.docker.internal` route with a firewall-restricted native listener, or a separate Ollama container on the Compose private network with no public port. Do not expose unauthenticated Ollama on all interfaces merely to make it reachable. Choose and test one profile; initial recommended isolation is a private Compose Ollama service if safe native access cannot be established. If native listener needs non-loopback binding, restrict inbound firewall to the actual trusted Docker path and test external rejection before activation. No application-config change can prove this network boundary by itself.

One local host slot covers chat and embeddings. Run chat model first. After model is idle, unload via an explicit operator request/keep_alive=0, then benchmark `embeddinggemma:300m` only if optional embedding slice is implemented. No concurrent two-model residency assumed. Start with keyword retrieval; a chat run never waits for an automatic indexing job. If supported/qualified, `/api/embed` uses dimensions=256, truncate=false and per-model task formatting; otherwise embeddings remain disabled. Do not silently truncate vectors or input documents.

## Safe profiles

1. **Ollama only:** cloud false, mode local_only, zero spend, installed qualified local digest; keyword source retrieval and deterministic fallback. Missing local model yields explicit unavailable plus useful deterministic results.
2. **Ollama + mocked cloud:** same real-cloud-disabled policy; tests inject authorized synthetic adapters/transport, synthetic credentials only; global deny-network fixture. No real account needed.
3. **Explicit real free hybrid:** cloud true plus exact provider/model/account binding, independently verified non-billable tier, quotas and data policy. Configure maximum requests/tokens/concurrency, zero spend and source minimization. Free-tier terms can permit provider training; account approval must cover it. Preserve current Gemini confirmation, but do not infer new-provider permission from it. Groq stays disabled until its own verification. No paid smoke fallback.

Cloud quota/terms reviewed at setup and on provider/model/tier change. No automatic daily confirmation expiry is introduced. Unknown/no-billing state cannot be guaranteed by setting price=0; strict deployments leave cloud disabled. Do not rotate keys/accounts to evade restrictions.

## Migration and testing order

Before enabling v2, verify source versus actual database revision. Planning source had 0014; implementation adds 0015, while normal remains 0012. Test the additive migration in isolated DB first, then prepare preservation-backed forward rollout. Do not run `alembic upgrade head` on the normal stack merely to read this guide. Existing migration scripts are not idempotent data-backup replacements. Normal recovery is forward-only.

Use C1/C4 immediately; C2/C3 after isolated implementation setup; C5 for synthetic local qualification; C6 only with exact free-provider authorization. Commands and guards in [test plan](SPRINT_11_1_TEST_PLAN.md). Keep v2 disabled until runtime/schema/readiness match; a healthy container is not proof it runs checkout HEAD.

## Troubleshooting

| Symptom | Inspect / safe action |
| --- | --- |
| Ollama running, model absent | tags/show and configured digest; MODEL_NOT_INSTALLED. Operator explicitly installs correct model; backend never downloads. |
| Timeout/OOM/paging | host RAM plus Docker/API/browser usage; one model/slot; smaller qualified model or smaller scope; do not raise context/output automatically. |
| Docker cannot reach Ollama | verify endpoint from worker and firewall; do not expose keys/listener to browser or public LAN. |
| Cloud 401/403 | credential binding disabled; privately verify key/project/model; reauthorize before resume/new run. Never log key. |
| 429/quota | read safe scope cooldown; local fallback if eligible; wait until true reset, no second-key bypass. |
| No eligible provider | diagnostic lists safe exclusion codes; deterministic/keyword fallback; no paid switch. |
| Source unavailable | reselect current permitted version, new run; do not revive tombstones or relax RLS. |
| Partial assessment or role interpretation | review baseline versus semantic covered/deferred IDs; explicit narrow run, original scores/metrics unchanged. A successful template is not completed requested AI reasoning. |
| Worker restarted | inspect committed sections/unknown attempts; allow recovery within deadline; new run for terminal gaps, not counter reset. |
| Schema readiness failure | compare expected revision and actual deployed code; preserve normal data, prepare forward correction. |
