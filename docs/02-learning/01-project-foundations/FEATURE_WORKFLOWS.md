# Main features: what happens after an action

[Learning roadmap](../00-getting-started/README.md) Â· Next: [scores and dashboard calculations](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md)

## Project and delivery records

This feature keeps project plans and delivery facts together. Users with the right access create/edit projects and associated work, inspect a board or timeline, record milestones and blockers, and keep financial/history records.

The UI is `apps/web/components/delivery.tsx:Delivery` and `RecordEditor`; `delivery-fields.ts` defines the forms. It calls `/api/v1/delivery/{kind}` for lists and creates, and `/{kind}/{id_}` for details and updates. `delivery.listing`, `detail`, `create` and `update` handle those operations; `write`, `authorize`, `refs` and `cycle_check` enforce the rules.

The core tables are `ppm_projects`, `ppm_work_items`, `ppm_sprints`, `ppm_milestones`, `ppm_blockers` and `ppm_dependencies`, connected to portfolios/programs. After a successful save, `Delivery` reloads server data. Chapter [2](../02-backend/REQUEST_LIFECYCLE.md) traces the whole create request.

The rules matter to users. A project moves draft â†’ active/cancelled; active â†’ on_hold/completed/cancelled; on_hold â†’ active/cancelled. Reopening a completed/cancelled project requires a reason and creates a new baseline. A completed project needs an actual finish date. Archived projects must be restored before editing.

Work moves through backlog, ready, in_progress and done using allowed transitions; reopening done work needs a reason. Sprints move planned â†’ active â†’ closed, and closed definitions are immutable. `cycle_check` rejects dependency loops, where A depends on B and B eventually depends on A. Cross-project dependency changes require Admin because a scoped manager may not see the whole graph.

**Inspect:** read `tests/test_delivery.py` and `tests/browser/delivery.spec.ts`. Confirm the row, summary and history after a save in an authorized test workflow. The module does not provide unlimited lists, automatic conflict merging or an AI schedule optimizer.

## Spending, status reports and history

These records explain why today's project differs from an earlier plan. Approved `ppm_budget_lines` provide budget; signed `ppm_expenditures` provide spend. `delivery.summary` sums them, and `metric_math.budget_usage` supplies a percentage only when budget is nonzero and `ledger_complete` is true.

An expenditure correction adds an exact negative reversal linked to the original. It must use the same project/currency and cannot reverse a reversal. Project currency cannot change after financial records exist. The API kinds are `budget_lines` and `expenditures`.

`status_updates` append human reports and update the current project's `reported_health`. `baselines` call `delivery.snapshot` to freeze plan facts. `audit_change` saves actor, before/after data and request ID in `ppm_audit` on the same transaction connection as the change. GET `/api/v1/delivery/history/{kind}/{id_}` displays currently authorized history through `ChangeDetails`.

Baselines, expenditure rows and status updates are append-only for the app role. Request timing logs are different from this business history. The migration owner remains powerful; the app does not implement cryptographically signed history or reconstruct every past dashboard state. History output is bounded to the latest 100 entries.

**Inspect:** find `audit_change`, `snapshot` and the financial checks in `write`. Tests in `test_delivery.py` cover budget, reversal and immutable history behavior.

## Resources and capacity

This feature helps planners see whether allocated work fits the recorded calendar. A resource is a workforce profile, not necessarily a person with an app login. Users can record skills, team links, availability, leave, project allocations and effort where permitted.

`apps/web/components/capacity.tsx:Capacity` uses delivery forms for resource record kinds. GET `/api/v1/capacity/resources/{rid}` calls `resource_summary` â†’ `summary` â†’ `sources_for` â†’ `calculate`. GET `/capacity/teams/{tid}` calls `team_summary`; `/capacity/snapshots/{id_}` reads saved planning results.

`ppm_resources`, `ppm_calendars`, `ppm_availability`, `ppm_time_off` and `ppm_allocations` supply planning data. `ppm_effort`, `ppm_effort_coverage` and `ppm_resource_access` support private actual-effort reporting. Chapter [8](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md) derives the hours and percentages.

The result appears as resource/day/week views and workload information. Missing calendars mean unknown available hours. Seeing one project's allocations does not prove whole-resource workload. Sensitive effort needs a separate effort grant even for Admin, and actual utilization needs completeness for every day. Editing effort invalidates affected completeness records.

Calendars and saved planning snapshots are immutable. Snapshots exclude private actual effort. Team summaries need Admin and at least five resources on every date; small or incomplete cohorts are suppressed or qualified. Leave hours are recorded directly; no leave-request approval workflow exists, and medical narrative reasons are prohibited in those records.

**Inspect:** `tests/test_capacity.py` covers split allocation, leave, missing data, scope, effort revocation and small cohorts; `tests/browser/capacity.spec.ts` follows the UI. Workload signals are fixed thresholds, not medical judgments or AI predictions.

## Assessments and independent review

This feature lets an organization define questions, collect answers and compare results under a stable definition. A framework is an editable set of dimensions and questions. Publishing stores a frozen version; later edits do not change old assessments.

