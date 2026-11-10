# Current code and test navigation

Source-derived AST inventory. Search symbols instead of relying on line numbers; a test definition is not an executed result. Run `python scripts/documentation_inventory.py --check` for drift. Actual results: [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md) and [Gemini follow-up](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).

## scripts/account_status.py

[Source](../../scripts/account_status.py)

- `set_status` — line 19
- `run` — line 66

## scripts/benchmark_agent_runtime.py

[Source](../../scripts/benchmark_agent_runtime.py)

- `load_corpus` — line 48
- `fixture_context` — line 71
- `ollama_process_ids` — line 134
- `ollama_rss_mb` — line 148
- `ProcessEntry` — line 154
- `Counters` — line 168
- `write_new` — line 232
- `save_ledger` — line 239
- `run` — line 246
- `monitor` — line 397
- `main` — line 504

## scripts/benchmark_cloud_batches.py

[Source](../../scripts/benchmark_cloud_batches.py)

- `strategy_hash` — line 58
- `fixture_batch` — line 78
- `prepare_phase` — line 107
- `run` — line 139
- `checkpoint` — line 335
- `main` — line 406

## scripts/benchmark_cloud_specialists.py

[Source](../../scripts/benchmark_cloud_specialists.py)

- `legacy_gemini_calls` — line 50
- `retained_history` — line 80
- `check_admission` — line 105
- `run` — line 145
- `checkpoint` — line 329
- `main` — line 404

## scripts/bootstrap_identity.py

[Source](../../scripts/bootstrap_identity.py)

- `run` — line 16

## scripts/browser_agent_fixture.py

[Source](../../scripts/browser_agent_fixture.py)

- `run` — line 29
- `no_network` — line 54

## scripts/browser_identity_fixture.py

[Source](../../scripts/browser_identity_fixture.py)

- `run` — line 16

## scripts/browser_pilot_fixture.py

[Source](../../scripts/browser_pilot_fixture.py)

- `run` — line 17
- `delivery` — line 72

## scripts/check_documentation.py

[Source](../../scripts/check_documentation.py)

- `without_fences` — line 12
- `anchors` — line 16
- `main` — line 28

## scripts/check_local_model.py

[Source](../../scripts/check_local_model.py)

- `main` — line 13

## scripts/check_model_qualification.py

[Source](../../scripts/check_model_qualification.py)

- `main` — line 16

## scripts/check_previous_sprint_docs.py

[Source](../../scripts/check_previous_sprint_docs.py)

- `main` — line 8

## scripts/check_provider_setup.py

[Source](../../scripts/check_provider_setup.py)

- `read_keys` — line 22
- `inspect` — line 47
- `main` — line 171

## scripts/check_sprint12_preservation.py

[Source](../../scripts/check_sprint12_preservation.py)

- `verify` — line 12

## scripts/check_walkthrough.py

[Source](../../scripts/check_walkthrough.py)

- `run` — line 19

## scripts/configure_gemini_free_tier.py

[Source](../../scripts/configure_gemini_free_tier.py)

- `main` — line 14

## scripts/documentation_inventory.py

[Source](../../scripts/documentation_inventory.py)

- `cell` — line 19
- `inventories` — line 23
- `main` — line 205

## scripts/fill_current_portal.py

[Source](../../scripts/fill_current_portal.py)

- `run` — line 48
- `add` — line 163
- `child` — line 181

## scripts/prepare_agent_training.py

[Source](../../scripts/prepare_agent_training.py)

- `examples` — line 22
- `main` — line 69

## scripts/prepare_cloud_acceptance.py

[Source](../../scripts/prepare_cloud_acceptance.py)

- `draft` — line 97
- `approval` — line 273
- `prepare_authorization` — line 294

## scripts/prepare_cloud_review.py

[Source](../../scripts/prepare_cloud_review.py)

- `prepare` — line 23

## scripts/prepare_cloud_specialists.py

[Source](../../scripts/prepare_cloud_specialists.py)

- `gemini_settings` — line 20
- `prepare` — line 32

## scripts/repair_hement_access.py

[Source](../../scripts/repair_hement_access.py)

- `run` — line 20

## scripts/repair_preserve.py

[Source](../../scripts/repair_preserve.py)

- `sql` — line 17

## scripts/score_agent_benchmark.py

[Source](../../scripts/score_agent_benchmark.py)

- `sha` — line 30
- `review_template` — line 35
- `score` — line 69
- `total` — line 174
- `main` — line 230

## scripts/score_cloud_benchmark.py

[Source](../../scripts/score_cloud_benchmark.py)

- `score` — line 33

## scripts/seed_delivery_demo.py

[Source](../../scripts/seed_delivery_demo.py)

- `id_for` — line 22
- `run` — line 26
- `add` — line 93

## scripts/seed_walkthrough.py

[Source](../../scripts/seed_walkthrough.py)

- `ident` — line 24
- `run` — line 28
- `command` — line 156
- `add` — line 171

## scripts/setup_guided_demo.py

[Source](../../scripts/setup_guided_demo.py)

- `ident` — line 22
- `run` — line 27
- `add` — line 82

## scripts/smoke_gemini_free_tier.py

[Source](../../scripts/smoke_gemini_free_tier.py)

- `main` — line 17

## scripts/smoke_groq_provider.py

[Source](../../scripts/smoke_groq_provider.py)

- `fixture_context` — line 58
- `authorize` — line 79
- `run` — line 122
- `safe_error_hint` — line 194
- `main` — line 366

## scripts/smoke_guided_demo.py

[Source](../../scripts/smoke_guided_demo.py)

- `run` — line 14
- `post` — line 27

## scripts/sprint08_preserve.py

[Source](../../scripts/sprint08_preserve.py)

- `sql` — line 15

## scripts/sprint09_checkpoint.py

[Source](../../scripts/sprint09_checkpoint.py)

- `output` — line 13

## scripts/sprint09_document_recovery_run.py

[Source](../../scripts/sprint09_document_recovery_run.py)

- `sql` — line 27
- `hashes` — line 34

## scripts/sprint09_document_restore.py

[Source](../../scripts/sprint09_document_restore.py)

- `run` — line 23
- `send` — line 90

## scripts/sprint09_preserve.py

[Source](../../scripts/sprint09_preserve.py)

- `sql` — line 21

## scripts/sprint09_recovery.py

[Source](../../scripts/sprint09_recovery.py)

- `sql` — line 16
- `manifest` — line 35

## scripts/sprint10_checkpoint.py

[Source](../../scripts/sprint10_checkpoint.py)

- `output` — line 13

## scripts/sprint10_preserve.py

[Source](../../scripts/sprint10_preserve.py)

- `sha` — line 14
- `files` — line 18
- `check` — line 61
- `database` — line 69
- `sql` — line 78
- `objects` — line 154
- `hashes` — line 181

## scripts/sprint10_runtime.py

[Source](../../scripts/sprint10_runtime.py)

- `get` — line 11

## scripts/sprint11_preserve.py

[Source](../../scripts/sprint11_preserve.py)

- `sha` — line 14
- `files` — line 18
- `check` — line 61
- `database` — line 69
- `sql` — line 78
- `objects` — line 157
- `hashes` — line 184

## scripts/sprint81_preserve.py

[Source](../../scripts/sprint81_preserve.py)

- `sql` — line 15

## scripts/sprint81_restore.py

[Source](../../scripts/sprint81_restore.py)

- `sql` — line 15

## scripts/sync_model_policy.py

[Source](../../scripts/sync_model_policy.py)

- `scope_rows` — line 15
- `sync` — line 45
- `main` — line 77

## scripts/verify_gemini_runtime.py

[Source](../../scripts/verify_gemini_runtime.py)

- `get` — line 12
- `main` — line 18

## services/api/migrations/env.py

[Source](../../services/api/migrations/env.py)

- `run_sync` — line 12
- `run_async` — line 18

## services/api/migrations/versions/0001_foundation.py

[Source](../../services/api/migrations/versions/0001_foundation.py)

- `upgrade` — line 15
- `downgrade` — line 27

## services/api/migrations/versions/0002_identity.py

[Source](../../services/api/migrations/versions/0002_identity.py)

- `upgrade` — line 92
- `downgrade` — line 135

## services/api/migrations/versions/0003_delivery.py

[Source](../../services/api/migrations/versions/0003_delivery.py)

- `col` — line 20
- `ref` — line 24
- `table` — line 34
- `owner` — line 57
- `project` — line 66
- `upgrade` — line 306
- `granted` — line 314
- `visible` — line 317
- `editable` — line 320
- `downgrade` — line 384

## services/api/migrations/versions/0004_capacity.py

[Source](../../services/api/migrations/versions/0004_capacity.py)

- `col` — line 20
- `ref` — line 24
- `table` — line 34
- `owner` — line 57
- `project` — line 66
- `resource` — line 322
- `period` — line 326
- `capability` — line 414
- `visible` — line 418
- `editable` — line 422
- `audit_policy` — line 426
- `upgrade` — line 439
- `downgrade` — line 490

## services/api/migrations/versions/0005_assessment.py

[Source](../../services/api/migrations/versions/0005_assessment.py)

- `ref` — line 26
- `member` — line 32
- `tab` — line 38
- `revision_column` — line 52
- `scope` — line 159
- `upgrade` — line 168
- `downgrade` — line 227

## services/api/migrations/versions/0006_command_center.py

[Source](../../services/api/migrations/versions/0006_command_center.py)

- `col` — line 17
- `ref` — line 21
- `table` — line 31
- `owner` — line 54
- `project` — line 63
- `upgrade` — line 149
- `downgrade` — line 187

## services/api/migrations/versions/0007_durable_jobs.py

[Source](../../services/api/migrations/versions/0007_durable_jobs.py)

- `tenant_table` — line 15
- `upgrade` — line 147
- `downgrade` — line 242

## services/api/migrations/versions/0008_pilot_completion.py

[Source](../../services/api/migrations/versions/0008_pilot_completion.py)

- `upgrade` — line 26
- `downgrade` — line 111

## services/api/migrations/versions/0009_account_repair.py

[Source](../../services/api/migrations/versions/0009_account_repair.py)

