# Code and test navigation index

**ARCHIVED pre-audit snapshot.** Use the current architecture/reference inventory; this retained snapshot is not a competing canonical guide.


[Master guide](../../AI-PPM-MASTER-LEARNING-GUIDE.md)

Line numbers apply to Git ef196c9; use symbol names after edits. Test existence does not imply a new passing execution.

## services/api/migrations/env.py

| Symbol | Line |
|---|---|
| [run_sync](../../../services/api/migrations/env.py) | 13 |
| [run_async](../../../services/api/migrations/env.py) | 19 |

## services/api/migrations/versions/0001_foundation.py

| Symbol | Line |
|---|---|
| [upgrade](../../../services/api/migrations/versions/0001_foundation.py) | 15 |
| [downgrade](../../../services/api/migrations/versions/0001_foundation.py) | 27 |

## services/api/migrations/versions/0002_identity.py

| Symbol | Line |
|---|---|
| [upgrade](../../../services/api/migrations/versions/0002_identity.py) | 92 |
| [downgrade](../../../services/api/migrations/versions/0002_identity.py) | 135 |

## services/api/migrations/versions/0003_delivery.py

| Symbol | Line |
|---|---|
| [col](../../../services/api/migrations/versions/0003_delivery.py) | 20 |
| [ref](../../../services/api/migrations/versions/0003_delivery.py) | 24 |
| [table](../../../services/api/migrations/versions/0003_delivery.py) | 34 |
| [owner](../../../services/api/migrations/versions/0003_delivery.py) | 57 |
| [project](../../../services/api/migrations/versions/0003_delivery.py) | 66 |
| [upgrade](../../../services/api/migrations/versions/0003_delivery.py) | 306 |
| [downgrade](../../../services/api/migrations/versions/0003_delivery.py) | 384 |

## services/api/migrations/versions/0004_capacity.py

| Symbol | Line |
|---|---|
| [col](../../../services/api/migrations/versions/0004_capacity.py) | 20 |
| [ref](../../../services/api/migrations/versions/0004_capacity.py) | 24 |
| [table](../../../services/api/migrations/versions/0004_capacity.py) | 34 |
| [owner](../../../services/api/migrations/versions/0004_capacity.py) | 57 |
| [project](../../../services/api/migrations/versions/0004_capacity.py) | 66 |
| [resource](../../../services/api/migrations/versions/0004_capacity.py) | 322 |
| [period](../../../services/api/migrations/versions/0004_capacity.py) | 326 |
| [capability](../../../services/api/migrations/versions/0004_capacity.py) | 414 |
| [visible](../../../services/api/migrations/versions/0004_capacity.py) | 418 |
| [editable](../../../services/api/migrations/versions/0004_capacity.py) | 422 |
| [audit_policy](../../../services/api/migrations/versions/0004_capacity.py) | 426 |
| [upgrade](../../../services/api/migrations/versions/0004_capacity.py) | 439 |
| [downgrade](../../../services/api/migrations/versions/0004_capacity.py) | 490 |

## services/api/migrations/versions/0005_assessment.py

| Symbol | Line |
|---|---|
| [ref](../../../services/api/migrations/versions/0005_assessment.py) | 26 |
| [member](../../../services/api/migrations/versions/0005_assessment.py) | 32 |
| [tab](../../../services/api/migrations/versions/0005_assessment.py) | 38 |
| [revision_column](../../../services/api/migrations/versions/0005_assessment.py) | 52 |
| [scope](../../../services/api/migrations/versions/0005_assessment.py) | 159 |
| [upgrade](../../../services/api/migrations/versions/0005_assessment.py) | 168 |
| [downgrade](../../../services/api/migrations/versions/0005_assessment.py) | 227 |

## services/api/migrations/versions/0006_command_center.py

| Symbol | Line |
|---|---|
| [col](../../../services/api/migrations/versions/0006_command_center.py) | 17 |
| [ref](../../../services/api/migrations/versions/0006_command_center.py) | 21 |
| [table](../../../services/api/migrations/versions/0006_command_center.py) | 31 |
| [owner](../../../services/api/migrations/versions/0006_command_center.py) | 54 |
| [project](../../../services/api/migrations/versions/0006_command_center.py) | 63 |
| [upgrade](../../../services/api/migrations/versions/0006_command_center.py) | 149 |
| [downgrade](../../../services/api/migrations/versions/0006_command_center.py) | 187 |

