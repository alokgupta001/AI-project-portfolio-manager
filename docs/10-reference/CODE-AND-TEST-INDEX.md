# Current code and test navigation

Source-derived AST inventory. Search symbols instead of relying on line numbers; a test definition is not an executed result. Run `python scripts/documentation_inventory.py --check` for drift. Actual results: [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md) and [Gemini follow-up](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).

## scripts/account_status.py

[Source](../../scripts/account_status.py)

- `set_status` — line 19
- `run` — line 66

## scripts/bootstrap_identity.py

[Source](../../scripts/bootstrap_identity.py)

- `run` — line 16

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

## scripts/check_previous_sprint_docs.py

[Source](../../scripts/check_previous_sprint_docs.py)

- `main` — line 8

## scripts/check_walkthrough.py

[Source](../../scripts/check_walkthrough.py)

- `run` — line 19

## scripts/configure_gemini_free_tier.py

[Source](../../scripts/configure_gemini_free_tier.py)

- `main` — line 14

## scripts/documentation_inventory.py

[Source](../../scripts/documentation_inventory.py)

- `cell` — line 16
- `inventories` — line 20
- `main` — line 198

## scripts/fill_current_portal.py

[Source](../../scripts/fill_current_portal.py)

- `run` — line 48
- `add` — line 163
- `child` — line 181

## scripts/repair_hement_access.py

[Source](../../scripts/repair_hement_access.py)

- `run` — line 20

## scripts/repair_preserve.py

[Source](../../scripts/repair_preserve.py)

- `sql` — line 17

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

## scripts/smoke_gemini_free_tier.py

[Source](../../scripts/smoke_gemini_free_tier.py)

- `main` — line 17

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

## scripts/sprint81_preserve.py

[Source](../../scripts/sprint81_preserve.py)

- `sql` — line 15

## scripts/sprint81_restore.py

[Source](../../scripts/sprint81_restore.py)

- `sql` — line 15

## scripts/verify_gemini_runtime.py

[Source](../../scripts/verify_gemini_runtime.py)

- `get` — line 12
- `main` — line 18

## services/api/migrations/env.py

[Source](../../services/api/migrations/env.py)

- `run_sync` — line 22
- `run_async` — line 28

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

## services/api/ppm_api/account_mail.py

[Source](../../services/api/ppm_api/account_mail.py)

- `local_delivery` — line 20
- `account_message` — line 32
- `smtp_delivery` — line 94
- `enqueue` — line 107
- `deliver_due` — line 132

## services/api/ppm_api/ai.py

[Source](../../services/api/ppm_api/ai.py)

- `oid` — line 62
- `admin` — line 66
- `call_cap` — line 71
- `provider_status` — line 84
- `status` — line 104
- `budget` — line 108
- `access` — line 136
- `view` — line 147
- `tokens` — line 176
- `listing` — line 221
- `detail` — line 235
- `evaluation` — line 240
- `operations` — line 248
- `configure` — line 270
- `create` — line 292
- `cancel` — line 434
- `progress` — line 456
- `stages` — line 464
- `diagnostics` — line 480
- `worker_context` — line 518
- `settle` — line 542
- `Branch` — line 590
- `Runtime` — line 596
- `__init__` — line 597
- `state` — line 610
- `call` — line 625
- `keyword_branch` — line 771
- `hybrid_branch` — line 779
- `index` — line 818
- `ai_worker` — line 849

## services/api/ppm_api/ai_evaluation.py

[Source](../../services/api/ppm_api/ai_evaluation.py)

- `run_evaluation` — line 12

## services/api/ppm_api/ai_provider.py

[Source](../../services/api/ppm_api/ai_provider.py)

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

## services/api/ppm_api/ai_retrieval.py

[Source](../../services/api/ppm_api/ai_retrieval.py)

- `digest` — line 20
- `SourceTool` — line 24
- `authorize_tool` — line 29
- `snapshot` — line 36
- `keyword` — line 45
- `validate_snapshot` — line 50
- `index_chunks` — line 65
- `cosine` — line 96
- `merge` — line 101
- `evaluate` — line 113

## services/api/ppm_api/ai_schemas.py

[Source](../../services/api/ppm_api/ai_schemas.py)