- `upgrade` — line 12
- `downgrade` — line 21

## services/api/migrations/versions/0010_account_authority.py

[Source](../../services/api/migrations/versions/0010_account_authority.py)

- `install` — line 11
- `upgrade` — line 53
- `downgrade` — line 57

## services/api/migrations/versions/0011_document_sources.py

[Source](../../services/api/migrations/versions/0011_document_sources.py)

- `tab` — line 15
- `upgrade` — line 109
- `downgrade` — line 286

## services/api/migrations/versions/0012_ai_runtime.py

[Source](../../services/api/migrations/versions/0012_ai_runtime.py)

- `tab` — line 15
- `upgrade` — line 108
- `downgrade` — line 232

## services/api/migrations/versions/0013_specialist_reviews.py

[Source](../../services/api/migrations/versions/0013_specialist_reviews.py)

- `tab` — line 15
- `upgrade` — line 84
- `downgrade` — line 139

## services/api/migrations/versions/0014_specialist_reviewer.py

[Source](../../services/api/migrations/versions/0014_specialist_reviewer.py)

- `upgrade` — line 23
- `downgrade` — line 27

## services/api/migrations/versions/0015_agent_task_runtime.py

[Source](../../services/api/migrations/versions/0015_agent_task_runtime.py)

- `upgrade` — line 49
- `downgrade` — line 214

## services/api/migrations/versions/0016_guided_project_access.py

[Source](../../services/api/migrations/versions/0016_guided_project_access.py)

- `worker_authority` — line 19
- `policies` — line 37
- `upgrade` — line 76
- `downgrade` — line 122

## services/api/migrations/versions/0017_local_ml_foundations.py

[Source](../../services/api/migrations/versions/0017_local_ml_foundations.py)

- `tenant_table` — line 15
- `project_table` — line 70
- `upgrade` — line 127
- `downgrade` — line 311

## services/api/migrations/versions/0018_csv_source_namespaces.py

[Source](../../services/api/migrations/versions/0018_csv_source_namespaces.py)

- `upgrade` — line 12
- `downgrade` — line 31

## services/api/migrations/versions/0019_selection_pilot.py

[Source](../../services/api/migrations/versions/0019_selection_pilot.py)

- `upgrade` — line 11
- `downgrade` — line 33

## services/api/migrations/versions/0020_guided_cloud_timeout.py

[Source](../../services/api/migrations/versions/0020_guided_cloud_timeout.py)

- `change` — line 26
- `upgrade` — line 45
- `downgrade` — line 50

## services/api/ppm_api/config.py

[Source](../../services/api/ppm_api/config.py)

- `Settings` — line 22
- `validate_mail` — line 82
- `validate_key` — line 106
- `validate_origin` — line 114
- `validate_database` — line 129
- `validate_redis` — line 141
- `load_settings` — line 151

## services/api/ppm_api/database.py

[Source](../../services/api/ppm_api/database.py)

- `Base` — line 11
- `FoundationState` — line 15
- `make_engine` — line 25

## services/api/ppm_api/errors.py

[Source](../../services/api/ppm_api/errors.py)

- `DomainError` — line 6

## services/api/ppm_api/main.py

[Source](../../services/api/ppm_api/main.py)

- `error_response` — line 57
- `create_app` — line 69
- `lifespan` — line 73
- `request_context` — line 105
- `http_error` — line 167
- `validation_error` — line 203
- `live` — line 217
- `ready` — line 227
- `database_probe` — line 230
- `redis_probe` — line 240
- `storage_probe` — line 244
- `probe` — line 249
- `foundation` — line 274

## services/api/ppm_api/modules/agents/batch.py

[Source](../../services/api/ppm_api/modules/agents/batch.py)

- `batch_prompt` — line 12
- `strings` — line 32
- `obj` — line 42
- `compact_payload` — line 49
- `compact_schema` — line 73
- `pack_batch` — line 143
- `normalize` — line 189
- `validate_batch` — line 255

## services/api/ppm_api/modules/agents/context.py

[Source](../../services/api/ppm_api/modules/agents/context.py)

- `section_schema` — line 10
- `visit` — line 20
- `pack` — line 41

## services/api/ppm_api/modules/agents/critique.py

[Source](../../services/api/ppm_api/modules/agents/critique.py)

- `Decision` — line 20
- `Critique` — line 27
- `pack_review` — line 32
- `validate_review` — line 78

## services/api/ppm_api/modules/agents/engine.py

[Source](../../services/api/ppm_api/modules/agents/engine.py)

- `canonical` — line 62
- `definitions` — line 66
- `supported_spans` — line 79
- `aggregate` — line 89
- `deterministic` — line 135
- `semantic_suggestions` — line 172
- `evaluate` — line 236

## services/api/ppm_api/modules/agents/guided_review.py

[Source](../../services/api/ppm_api/modules/agents/guided_review.py)

- `prompt` — line 34
- `granted_projects` — line 43
- `Choice` — line 78
- `distinct` — line 82
- `Observation` — line 89
- `SelectionInput` — line 94
- `Card` — line 99
- `Checklist` — line 106
- `GuidedReview` — line 112
- `plan` — line 125
- `fact` — line 174
- `pack` — line 209
- `validate` — line 250
- `view` — line 264
- `check_request` — line 290

## services/api/ppm_api/modules/agents/planner.py

[Source](../../services/api/ppm_api/modules/agents/planner.py)

- `build_plan` — line 19
- `batch_plan` — line 185
- `base` — line 189
- `group` — line 203

## services/api/ppm_api/modules/agents/prompts.py

[Source](../../services/api/ppm_api/modules/agents/prompts.py)

- `cloud_prompt` — line 35

## services/api/ppm_api/modules/agents/provider.py

[Source](../../services/api/ppm_api/modules/agents/provider.py)

- `AgentProvider` — line 11
- `__init__` — line 12
- `embed` — line 16
- `complete` — line 19

## services/api/ppm_api/modules/agents/recovery.py

[Source](../../services/api/ppm_api/modules/agents/recovery.py)

- `recovery` — line 6

## services/api/ppm_api/modules/agents/registry.py

[Source](../../services/api/ppm_api/modules/agents/registry.py)

- `Capability` — line 9
- `definitions` — line 106

## services/api/ppm_api/modules/agents/router.py

[Source](../../services/api/ppm_api/modules/agents/router.py)

- `definitions` — line 21
- `create` — line 27
- `listing` — line 33
- `detail` — line 39
- `review` — line 45

## services/api/ppm_api/modules/agents/runtime.py

[Source](../../services/api/ppm_api/modules/agents/runtime.py)

- `initialize` — line 47
- `task_update` — line 97
- `commit_section` — line 118
- `baseline` — line 155
- `heartbeat` — line 190
- `batch_window_delay` — line 208
- `complete_task` — line 224
- `execute` — line 503
- `live_sections` — line 692
- `reviewed_findings` — line 734
- `assemble` — line 765

## services/api/ppm_api/modules/agents/schemas.py

[Source](../../services/api/ppm_api/modules/agents/schemas.py)

- `AnalysisInput` — line 43
- `Span` — line 49
- `Candidate` — line 55
- `SpecialistOutput` — line 63
- `RubricMatch` — line 69
- `AgentBatch` — line 76
- `AgentDefinition` — line 81
- `EvidenceView` — line 96
- `AgentState` — line 104
- `ReviewInput` — line 110
- `ReviewView` — line 116
- `FindingView` — line 124
- `SuggestionView` — line 145
- `AnalysisRunSummary` — line 161
- `AnalysisSummary` — line 167
- `AnalysisView` — line 172

## services/api/ppm_api/modules/agents/service.py

[Source](../../services/api/ppm_api/modules/agents/service.py)

- `internal_request` — line 41
- `private_access` — line 46
- `capture` — line 55
- `add` — line 68
- `get_analysis` — line 315
- `current_sources` — line 329
- `can_review` — line 361
- `definitions` — line 375
- `create` — line 393
- `listing` — line 399
- `detail` — line 429
- `item` — line 463
- `review` — line 596
- `execute` — line 663
- `publish` — line 707

## services/api/ppm_api/modules/agents/validation.py

[Source](../../services/api/ppm_api/modules/agents/validation.py)

- `numbers` — line 20
- `validate_section` — line 25
- `spans` — line 38
- `item` — line 48
- `reconcile` — line 205

## services/api/ppm_api/modules/ai/adapters.py

[Source](../../services/api/ppm_api/modules/ai/adapters.py)

- `strict_schema` — line 35
- `visit` — line 39
- `NativeAdapter` — line 64
- `__init__` — line 65
- `permit` — line 77
- `origin` — line 125
- `execute` — line 149
- `gemini_chat` — line 222
- `puter_chat` — line 249
- `puter_result` — line 304
- `read` — line 337
- `cloud_chat` — line 427
- `check_openrouter_price` — line 478
- `chat_result` — line 503
- `ollama_result` — line 577
- `gemini_result` — line 604

## services/api/ppm_api/modules/ai/contracts.py

[Source](../../services/api/ppm_api/modules/ai/contracts.py)

- `HybridSelection` — line 66
- `distinct_selection` — line 76
- `uses_v2` — line 114
- `CompactSpan` — line 119
- `nonempty` — line 125
- `SectionFinding` — line 132
- `SectionMatch` — line 144
- `NarrativeItem` — line 150
- `SectionGap` — line 160
- `SectionOutput` — line 165
- `consistent` — line 176
- `CapabilityDetail` — line 196
- `honest_coverage` — line 218
- `ModelUsage` — line 228
- `ModelResult` — line 235
- `ModelFailure` — line 272
- `__init__` — line 273
- `ExecutionPermit` — line 285
- `ModelRequest` — line 297
- `ModelAdapter` — line 312
- `execute` — line 313

## services/api/ppm_api/modules/ai/deadlines.py

[Source](../../services/api/ppm_api/modules/ai/deadlines.py)

- `ordinary_guided` — line 7
- `completion_timeout` — line 16

## services/api/ppm_api/modules/ai/evaluation.py

[Source](../../services/api/ppm_api/modules/ai/evaluation.py)

- `run_evaluation` — line 12

## services/api/ppm_api/modules/ai/model_router.py