## services/api/ppm_api/assessment.py

| Symbol | Line |
|---|---|
| [BoundedRoute](../../../services/api/ppm_api/assessment.py) | 46 |
| [oid](../../../services/api/ppm_api/assessment.py) | 71 |
| [get](../../../services/api/ppm_api/assessment.py) | 75 |
| [grant](../../../services/api/ppm_api/assessment.py) | 90 |
| [can_edit](../../../services/api/ppm_api/assessment.py) | 105 |
| [eligible](../../../services/api/ppm_api/assessment.py) | 111 |
| [respondent](../../../services/api/ppm_api/assessment.py) | 116 |
| [reviewer](../../../services/api/ppm_api/assessment.py) | 122 |
| [evidence_access](../../../services/api/ppm_api/assessment.py) | 128 |
| [command_access](../../../services/api/ppm_api/assessment.py) | 135 |
| [mutation](../../../services/api/ppm_api/assessment.py) | 155 |
| [revision](../../../services/api/ppm_api/assessment.py) | 214 |
| [bump](../../../services/api/ppm_api/assessment.py) | 222 |
| [event](../../../services/api/ppm_api/assessment.py) | 230 |
| [questions](../../../services/api/ppm_api/assessment.py) | 245 |
| [validate_definition](../../../services/api/ppm_api/assessment.py) | 249 |
| [_normalize_rubric](../../../services/api/ppm_api/assessment.py) | 266 |
| [valid_answer](../../../services/api/ppm_api/assessment.py) | 276 |
| [compute_scores](../../../services/api/ppm_api/assessment.py) | 286 |
| [answer_map](../../../services/api/ppm_api/assessment.py) | 347 |
| [scoring](../../../services/api/ppm_api/assessment.py) | 364 |
| [fw_view](../../../services/api/ppm_api/assessment.py) | 374 |
| [a_view](../../../services/api/ppm_api/assessment.py) | 389 |
| [list_frameworks](../../../services/api/ppm_api/assessment.py) | 419 |
| [create_framework](../../../services/api/ppm_api/assessment.py) | 435 |
| [edit_framework](../../../services/api/ppm_api/assessment.py) | 458 |
| [publish_framework](../../../services/api/ppm_api/assessment.py) | 480 |
| [versions](../../../services/api/ppm_api/assessment.py) | 521 |
| [seed_examples](../../../services/api/ppm_api/assessment.py) | 537 |
| [set_access](../../../services/api/ppm_api/assessment.py) | 580 |
| [assign](../../../services/api/ppm_api/assessment.py) | 614 |
| [list_assessments](../../../services/api/ppm_api/assessment.py) | 661 |
| [detail](../../../services/api/ppm_api/assessment.py) | 681 |
| [save_answers](../../../services/api/ppm_api/assessment.py) | 696 |
| [finalize_check](../../../services/api/ppm_api/assessment.py) | 754 |
| [submit](../../../services/api/ppm_api/assessment.py) | 763 |
| [review](../../../services/api/ppm_api/assessment.py) | 792 |
| [history](../../../services/api/ppm_api/assessment.py) | 851 |
| [evidence_list](../../../services/api/ppm_api/assessment.py) | 867 |
| [upload](../../../services/api/ppm_api/assessment.py) | 886 |
| [download](../../../services/api/ppm_api/assessment.py) | 949 |
| [delete_evidence](../../../services/api/ppm_api/assessment.py) | 973 |
| [preview_evidence](../../../services/api/ppm_api/assessment.py) | 994 |
| [release_evidence](../../../services/api/ppm_api/assessment.py) | 1014 |

## services/api/ppm_api/assessment_schemas.py