- `AIRunInput` — line 18
- `AIExcerpt` — line 25
- `AIOutput` — line 30
- `AIEvidence` — line 35
- `AIRunView` — line 44
- `AIBudgetInput` — line 75
- `AIProviderStatus` — line 80
- `AIOperations` — line 89
- `AICallView` — line 102
- `AIDiagnostics` — line 114
- `AIEvaluation` — line 125

## services/api/ppm_api/assessment.py

[Source](../../services/api/ppm_api/assessment.py)

- `BoundedRoute` — line 46
- `get_route_handler` — line 47
- `bounded` — line 50
- `oid` — line 71
- `get` — line 75
- `grant` — line 90
- `can_edit` — line 105
- `eligible` — line 111
- `respondent` — line 116
- `reviewer` — line 122
- `evidence_access` — line 128
- `command_access` — line 135
- `mutation` — line 155
- `wrapped` — line 158
- `revision` — line 214
- `bump` — line 222
- `event` — line 230
- `questions` — line 245
- `validate_definition` — line 249
- `_normalize_rubric` — line 266
- `valid_answer` — line 276
- `compute_scores` — line 286
- `answer_map` — line 347
- `scoring` — line 364
- `fw_view` — line 374
- `a_view` — line 389
- `list_frameworks` — line 419
- `create_framework` — line 435
- `edit_framework` — line 458
- `publish_framework` — line 480
- `versions` — line 521
- `seed_examples` — line 537
- `set_access` — line 580
- `assign` — line 614
- `list_assessments` — line 665
- `detail` — line 688
- `save_answers` — line 703
- `finalize_check` — line 761
- `submit` — line 770
- `review` — line 809
- `history` — line 868
- `evidence_list` — line 884
- `upload` — line 903
- `download` — line 966
- `delete_evidence` — line 990
- `preview_evidence` — line 1011
- `release_evidence` — line 1031
- `access_list` — line 1065

## services/api/ppm_api/assessment_schemas.py

[Source](../../services/api/ppm_api/assessment_schemas.py)

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

## services/api/ppm_api/assessment_tables.py

[Source](../../services/api/ppm_api/assessment_tables.py)

- `ref` — line 25
- `member` — line 31
- `tab` — line 37
- `revision` — line 51

## services/api/ppm_api/capacity.py

[Source](../../services/api/ppm_api/capacity.py)

- `access` — line 36
- `authorize` — line 53
- `validate` — line 81
- `rows` — line 115
- `ratio` — line 133
- `in_period` — line 141
- `calculate` — line 145
- `bounded` — line 197
- `sources_for` — line 202
- `summary` — line 225
- `snapshot` — line 290
- `resource_summary` — line 309
- `saved_snapshot` — line 316
- `team_summary` — line 322

## services/api/ppm_api/capacity_schemas.py

[Source](../../services/api/ppm_api/capacity_schemas.py)

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

## services/api/ppm_api/command.py

[Source](../../services/api/ppm_api/command.py)

- `workdays` — line 25
- `combined` — line 39
- `clamped` — line 47
- `snapshot` — line 52
- `load` — line 63
- `freshness` — line 118
- `fact` — line 127
- `metric` — line 132

## services/api/ppm_api/command_schemas.py

[Source](../../services/api/ppm_api/command_schemas.py)

- `Fact` — line 14
- `Metric` — line 22
- `ProjectMetrics` — line 37
- `Velocity` — line 48
- `ResourceMetric` — line 61
- `TeamMetric` — line 67
- `CommandSnapshot` — line 72

## services/api/ppm_api/config.py

[Source](../../services/api/ppm_api/config.py)

- `Settings` — line 21
- `validate_mail` — line 56
- `validate_key` — line 79
- `validate_origin` — line 86
- `validate_database` — line 100
- `validate_redis` — line 111
- `load_settings` — line 120

## services/api/ppm_api/database.py

[Source](../../services/api/ppm_api/database.py)

- `Base` — line 11
- `FoundationState` — line 15
- `make_engine` — line 25

## services/api/ppm_api/delivery.py

[Source](../../services/api/ppm_api/delivery.py)