[Source](../../services/api/ppm_api/modules/ai/model_router.py)

- `RouteRequirements` — line 17
- `eligibility` — line 27
- `candidates` — line 125

## services/api/ppm_api/modules/ai/provider.py

[Source](../../services/api/ppm_api/modules/ai/provider.py)

- `ProviderError` — line 35
- `__init__` — line 36
- `ProviderResult` — line 43
- `Provider` — line 49
- `complete` — line 52
- `embed` — line 53
- `enabled` — line 56
- `gemini_block_reason` — line 72
- `policy_snapshot` — line 108
- `vectors` — line 123
- `OpenAIProvider` — line 142
- `__init__` — line 145
- `post` — line 148
- `NoRedirect` — line 165
- `redirect_request` — line 166
- `complete` — line 190
- `embed` — line 217
- `DisabledProvider` — line 241
- `complete` — line 244
- `embed` — line 247
- `provider` — line 251
- `GeminiProvider` — line 259
- `__init__` — line 262
- `post` — line 265
- `NoRedirect` — line 289
- `redirect_request` — line 290
- `complete` — line 321
- `embed` — line 370

## services/api/ppm_api/modules/ai/qualification.py

[Source](../../services/api/ppm_api/modules/ai/qualification.py)

- `ClassMeasurement` — line 11
- `denominators` — line 29
- `qualifies` — line 44
- `QualificationReport` — line 64
- `distinct_classes` — line 82
- `qualified_classes` — line 88
- `CloudQualificationReport` — line 102
- `distinct` — line 123
- `qualified_classes` — line 129

## services/api/ppm_api/modules/ai/readiness.py

[Source](../../services/api/ppm_api/modules/ai/readiness.py)

- `windows_memory` — line 14
- `MemoryStatus` — line 19
- `readiness` — line 40
- `read` — line 83

## services/api/ppm_api/modules/ai/registry.py

[Source](../../services/api/ppm_api/modules/ai/registry.py)

- `canonical` — line 16
- `digest` — line 21
- `ModelProfile` — line 26
- `bounded_local` — line 62
- `ModelPolicy` — line 74
- `distinct` — line 79
- `policy_hash` — line 109
- `trusted_json` — line 114
- `load_policy` — line 131

## services/api/ppm_api/modules/ai/retrieval.py

[Source](../../services/api/ppm_api/modules/ai/retrieval.py)

- `digest` — line 21
- `SourceTool` — line 25
- `authorize_tool` — line 30
- `snapshot` — line 37
- `keyword` — line 46
- `validate_snapshot` — line 51
- `index_chunks` — line 66
- `cosine` — line 97
- `merge` — line 102
- `evaluate` — line 114

## services/api/ppm_api/modules/ai/router.py

[Source](../../services/api/ppm_api/modules/ai/router.py)

- `status` — line 25
- `listing` — line 31
- `detail` — line 39
- `evaluation` — line 45
- `operations` — line 51
- `configure` — line 57
- `create` — line 63
- `cancel` — line 69
- `progress` — line 75
- `stages` — line 81
- `diagnostics` — line 87

## services/api/ppm_api/modules/ai/schemas.py

[Source](../../services/api/ppm_api/modules/ai/schemas.py)

- `AIRunInput` — line 19
- `AIExcerpt` — line 28
- `AIOutput` — line 33
- `AIEvidence` — line 38
- `AIRunView` — line 47
- `AIBudgetInput` — line 78
- `AIProviderStatus` — line 83
- `AIOperations` — line 92
- `AICallView` — line 105
- `AIDiagnostics` — line 117
- `AIEvaluation` — line 128

## services/api/ppm_api/modules/ai/service.py

[Source](../../services/api/ppm_api/modules/ai/service.py)

- `oid` — line 59
- `admin` — line 64
- `call_cap` — line 70
- `provider_status` — line 84
- `status` — line 104
- `budget` — line 109
- `access` — line 135
- `view` — line 159
- `tokens` — line 189
- `listing` — line 234
- `detail` — line 246
- `evaluation` — line 251
- `operations` — line 259
- `configure` — line 281
- `create` — line 303
- `cancel` — line 546
- `progress` — line 576
- `stages` — line 584
- `diagnostics` — line 600
- `worker_context` — line 639
- `settle` — line 664
- `Branch` — line 714
- `Runtime` — line 720
- `__init__` — line 721
- `state` — line 735
- `call` — line 751
- `keyword_branch` — line 903
- `hybrid_branch` — line 912
- `index` — line 952
- `ai_worker` — line 984

## services/api/ppm_api/modules/ai/timing.py

[Source](../../services/api/ppm_api/modules/ai/timing.py)

- `TransportTiming` — line 24
- `__init__` — line 25
- `trace` — line 30

## services/api/ppm_api/modules/assessments/access.py

[Source](../../services/api/ppm_api/modules/assessments/access.py)

- `oid` — line 16
- `get` — line 20
- `grant` — line 35
- `can_edit` — line 50
- `eligible` — line 56
- `respondent` — line 61
- `reviewer` — line 67
- `evidence_access` — line 73
- `command_access` — line 80

## services/api/ppm_api/modules/assessments/evidence.py

[Source](../../services/api/ppm_api/modules/assessments/evidence.py)

- `list_evidence` — line 25
- `upload_evidence` — line 40
- `download_evidence` — line 104
- `delete_evidence` — line 128
- `preview_evidence` — line 148
- `release_evidence` — line 164

## services/api/ppm_api/modules/assessments/frameworks.py

[Source](../../services/api/ppm_api/modules/assessments/frameworks.py)

- `fw_view` — line 26
- `list_frameworks` — line 41
- `create_framework` — line 53
- `edit_framework` — line 74
- `publish_framework` — line 94
- `list_framework_versions` — line 132
- `seed_examples` — line 146

## services/api/ppm_api/modules/assessments/mutations.py

[Source](../../services/api/ppm_api/modules/assessments/mutations.py)

- `mutation` — line 22
- `wrapped` — line 25
- `revision` — line 81

## services/api/ppm_api/modules/assessments/router.py

[Source](../../services/api/ppm_api/modules/assessments/router.py)

- `BoundedRoute` — line 34
- `get_route_handler` — line 35
- `bounded` — line 38
- `list_frameworks` — line 57
- `create_framework` — line 65
- `edit_framework` — line 71
- `publish_framework` — line 81
- `versions` — line 90
- `seed_examples` — line 96
- `set_access` — line 102
- `assign` — line 108
- `list_assessments` — line 113
- `detail` — line 126
- `save_answers` — line 132
- `submit` — line 142
- `review` — line 150
- `history` — line 157
- `evidence_list` — line 162
- `upload` — line 170
- `download` — line 177
- `delete_evidence` — line 185
- `preview_evidence` — line 194
- `release_evidence` — line 206
- `access_list` — line 215

## services/api/ppm_api/modules/assessments/schemas.py

[Source](../../services/api/ppm_api/modules/assessments/schemas.py)

- `Strict` — line 16
- `Level` — line 20
- `Question` — line 26
- `Dimension` — line 36
- `FrameworkInput` — line 44
- `unique_ids` — line 52
- `FrameworkRecord` — line 59
- `VersionRecord` — line 66
- `AssignmentInput` — line 74
- `separate_people` — line 83
- `AnswerInput` — line 89
- `AnswerBatchInput` — line 95
- `AnswerRecord` — line 99
- `ActionInput` — line 105
- `Adjustment` — line 109
- `ReviewInput` — line 115
- `DimensionScoreDetail` — line 121
- `AssessmentRecord` — line 132
- `AssessmentDetail` — line 146
- `EventRecord` — line 153
- `EvidenceInput` — line 162
- `EvidenceRecord` — line 170
- `AccessInput` — line 180
- `one_scope` — line 187

## services/api/ppm_api/modules/assessments/scoring.py

[Source](../../services/api/ppm_api/modules/assessments/scoring.py)

- `_normalize_rubric` — line 11
- `compute_scores` — line 21

## services/api/ppm_api/modules/assessments/service.py

[Source](../../services/api/ppm_api/modules/assessments/service.py)

- `bump` — line 31
- `event` — line 39
- `answer_map` — line 54
- `scoring` — line 71
- `a_view` — line 81
- `finalize_check` — line 110
- `assign_assessment` — line 117
- `list_assessments` — line 167
- `get_assessment` — line 185
- `save_answers` — line 198
- `submit_assessment` — line 256
- `review_assessment` — line 295
- `set_access_grant` — line 355
- `list_assessment_events` — line 387
- `list_access_grants` — line 402

## services/api/ppm_api/modules/assessments/tables.py

[Source](../../services/api/ppm_api/modules/assessments/tables.py)

- `ref` — line 25
- `member` — line 31
- `tab` — line 37
- `revision` — line 51

## services/api/ppm_api/modules/assessments/validation.py

[Source](../../services/api/ppm_api/modules/assessments/validation.py)

- `questions` — line 11
- `validate_definition` — line 15
- `valid_answer` — line 32

## services/api/ppm_api/modules/capacity/router.py

[Source](../../services/api/ppm_api/modules/capacity/router.py)

- `resource_summary` — line 16
- `saved_snapshot` — line 25
- `team_summary` — line 30

## services/api/ppm_api/modules/capacity/schemas.py

[Source](../../services/api/ppm_api/modules/capacity/schemas.py)

- `CapacityCommon` — line 14
- `ResourceInput` — line 21
- `CalendarInput` — line 26
- `zone` — line 40
- `days` — line 49
- `ResourceChild` — line 57
- `DatedResource` — line 61
- `dates` — line 66
- `AvailabilityInput` — line 72
- `ResourceTeamInput` — line 77
- `ResourceSkillInput` — line 82
- `TimeOffInput` — line 87
- `AllocationInput` — line 94
- `ResourceAccessInput` — line 100
- `EffortInput` — line 107
- `overtime` — line 115
- `EffortCoverageInput` — line 121
- `CapacitySnapshotInput` — line 127
- `bounded` — line 131
- `CapacityDay` — line 137
- `CapacityWeek` — line 151
- `CapacityView` — line 160
- `TeamCapacityView` — line 181
- `SnapshotView` — line 196