`apps/web/components/assessments.tsx:Assessments` calls routes in `assessment.py`. POST `/api/v1/assessment/frameworks` calls `create_framework`; POST `/frameworks/{framework_id}/publish` calls `publish_framework`; POST `/assessments` calls `assign`. Assignment ties a frozen version to a respondent and a different reviewer.

`ppm_frameworks.definition` and `ppm_framework_versions.snapshot` store the structures as JSONB. `ppm_assessments` stores assignment/status/results; `ppm_answers` stores each question's raw value, evidence narrative and optional reviewer adjustment.

1. The respondent edits answers in the UI. Debounced autosave sends PUT `/assessments/{assessment_id}/answers`.
2. `save_answers` checks revision, editable state and that each question belongs to the frozen framework and appears once. It validates nonempty answers against the published answer type/rubric.
3. It inserts/updates answers, clears old adjustments on affected answers, clears stored assessment results, bumps revision and appends answer events.
4. POST `.../submit` calls `submit`. `finalize_check` rejects missing required answers or an uncomputable score before storing submitted results.
5. POST `.../review` calls `review` for start, return or complete. Only the assigned independent reviewer may act. Numeric overrides are 0â€“100 and need a reason; raw answers are retained.
6. The UI shows dimension bars and tables. Completed comparisons require the same framework version. Returned assessments can be answered again; completed results stay tied to their original definition.

The state path is draft/returned â†’ submitted â†’ in_review â†’ returned/completed. Read exact `review` conditions: the handler permits some actions from submitted too, so every UI step is not an unconditional API requirement.

`ppm_assessment_events` preserves actions; `ppm_assessment_access` stores additional scoped access; `ppm_assessment_requests` prevents duplicate mutation effects. Framework editing and completed-result grants are administered through browser Access panels. Result-only access does not disclose private answers or attachments. There is no semantic AI scoring or radar chart. Chapter [8](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md) explains the score arithmetic.

**Inspect:** `tests/test_assessment.py`, especially `test_weighting_unknown_and_coverage`, and `tests/browser/assessment.spec.ts`. Use separate test respondent/reviewer accounts when verifying the full workflow.

## Assessment evidence files

POST `/api/v1/assessment/assessments/{assessment_id}/evidence` calls `upload`. It accepts base64-encoded UTF-8 `.txt`, 1â€“524288 bytes, with at most 50 attachments. The request body limit is 2 MiB. Content checks reject active markup, prohibited control bytes and a test-malware signature.

The backend generates organization/assessment/UUID storage paths and uses `LocalObjectStore` for bytes. `ppm_evidence_attachments` stores size, digest, generated path and release status. After submission, the independent reviewer may preview and release with a reason through `preview_evidence` and `release_evidence`. Downloads recheck access, require release, verify the digest and force a plain-text attachment response.

Unreleased attachments block completion. Released attachments can count toward evidence coverage. This supports a narrow text-evidence workflow. PDF/Word ingestion, automatic malware scanning and automated orphan retention are incomplete or future work. Database rollback cannot remove a file write automatically; removing draft metadata can leave inaccessible bytes.

## Risks, benefits and command-center views

Users record risks, benefits and metric inputs through delivery kinds `risks`, `benefits` and `metric_plans`. `ppm_metric_policies` stores validated organization thresholds; `ppm_saved_views` stores personal filters. These writes reuse `delivery.write` and audit rules. Reopening a closed risk requires a reason.

`CommandCenter.refresh` requests GET `/api/v1/command/snapshot` with dates and optional portfolio. `command.snapshot` reads authorized delivery/capacity sources and returns one `CommandSnapshot` consumed by Executive, Delivery, Risk and Resource views. A request counter prevents an older response replacing a newer filter selection.

The source drawer shows contributing facts, coverage and freshness. Saved views store filters, not rows or permissions. JSON download makes a fresh authorized fetch. Risk-register likelihood/severity fields are not inputs to the fixed schedule/financial/capacity health calculation. There are no scheduled report emails or historical dashboard reconstruction.

**Inspect:** `tests/test_command.py`, `tests/browser/command.spec.ts`, and the formulas in the next chapter.


## Source-reviewed Sprint 8.1 update — 9 October 2026

My work uses `pilot.my_work` and `records` to select personal permitted records, including assigned/reviewer assessments not completed. Receipts are created transactionally by owning writes; `notify`, `feed`, `eligible_notification`, `mark_read` and `preference` implement deduplication, revalidation, read state and opt-out. A missing or revoked target is hidden before labels/counts. Thirty days is the presentation window, not purge. Scheduled reminders, approvals and external alerts are PLANNED for Sprints 15/21. Debug receipt kind, target access, enabled preference and timestamp before expecting a feed entry.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

The account workflow is website request → durable queue → Gmail message → one-time completion → separate sign-in. Actual signup, existing-account Viewer invitation and recovery are verified. Project/portfolio grants, Resource access, framework Access and completed-result Access are browser administration flows. Their grants are distinct from organization roles and named assessment assignments. Follow [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md).