- `encode` — line 49
- `fail` — line 53
- `view` — line 57
- `get` — line 83
- `grant` — line 103
- `can_edit` — line 120
- `lock` — line 128
- `authorize` — line 163
- `refs` — line 207
- `cycle_check` — line 281
- `endpoint` — line 295
- `audit_change` — line 327
- `snapshot` — line 362
- `archive_guard` — line 388
- `people` — line 407
- `history` — line 434
- `portfolio_summary` — line 448
- `summary` — line 487
- `listing` — line 563
- `detail` — line 627
- `write` — line 631
- `create` — line 923
- `update` — line 971

## services/api/ppm_api/document_parser.py

[Source](../../services/api/ppm_api/document_parser.py)

- `IntakeError` — line 24
- `validate` — line 28
- `scan` — line 86
- `ocr` — line 109
- `validate_pdf_objects` — line 125
- `extract` — line 167
- `isolated_extract` — line 314

## services/api/ppm_api/document_retrieval.py

[Source](../../services/api/ppm_api/document_retrieval.py)

- `EmbeddingRequest` — line 11
- `EmbeddingBackend` — line 20
- `index` — line 21
- `CandidateFinding` — line 26

## services/api/ppm_api/document_schemas.py

[Source](../../services/api/ppm_api/document_schemas.py)

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

## services/api/ppm_api/document_tables.py

[Source](../../services/api/ppm_api/document_tables.py)

- `tab` — line 9

## services/api/ppm_api/documents.py

[Source](../../services/api/ppm_api/documents.py)

- `orphan_keys` — line 56
- `candidates` — line 72
- `orphan_preview` — line 100
- `orphan_purge` — line 105
- `document` — line 116
- `version` — line 135
- `writable` — line 146
- `revision` — line 155
- `view` — line 163
- `library` — line 191
- `search` — line 221
- `detail` — line 263
- `enqueue` — line 267
- `request_identity` — line 323
- `replay` — line 332
- `upload` — line 356
- `preview` — line 461
- `citation` — line 485
- `ticket` — line 499
- `download` — line 523
- `job_status` — line 561
- `reprocess` — line 590
- `cancel` — line 618
- `governance` — line 640
- `delete` — line 672
- `purge` — line 688
- `link` — line 710
- `evidence_references` — line 742
- `document_worker` — line 775
- `principal` — line 779

## services/api/ppm_api/errors.py

[Source](../../services/api/ppm_api/errors.py)

- `DomainError` — line 6

## services/api/ppm_api/identity.py

[Source](../../services/api/ppm_api/identity.py)

- `now` — line 57
- `digest` — line 61
- `delivery_instructions` — line 65
- `deny` — line 82
- `password_hash` — line 88
- `password_matches` — line 94
- `context` — line 101
- `limited` — line 115
- `cookie` — line 132
- `access_cookie` — line 151
- `record` — line 170
- `issue_challenge` — line 193
- `Principal` — line 243
- `authenticated` — line 251
- `principal` — line 324
- `account_principal` — line 332
- `admin` — line 342
- `account` — line 363
- `csrf` — line 388
- `login` — line 395
- `refresh` — line 440
- `me` — line 520
- `profile` — line 525
- `switch` — line 532
- `logout` — line 563
- `list_sessions` — line 574
- `revoke` — line 601
- `reset_request` — line 617
- `complete` — line 636
- `member_list` — line 811
- `invite` — line 829
- `change_member` — line 855
- `audit_list` — line 919
- `register` — line 933
- `organization_profile` — line 965
- `edit_organization` — line 1031
- `invitation_reference` — line 1060
- `invitation_list` — line 1066
- `invitation_action` — line 1107

## services/api/ppm_api/identity_schemas.py

[Source](../../services/api/ppm_api/identity_schemas.py)

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

## services/api/ppm_api/ingestion.py

[Source](../../services/api/ppm_api/ingestion.py)

- `ConnectorConfig` — line 24
- `mapping_allowlist` — line 52
- `target` — line 76
- `ImportInput` — line 96
- `bounded` — line 102
- `fingerprint` — line 110
- `project_rows` — line 114
- `rows` — line 133
- `normalize` — line 155
- `Retryable` — line 191
- `__init__` — line 192
- `NoRedirect` — line 196
- `redirect_request` — line 197
- `fetch_page` — line 203
- `remote_page` — line 286

## services/api/ppm_api/job_limits.py

[Source](../../services/api/ppm_api/job_limits.py)

