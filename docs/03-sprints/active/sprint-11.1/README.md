# Sprint 11.1 implementation

**23 October review closeout:** PR #4 is merged after both hosted CI runs passed.
The follow-up fixes four remaining verified CodeRabbit findings: stable local
attempt roots, cancellation propagation after settlement, bounded context binding,
and heartbeat cleanup that preserves the run outcome. Function contracts now cover
all 186 production Python functions in the original sprint diff, excluding applied
migrations. The user asked us to arrange the independent review; a separate AI
label audit is being requested. Labels and model accuracy remain unapproved.
See the [closeout evidence](../../../verification/sprint11_1/review-closeout/README.md).
Earlier checkpoints below retain their original review and verification status.

**Current repair:** [four-call/nine-role batching](../../../verification/sprint11_1/CLOUD_BATCH_REPAIR.md)
adds the explicit all-specialists UI goal and separate cloud acceptance tooling.
Measured fit changes the candidate assignment to Gemini delivery, Puter assurance,
Groq synthesis. Eighteen additional repair requests retain three Groq failures and
42 hard-valid role results. Fresh 108 draft cases/54 held out prepare offline.
The user will nominate the [independent reviewer](../../../verification/sprint11_1/REVIEWER_GUIDE.md).
Acceptance and normal activation remain blocked; no weight-training claim. Earlier
counts and allocation below are historical.

**Current: cloud specialist follow-up.** Ollama is stopped at the user's request.
[Three providers/nine roles](CLOUD_SPECIALISTS.md) and
[live calibration results](../../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md)
record 26 synthetic requests, a supported hard-validated result for each role, and
seven/nine absence cases passing (financial/resource rejected). Implemented native
Puter transport and example-based prompts; 36 original draft training examples,
no weight training. Final 198 offline/101 DB-provider/37 prompt-fence checks pass
(overlap); full-suite failures/corrections and preservation exception are recorded
in the handoff. All profiles remain disabled/unqualified; AT17 remains BLOCKED.
Earlier sections below describe their recorded historical checkpoints.

The subsequent user-approved [small Ollama trial](OLLAMA_SMALL.md) succeeded for
experimental native chat: Qwen3 0.6B/`ppm-small` is installed with 2K context/512-output
defaults and immediate-unload launcher. Four local requests ran alongside the project;
two basic controls passed and two project-format attempts failed strict validation.
The small model remains unqualified for project roles. Its measured reservation is
1.5 GiB plus the unchanged 2 GiB headroom. Earlier local-testing deferrals below are
superseded for this specific completed trial; no model activation is implied.

Current hardware decision: the user cannot make sufficient free RAM available on
this laptop. Ollama inference remains optional and unavailable on this device;
future work should continue the existing free-cloud qualification path instead of
repeatedly requesting RAM cleanup. Installed files and memory gates are unchanged.
All model profiles remain disabled/unqualified, and no additional live call occurred.

The user subsequently requested the whole documented sprint. The remaining T12
benchmark implementation now exists: a 108-case synthetic corpus, bounded local
runner, persistent attempt/unknown-state ledger, sampled memory/timing telemetry and
fingerprint-bound independent review/scoring. See [benchmark workflow](BENCHMARK.md).
All cases were prepared offline in four explicit groups; 45 new focused tests pass.
Labels remain draft and local inference remains deferred. This finishes the missing
benchmark code, not the outstanding independent/model-quality acceptance gate.

Current regression evidence: full lifecycle/drift passed; 422 backend tests passed
and six missing-template fixture errors were fixed and passed in a rebuilt 58-test
scope. The final corpus/qualification scope passes 51 tests. Full browser: 18 passed,
with the separate hybrid journey also passing. Counts overlap. Fresh preservation
confirms normal 0012, 70 table hashes/counts, five original objects and 24 frozen files
unchanged. See the [exact receipts](../../../verification/sprint11_1/IMPLEMENTATION.md).