| Symbol | Line |
|---|---|
| [Strict](../../../services/api/ppm_api/assessment_schemas.py) | 16 |
| [Level](../../../services/api/ppm_api/assessment_schemas.py) | 20 |
| [Question](../../../services/api/ppm_api/assessment_schemas.py) | 26 |
| [Dimension](../../../services/api/ppm_api/assessment_schemas.py) | 36 |
| [FrameworkInput](../../../services/api/ppm_api/assessment_schemas.py) | 44 |
| [FrameworkRecord](../../../services/api/ppm_api/assessment_schemas.py) | 59 |
| [VersionRecord](../../../services/api/ppm_api/assessment_schemas.py) | 66 |
| [AssignmentInput](../../../services/api/ppm_api/assessment_schemas.py) | 74 |
| [AnswerInput](../../../services/api/ppm_api/assessment_schemas.py) | 89 |
| [AnswerBatchInput](../../../services/api/ppm_api/assessment_schemas.py) | 95 |
| [AnswerRecord](../../../services/api/ppm_api/assessment_schemas.py) | 99 |
| [ActionInput](../../../services/api/ppm_api/assessment_schemas.py) | 105 |
| [Adjustment](../../../services/api/ppm_api/assessment_schemas.py) | 109 |
| [ReviewInput](../../../services/api/ppm_api/assessment_schemas.py) | 115 |
| [DimensionScoreDetail](../../../services/api/ppm_api/assessment_schemas.py) | 121 |
| [AssessmentRecord](../../../services/api/ppm_api/assessment_schemas.py) | 132 |
| [AssessmentDetail](../../../services/api/ppm_api/assessment_schemas.py) | 146 |
| [EventRecord](../../../services/api/ppm_api/assessment_schemas.py) | 153 |
| [EvidenceInput](../../../services/api/ppm_api/assessment_schemas.py) | 162 |
| [EvidenceRecord](../../../services/api/ppm_api/assessment_schemas.py) | 170 |
| [AccessInput](../../../services/api/ppm_api/assessment_schemas.py) | 180 |

## services/api/ppm_api/assessment_tables.py

| Symbol | Line |
|---|---|
| [ref](../../../services/api/ppm_api/assessment_tables.py) | 25 |
| [member](../../../services/api/ppm_api/assessment_tables.py) | 31 |
| [tab](../../../services/api/ppm_api/assessment_tables.py) | 37 |
| [revision](../../../services/api/ppm_api/assessment_tables.py) | 51 |

## services/api/ppm_api/capacity.py

| Symbol | Line |
|---|---|
| [access](../../../services/api/ppm_api/capacity.py) | 36 |
| [authorize](../../../services/api/ppm_api/capacity.py) | 53 |
| [validate](../../../services/api/ppm_api/capacity.py) | 81 |
| [rows](../../../services/api/ppm_api/capacity.py) | 115 |
| [ratio](../../../services/api/ppm_api/capacity.py) | 133 |
| [in_period](../../../services/api/ppm_api/capacity.py) | 141 |
| [calculate](../../../services/api/ppm_api/capacity.py) | 145 |
| [bounded](../../../services/api/ppm_api/capacity.py) | 197 |
| [sources_for](../../../services/api/ppm_api/capacity.py) | 202 |
| [summary](../../../services/api/ppm_api/capacity.py) | 225 |
| [snapshot](../../../services/api/ppm_api/capacity.py) | 290 |
| [resource_summary](../../../services/api/ppm_api/capacity.py) | 309 |
| [saved_snapshot](../../../services/api/ppm_api/capacity.py) | 316 |
| [team_summary](../../../services/api/ppm_api/capacity.py) | 322 |

## services/api/ppm_api/capacity_schemas.py

| Symbol | Line |
|---|---|
| [CapacityCommon](../../../services/api/ppm_api/capacity_schemas.py) | 14 |
| [ResourceInput](../../../services/api/ppm_api/capacity_schemas.py) | 21 |
| [CalendarInput](../../../services/api/ppm_api/capacity_schemas.py) | 26 |
| [ResourceChild](../../../services/api/ppm_api/capacity_schemas.py) | 57 |
| [DatedResource](../../../services/api/ppm_api/capacity_schemas.py) | 61 |
| [AvailabilityInput](../../../services/api/ppm_api/capacity_schemas.py) | 72 |
| [ResourceTeamInput](../../../services/api/ppm_api/capacity_schemas.py) | 77 |
| [ResourceSkillInput](../../../services/api/ppm_api/capacity_schemas.py) | 82 |
| [TimeOffInput](../../../services/api/ppm_api/capacity_schemas.py) | 87 |
| [AllocationInput](../../../services/api/ppm_api/capacity_schemas.py) | 94 |
| [ResourceAccessInput](../../../services/api/ppm_api/capacity_schemas.py) | 100 |
| [EffortInput](../../../services/api/ppm_api/capacity_schemas.py) | 107 |
| [EffortCoverageInput](../../../services/api/ppm_api/capacity_schemas.py) | 121 |
| [CapacitySnapshotInput](../../../services/api/ppm_api/capacity_schemas.py) | 127 |
| [CapacityDay](../../../services/api/ppm_api/capacity_schemas.py) | 137 |
| [CapacityWeek](../../../services/api/ppm_api/capacity_schemas.py) | 151 |
| [CapacityView](../../../services/api/ppm_api/capacity_schemas.py) | 160 |
| [TeamCapacityView](../../../services/api/ppm_api/capacity_schemas.py) | 181 |
| [SnapshotView](../../../services/api/ppm_api/capacity_schemas.py) | 196 |

