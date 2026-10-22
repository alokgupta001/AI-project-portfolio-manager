# Testing and local benchmark plan

## Fresh baseline versus future gates

17 October 2026, existing code: **148 passed, 1 skipped, 108 deselected**, one existing Starlette/httpx deprecation warning; focused existing AI/contracts/Gemini: **85 passed, 13 deselected**. These sets overlap. They ran outside the sandbox after sandbox runs stalled with errors; see [verification](../../verification/sprint11_1/README.md). No application source was changed. New tests below are specifications, not existing/passing tests. Historical 257 backend/18 browser results are not reclassified as fresh.

## Command groups

Run from repository root. PowerShell shown. Separate commands are intentional; inspect each exit status. Capture redacted output under `docs/verification/sprint11_1/` with unique filenames.

**C1 — offline tests, immediately runnable**

```powershell
.venv/Scripts/python.exe -m pytest -q -m "not integration and not worker" --basetemp=artifacts/sprint11_1-offline-UNIQUE
.venv/Scripts/python.exe -m pytest -q tests/test_agents.py tests/test_ai_contracts.py tests/test_gemini.py -m "not integration and not worker" --basetemp=artifacts/sprint11_1-ai-UNIQUE
```

Choose a new empty task-owned basetemp each execution; pytest may delete its basetemp. Do not point it at general artifacts, existing backups or user data. Sandbox filesystem errors must be recorded, not “fixed” by weakening app policy. Existing Gemini fixtures intercept HTTP; new tests must deny all external calls by default.

**C2 — future isolated DB/worker integration**

```powershell
docker compose -f compose.yaml -f compose.documents.yaml --profile test build test
docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps test python scripts/test_backend.py
docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps test python scripts/check_agent_migration.py
```

Read scripts first. Runner verifies PPM_APP_ENV=test and database name ppm_test, then performs destructive migration lifecycle in that disposable database. Confirm actual DB role/host/project and no real objects; add a distinct isolated Compose project/ports if current ppm_test is in use. Test env overrides provider disabled and key empty, but inspect optional secret env-file precedence without printing secrets. Do not run these commands against normal/demo DB or during planning-only no-destructive-data scope. New storage tests must cover base→head, 0012→head and 0014→head, repeated upgrade, drift and controlled disposable downgrade.

**C3 — future isolated browser regression**

```powershell
node scripts/check-identity-browser.mjs agents.spec.ts ai.spec.ts documents.spec.ts assessment.spec.ts
node scripts/check-identity-browser.mjs --workers=2
```

Existing runner uses separate fixtures/ports/provider-disabled stack. Inspect current runner before use. Capture fresh screenshots privately; do not overwrite historical review screenshots. Synthetic deterministic fixtures are not live model quality evidence.

**C4 — static, contracts and documentation**

```powershell
npm run contracts:generate
npm run contracts:check
npm run typecheck
npm run lint
npm run format:check
.venv/Scripts/ruff.exe check services scripts tests
.venv/Scripts/ruff.exe format --check services scripts tests
.venv/Scripts/mypy.exe services/api/ppm_api services/worker/ppm_worker
.venv/Scripts/python.exe scripts/check_sources.py
.venv/Scripts/python.exe scripts/documentation_inventory.py --check
.venv/Scripts/python.exe scripts/check_documentation.py
.venv/Scripts/python.exe scripts/check_previous_sprint_docs.py
```

Generate contracts only after public schema changes; planning uses check only. Dependency security audit is required if T04 changes dependency placement/version. Do not change lock versions merely to resolve unrelated warning.

**C5 — implemented local benchmark, dry-run by default**

```powershell
.venv/Scripts/python.exe scripts/benchmark_agent_runtime.py --mode local-only --model qwen3:4b --cases tests/fixtures/agent_v2_quality.json --context 4096 --max-output 512 --concurrency 1 --max-calls 30 --output docs/verification/sprint11_1/benchmarks/qwen4-run1.json
```

Harness must require installed digest/profile, synthetic cases, global limits, bounded repeats and explicit output path. Repeat separate commands for 1.7B/Gemma comparator, never load models concurrently. At most 30 calls/invocation; split evaluation corpus into explicit bounded sessions with record of all cases. Benchmark mode still applies per-run attempt/time limits and may not disguise inference failures.

Implementation checkpoint: the command above prepares its selected group without
inference. `--execute` explicitly requests actual local measurement; `--case-id` chooses
remaining cases, and `--warm-repeats` reserves up to five timing-only repetitions inside
the same explicit call budget. See the [actual workflow and limitations](../../03-sprints/active/sprint-11.1/BENCHMARK.md).
All 108 cases are present with draft labels and six held-out cases per class.
Independent label approval and actual measurements are still absent; dry runs cannot
qualify a model. Local testing remains user-deferred.

