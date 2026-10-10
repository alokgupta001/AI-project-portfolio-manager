# Current code and test navigation

Source-derived AST inventory, 9 October 2026. Search symbols instead of relying on line numbers; a test definition is not an executed result. Includes current pilot/mail modules and all migrations.

## services/api/migrations/env.py

[Source](../../services/api/migrations/env.py)

- `run_sync` — line 20
- `run_async` — line 26

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
- `downgrade` — line 384
- `granted` — line 314
- `visible` — line 317
- `editable` — line 320

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

## services/api/ppm_api/account_mail.py

[Source](../../services/api/ppm_api/account_mail.py)

- `local_delivery` — line 19
- `smtp_delivery` — line 31
- `enqueue` — line 49
- `deliver_due` — line 72

## services/api/ppm_api/assessment.py

[Source](../../services/api/ppm_api/assessment.py)

- `BoundedRoute` — line 46
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
- `get_route_handler` — line 47
- `wrapped` — line 158
- `bounded` — line 50

## services/api/ppm_api/assessment_schemas.py

[Source](../../services/api/ppm_api/assessment_schemas.py)

- `Strict` — line 16
- `Level` — line 20
- `Question` — line 26
- `Dimension` — line 36
- `FrameworkInput` — line 44
- `FrameworkRecord` — line 59
- `VersionRecord` — line 66
- `AssignmentInput` — line 74
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
- `unique_ids` — line 52
- `separate_people` — line 83
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
- `ResourceChild` — line 57
- `DatedResource` — line 61
- `AvailabilityInput` — line 72
- `ResourceTeamInput` — line 77
- `ResourceSkillInput` — line 82
- `TimeOffInput` — line 87
- `AllocationInput` — line 94
- `ResourceAccessInput` — line 100
- `EffortInput` — line 107
- `EffortCoverageInput` — line 121
- `CapacitySnapshotInput` — line 127
- `CapacityDay` — line 137
- `CapacityWeek` — line 151
- `CapacityView` — line 160
- `TeamCapacityView` — line 181
- `SnapshotView` — line 196
- `zone` — line 40
- `days` — line 49
- `dates` — line 66
- `overtime` — line 115
- `bounded` — line 131

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

- `Settings` — line 11
- `load_settings` — line 71
- `validate_key` — line 30
- `validate_origin` — line 37
- `validate_database` — line 51
- `validate_redis` — line 62

## services/api/ppm_api/database.py

[Source](../../services/api/ppm_api/database.py)

- `Base` — line 11
- `FoundationState` — line 15
- `make_engine` — line 25

## services/api/ppm_api/delivery.py

[Source](../../services/api/ppm_api/delivery.py)

- `encode` — line 48
- `DomainError` — line 52
- `fail` — line 56
- `view` — line 60
- `get` — line 86
- `grant` — line 106
- `can_edit` — line 123
- `lock` — line 131
- `authorize` — line 162
- `refs` — line 206
- `cycle_check` — line 280
- `audit_change` — line 326
- `snapshot` — line 361
- `archive_guard` — line 387
- `people` — line 406
- `history` — line 433
- `portfolio_summary` — line 447
- `summary` — line 486
- `listing` — line 562
- `detail` — line 626
- `write` — line 630
- `create` — line 904
- `update` — line 952
- `endpoint` — line 294

## services/api/ppm_api/identity.py

[Source](../../services/api/ppm_api/identity.py)

- `now` — line 55
- `digest` — line 59
- `deny` — line 63
- `password_hash` — line 67
- `password_matches` — line 73
- `context` — line 80
- `limited` — line 94
- `cookie` — line 111
- `access_cookie` — line 130
- `record` — line 149
- `issue_challenge` — line 170
- `Principal` — line 213
- `principal` — line 220
- `admin` — line 289
- `account` — line 306
- `csrf` — line 331
- `login` — line 338
- `refresh` — line 385
- `me` — line 455
- `profile` — line 460
- `switch` — line 467
- `logout` — line 498
- `list_sessions` — line 509
- `revoke` — line 536
- `reset_request` — line 552
- `complete` — line 571
- `member_list` — line 733
- `invite` — line 751
- `change_member` — line 777
- `audit_list` — line 840
- `register` — line 854
- `organization_profile` — line 886
- `edit_organization` — line 900
- `invitation_reference` — line 923
- `invitation_list` — line 929
- `invitation_action` — line 964

## services/api/ppm_api/identity_schemas.py