## services/api/ppm_api/modules/capacity/service.py

[Source](../../services/api/ppm_api/modules/capacity/service.py)

- `access` — line 33
- `authorize` — line 50
- `validate` — line 78
- `rows` — line 112
- `ratio` — line 130
- `in_period` — line 138
- `calculate` — line 142
- `bounded` — line 194
- `sources_for` — line 199
- `summary` — line 222
- `snapshot` — line 287
- `resource_summary` — line 305
- `saved_snapshot` — line 311
- `team_summary` — line 316

## services/api/ppm_api/modules/capacity/tables.py

[Source](../../services/api/ppm_api/modules/capacity/tables.py)

- `resource` — line 32
- `period` — line 36

## services/api/ppm_api/modules/command/record_schemas.py

[Source](../../services/api/ppm_api/modules/command/record_schemas.py)

- `RiskInput` — line 13
- `readiness` — line 24
- `BenefitInput` — line 32
- `period` — line 41
- `MetricPlanInput` — line 47
- `MetricPolicyInput` — line 54
- `thresholds` — line 61
- `SavedViewInput` — line 67
- `period` — line 76

## services/api/ppm_api/modules/command/router.py

[Source](../../services/api/ppm_api/modules/command/router.py)

- `snapshot` — line 17

## services/api/ppm_api/modules/command/schemas.py

[Source](../../services/api/ppm_api/modules/command/schemas.py)

- `Fact` — line 14
- `Metric` — line 22
- `ProjectMetrics` — line 37
- `Velocity` — line 48
- `ResourceMetric` — line 61
- `TeamMetric` — line 67
- `CommandSnapshot` — line 72

## services/api/ppm_api/modules/command/service.py

[Source](../../services/api/ppm_api/modules/command/service.py)

- `workdays` — line 25
- `combined` — line 39
- `clamped` — line 47
- `snapshot` — line 51
- `load` — line 62
- `freshness` — line 117
- `fact` — line 126
- `metric` — line 131

## services/api/ppm_api/modules/delivery/metrics.py

[Source](../../services/api/ppm_api/modules/delivery/metrics.py)

- `budget_usage` — line 7
- `alignment_score` — line 11

## services/api/ppm_api/modules/delivery/router.py

[Source](../../services/api/ppm_api/modules/delivery/router.py)

- `people` — line 26
- `history` — line 36
- `portfolio_summary` — line 41
- `summary` — line 46
- `listing` — line 51
- `detail` — line 84
- `create` — line 89
- `update` — line 102

## services/api/ppm_api/modules/delivery/schemas.py

[Source](../../services/api/ppm_api/modules/delivery/schemas.py)

- `SettingsInput` — line 42
- `valid_timezone` — line 49
- `DepartmentInput` — line 57
- `GoalInput` — line 61
- `PortfolioInput` — line 65
- `TeamInput` — line 69
- `ProgramInput` — line 74
- `ProjectInput` — line 79
- `dates` — line 101
- `GrantInput` — line 116
- `target` — line 124
- `TeamMemberInput` — line 132
- `dates` — line 140
- `SprintInput` — line 146
- `dates` — line 154
- `WorkInput` — line 160
- `dates` — line 173
- `MilestoneInput` — line 179
- `BlockerInput` — line 186
- `DependencyInput` — line 193
- `endpoints` — line 202
- `BudgetInput` — line 213
- `ExpenditureInput` — line 220
- `StatusInput` — line 228
- `BaselineInput` — line 233
- `AlignmentInput` — line 237
- `target` — line 246
- `RecordView` — line 292
- `PageView` — line 301
- `BaselineView` — line 309
- `MoneyTotal` — line 317
- `SummaryView` — line 325
- `AlignmentSet` — line 339
- `PersonView` — line 344
- `HistoryView` — line 349
- `PortfolioSummary` — line 357

## services/api/ppm_api/modules/delivery/service.py

[Source](../../services/api/ppm_api/modules/delivery/service.py)

- `encode` — line 43
- `fail` — line 47
- `view` — line 51
- `get` — line 77
- `grant` — line 97
- `can_edit` — line 114
- `lock` — line 122
- `authorize` — line 162
- `refs` — line 215
- `cycle_check` — line 289
- `endpoint` — line 303
- `audit_change` — line 335
- `snapshot` — line 370
- `archive_guard` — line 396
- `people` — line 414
- `history` — line 435
- `portfolio_summary` — line 448
- `summary` — line 486
- `listing` — line 561
- `detail` — line 624
- `write` — line 628
- `create` — line 919
- `update` — line 962

## services/api/ppm_api/modules/documents/access.py

[Source](../../services/api/ppm_api/modules/documents/access.py)

- `document` — line 14
- `version` — line 33
- `writable` — line 44

## services/api/ppm_api/modules/documents/files.py

[Source](../../services/api/ppm_api/modules/documents/files.py)

- `upload` — line 26
- `ticket` — line 130
- `download` — line 153
- `reprocess` — line 188

## services/api/ppm_api/modules/documents/lifecycle.py

[Source](../../services/api/ppm_api/modules/documents/lifecycle.py)

- `orphan_keys` — line 24
- `candidates` — line 40
- `orphan_preview` — line 67
- `orphan_purge` — line 71
- `cancel` — line 82
- `governance` — line 103
- `delete` — line 134
- `purge` — line 149
- `link` — line 170

## services/api/ppm_api/modules/documents/mutations.py

[Source](../../services/api/ppm_api/modules/documents/mutations.py)

- `revision` — line 13
- `request_identity` — line 21

## services/api/ppm_api/modules/documents/parser.py

[Source](../../services/api/ppm_api/modules/documents/parser.py)

- `IntakeError` — line 24
- `validate` — line 28
- `scan` — line 86
- `ocr` — line 109
- `validate_pdf_objects` — line 125
- `extract` — line 167
- `isolated_extract` — line 314

## services/api/ppm_api/modules/documents/queries.py

[Source](../../services/api/ppm_api/modules/documents/queries.py)

- `library` — line 18
- `search` — line 42
- `detail` — line 77
- `preview` — line 81
- `citation` — line 99
- `job_status` — line 112
- `evidence_references` — line 140

## services/api/ppm_api/modules/documents/retrieval.py

[Source](../../services/api/ppm_api/modules/documents/retrieval.py)

- `EmbeddingRequest` — line 11
- `EmbeddingBackend` — line 20
- `index` — line 21
- `CandidateFinding` — line 26

## services/api/ppm_api/modules/documents/router.py

[Source](../../services/api/ppm_api/modules/documents/router.py)

- `orphan_preview` — line 32
- `orphan_purge` — line 37
- `library` — line 42
- `search` — line 56
- `detail` — line 67
- `upload` — line 72
- `preview` — line 77
- `citation` — line 87
- `ticket` — line 92
- `download` — line 97
- `job_status` — line 104
- `reprocess` — line 109
- `cancel` — line 114
- `governance` — line 119
- `delete` — line 124
- `purge` — line 129
- `link` — line 134
- `evidence_references` — line 139

## services/api/ppm_api/modules/documents/schemas.py

[Source](../../services/api/ppm_api/modules/documents/schemas.py)

- `Strict` — line 12
- `Upload` — line 16
- `Policy` — line 25
- `ordered` — line 34
- `Governance` — line 40
- `timezone` — line 46
- `VersionView` — line 52
- `DocumentView` — line 67
- `DocumentPage` — line 82
- `ChunkView` — line 88
- `SearchHit` — line 98
- `Retrieval` — line 106
- `DownloadTicket` — line 113
- `JobStatus` — line 118
- `Accepted` — line 125
- `EvidenceLink` — line 132
- `EvidenceReference` — line 136
- `Result` — line 142
- `OrphanPage` — line 146
- `OrphanPurge` — line 152

## services/api/ppm_api/modules/documents/service.py

[Source](../../services/api/ppm_api/modules/documents/service.py)

- `view` — line 17
- `enqueue` — line 44
- `replay` — line 100

## services/api/ppm_api/modules/documents/tables.py

[Source](../../services/api/ppm_api/modules/documents/tables.py)

- `tab` — line 9

## services/api/ppm_api/modules/documents/worker.py

[Source](../../services/api/ppm_api/modules/documents/worker.py)

- `document_worker` — line 27
- `principal` — line 31

## services/api/ppm_api/modules/identity/mail.py

[Source](../../services/api/ppm_api/modules/identity/mail.py)

- `local_delivery` — line 19
- `account_message` — line 31
- `smtp_delivery` — line 93
- `enqueue` — line 106
- `deliver_due` — line 131

## services/api/ppm_api/modules/identity/router.py

[Source](../../services/api/ppm_api/modules/identity/router.py)

- `csrf` — line 33
- `login` — line 38
- `refresh` — line 43
- `me` — line 48
- `profile` — line 53
- `switch` — line 58
- `logout` — line 65
- `list_sessions` — line 70
- `revoke` — line 75
- `reset_request` — line 80
- `complete` — line 85
- `member_list` — line 90
- `invite` — line 95
- `change_member` — line 100
- `audit_list` — line 113
- `register` — line 118
- `organization_profile` — line 123
- `edit_organization` — line 128
- `invitation_list` — line 138
- `invitation_action` — line 143

## services/api/ppm_api/modules/identity/schemas.py

[Source](../../services/api/ppm_api/modules/identity/schemas.py)

- `Input` — line 10
- `Credentials` — line 14
- `EmailInput` — line 19
- `nonblank` — line 23
- `RegistrationInput` — line 29
- `OrganizationProfileInput` — line 34
- `CompleteChallenge` — line 42
- `password_bytes` — line 49
- `ProfileInput` — line 55
- `SwitchInput` — line 59
- `InviteInput` — line 63
- `MemberInput` — line 67
- `Message` — line 72
- `CsrfResponse` — line 76
- `OrganizationView` — line 80
- `AccountView` — line 86
- `MemberView` — line 95
- `MembersView` — line 104
- `SessionView` — line 110
- `SessionsView` — line 117
- `AuditView` — line 121
- `AuditsView` — line 130

## services/api/ppm_api/modules/identity/service.py