- `IntegrationBodyLimit` — line 9
- `__init__` — line 10
- `__call__` — line 13
- `bounded_receive` — line 48

## services/api/ppm_api/job_tables.py

[Source](../../services/api/ppm_api/job_tables.py)

- `tenant_table` — line 11

## services/api/ppm_api/jobs.py

[Source](../../services/api/ppm_api/jobs.py)

- `IntegrationView` — line 40
- `StageView` — line 49
- `JobView` — line 56
- `Preview` — line 71
- `EnabledInput` — line 77
- `SourceView` — line 81
- `source_evidence` — line 92
- `get_integration` — line 107
- `get_job` — line 119
- `admin_write` — line 133
- `secret_scope` — line 139
- `stage` — line 148
- `list_integrations` — line 173
- `create_integration` — line 183
- `enable_integration` — line 224
- `preview` — line 254
- `enqueue` — line 283
- `sync` — line 386
- `webhook` — line 394
- `activity` — line 414
- `job_detail` — line 430
- `stage_history` — line 435
- `cancel` — line 451
- `event_batch` — line 462
- `stream` — line 486
- `generate` — line 495
- `worker_principal` — line 535
- `worker_transaction` — line 567
- `apply_source` — line 598
- `run_job` — line 697
- `github_hook` — line 894

## services/api/ppm_api/main.py

[Source](../../services/api/ppm_api/main.py)

- `error_response` — line 54
- `create_app` — line 65
- `lifespan` — line 67
- `request_context` — line 94
- `http_error` — line 155
- `validation_error` — line 190
- `live` — line 203
- `ready` — line 212
- `database_probe` — line 213
- `redis_probe` — line 222
- `storage_probe` — line 225
- `probe` — line 229
- `foundation` — line 253

## services/api/ppm_api/metric_math.py

[Source](../../services/api/ppm_api/metric_math.py)

- `budget_usage` — line 7
- `alignment_score` — line 11

## services/api/ppm_api/pilot.py

[Source](../../services/api/ppm_api/pilot.py)

- `term` — line 29
- `destination` — line 33
- `SearchItem` — line 41
- `SearchPage` — line 51
- `records` — line 58
- `search` — line 132
- `my_work` — line 143
- `setup` — line 150
- `comparison` — line 197
- `notify` — line 236
- `eligible_notification` — line 256
- `feed` — line 287
- `PreferenceInput` — line 349
- `preference` — line 355
- `mark_read` — line 369
- `freshness` — line 388
- `stream` — line 418
- `generate` — line 421

## services/api/ppm_api/ppm_schemas.py

[Source](../../services/api/ppm_api/ppm_schemas.py)

- `Common` — line 70
- `Owned` — line 77
- `SettingsInput` — line 81
- `valid_timezone` — line 88
- `DepartmentInput` — line 96
- `GoalInput` — line 100
- `PortfolioInput` — line 104
- `TeamInput` — line 108
- `ProgramInput` — line 113
- `ProjectInput` — line 118
- `dates` — line 140
- `GrantInput` — line 155
- `target` — line 163
- `TeamMemberInput` — line 171
- `dates` — line 179
- `ProjectChild` — line 185
- `SprintInput` — line 189
- `dates` — line 197
- `WorkInput` — line 203
- `dates` — line 216
- `MilestoneInput` — line 222
- `BlockerInput` — line 229
- `DependencyInput` — line 236
- `endpoints` — line 245
- `BudgetInput` — line 256
- `ExpenditureInput` — line 263
- `StatusInput` — line 271
- `BaselineInput` — line 276
- `AlignmentInput` — line 280
- `target` — line 289
- `RiskInput` — line 295
- `readiness` — line 306
- `BenefitInput` — line 314
- `period` — line 323
- `MetricPlanInput` — line 329
- `MetricPolicyInput` — line 336
- `thresholds` — line 343
- `SavedViewInput` — line 349
- `period` — line 358
- `RecordView` — line 404
- `PageView` — line 413
- `BaselineView` — line 421
- `MoneyTotal` — line 429
- `SummaryView` — line 437
- `AlignmentSet` — line 451
- `PersonView` — line 456
- `HistoryView` — line 461
- `PortfolioSummary` — line 469

## services/api/ppm_api/ppm_tables.py

[Source](../../services/api/ppm_api/ppm_tables.py)