[Source](../../services/api/ppm_api/identity_schemas.py)

- `Input` — line 10
- `Credentials` — line 14
- `EmailInput` — line 19
- `nonblank` — line 23
- `RegistrationInput` — line 29
- `OrganizationProfileInput` — line 34
- `CompleteChallenge` — line 39
- `ProfileInput` — line 52
- `SwitchInput` — line 56
- `InviteInput` — line 60
- `MemberInput` — line 64
- `Message` — line 69
- `CsrfResponse` — line 73
- `OrganizationView` — line 77
- `AccountView` — line 83
- `MemberView` — line 92
- `MembersView` — line 101
- `SessionView` — line 107
- `SessionsView` — line 114
- `AuditView` — line 118
- `AuditsView` — line 127
- `password_bytes` — line 46

## services/api/ppm_api/ingestion.py

[Source](../../services/api/ppm_api/ingestion.py)

- `ConnectorConfig` — line 24
- `ImportInput` — line 96
- `fingerprint` — line 110
- `project_rows` — line 114
- `rows` — line 133
- `normalize` — line 155
- `Retryable` — line 191
- `NoRedirect` — line 196
- `fetch_page` — line 203
- `remote_page` — line 286
- `mapping_allowlist` — line 52
- `target` — line 76
- `bounded` — line 102
- `__init__` — line 192
- `redirect_request` — line 197

## services/api/ppm_api/job_limits.py

[Source](../../services/api/ppm_api/job_limits.py)

- `IntegrationBodyLimit` — line 9
- `__init__` — line 10
- `__call__` — line 13
- `bounded_receive` — line 45

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
- `admin_write` — line 128
- `secret_scope` — line 134
- `stage` — line 143
- `list_integrations` — line 168
- `create_integration` — line 178
- `enable_integration` — line 219
- `preview` — line 249
- `enqueue` — line 278
- `sync` — line 381
- `webhook` — line 389
- `activity` — line 409
- `job_detail` — line 425
- `stage_history` — line 430
- `cancel` — line 446
- `event_batch` — line 457
- `stream` — line 481
- `worker_principal` — line 530
- `worker_transaction` — line 561
- `apply_source` — line 592
- `run_job` — line 691
- `github_hook` — line 879
- `generate` — line 490

## services/api/ppm_api/main.py

[Source](../../services/api/ppm_api/main.py)

- `error_response` — line 52
- `create_app` — line 63
- `lifespan` — line 65
- `request_context` — line 90
- `http_error` — line 151
- `validation_error` — line 163
- `live` — line 176
- `ready` — line 185
- `foundation` — line 226
- `database_probe` — line 186
- `redis_probe` — line 195
- `storage_probe` — line 198
- `probe` — line 202

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
- `DepartmentInput` — line 96
- `GoalInput` — line 100
- `PortfolioInput` — line 104
- `TeamInput` — line 108
- `ProgramInput` — line 113
- `ProjectInput` — line 118
- `GrantInput` — line 155
- `TeamMemberInput` — line 171
- `ProjectChild` — line 185
- `SprintInput` — line 189
- `WorkInput` — line 203
- `MilestoneInput` — line 222
- `BlockerInput` — line 229
- `DependencyInput` — line 236
- `BudgetInput` — line 256
- `ExpenditureInput` — line 263
- `StatusInput` — line 271
- `BaselineInput` — line 276
- `AlignmentInput` — line 280
- `RiskInput` — line 295
- `BenefitInput` — line 314
- `MetricPlanInput` — line 329
- `MetricPolicyInput` — line 336
- `SavedViewInput` — line 349
- `RecordView` — line 404
- `PageView` — line 413
- `BaselineView` — line 421
- `MoneyTotal` — line 429
- `SummaryView` — line 437
- `AlignmentSet` — line 451
- `PersonView` — line 456
- `HistoryView` — line 461
- `PortfolioSummary` — line 469
- `valid_timezone` — line 88
- `dates` — line 140
- `target` — line 163
- `dates` — line 179
- `dates` — line 197
- `dates` — line 216
- `endpoints` — line 245
- `target` — line 289
- `readiness` — line 306
- `period` — line 323
- `thresholds` — line 343
- `period` — line 358

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
- `LocalObjectStore` — line 15
- `put` — line 10
- `get` — line 11
- `delete` — line 12
- `__init__` — line 16
- `_path` — line 19
- `put` — line 34
- `get` — line 46
- `delete` — line 49
- `ready` — line 52