## services/api/ppm_api/command.py

| Symbol | Line |
|---|---|
| [workdays](../../../services/api/ppm_api/command.py) | 25 |
| [combined](../../../services/api/ppm_api/command.py) | 39 |
| [clamped](../../../services/api/ppm_api/command.py) | 47 |
| [snapshot](../../../services/api/ppm_api/command.py) | 52 |

## services/api/ppm_api/command_schemas.py

| Symbol | Line |
|---|---|
| [Fact](../../../services/api/ppm_api/command_schemas.py) | 14 |
| [Metric](../../../services/api/ppm_api/command_schemas.py) | 22 |
| [ProjectMetrics](../../../services/api/ppm_api/command_schemas.py) | 37 |
| [Velocity](../../../services/api/ppm_api/command_schemas.py) | 48 |
| [ResourceMetric](../../../services/api/ppm_api/command_schemas.py) | 61 |
| [TeamMetric](../../../services/api/ppm_api/command_schemas.py) | 67 |
| [CommandSnapshot](../../../services/api/ppm_api/command_schemas.py) | 72 |

## services/api/ppm_api/config.py

| Symbol | Line |
|---|---|
| [Settings](../../../services/api/ppm_api/config.py) | 11 |
| [load_settings](../../../services/api/ppm_api/config.py) | 65 |

## services/api/ppm_api/database.py

| Symbol | Line |
|---|---|
| [Base](../../../services/api/ppm_api/database.py) | 11 |
| [FoundationState](../../../services/api/ppm_api/database.py) | 15 |
| [make_engine](../../../services/api/ppm_api/database.py) | 25 |

## services/api/ppm_api/delivery.py

| Symbol | Line |
|---|---|
| [encode](../../../services/api/ppm_api/delivery.py) | 48 |
| [DomainError](../../../services/api/ppm_api/delivery.py) | 52 |
| [fail](../../../services/api/ppm_api/delivery.py) | 56 |
| [view](../../../services/api/ppm_api/delivery.py) | 60 |
| [get](../../../services/api/ppm_api/delivery.py) | 86 |
| [grant](../../../services/api/ppm_api/delivery.py) | 106 |
| [can_edit](../../../services/api/ppm_api/delivery.py) | 123 |
| [lock](../../../services/api/ppm_api/delivery.py) | 131 |
| [authorize](../../../services/api/ppm_api/delivery.py) | 162 |
| [refs](../../../services/api/ppm_api/delivery.py) | 206 |
| [cycle_check](../../../services/api/ppm_api/delivery.py) | 280 |
| [audit_change](../../../services/api/ppm_api/delivery.py) | 326 |
| [snapshot](../../../services/api/ppm_api/delivery.py) | 345 |
| [archive_guard](../../../services/api/ppm_api/delivery.py) | 371 |
| [people](../../../services/api/ppm_api/delivery.py) | 390 |
| [history](../../../services/api/ppm_api/delivery.py) | 408 |
| [portfolio_summary](../../../services/api/ppm_api/delivery.py) | 422 |
| [summary](../../../services/api/ppm_api/delivery.py) | 461 |
| [listing](../../../services/api/ppm_api/delivery.py) | 537 |
| [detail](../../../services/api/ppm_api/delivery.py) | 596 |
| [write](../../../services/api/ppm_api/delivery.py) | 600 |
| [create](../../../services/api/ppm_api/delivery.py) | 871 |
| [update](../../../services/api/ppm_api/delivery.py) | 919 |

## services/api/ppm_api/identity.py