[Source](../../services/api/ppm_api/modules/identity/service.py)

- `now` — line 49
- `digest` — line 53
- `delivery_instructions` — line 57
- `deny` — line 74
- `password_hash` — line 80
- `password_matches` — line 86
- `context` — line 93
- `limited` — line 107
- `cookie` — line 124
- `access_cookie` — line 143
- `record` — line 162
- `issue_challenge` — line 185
- `Principal` — line 235
- `authenticated` — line 244
- `principal` — line 317
- `account_principal` — line 325
- `admin` — line 335
- `account` — line 356
- `csrf` — line 380
- `login` — line 386
- `refresh` — line 430
- `me` — line 509
- `profile` — line 513
- `switch` — line 519
- `logout` — line 549
- `list_sessions` — line 559
- `revoke` — line 585
- `reset_request` — line 600
- `complete` — line 618
- `member_list` — line 792
- `invite` — line 809
- `change_member` — line 834
- `audit_list` — line 893
- `register` — line 906
- `organization_profile` — line 937
- `edit_organization` — line 1002
- `invitation_reference` — line 1028
- `invitation_list` — line 1033
- `invitation_action` — line 1073

## services/api/ppm_api/modules/integrations/connector_router.py

[Source](../../services/api/ppm_api/modules/integrations/connector_router.py)

- `authority` — line 20
- `approve` — line 25
- `review` — line 31
- `resolve` — line 36

## services/api/ppm_api/modules/integrations/connectors.py

[Source](../../services/api/ppm_api/modules/integrations/connectors.py)

- `authority` — line 24
- `approve` — line 36
- `connector_principal` — line 83
- `recheck` — line 115
- `logical_key` — line 127
- `record_conflict` — line 143
- `review` — line 190
- `resolve` — line 216
- `schedule_connectors` — line 288

## services/api/ppm_api/modules/integrations/ingestion.py

[Source](../../services/api/ppm_api/modules/integrations/ingestion.py)

- `ConnectorConfig` — line 24
- `mapping_allowlist` — line 55
- `target` — line 79
- `ImportInput` — line 99
- `bounded` — line 105
- `fingerprint` — line 113
- `project_rows` — line 117
- `rows` — line 136
- `normalize` — line 158
- `Retryable` — line 194
- `__init__` — line 195
- `NoRedirect` — line 199
- `redirect_request` — line 200
- `fetch_page` — line 206
- `remote_page` — line 289

## services/api/ppm_api/modules/integrations/jobs.py

[Source](../../services/api/ppm_api/modules/integrations/jobs.py)

- `source_evidence` — line 42
- `get_integration` — line 57
- `get_job` — line 69
- `admin_write` — line 87
- `secret_scope` — line 93
- `stage` — line 102
- `list_integrations` — line 126
- `create_integration` — line 135
- `enable_integration` — line 177
- `preview` — line 206
- `enqueue` — line 235
- `sync` — line 351
- `webhook` — line 358
- `activity` — line 377
- `job_detail` — line 394
- `stage_history` — line 398
- `cancel` — line 413
- `event_batch` — line 424
- `stream` — line 447
- `generate` — line 456
- `worker_principal` — line 496
- `worker_transaction` — line 534
- `apply_source` — line 588
- `run_job` — line 752
- `github_hook` — line 961

## services/api/ppm_api/modules/integrations/limits.py

[Source](../../services/api/ppm_api/modules/integrations/limits.py)

- `IntegrationBodyLimit` — line 9
- `__init__` — line 10
- `__call__` — line 13
- `bounded_receive` — line 48

## services/api/ppm_api/modules/integrations/router.py

[Source](../../services/api/ppm_api/modules/integrations/router.py)

- `source_evidence` — line 27
- `list_integrations` — line 32
- `create_integration` — line 37
- `enable_integration` — line 42
- `preview` — line 47
- `sync` — line 52
- `webhook` — line 57
- `activity` — line 63
- `job_detail` — line 68
- `stage_history` — line 73
- `cancel` — line 78
- `stream` — line 83
- `github_hook` — line 88

## services/api/ppm_api/modules/integrations/schemas.py

[Source](../../services/api/ppm_api/modules/integrations/schemas.py)

- `IntegrationView` — line 14
- `StageView` — line 23
- `JobView` — line 30
- `Preview` — line 46
- `EnabledInput` — line 52
- `SourceView` — line 56
- `AuthorityInput` — line 66
- `AuthorityView` — line 76
- `ConflictView` — line 87
- `Resolution` — line 100

## services/api/ppm_api/modules/ml/pipeline.py

[Source](../../services/api/ppm_api/modules/ml/pipeline.py)

- `label` — line 17
- `build_dataset` — line 41
- `evaluate` — line 167
- `metrics` — line 266

## services/api/ppm_api/modules/ml/router.py

[Source](../../services/api/ppm_api/modules/ml/router.py)

- `template` — line 23
- `history_list` — line 28
- `import_history` — line 33
- `withdraw` — line 38
- `dataset_list` — line 43
- `create_dataset` — line 48
- `dataset_detail` — line 53
- `run_list` — line 58
- `train` — line 63
- `run_detail` — line 68
- `artifacts` — line 73

## services/api/ppm_api/modules/ml/schemas.py

[Source](../../services/api/ppm_api/modules/ml/schemas.py)

- `Strict` — line 27
- `Features` — line 31
- `Outcome` — line 40
- `no_ai_labels` — line 60
- `Observation` — line 68
- `dates` — line 77
- `HistoryInput` — line 98
- `suitable` — line 111
- `DatasetInput` — line 131
- `chronology` — line 140
- `DatasetView` — line 148
- `MLHistoryView` — line 157
- `RunInput` — line 168
- `RunView` — line 172

## services/api/ppm_api/modules/ml/service.py

[Source](../../services/api/ppm_api/modules/ml/service.py)

- `admin` — line 27
- `get` — line 33
- `active_dataset` — line 42
- `access_run` — line 50
- `request_id` — line 56
- `fixture` — line 63
- `template` — line 127
- `history_list` — line 133
- `import_history` — line 145
- `withdraw` — line 208
- `dataset_list` — line 221
- `create_dataset` — line 233
- `dataset_detail` — line 276
- `run_list` — line 280
- `train` — line 297
- `run_detail` — line 373
- `artifacts` — line 377
- `ml_worker` — line 382

## services/api/ppm_api/modules/ml/tables.py

[Source](../../services/api/ppm_api/modules/ml/tables.py)

- `project_table` — line 9

## services/api/ppm_api/modules/selection/audit.py

[Source](../../services/api/ppm_api/modules/selection/audit.py)

- `audit` — line 13

## services/api/ppm_api/modules/selection/protocol.py

[Source](../../services/api/ppm_api/modules/selection/protocol.py)

- `protocol` — line 34
- `fixture_sources` — line 62
- `summarize` — line 94

## services/api/ppm_api/modules/selection/router.py

[Source](../../services/api/ppm_api/modules/selection/router.py)

- `listing` — line 15
- `create` — line 21
- `detail` — line 27
- `approve` — line 33
- `automated_review` — line 39
- `measure` — line 45

## services/api/ppm_api/modules/selection/schemas.py

[Source](../../services/api/ppm_api/modules/selection/schemas.py)

- `PilotInput` — line 12
- `LabelReview` — line 16
- `AutomatedReview` — line 24
- `PilotCase` — line 30
- `PilotObservation` — line 44
- `ProtocolCase` — line 51
- `PilotProtocol` — line 58
- `PilotView` — line 68

## services/api/ppm_api/modules/selection/service.py

[Source](../../services/api/ppm_api/modules/selection/service.py)

- `automated_allowed` — line 23
- `scope` — line 32
- `binding` — line 43
- `get` — line 67
- `reviewed` — line 79
- `view` — line 112
- `revision` — line 216
- `listing` — line 222
- `create` — line 236
- `detail` — line 269
- `approve` — line 274
- `automated_review` — line 324
- `snapshot` — line 387
- `measure` — line 423

## services/api/ppm_api/modules/workspace/router.py

[Source](../../services/api/ppm_api/modules/workspace/router.py)

- `search` — line 17
- `my_work` — line 28
- `setup` — line 35
- `comparison` — line 40
- `feed` — line 47
- `preference` — line 52
- `mark_read` — line 57
- `stream` — line 62

## services/api/ppm_api/modules/workspace/schemas.py

[Source](../../services/api/ppm_api/modules/workspace/schemas.py)

- `SearchItem` — line 12
- `SearchPage` — line 22
- `PreferenceInput` — line 29

## services/api/ppm_api/modules/workspace/service.py

[Source](../../services/api/ppm_api/modules/workspace/service.py)

- `term` — line 26
- `destination` — line 30
- `records` — line 38
- `search` — line 111
- `my_work` — line 117
- `setup` — line 121
- `comparison` — line 167
- `notify` — line 206
- `eligible_notification` — line 226
- `feed` — line 256
- `preference` — line 318
- `mark_read` — line 331
- `freshness` — line 350
- `stream` — line 379
- `generate` — line 382

## services/api/ppm_api/schemas.py

[Source](../../services/api/ppm_api/schemas.py)

- `ErrorDetail` — line 10
- `ErrorBody` — line 15
- `ErrorResponse` — line 22
- `HealthResponse` — line 26
- `DependencyStatus` — line 31
- `ReadyResponse` — line 36
- `FoundationResponse` — line 41

## services/api/ppm_api/shared/record_schemas.py

[Source](../../services/api/ppm_api/shared/record_schemas.py)

- `Common` — line 58
- `Owned` — line 65
- `ProjectChild` — line 69

## services/api/ppm_api/shared/table_base.py

[Source](../../services/api/ppm_api/shared/table_base.py)

- `col` — line 13
- `ref` — line 17
- `table` — line 27
- `owner` — line 50
- `project` — line 59
- `tenant_table` — line 67

## services/api/ppm_api/storage.py

[Source](../../services/api/ppm_api/storage.py)

- `ObjectStore` — line 9
- `put` — line 10
- `get` — line 11
- `delete` — line 12
- `LocalObjectStore` — line 15
- `__init__` — line 16
- `_path` — line 19
- `put` — line 34
- `get` — line 46
- `delete` — line 49
- `ready` — line 52