The user authorized implementation after the [architecture revision](../../../09-planning/sprint-11.1/README.md), then provider/local setup and cloud-only continuation. Source baseline is `d0ebe32e691a3d63166ced669450911c63151127`. Work is uncommitted. Normal remains `0012_ai_runtime`; new 0015 is tested only in disposable databases. V2 defaults off. Ollama/Qwen are installed. Three fixed synthetic Groq requests used the confirmed free account; no normal activation or paid fallback occurred.

Current [cloud provider status](CLOUD_PROVIDER_STATUS.md): Groq/Puter/DeepInfra credentials authenticate; DeepInfra is suspended for balance and Puter's native free path is unverified. All three live Groq checks stopped on configuration/hard-gate failures. Identity/schema corrections passed 110 offline tests; no live retest/quality promotion is claimed. OpenRouter/Mistral remain absent, and local testing is deferred by the user.

## Implemented behavior

All nine existing role IDs have an optional, qualified interpretation path. Python keeps existing calculations, scoring, privacy, access checks and execution control. Goal-aware planning reserves requested PMO/Executive synthesis and admits at most three initial semantic sections; repair or optional critique shares the fourth attempt. The hard 512-output-token, two-attempt-per-section, four-attempt-per-run, 90-second and 24-task bounds remain.

New task/section checkpoints preserve accepted work and permit validation of a saved candidate after worker loss. Unknown external outcomes are not replayed. PostgreSQL serializes provider-scope quota admission; all local profiles share one generation slot. Unknown local work blocks new generation until an operator verifies it stopped. Tenant application roles cannot read or modify global quota tables.

Private operator profiles filter tenant/project scope, task-class qualification, egress, exact installed model digest, memory, output/context capability and zero-spend authorization before stable ranking. Ollama, the existing Gemini binding and user-selected Groq/OpenRouter/Mistral use bounded asynchronous transports without app retries. OpenRouter additionally pins one reviewed free model/upstream with zero-price/data controls. Missing profiles preserve useful baselines and report requested AI work as unavailable/deferred. Metrics-only runs admit no model calls.

Strict mode-specific outputs use aliases and exact original spans. Numerical prose requires an exact cited numerical statement; canonical calculations remain separate. Distinct claims survive reconciliation. Optional critique can withhold unsupported claims and transitive summaries; agreement remains model review only. Synthesis receives missing-interpretation scope and Python adds mandatory gap/conflict disclosures.

The Agents page adds goal/role controls and separate baseline/AI coverage, deferred scope, nullable unknown confidence and safe attempt/usage diagnostics. Existing independent append-only human review and original/suggested/approved score separation remain.

## Current verification and remaining gates

The [tracker](../../../09-planning/sprint-11.1/SPRINT_11_1_TASK_TRACKER.md) records individual task status. [Verification](../../../verification/sprint11_1/IMPLEMENTATION.md) distinguishes final and intermediate receipts: 314 full-suite checkpoint tests plus lifecycle/drift passed; the core checkpoint passed 52 focused unit and 13 v2 DB tests before the provider follow-up below. Counts overlap. Hybrid and legacy specialist browser journeys, static/contracts/source inventory checks and the zero-vulnerability audit passed at that checkpoint. Normal DB/object/frozen-file hashes matched the private baseline. [Acceptance disposition](TESTING_REPORT.md) records remaining external gates; [user steps](USER_GUIDE.md) explain the new controls.

The [setup follow-up](PROVIDER_SETUP.md) adds 103 focused offline passes and 16 isolated DB passes, including the three new providers' shared admission/quota exhaustion. Ollama 0.40.5/Qwen3 4B Q4_K_M digest and private Docker reachability are recorded. Last measured available host RAM was 1261 MiB, below the 6144 MiB 4B gate; this completion pass does not remeasure or load the model. Groq/Puter/DeepInfra keys are already saved and authenticated. Independent label review and measured inference latency/quality remain pending. No model is qualified. The completed runner/scorer is documented above; profiles remain disabled/benchmark-only. Local embeddings stay deferred; keyword retrieval remains available. Normal forward rollout, real-model activation and Sprint 12 have not occurred.

See [handoff](HANDOFF.md) for resumption and [operator setup](../../../09-planning/sprint-11.1/SPRINT_11_1_SETUP.md) for private configuration.