| Symbol | Line |
|---|---|
| [now](../../../services/api/ppm_api/identity.py) | 55 |
| [digest](../../../services/api/ppm_api/identity.py) | 59 |
| [deny](../../../services/api/ppm_api/identity.py) | 63 |
| [password_hash](../../../services/api/ppm_api/identity.py) | 67 |
| [password_matches](../../../services/api/ppm_api/identity.py) | 73 |
| [context](../../../services/api/ppm_api/identity.py) | 80 |
| [limited](../../../services/api/ppm_api/identity.py) | 94 |
| [cookie](../../../services/api/ppm_api/identity.py) | 111 |
| [access_cookie](../../../services/api/ppm_api/identity.py) | 130 |
| [record](../../../services/api/ppm_api/identity.py) | 149 |
| [issue_challenge](../../../services/api/ppm_api/identity.py) | 170 |
| [Principal](../../../services/api/ppm_api/identity.py) | 216 |
| [principal](../../../services/api/ppm_api/identity.py) | 223 |
| [admin](../../../services/api/ppm_api/identity.py) | 291 |
| [account](../../../services/api/ppm_api/identity.py) | 308 |
| [csrf](../../../services/api/ppm_api/identity.py) | 333 |
| [login](../../../services/api/ppm_api/identity.py) | 340 |
| [refresh](../../../services/api/ppm_api/identity.py) | 387 |
| [me](../../../services/api/ppm_api/identity.py) | 457 |
| [profile](../../../services/api/ppm_api/identity.py) | 462 |
| [switch](../../../services/api/ppm_api/identity.py) | 469 |
| [logout](../../../services/api/ppm_api/identity.py) | 500 |
| [list_sessions](../../../services/api/ppm_api/identity.py) | 511 |
| [revoke](../../../services/api/ppm_api/identity.py) | 538 |
| [reset_request](../../../services/api/ppm_api/identity.py) | 554 |
| [complete](../../../services/api/ppm_api/identity.py) | 570 |
| [member_list](../../../services/api/ppm_api/identity.py) | 701 |
| [invite](../../../services/api/ppm_api/identity.py) | 719 |
| [change_member](../../../services/api/ppm_api/identity.py) | 736 |
| [audit_list](../../../services/api/ppm_api/identity.py) | 799 |

## services/api/ppm_api/identity_schemas.py

| Symbol | Line |
|---|---|
| [Input](../../../services/api/ppm_api/identity_schemas.py) | 10 |
| [Credentials](../../../services/api/ppm_api/identity_schemas.py) | 14 |
| [EmailInput](../../../services/api/ppm_api/identity_schemas.py) | 19 |
| [CompleteChallenge](../../../services/api/ppm_api/identity_schemas.py) | 23 |
| [ProfileInput](../../../services/api/ppm_api/identity_schemas.py) | 36 |
| [SwitchInput](../../../services/api/ppm_api/identity_schemas.py) | 40 |
| [InviteInput](../../../services/api/ppm_api/identity_schemas.py) | 44 |
| [MemberInput](../../../services/api/ppm_api/identity_schemas.py) | 48 |
| [Message](../../../services/api/ppm_api/identity_schemas.py) | 53 |
| [CsrfResponse](../../../services/api/ppm_api/identity_schemas.py) | 57 |
| [OrganizationView](../../../services/api/ppm_api/identity_schemas.py) | 61 |
| [AccountView](../../../services/api/ppm_api/identity_schemas.py) | 67 |
| [MemberView](../../../services/api/ppm_api/identity_schemas.py) | 76 |
| [MembersView](../../../services/api/ppm_api/identity_schemas.py) | 85 |
| [SessionView](../../../services/api/ppm_api/identity_schemas.py) | 91 |
| [SessionsView](../../../services/api/ppm_api/identity_schemas.py) | 98 |
| [AuditView](../../../services/api/ppm_api/identity_schemas.py) | 102 |
| [AuditsView](../../../services/api/ppm_api/identity_schemas.py) | 111 |

## services/api/ppm_api/main.py

| Symbol | Line |
|---|---|
| [error_response](../../../services/api/ppm_api/main.py) | 47 |
| [create_app](../../../services/api/ppm_api/main.py) | 58 |

## services/api/ppm_api/metric_math.py

| Symbol | Line |
|---|---|
| [budget_usage](../../../services/api/ppm_api/metric_math.py) | 7 |
| [alignment_score](../../../services/api/ppm_api/metric_math.py) | 11 |

## services/api/ppm_api/ppm_schemas.py