**C6 — optional real free-provider qualification, disabled by default**

Proposed same harness with `--mode authorized-free --profile <reviewed-id> --max-calls 3 --max-spend-usd 0 --authorization-record <private-metadata-path>`. Refuse execution unless exact provider/model/account policy/egress authorization is recorded. Do not add a paid smoke mode to CI. Do not invoke current smoke scripts as proof of new domain quality; they exercise a different extractive contract.

Disposition: this optional generalized cloud qualification mode remains unimplemented
and is rejected by the local runner. Existing Groq transport/control checks and the
production Groq/OpenRouter/Mistral seams do not establish broad quality. Their original
three diagnostic admissions remain retained; no ledger reset or additional live call
was used to close the implementation work. Optional embeddings and Puter's native
free driver remain disabled, as T13 permits.

## Acceptance matrix (future tests)

| ID | Expected positive/negative behavior | Level / owner |
| --- | --- | --- |
| AT01 | All nine hybrid role contracts: baseline plus optional qualified interpretation; supported/missing/contradictory/malicious and no-model cases per role. Metrics-only mode makes zero calls. Previously excluded roles can perform cited interpretation without changing canonical numbers or privacy. | Unit + domain DB, T02/T09 |
| AT02 | Stable acyclic goal-aware plan; ≤24 nodes/≤3 initial sections from any eligible role, ordered explicit priority in fingerprint. Executive-only reserves its synthesis call; financial/schedule/resource can receive all three; metrics mode zero calls; nine-role semantics exceeding budget deferred visibly. Unknown agent/tool/cycle denied. | Unit, T07 |
| AT03 | Eligibility before ranking for all nine task classes; absent auth/egress/capability/quality/policy rejects regardless of preference. No permanent role exclusion; synthesis requires its own qualification. Model switch independent of domain code. | Unit/router DB, T06 |
| AT04 | Every adapter: complete/length/unknown/refused, malformed JSON, 401/403/429/5xx, missing usage, context error, timeout, disconnect, redirect, tool/thought payload. Correct normalized outcome; no secret leak. | Intercepted contract, T04/T05/T13 |
| AT05 | Missing spend limit/tier/enabled flag denies network; paid provider never selected; same quota scope shared by keys/tenants; concurrent admission cannot exceed cap; unknown usage retains reservation. | Unit + concurrent DB, T03/T06 |
| AT06 | Valid state transitions only; duplicate messages finalize once; task/section uniqueness; DB truth recovers after lost Redis message; tenant/task/reference mismatch denied. | DB + worker, T03/T08 |
| AT07 | Crash at each boundary retains accepted sections and original attempts; unknown cloud result not resent; stale token cannot publish; deadline/call/root counters never reset. | Failure injection, T08/T10 |
| AT08 | Cancel queued/waiting/in-flight/validating; revoke session/membership/project while running; no late publication or new calls; usage retained, unused slots released safely. | DB + fake slow HTTP, T08 |
| AT09 | Cross-tenant/project/policy/private assessment access denied; scope cannot grow through dependencies; group sizes 4/5; source tombstone/edit and Unicode span offsets; raw notes absent. | Security unit/DB/browser, T07/T11 |
| AT10 | Canonical Decimal numbers/currency/periods, rubric exact level/question support and score separation. AI explanation cannot recalculate or overwrite metric values. Synthesis basis aliases and original spans must resolve to permitted accepted items; unsupported numbers/failed basis/duplicate matches rejected. | Unit + assessment DB, T09 |
| AT11 | Truncation, malformed JSON, missing mandatory section, context overflow, oversized document, repeated/failed continuation and exhausted model all terminate within limits; no partial-JSON concatenation. | Unit + runtime DB, T10 |
| AT12 | Same-source distinct issues/conflicts preserved; seven successful/two failed stays partial; no missing numeric=zero. Successful roll-up/briefing baseline plus deferred requested AI remains partial. Python appends mandatory conflict/gap disclosures even when PMO/Executive model omits them. | Unit + browser, T09/T11 |
| AT13 | Irrelevant-but-real quote, same-model agreement, missing facts and unsupported causal claim do not pass as verified; evaluator can abstain and cannot mutate/approve; no slot means no critique. | Unit + human-scored local cases, T10/T12 |
| AT14 | Safe stage/route/latency/coverage/usage diagnostics, null unknown usage, no raw key/prompt/source/exception/reasoning; inaccessible run cannot leak through SSE/task list. | API/security/browser, T08/T11 |
| AT15 | Missing local model/OOM/CPU timeout/private endpoint refusal correct; no auto pull/cloud call; one generation globally across tenants; only one model active; memory stop. | Mock contract + real hardware, T05/T12 |
| AT16 | Legacy replay/status/reviews unchanged; v2 role selection/analysis modes show baseline versus AI coverage. Deferred requested financial/synthesis work cannot show completed AI. Clients, keyboard/mobile/themes, revocation and partial UI match contracts. | Regression + browser, T11/T14 |
| AT17 | Candidate local profile meets measured latency/memory/control/quality rubric per task class; failed qualification remains disabled/benchmark_only; results distinguish model inference from deterministic fallback. | Benchmark, T12 |
| AT18 | Embedding count/dimension/nonfinite/zero/model-version mismatch rejected; no cross-model cosine; reindex explicit; keyword fallback on unavailable embedding. Groq mock capability and shared organization quota verified. | Optional unit/DB/local, T13 |
| AT19 | No applied migration/source/history/object changes from planning; future forward migration preserves prior rows and hashes, review immutability and authorization; rollout flag rollback retains data. | Preservation/integration, T01/T14 |
| AT20 | All requirement/task/test links resolve, all implementation statuses evidenced, no proposed module claimed existing, handover identifies next task and conflicts. | Documentation/manual audit, T14 |