## services/worker/ppm_worker/app.py

[Source](../../services/worker/ppm_worker/app.py)

- `database_checkpoint` — line 31
- `run` — line 32
- `dispatch` — line 48
- `run` — line 49
- `pipeline_run` — line 77
- `run` — line 82

## tests/conftest.py

[Source](../../tests/conftest.py)

- `settings` — line 8

## tests/test_account_mail.py

[Source](../../tests/test_account_mail.py)

- `smtp_settings` — line 13
- `payload` — line 25
- `test_messages_contain_correct_private_journey` — line 37
- `test_organization_linebreaks_cannot_inject_headers` — line 58
- `test_smtp_tls_auth_and_recipient_acceptance` — line 65
- `Server` — line 68
- `__init__` — line 69
- `__enter__` — line 72
- `__exit__` — line 75
- `starttls` — line 78
- `login` — line 82
- `send_message` — line 86
- `test_smtp_configuration_fails_before_accepting_requests` — line 112
- `test_mail_model_error_reports_names_without_secrets` — line 119
- `test_local_mode_and_smtp_relay_are_deliberate` — line 134

## tests/test_account_repair.py

[Source](../../tests/test_account_repair.py)

- `test_no_membership_login_refresh_personal_profile_and_logout` — line 21
- `test_explicit_operator_status_preserves_memberships_and_last_admin` — line 43
- `test_duplicate_grant_preserves_business_reason_and_record_count` — line 71
- `test_admin_revocation_preserves_global_session_and_other_organization` — line 108
- `test_inactive_global_account_blocks_existing_session_login_reset_and_invitation` — line 138
- `test_profile_persistence_admin_relationship_validation_and_noop` — line 175
- `test_hement_sprint_requires_project_grant_and_planned_initial_state` — line 244

## tests/test_agent_batches.py

[Source](../../tests/test_agent_batches.py)

- `cases` — line 33
- `compact` — line 38
- `test_all_nine_plan_has_four_calls_and_real_synthesis_dependencies` — line 59
- `test_batch_roles_cannot_cover_or_cite_each_others_aliases` — line 74
- `test_no_adverse_predicate_cannot_report_an_adverse_signal` — line 88
- `test_invalid_member_rejects_whole_batch` — line 112
- `test_batch_eligibility_requires_every_member_class` — line 131
- `test_batch_wait_respects_one_minute_and_deadline` — line 159
- `test_batch_revocation_withholds_all_members_including_no_findings` — line 176
- `test_batched_and_individual_attempts_share_case_exhaustion` — line 196
- `test_real_packer_isolated_and_private_answers_rejected` — line 218
- `repair` — line 234
- `test_repair_dry_run_keeps_original_authorization_and_rejects_holdout` — line 244
- `forbid` — line 248
- `test_batch_unknown_blocks_replay_and_retains_each_case_root` — line 265
- `lose` — line 269
- `test_groq_schema_errors_are_repairable_but_counted` — line 291
- `test_cloud_review_cannot_approve_itself_or_ignore_frozen_strategy` — line 308
- `test_fresh_acceptance_cases_are_unseen_distinct_and_prepare_offline` — line 320
- `test_independent_approval_is_required_before_heldout_cloud_prepare` — line 335
- `forbid` — line 367
- `test_cloud_score_binds_approval_candidate_and_complete_ledger_without_qualifying` — line 387

## tests/test_agent_benchmark.py

[Source](../../tests/test_agent_benchmark.py)

- `profile` — line 21
- `corpus` — line 35
- `test_corpus_has_all_classes_and_holdouts_and_never_packs_labels` — line 39
- `test_each_role_baseline_and_control_cases` — line 61
- `test_dry_run_cannot_make_http_and_does_not_create_ledger` — line 96
- `refuse` — line 99
- `test_new_artifact_hash_survives_lf_checkout` — line 117
- `test_memory_failure_never_generates_or_forges_latency` — line 127
- `test_unknown_attempt_survives_restart` — line 143
- `missing_benchmark` — line 152
- `respond` — line 166
- `test_logical_attempts_survive_output_corpus_and_case_name_changes` — line 193
- `test_reordered_sources_cannot_renew_quality_attempts` — line 211
- `test_legacy_opaque_roots_fail_closed_without_rewriting_history` — line 224
- `test_warm_timing_does_not_consume_or_replace_quality_attempts` — line 240
- `test_explicit_budget_and_context_fail_before_inference` — line 252
- `test_draft_review_and_empty_measurements_cannot_qualify` — line 266
- `test_every_fixture_fits_bounded_context_without_expected_answers` — line 273
- `test_memory_inventory_includes_runner_descendants_without_unrelated_processes` — line 280
- `test_review_must_match_candidate_and_can_reject_real_citation` — line 292
- `test_transport_complete_is_still_pending_independent_review` — line 388
- `respond` — line 412

## tests/test_agent_critique.py

[Source](../../tests/test_agent_critique.py)

- `finding` — line 12
- `test_python_baseline_does_not_count_uninterpreted_documents_as_covered` — line 32
- `test_critique_withdraws_transitive_synthesis_but_preserves_original_sections` — line 44
- `test_distinct_claims_preserved_and_source_overlap_is_not_proven_opposition` — line 93

## tests/test_agent_planner.py

[Source](../../tests/test_agent_planner.py)

- `snapshot` — line 16
- `test_any_roles_can_receive_initial_calls_and_dag_is_topological` — line 37
- `test_metrics_no_calls_executive_reserved_and_no_hidden_dependency_inference` — line 55
- `test_nine_requested_roles_do_not_falsely_fit_in_three_slots` — line 77
- `test_context_isolated_spans_numerics_and_schema_modes` — line 85
- `test_recovery_never_resets_section_run_or_deadline` — line 137

## tests/test_agent_v2_contracts.py

[Source](../../tests/test_agent_v2_contracts.py)

- `test_nine_hybrid_roles_and_legacy_fingerprint_shape` — line 13
- `test_invalid_or_scope_expanding_requests_rejected` — line 39
- `test_requested_priority_is_preserved` — line 44
- `test_strict_section_modes_spans_and_coverage` — line 51
- `test_synthesis_requires_known_alias_shape_and_evidence` — line 70
- `test_baseline_cannot_manufacture_semantic_completion` — line 92
- `test_v2_settings_are_default_off_and_bounded` — line 100

## tests/test_agent_v2_runtime.py

[Source](../../tests/test_agent_v2_runtime.py)

- `configure` — line 34
- `execute` — line 121
- `test_nine_roles_use_four_durable_admissions_and_never_hide_a_fifth` — line 159
- `synthetic_capture` — line 190
- `batch_execute` — line 223
- `ProcessLost` — line 262
- `lose_candidate` — line 268
- `test_new_cloud_provider_uses_real_shared_admission_and_daily_cap` — line 316
- `test_metrics_runs_persist_tasks_and_never_call_model` — line 357
- `test_real_admission_checkpoint_replay_and_immutable_result` — line 404
- `test_no_profile_preserves_baseline_but_cannot_claim_ai_complete` — line 440
- `test_v2_flag_does_not_enable_itself` — line 459
- `test_truncation_uses_one_smaller_replacement_and_retains_usage` — line 473
- `truncated` — line 484
- `test_unknown_outcome_is_not_replayed_and_quarantines_local_host` — line 515
- `unknown` — line 523
- `test_exhausted_daily_scope_makes_no_external_call` — line 568
- `test_two_workers_share_one_local_generation` — line 589
- `paused` — line 598
- `test_crash_after_candidate_resumes_without_second_inference` — line 631
- `ProcessLost` — line 639
- `checkpoint` — line 645
- `test_worker_cancellation_settles_and_propagates` — line 679
- `interrupted` — line 690
- `unavailable` — line 715
- `test_failed_heartbeat_does_not_replace_completed_result` — line 779
- `failed` — line 793
- `test_worker_cancellation_during_heartbeat_cleanup_is_not_swallowed` — line 818
- `lingering` — line 824
- `test_oversized_bound_context_keeps_baseline_and_reports_partial` — line 853
- `oversized` — line 870
- `test_v2_late_output_is_fenced` — line 906
- `paused` — line 917

## tests/test_agents.py

[Source](../../tests/test_agents.py)

- `source` — line 38
- `candidate` — line 51
- `test_every_agent_support_missing_conflict_and_injection` — line 63
- `test_deterministic_merge_order_partial_and_typed_limits` — line 88
- `test_semantic_rubric_weights_gaps_levels_and_duplicate_matches` — line 120
- `test_domain_transport_keeps_gemini_allowlist_and_output_bound` — line 164
- `test_realistic_specialist_batch_truncation_keeps_existing_budget` — line 174
- `Double` — line 207
- `__init__` — line 210
- `complete` — line 214
- `start` — line 255
- `work` — line 266
- `fixture` — line 276
- `test_hidden_risk_disabled_replay_independent_review_and_preservation` — line 290
- `no_evidence_walk` — line 317
- `test_semantic_review_scores_rejection_immutable_history_and_stale_answers` — line 419
- `test_domain_provider_failures_are_honest_and_bounded` — line 545
- `test_late_output_fenced_and_call_accounting_retained` — line 574
- `test_all_nine_agents_group_threshold_and_live_revocation` — line 637
- `test_terminal_job_cannot_hide_new_run_diagnostics` — line 732
- `pause_after_snapshot` — line 746
- `test_worker_metrics_register_without_web_application_startup` — line 771

## tests/test_ai.py

[Source](../../tests/test_ai.py)