## services/worker/ppm_worker/app.py

[Source](../../services/worker/ppm_worker/app.py)

- `database_checkpoint` — line 31
- `dispatch` — line 48
- `pipeline_run` — line 74
- `run` — line 32
- `run` — line 49
- `run` — line 79

## tests/conftest.py

[Source](../../tests/conftest.py)

- `settings` — line 8

## tests/test_api.py

[Source](../../tests/test_api.py)

- `test_liveness_survives_unavailable_dependencies` — line 8
- `test_correlation_and_error_envelope` — line 21
- `test_secret_values_not_in_error_or_request_logs` — line 32
- `test_validation_details_do_not_echo_inputs` — line 52
- `trigger` — line 36
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
- `snap` — line 119
- `metric` — line 128
- `test_command_reconciliation_discrepancy_history_filters` — line 134
- `test_command_scopes_personal_views_rls_csrf_and_replay` — line 259
- `count_queries` — line 81

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

## tests/test_identity.py

[Source](../../tests/test_identity.py)

- `identity` — line 40
- `send` — line 88
- `login` — line 99
- `challenge` — line 110
- `test_roles_tenant_selectors_hidden_ids_and_audit` — line 126
- `test_csrf_secure_cookies_expired_forged_and_logout` — line 181
- `test_refresh_rotation_replay_and_concurrent_replay` — line 214
- `test_final_admin_stale_revision_live_role_and_removal` — line 244
- `test_activation_invitation_scope_and_single_use` — line 306
- `test_reset_expiry_non_enumeration_bcrypt_bytes_and_session_revoke` — line 345
- `test_rls_pool_reuse_foreign_writes_and_composite_fk` — line 378
- `test_rate_limit_and_session_id_guessing` — line 455
- `test_existing_account_invites_and_revoked_inviter` — line 474
- `test_concurrent_last_admin_demotion_keeps_one_admin` — line 512
- `test_session_expiry_foreign_session_and_revocation` — line 551
- `test_controlled_operator_bootstrap_activation` — line 579

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
- `test_retry_backoff_partial_page_recovery_and_dead_letter` — line 127
- `test_revoked_worker_and_progress_retention` — line 190
- `test_actual_celery_process_crash_and_lease_recovery` — line 238
- `config` — line 338
- `test_adapter_validation_and_network_allowlist` — line 342
- `connection` — line 372
- `submit` — line 384
- `execute` — line 394
- `test_import_atomic_replay_partial_recovery_revision_conflict_and_sse` — line 407
- `test_signed_webhook_replay_cancellation_and_tenant_rls` — line 510
- `test_github_jira_contract_fixtures_and_sprint_ingestion` — line 570
- `signed` — line 79
- `remote` — line 142
- `start` — line 261

## tests/test_pilot.py

[Source](../../tests/test_pilot.py)

- `mailbox` — line 27
- `test_registration_replacement_replay_and_organization` — line 35
- `test_invitation_resend_cancel_profile_roles_and_foreign_ids` — line 68
- `test_notification_insert_app_role_and_dedup` — line 137
- `test_search_125_records_roles_metadata_notifications_revocation` — line 157
- `test_full_cohort_paging_result_grants_and_equal_timestamps` — line 243
- `test_mail_adapter_templates_retry_expiry_and_redaction` — line 309
- `test_freshness_rollback_other_tenant_and_membership_revoke` — line 393
- `test_workspace_stream_reconnect_and_live_revocation` — line 434
- `adapter` — line 318
- `timeout` — line 338
- `signature` — line 401
- `ConnectedRequest` — line 442
- `response` — line 446
- `is_disconnected` — line 443

## tests/test_transaction_boundary.py

[Source](../../tests/test_transaction_boundary.py)

- `test_auth_transaction_finishes_before_response` — line 10
- `transaction` — line 14
- `write` — line 23
- `observed` — line 26
- `capture` — line 27

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

## scripts/seed_delivery_demo.py

[Source](../../scripts/seed_delivery_demo.py)

- `id_for` — line 22
- `run` — line 26
- `add` — line 93

## scripts/sprint08_preserve.py

[Source](../../scripts/sprint08_preserve.py)

- `sql` — line 15

## scripts/sprint81_preserve.py

[Source](../../scripts/sprint81_preserve.py)

- `sql` — line 15

## scripts/sprint81_restore.py

[Source](../../scripts/sprint81_restore.py)

- `sql` — line 15