## Benchmark protocol and thresholds

Do not infer runtime memory from model download size. Record Windows version, physical/available RAM, CPU, GPU/processor use from Ollama, Docker resource cap, active services, Ollama version and installed model digest/quantization. Baseline app idle and app under normal browser/API activity. Use fresh synthetic tenant/data only; no real company or personnel data.

Models: Qwen3 4B Q4_K_M first; Qwen3 1.7B smaller comparator; Gemma3 4B comparator with license/extra modality overhead recorded. Context profiles 2048 and 4096; 8192 is measurement-only exploratory and cannot become default without approved design change. Output targets 256 and 512, thinking disabled where supported. One cold request after unload and at least five warm repeats of each representative extraction/rubric/advice task; explicit request groups ≤30. Capture time-to-first-byte if transport exposes it, total/loading/generation duration, prompt/eval tokens, tokens/s, process RSS, host available RAM, timeout/OOM, schema validity, accepted findings, deferred scope and case-level support.

Proposed admission memory rule: reserve at least 2 GB host headroom plus measured model peak (with 25% safety margin); until measured, require 6 GB available for 4B and 4 GB for smaller candidate. These are conservative policy starting points, not facts about models. Observe total host RAM, not just container cgroup. If a trustworthy host measurement cannot be read, automatic 4B admission is blocked until an operator-defined tested memory envelope exists. Stop benchmark if available RAM <2 GB or sustained paging affects app responsiveness. No guaranteed GPU acceleration.

Operational qualification: zero OOM and no concurrent local generations; all hard safety/control invariants pass; p95 warm attempt ≤20 s to leave margin inside 22 s timeout, complete required small fixture within 90 s run deadline. Cold start must either fit the same timeout or report bounded unavailable; cannot hide cold failure by only reporting warm throughput. Host minimum headroom 2 GB. These are chosen usability/resource gates, not measured claims. Larger/slower profiles remain experimental. A small domain fixture can still qualify useful partial analysis; do not claim large-assessment completion.

Semantic corpus: at least 108 independently labeled cases (12 for each of the nine interpretation task classes), including supported, absent, conflicting and injection cases; additionally each of nine roles' four baseline/control cases. Keep at least six cases/class held out from prompt tuning. Financial/schedule/resource cases must test explanations grounded in narrative plus canonical numbers; team-support advice must reject emotional/individual claims; PMO/Executive cases must test basis references, cross-domain synthesis and mandatory uncertainty/conflict disclosure. Label expected evidence support, conditional advice relevance, abstention, rubric levels and material omissions. Human reviewer scores without model identity when practical. A model can qualify a subset of classes, but extraction performance cannot establish synthesis quality and no universal nine-role claim is allowed without all nine classes evaluated.

Promotion per activated class requires zero access leak/unsupported numerical claim, 100% citation identity validity, ≥90% precision among emitted semantic claims and ≥80% recall on eligible supported fixture items, with separate abstention/missing-evidence accuracy ≥90%. These are provisional engineering gates for this small test corpus, not calibrated real-world accuracy or model confidence. Always publish counts/denominators, advice-relevance decisions and failures; tiny denominators or empty emissions cannot pass precision alone. Compare the hybrid output against its deterministic baseline on the same cases: preserve 100% of canonical numeric results and mandatory warnings, and show at least one correctly supported non-template interpretation per class. This minimum demonstrates some added reasoning; it does not establish broad superiority. Keep future source requirements such as broader predictive accuracy unchanged. Run the corpus in explicit bounded sessions under C5's call caps; do not auto-spawn runs to evade user limits.

Latency, memory, throughput, retrieval quality and semantic quality remain **unmeasured** until this protocol runs. A mock proves policy logic only. If no model qualifies, deliver deterministic/keyword local mode and explicit unavailable semantic capabilities, record model-quality blocker, and revisit model/context/timeout via decision log rather than quietly lowering gates.