- `Double` — line 36
- `__init__` — line 39
- `embed` — line 45
- `complete` — line 51
- `fixture` — line 73
- `start` — line 110
- `work` — line 121
- `test_disabled_fallback_replay_sse_and_deleted_citation` — line 129
- `test_index_hybrid_usage_version_invalidation_and_immutable_snapshot` — line 161
- `test_provider_failures_truthful_partial_and_bounded_accounting` — line 214
- `test_concurrent_budget_reservations_and_revision_guards` — line 246
- `test_roles_tenants_tools_foreign_ids_and_private_diagnostics` — line 287
- `test_inflight_revocation_or_cancel_fences_late_publication` — line 317
- `Slow` — line 322
- `complete` — line 323
- `observed_batch` — line 339
- `test_crash_unknown_worker_lease_and_deadline_no_replay_spend` — line 417
- `test_circuit_opens_and_recovers` — line 452
- `test_unsupported_numerical_output_is_rejected` — line 483
- `Invented` — line 484
- `complete` — line 485
- `test_real_wait_timeout_missing_evidence_and_bad_vector_fallback` — line 512
- `Timeout` — line 513
- `embed` — line 514
- `test_inflight_source_tombstone_and_forged_tuple_are_safe` — line 534
- `SlowIndex` — line 537
- `embed` — line 538
- `test_worker_token_fencing_blocks_late_result` — line 598
- `Slow` — line 601
- `complete` — line 602
- `test_foreign_source_scope_csrf_rls_and_replay_hash_conflict` — line 649
- `test_gemini_zero_ledger_quota_fallback_and_persistent_call_limit` — line 683
- `test_gemini_disabled_embeddings_do_not_consume_attempts_or_failures` — line 743

## tests/test_ai_contracts.py

[Source](../../tests/test_ai_contracts.py)

- `test_versioned_release_gate_fixtures` — line 11
- `test_malformed_embeddings_rejected` — line 21
- `test_missing_key_disabled_and_fixed_provider_shape` — line 26
- `fake_post` — line 31
- `test_arbitrary_tools_scope_and_mutation_fields_are_not_inputs` — line 52

## tests/test_api.py

[Source](../../tests/test_api.py)

- `test_liveness_survives_unavailable_dependencies` — line 8
- `test_correlation_and_error_envelope` — line 21
- `test_secret_values_not_in_error_or_request_logs` — line 32
- `trigger` — line 36
- `test_validation_details_do_not_echo_inputs` — line 52
- `validate` — line 56

## tests/test_assessment.py

[Source](../../tests/test_assessment.py)

- `definition` — line 20
- `test_weighting_unknown_and_coverage` — line 53
- `test_invalid_rubrics_and_duplicate_ids` — line 69
- `write` — line 85
- `ok` — line 92
- `fixture` — line 98
- `save` — line 118
- `test_two_departments_review_versions_evidence_and_retries` — line 141
- `test_tenants_rls_immutable_and_invalid_input` — line 362
- `test_examples_publish_and_text_completeness` — line 445

## tests/test_capacity.py

[Source](../../tests/test_capacity.py)

- `calendar` — line 20
- `fixture` — line 33
- `summary` — line 49
- `allocation` — line 57
- `test_split_capacity_leave_holiday_zero_and_snapshot_history` — line 70
- `test_dst_local_dates_and_part_time_boundary_validation` — line 115
- `test_resource_manager_scope_viewer_hidden_projects_and_live_revoke` — line 147
- `test_sensitive_effort_completeness_and_audit_revocation` — line 220
- `test_allocation_concurrency_retry_and_database_isolation` — line 260
- `test_team_privacy_skills_and_sustained_overload` — line 312

## tests/test_cloud_chat_providers.py

[Source](../../tests/test_cloud_chat_providers.py)

- `cloud` — line 17
- `reply` — line 68
- `test_bounded_cloud_requests_preserve_completion_and_usage` — line 85
- `handler` — line 89
- `test_policy_denial_precedes_any_cloud_http` — line 121
- `forbidden` — line 139
- `test_tools_and_reasoning_never_become_output` — line 154
- `test_provider_specific_free_and_version_guards` — line 161
- `test_openrouter_nonzero_catalog_price_prevents_generation` — line 178
- `handler` — line 184
- `test_missing_usage_stays_unknown_and_provider_error_is_sanitized` — line 195
- `fail` — line 208
- `test_timeout_retains_safe_transport_milestones_without_retry` — line 220
- `handler` — line 226

## tests/test_cloud_specialists.py

[Source](../../tests/test_cloud_specialists.py)

- `test_assignment_covers_nine_roles_without_granting_qualification` — line 27
- `test_assigned_role_cannot_be_bypassed_by_qualification` — line 42
- `test_pending_task_cannot_resume_with_changed_prompt` — line 53
- `puter` — line 68
- `test_native_puter_preserves_actual_completion_and_bounds` — line 116
- `respond` — line 120
- `test_native_puter_rejects_unsafe_or_unbound_responses` — line 150
- `respond` — line 153
- `test_puter_native_catalogue_identity_is_preserved` — line 181
- `test_training_examples_are_separate_and_hard_validated` — line 196
- `test_history_unknown_budget_and_root_limits_are_preserved` — line 209
- `calibration` — line 230
- `test_cloud_calibration_dry_run_never_calls_or_promotes` — line 273
- `forbid` — line 276
- `test_cloud_unknown_is_checkpointed_and_cannot_be_replayed` — line 289
- `lose` — line 293
- `test_cloud_success_retains_raw_and_semantic_review_is_pending` — line 310
- `respond` — line 313

## tests/test_command.py

[Source](../../tests/test_command.py)

- `test_rule_arithmetic_and_calendar` — line 18
- `test_complete_health_capacity_thresholds_and_currency_scope` — line 28
- `count_queries` — line 81
- `snap` — line 119
- `metric` — line 128
- `test_command_reconciliation_discrepancy_history_filters` — line 134
- `test_command_scopes_personal_views_rls_csrf_and_replay` — line 259

## tests/test_config_storage.py

[Source](../../tests/test_config_storage.py)

- `test_missing_configuration_reports_names_without_secrets` — line 9
- `test_production_disabled_until_security_modules` — line 16
- `test_storage_roundtrip_persists_between_adapter_instances` — line 26
- `test_storage_rejects_escaping_keys` — line 37

## tests/test_delivery.py

[Source](../../tests/test_delivery.py)

- `create` — line 18
- `change` — line 30
- `setup` — line 40
- `test_hierarchy_delivery_money_and_baseline` — line 56
- `test_scope_grants_and_live_revocation` — line 167
- `test_idempotency_versions_dates_and_cross_tenant` — line 192
- `test_dependencies_cycle_and_same_project_references` — line 242
- `test_money_immutability_and_program_constraints` — line 292
- `test_real_rls_missing_context_and_foreign_keys` — line 327
- `test_pm_portfolio_creation_and_concurrent_revision` — line 345
- `test_currency_groups_and_scoped_portfolio_totals` — line 357
- `test_database_rejects_foreign_parent_and_ledger_mutation` — line 373
- `test_seed_refuses_non_demo_database` — line 413

## tests/test_document_parser.py

[Source](../../tests/test_document_parser.py)

- `office` — line 14
- `text_pdf` — line 40
- `compressed_objects_pdf` — line 64
- `add` — line 73
- `stream` — line 77
- `test_benign_compressed_pdf_with_cyclic_page_references_extracts` — line 112
- `test_active_names_in_compressed_pdf_objects_are_rejected` — line 138
- `scanned_pdf` — line 146
- `test_formats_and_source_locations` — line 201
- `test_untrusted_intake_rejected` — line 232
- `test_prompt_injection_is_ordinary_escaped_text_and_chunking_is_bounded` — line 237
- `test_chunk_budget_refuses_an_unpageable_partial_source` — line 244
- `test_real_scanned_pdf_and_image_ocr` — line 254

## tests/test_documents.py

[Source](../../tests/test_documents.py)

- `upload` — line 30
- `process` — line 50
- `clean_scanner` — line 56
- `test_library_versions_idempotency_retrieval_citations_and_download` — line 61
- `test_scoped_roles_counts_revocation_worker_and_signed_capabilities` — line 128
- `test_quarantine_failure_cancel_deletion_and_inflight_revocation` — line 206
- `delayed` — line 250
- `test_policy_retention_hold_purge_and_scope` — line 271
- `test_category_matrix_and_labeled_retrieval_evaluation` — line 346
- `test_real_clamd_and_processing_job` — line 371
- `test_125_document_paging_bounds_and_concurrent_replay` — line 394
- `test_transport_replay_integrity_expiry_orphans_and_holds` — line 431
- `test_assessment_bridge_preserves_completed_scores_and_private_grants` — line 520

## tests/test_gemini.py

[Source](../../tests/test_gemini.py)

- `gemini` — line 17
- `response` — line 33
- `transport` — line 44
- `open_` — line 47
- `test_zero_dollars_configured_and_openai_never_selected` — line 58
- `test_fail_closed_before_network` — line 90
- `test_verified_project_does_not_expire` — line 99
- `test_completion_headers_payload_output_and_tokens` — line 108
- `test_http_errors_are_redacted_no_paid_fallback` — line 141
- `test_timeout_malformed_and_response_bound` — line 160
- `test_untrusted_or_incomplete_completion_rejected` — line 175
- `test_embedding_dimensions_count_and_optional_disabled` — line 194
- `test_input_path_bounds_redirects_and_revocation` — line 210
- `redirect` — line 217

## tests/test_groq_smoke.py

[Source](../../tests/test_groq_smoke.py)

- `prepared` — line 17
- `response` — line 48
- `test_default_is_dry_run_without_network_or_promotion` — line 76
- `forbidden` — line 79
- `test_three_calls_are_durable_and_cannot_be_repeated_same_day` — line 88
- `test_changed_key_and_changed_corpus_are_denied_before_http` — line 101
- `test_ambiguous_failure_stops_and_blocks_replay` — line 110
- `timeout` — line 114
- `test_cooldown_stops_subsequent_requests` — line 125
- `quota` — line 128
- `test_logical_section_attempt_limit_survives_a_new_invocation` — line 137
- `forbidden` — line 150
- `test_runtime_schema_binds_identity_before_external_decoding` — line 157

## tests/test_guided_access.py

[Source](../../tests/test_guided_access.py)

- `test_guided_grant_preserves_role_and_checks_every_boundary` — line 33
- `execute` — line 119

## tests/test_guided_review.py

[Source](../../tests/test_guided_review.py)