| Symbol | Line |
|---|---|
| [Common](../../../services/api/ppm_api/ppm_schemas.py) | 70 |
| [Owned](../../../services/api/ppm_api/ppm_schemas.py) | 77 |
| [SettingsInput](../../../services/api/ppm_api/ppm_schemas.py) | 81 |
| [DepartmentInput](../../../services/api/ppm_api/ppm_schemas.py) | 96 |
| [GoalInput](../../../services/api/ppm_api/ppm_schemas.py) | 100 |
| [PortfolioInput](../../../services/api/ppm_api/ppm_schemas.py) | 104 |
| [TeamInput](../../../services/api/ppm_api/ppm_schemas.py) | 108 |
| [ProgramInput](../../../services/api/ppm_api/ppm_schemas.py) | 113 |
| [ProjectInput](../../../services/api/ppm_api/ppm_schemas.py) | 118 |
| [GrantInput](../../../services/api/ppm_api/ppm_schemas.py) | 150 |
| [TeamMemberInput](../../../services/api/ppm_api/ppm_schemas.py) | 166 |
| [ProjectChild](../../../services/api/ppm_api/ppm_schemas.py) | 180 |
| [SprintInput](../../../services/api/ppm_api/ppm_schemas.py) | 184 |
| [WorkInput](../../../services/api/ppm_api/ppm_schemas.py) | 198 |
| [MilestoneInput](../../../services/api/ppm_api/ppm_schemas.py) | 215 |
| [BlockerInput](../../../services/api/ppm_api/ppm_schemas.py) | 222 |
| [DependencyInput](../../../services/api/ppm_api/ppm_schemas.py) | 229 |
| [BudgetInput](../../../services/api/ppm_api/ppm_schemas.py) | 249 |
| [ExpenditureInput](../../../services/api/ppm_api/ppm_schemas.py) | 256 |
| [StatusInput](../../../services/api/ppm_api/ppm_schemas.py) | 264 |
| [BaselineInput](../../../services/api/ppm_api/ppm_schemas.py) | 269 |
| [AlignmentInput](../../../services/api/ppm_api/ppm_schemas.py) | 273 |
| [RiskInput](../../../services/api/ppm_api/ppm_schemas.py) | 288 |
| [BenefitInput](../../../services/api/ppm_api/ppm_schemas.py) | 307 |
| [MetricPlanInput](../../../services/api/ppm_api/ppm_schemas.py) | 322 |
| [MetricPolicyInput](../../../services/api/ppm_api/ppm_schemas.py) | 329 |
| [SavedViewInput](../../../services/api/ppm_api/ppm_schemas.py) | 342 |
| [RecordView](../../../services/api/ppm_api/ppm_schemas.py) | 397 |
| [PageView](../../../services/api/ppm_api/ppm_schemas.py) | 406 |
| [BaselineView](../../../services/api/ppm_api/ppm_schemas.py) | 414 |
| [MoneyTotal](../../../services/api/ppm_api/ppm_schemas.py) | 422 |
| [SummaryView](../../../services/api/ppm_api/ppm_schemas.py) | 430 |
| [AlignmentSet](../../../services/api/ppm_api/ppm_schemas.py) | 444 |
| [PersonView](../../../services/api/ppm_api/ppm_schemas.py) | 449 |
| [HistoryView](../../../services/api/ppm_api/ppm_schemas.py) | 454 |
| [PortfolioSummary](../../../services/api/ppm_api/ppm_schemas.py) | 462 |

## services/api/ppm_api/ppm_tables.py

| Symbol | Line |
|---|---|
| [col](../../../services/api/ppm_api/ppm_tables.py) | 13 |
| [ref](../../../services/api/ppm_api/ppm_tables.py) | 17 |
| [table](../../../services/api/ppm_api/ppm_tables.py) | 27 |
| [owner](../../../services/api/ppm_api/ppm_tables.py) | 50 |
| [project](../../../services/api/ppm_api/ppm_tables.py) | 59 |
| [resource](../../../services/api/ppm_api/ppm_tables.py) | 315 |
| [period](../../../services/api/ppm_api/ppm_tables.py) | 319 |

## services/api/ppm_api/schemas.py

| Symbol | Line |
|---|---|
| [ErrorDetail](../../../services/api/ppm_api/schemas.py) | 8 |
| [ErrorBody](../../../services/api/ppm_api/schemas.py) | 13 |
| [ErrorResponse](../../../services/api/ppm_api/schemas.py) | 20 |
| [HealthResponse](../../../services/api/ppm_api/schemas.py) | 24 |
| [DependencyStatus](../../../services/api/ppm_api/schemas.py) | 29 |
| [ReadyResponse](../../../services/api/ppm_api/schemas.py) | 34 |
| [FoundationResponse](../../../services/api/ppm_api/schemas.py) | 39 |