- `col` — line 13
- `ref` — line 17
- `table` — line 27
- `owner` — line 50
- `project` — line 59
- `resource` — line 339
- `period` — line 343

## services/api/ppm_api/schemas.py

[Source](../../services/api/ppm_api/schemas.py)

- `ErrorDetail` — line 8
- `ErrorBody` — line 13
- `ErrorResponse` — line 20
- `HealthResponse` — line 24
- `DependencyStatus` — line 29
- `ReadyResponse` — line 34
- `FoundationResponse` — line 39

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
- `pipeline_run` — line 74
- `run` — line 79

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

- `definition` — line 19
- `test_weighting_unknown_and_coverage` — line 52
- `test_invalid_rubrics_and_duplicate_ids` — line 68
- `write` — line 84
- `ok` — line 91
- `fixture` — line 97
- `save` — line 117
- `test_two_departments_review_versions_evidence_and_retries` — line 140
- `test_tenants_rls_immutable_and_invalid_input` — line 330
- `test_examples_publish_and_text_completeness` — line 408

## tests/test_capacity.py

[Source](../../tests/test_capacity.py)

- `calendar` — line 19
- `fixture` — line 32
- `summary` — line 48
- `allocation` — line 56
- `test_split_capacity_leave_holiday_zero_and_snapshot_history` — line 69
- `test_dst_local_dates_and_part_time_boundary_validation` — line 114
- `test_resource_manager_scope_viewer_hidden_projects_and_live_revoke` — line 146
- `test_sensitive_effort_completeness_and_audit_revocation` — line 219
- `test_allocation_concurrency_retry_and_database_isolation` — line 259
- `test_team_privacy_skills_and_sustained_overload` — line 311

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

- `create` — line 17
- `change` — line 29
- `setup` — line 39
- `test_hierarchy_delivery_money_and_baseline` — line 55
- `test_scope_grants_and_live_revocation` — line 166
- `test_idempotency_versions_dates_and_cross_tenant` — line 191
- `test_dependencies_cycle_and_same_project_references` — line 241
- `test_money_immutability_and_program_constraints` — line 291
- `test_real_rls_missing_context_and_foreign_keys` — line 326
- `test_pm_portfolio_creation_and_concurrent_revision` — line 344
- `test_currency_groups_and_scoped_portfolio_totals` — line 356
- `test_database_rejects_foreign_parent_and_ledger_mutation` — line 372
- `test_seed_refuses_non_demo_database` — line 412

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
- `delayed` — line 248
- `test_policy_retention_hold_purge_and_scope` — line 269
- `test_category_matrix_and_labeled_retrieval_evaluation` — line 344
- `test_real_clamd_and_processing_job` — line 369
- `test_125_document_paging_bounds_and_concurrent_replay` — line 392
- `test_transport_replay_integrity_expiry_orphans_and_holds` — line 429
- `test_assessment_bridge_preserves_completed_scores_and_private_grants` — line 518

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
- `test_real_database_write_commit_read_roundtrip` — line 31
- `test_app_role_cannot_bypass_security_or_mutate_checkpoint` — line 47

## tests/test_jobs.py

[Source](../../tests/test_jobs.py)

- `test_overlapping_mapping_rejected_before_connection_is_persisted` — line 22
- `test_public_signed_github_delivery_and_revoked_authority` — line 47
- `signed` — line 79
- `test_retry_backoff_partial_page_recovery_and_dead_letter` — line 127
- `remote` — line 142
- `test_revoked_worker_and_progress_retention` — line 191
- `test_actual_celery_process_crash_and_lease_recovery` — line 246
- `start` — line 270
- `config` — line 350
- `test_adapter_validation_and_network_allowlist` — line 354
- `connection` — line 384
- `submit` — line 396
- `execute` — line 406
- `test_import_atomic_replay_partial_recovery_revision_conflict_and_sse` — line 419
- `test_signed_webhook_replay_cancellation_and_tenant_rls` — line 522
- `test_github_jira_contract_fixtures_and_sprint_ingestion` — line 582

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

## tests/test_transaction_boundary.py

[Source](../../tests/test_transaction_boundary.py)

- `test_auth_transaction_finishes_before_response` — line 10
- `transaction` — line 14
- `write` — line 23
- `observed` — line 26
- `capture` — line 27