- `source` — line 19
- `test_only_source_values_and_catalog_actions_can_be_displayed` — line 41
- `test_stale_other_role_and_free_text_are_never_sent` — line 70
- `test_unknown_and_revoked_metrics_are_withheld_and_partial_values_are_labeled` — line 75
- `test_one_role_plan_and_empty_evidence_keep_nine_truthful_checklists` — line 93
- `test_published_api_selection_is_withdrawn_when_source_changes` — line 112
- `test_guided_requests_exclude_other_projects_even_for_portfolio_roles` — line 125
- `test_adapter_limited_permission_cannot_send_general_prompts_or_wrong_role` — line 138

## tests/test_guided_runtime.py

[Source](../../tests/test_guided_runtime.py)

- `test_guided_selection_is_optional_single_call_and_never_qualifies_interpretation` — line 29
- `execute` — line 76
- `withdrawn` — line 128

## tests/test_identity.py

[Source](../../tests/test_identity.py)

- `identity` — line 40
- `send` — line 88
- `login` — line 102
- `challenge` — line 113
- `test_roles_tenant_selectors_hidden_ids_and_audit` — line 129
- `test_csrf_secure_cookies_expired_forged_and_logout` — line 184
- `test_refresh_rotation_replay_and_concurrent_replay` — line 217
- `test_final_admin_stale_revision_live_role_and_removal` — line 247
- `test_activation_invitation_scope_and_single_use` — line 311
- `test_reset_expiry_non_enumeration_bcrypt_bytes_and_session_revoke` — line 350
- `test_rls_pool_reuse_foreign_writes_and_composite_fk` — line 383
- `test_rate_limit_and_session_id_guessing` — line 460
- `test_existing_account_invites_and_revoked_inviter` — line 479
- `test_concurrent_last_admin_demotion_keeps_one_admin` — line 517
- `test_session_expiry_foreign_session_and_revocation` — line 556
- `test_controlled_operator_bootstrap_activation` — line 584

## tests/test_ingestion_mapping.py

[Source](../../tests/test_ingestion_mapping.py)

- `test_mapping_rejects_scalar_parent_of_another_field` — line 10
- `test_mapping_preserves_nested_siblings_and_discards_private_fields` — line 24

## tests/test_integration.py

[Source](../../tests/test_integration.py)

- `test_real_readiness_and_persisted_checkpoint` — line 20
- `test_real_database_write_commit_read_roundtrip` — line 32
- `test_app_role_cannot_bypass_security_or_mutate_checkpoint` — line 48

## tests/test_jobs.py

[Source](../../tests/test_jobs.py)

- `test_overlapping_mapping_rejected_before_connection_is_persisted` — line 28
- `test_public_signed_github_delivery_and_revoked_authority` — line 53
- `signed` — line 85
- `test_retry_backoff_partial_page_recovery_and_dead_letter` — line 133
- `remote` — line 148
- `test_revoked_worker_and_progress_retention` — line 197
- `test_actual_celery_process_crash_and_lease_recovery` — line 252
- `start` — line 276
- `config` — line 356
- `test_adapter_validation_and_network_allowlist` — line 360
- `connection` — line 390
- `submit` — line 402
- `execute` — line 412
- `test_import_atomic_replay_partial_recovery_revision_conflict_and_sse` — line 425
- `test_signed_webhook_replay_cancellation_and_tenant_rls` — line 528
- `test_github_jira_contract_fixtures_and_sprint_ingestion` — line 588

## tests/test_model_deadlines.py

[Source](../../tests/test_model_deadlines.py)

- `test_timeout_scope` — line 50
- `test_corrupt_frozen_bound_fails_closed` — line 58
- `test_operator_can_reduce_but_not_extend_frozen_wait` — line 71
- `test_adapter_rejects_unadmitted_or_nonordinary_long_wait` — line 90
- `test_actual_delayed_response_past_old_deadline_is_accepted` — line 106
- `delayed` — line 121
- `test_expiring_permit_bounds_wait_and_retains_unknown` — line 137
- `stalled` — line 151

## tests/test_model_qualification.py

[Source](../../tests/test_model_qualification.py)

- `report` — line 11
- `test_failed_hardware_or_latency_never_qualifies` — line 58
- `test_per_class_denominators_and_canonical_safety` — line 62
- `test_cloud_acceptance_has_real_identity_and_no_fabricated_local_measurements` — line 76

## tests/test_model_routing.py

[Source](../../tests/test_model_routing.py)

- `configured` — line 20
- `test_rank_only_eligible_and_task_class_specific` — line 53
- `test_retry_after_is_normalized_without_internal_retry` — line 72
- `respond` — line 76
- `test_cloud_is_fail_closed` — line 92
- `test_ollama_finish_usage_and_bounded_payload` — line 112
- `handler` — line 116
- `test_malformed_completed_message_is_invalid_output` — line 140
- `handler` — line 144
- `test_missing_model_does_not_download` — line 159
- `handler` — line 163
- `test_transport_errors_are_codes_without_provider_body` — line 182
- `handler` — line 185
- `test_direct_adapter_rechecks_policy_and_url` — line 193
- `forbidden` — line 196
- `test_shared_host_cannot_duplicate_quota_through_profile_alias` — line 208
- `test_authorized_native_gemini_preserves_finish_usage_and_egress` — line 221
- `respond` — line 263

## tests/test_model_timing.py

[Source](../../tests/test_model_timing.py)

- `test_transport_timing_keeps_only_known_monotonic_offsets` — line 8

## tests/test_pilot.py

[Source](../../tests/test_pilot.py)

- `mailbox` — line 27
- `test_registration_replacement_replay_and_organization` — line 35
- `test_invitation_resend_cancel_profile_roles_and_foreign_ids` — line 68
- `test_notification_insert_app_role_and_dedup` — line 137
- `test_search_125_records_roles_metadata_notifications_revocation` — line 157
- `test_full_cohort_paging_result_grants_and_equal_timestamps` — line 243
- `test_mail_adapter_templates_retry_expiry_and_redaction` — line 309
- `adapter` — line 318
- `timeout` — line 357
- `test_expired_invitation_visible_resend_and_historical_status` — line 412
- `test_freshness_rollback_other_tenant_and_membership_revoke` — line 462
- `signature` — line 470
- `test_workspace_stream_reconnect_and_live_revocation` — line 503
- `ConnectedRequest` — line 511
- `is_disconnected` — line 512
- `response` — line 515

## tests/test_provider_setup.py

[Source](../../tests/test_provider_setup.py)

- `test_metadata_verification_has_only_fixed_gets_and_no_secrets_in_output` — line 12
- `handler` — line 16
- `test_unconfirmed_or_missing_credentials_do_not_leave_the_machine` — line 50
- `forbidden` — line 51
- `test_authentication_error_cannot_echo_key_or_follow_redirect` — line 59
- `handler` — line 60
- `test_low_memory_stays_blocked_and_ollama_probe_cannot_load_a_model` — line 75
- `handler` — line 79
- `test_unknown_host_memory_and_external_origin_are_denied` — line 90
- `unavailable` — line 91
- `handler` — line 96
- `test_other_resident_model_does_not_silently_get_replaced` — line 107
- `handler` — line 110

## tests/test_selection_audit.py

[Source](../../tests/test_selection_audit.py)

- `test_exact_arithmetic_audit_is_reproducible_and_never_human` — line 12
- `test_changed_labels_sources_and_protocols_cannot_be_automatically_approved` — line 24

## tests/test_selection_pilot.py

[Source](../../tests/test_selection_pilot.py)

- `setup` — line 33
- `post` — line 92
- `review_body` — line 102
- `approved` — line 112
- `auto_approved` — line 129
- `test_twelve_case_pilot_uses_normal_jobs_quota_and_never_promotes` — line 146
- `execute` — line 157
- `test_unavailable_or_stale_pilot_cannot_measure_or_count_fallback` — line 283
- `execute` — line 289
- `test_tenant_roles_grant_and_approval_binding_are_enforced` — line 366
- `test_automated_review_is_local_one_pilot_bound_and_cannot_claim_human` — line 381
- `test_revoked_automated_authorization_stops_queued_worker_without_call` — line 419
- `forbidden` — line 428

## tests/test_selection_protocol.py

[Source](../../tests/test_selection_protocol.py)

- `test_protocol_is_frozen_numeric_only_and_has_independent_reserved_cases` — line 13
- `test_even_twelve_correct_synthetic_cases_cannot_qualify_semantics` — line 45
- `test_pilot_selection_cannot_add_real_evidence_or_other_roles` — line 76

## tests/test_sprint11_preserve.py

[Source](../../tests/test_sprint11_preserve.py)

- `test_failed_validation_leaves_backup_capture_retryable` — line 13
- `query` — line 20
- `checkpoint` — line 32
- `backup` — line 37

## tests/test_sprint12.py

[Source](../../tests/test_sprint12.py)

- `test_provider_identity_ignores_connection_names_and_manual_namespaces` — line 28
- `test_cpu_reproduction_and_split_contract` — line 40
- `test_history_rejects_leakage_unsuitable_labels_privacy_and_license` — line 78
- `test_entity_purge_late_label_incompatible_target_and_missing_behavior` — line 99
- `approve` — line 116
- `test_connector_logout_dedup_conflict_rotation_revocation_and_tenant` — line 127
- `test_connector_schedule_survives_session_and_stops_after_revoke` — line 233
- `remote` — line 270
- `test_connector_schedule_failure_backs_off_and_continues` — line 306
- `unreliable` — line 339
- `test_csv_namespace_backfill_preserves_explicit_namespaces_and_source_targets` — line 370
- `backfill` — line 397
- `test_csv_omitted_namespace_is_unique_explicit_manual_and_replays_are_preserved` — line 442
- `test_canonical_source_wins_over_legacy_null_key_without_rewriting_targets` — line 475
- `test_ml_archived_project_blocks_lookup_even_when_cancelling` — line 524
- `test_history_dataset_baseline_card_reproduction_withdrawal_and_access` — line 570
- `test_unlabeled_real_history_insufficient_card_and_session_revocation` — line 654

## tests/test_transaction_boundary.py

[Source](../../tests/test_transaction_boundary.py)

- `test_auth_transaction_finishes_before_response` — line 10
- `transaction` — line 14
- `write` — line 23
- `observed` — line 26
- `capture` — line 27