## services/api/ppm_api/storage.py

| Symbol | Line |
|---|---|
| [ObjectStore](../../../services/api/ppm_api/storage.py) | 9 |
| [LocalObjectStore](../../../services/api/ppm_api/storage.py) | 15 |

## services/worker/ppm_worker/app.py

| Symbol | Line |
|---|---|
| [database_checkpoint](../../../services/worker/ppm_worker/app.py) | 31 |

## Backend test cases

| Test | Source | Intended regression boundary (read assertions for exact scope) |
|---|---|---|
| `test_liveness_survives_unavailable_dependencies` | [tests/test_api.py](../../../tests/test_api.py):8 | liveness survives unavailable dependencies |
| `test_correlation_and_error_envelope` | [tests/test_api.py](../../../tests/test_api.py):21 | correlation and error envelope |
| `test_secret_values_not_in_error_or_request_logs` | [tests/test_api.py](../../../tests/test_api.py):32 | secret values not in error or request logs |
| `test_validation_details_do_not_echo_inputs` | [tests/test_api.py](../../../tests/test_api.py):52 | validation details do not echo inputs |
| `test_weighting_unknown_and_coverage` | [tests/test_assessment.py](../../../tests/test_assessment.py):52 | weighting unknown and coverage |
| `test_invalid_rubrics_and_duplicate_ids` | [tests/test_assessment.py](../../../tests/test_assessment.py):68 | invalid rubrics and duplicate ids |
| `test_two_departments_review_versions_evidence_and_retries` | [tests/test_assessment.py](../../../tests/test_assessment.py):140 | two departments review versions evidence and retries |
| `test_tenants_rls_immutable_and_invalid_input` | [tests/test_assessment.py](../../../tests/test_assessment.py):330 | tenants rls immutable and invalid input |
| `test_examples_publish_and_text_completeness` | [tests/test_assessment.py](../../../tests/test_assessment.py):408 | examples publish and text completeness |
| `test_split_capacity_leave_holiday_zero_and_snapshot_history` | [tests/test_capacity.py](../../../tests/test_capacity.py):69 | split capacity leave holiday zero and snapshot history |
| `test_dst_local_dates_and_part_time_boundary_validation` | [tests/test_capacity.py](../../../tests/test_capacity.py):114 | dst local dates and part time boundary validation |
| `test_resource_manager_scope_viewer_hidden_projects_and_live_revoke` | [tests/test_capacity.py](../../../tests/test_capacity.py):146 | resource manager scope viewer hidden projects and live revoke |
| `test_sensitive_effort_completeness_and_audit_revocation` | [tests/test_capacity.py](../../../tests/test_capacity.py):219 | sensitive effort completeness and audit revocation |
| `test_allocation_concurrency_retry_and_database_isolation` | [tests/test_capacity.py](../../../tests/test_capacity.py):259 | allocation concurrency retry and database isolation |
| `test_team_privacy_skills_and_sustained_overload` | [tests/test_capacity.py](../../../tests/test_capacity.py):311 | team privacy skills and sustained overload |
| `test_rule_arithmetic_and_calendar` | [tests/test_command.py](../../../tests/test_command.py):18 | rule arithmetic and calendar |
| `test_complete_health_capacity_thresholds_and_currency_scope` | [tests/test_command.py](../../../tests/test_command.py):28 | complete health capacity thresholds and currency scope |
| `test_command_reconciliation_discrepancy_history_filters` | [tests/test_command.py](../../../tests/test_command.py):134 | command reconciliation discrepancy history filters |
| `test_command_scopes_personal_views_rls_csrf_and_replay` | [tests/test_command.py](../../../tests/test_command.py):259 | command scopes personal views rls csrf and replay |
| `test_missing_configuration_reports_names_without_secrets` | [tests/test_config_storage.py](../../../tests/test_config_storage.py):9 | missing configuration reports names without secrets |
| `test_production_disabled_until_security_modules` | [tests/test_config_storage.py](../../../tests/test_config_storage.py):16 | production disabled until security modules |
| `test_storage_roundtrip_persists_between_adapter_instances` | [tests/test_config_storage.py](../../../tests/test_config_storage.py):26 | storage roundtrip persists between adapter instances |
| `test_storage_rejects_escaping_keys` | [tests/test_config_storage.py](../../../tests/test_config_storage.py):37 | storage rejects escaping keys |
| `test_hierarchy_delivery_money_and_baseline` | [tests/test_delivery.py](../../../tests/test_delivery.py):55 | hierarchy delivery money and baseline |
| `test_scope_grants_and_live_revocation` | [tests/test_delivery.py](../../../tests/test_delivery.py):166 | scope grants and live revocation |
| `test_idempotency_versions_dates_and_cross_tenant` | [tests/test_delivery.py](../../../tests/test_delivery.py):191 | idempotency versions dates and cross tenant |
| `test_dependencies_cycle_and_same_project_references` | [tests/test_delivery.py](../../../tests/test_delivery.py):241 | dependencies cycle and same project references |
| `test_money_immutability_and_program_constraints` | [tests/test_delivery.py](../../../tests/test_delivery.py):291 | money immutability and program constraints |
| `test_real_rls_missing_context_and_foreign_keys` | [tests/test_delivery.py](../../../tests/test_delivery.py):326 | real rls missing context and foreign keys |
| `test_pm_portfolio_creation_and_concurrent_revision` | [tests/test_delivery.py](../../../tests/test_delivery.py):344 | pm portfolio creation and concurrent revision |
| `test_currency_groups_and_scoped_portfolio_totals` | [tests/test_delivery.py](../../../tests/test_delivery.py):356 | currency groups and scoped portfolio totals |
| `test_database_rejects_foreign_parent_and_ledger_mutation` | [tests/test_delivery.py](../../../tests/test_delivery.py):372 | database rejects foreign parent and ledger mutation |
| `test_seed_refuses_non_demo_database` | [tests/test_delivery.py](../../../tests/test_delivery.py):412 | seed refuses non demo database |
| `test_roles_tenant_selectors_hidden_ids_and_audit` | [tests/test_identity.py](../../../tests/test_identity.py):126 | roles tenant selectors hidden ids and audit |
| `test_csrf_secure_cookies_expired_forged_and_logout` | [tests/test_identity.py](../../../tests/test_identity.py):181 | csrf secure cookies expired forged and logout |
| `test_refresh_rotation_replay_and_concurrent_replay` | [tests/test_identity.py](../../../tests/test_identity.py):214 | refresh rotation replay and concurrent replay |
| `test_final_admin_stale_revision_live_role_and_removal` | [tests/test_identity.py](../../../tests/test_identity.py):244 | final admin stale revision live role and removal |
| `test_activation_invitation_scope_and_single_use` | [tests/test_identity.py](../../../tests/test_identity.py):306 | activation invitation scope and single use |
| `test_reset_expiry_non_enumeration_bcrypt_bytes_and_session_revoke` | [tests/test_identity.py](../../../tests/test_identity.py):345 | reset expiry non enumeration bcrypt bytes and session revoke |
| `test_rls_pool_reuse_foreign_writes_and_composite_fk` | [tests/test_identity.py](../../../tests/test_identity.py):378 | rls pool reuse foreign writes and composite fk |
| `test_rate_limit_and_session_id_guessing` | [tests/test_identity.py](../../../tests/test_identity.py):455 | rate limit and session id guessing |
| `test_existing_account_invites_and_revoked_inviter` | [tests/test_identity.py](../../../tests/test_identity.py):474 | existing account invites and revoked inviter |
| `test_concurrent_last_admin_demotion_keeps_one_admin` | [tests/test_identity.py](../../../tests/test_identity.py):512 | concurrent last admin demotion keeps one admin |
| `test_session_expiry_foreign_session_and_revocation` | [tests/test_identity.py](../../../tests/test_identity.py):551 | session expiry foreign session and revocation |
| `test_controlled_operator_bootstrap_activation` | [tests/test_identity.py](../../../tests/test_identity.py):579 | controlled operator bootstrap activation |
| `test_real_readiness_and_persisted_checkpoint` | [tests/test_integration.py](../../../tests/test_integration.py):20 | real readiness and persisted checkpoint |
| `test_real_database_write_commit_read_roundtrip` | [tests/test_integration.py](../../../tests/test_integration.py):31 | real database write commit read roundtrip |
| `test_app_role_cannot_bypass_security_or_mutate_checkpoint` | [tests/test_integration.py](../../../tests/test_integration.py):47 | app role cannot bypass security or mutate checkpoint |
