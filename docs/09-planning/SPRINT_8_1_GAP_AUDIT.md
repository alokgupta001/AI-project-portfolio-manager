# Sprint 8.1 gap audit

**Execution update 2026-10-09:** Sprint 8.1 local implementation is recorded in the [report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md); parent acceptance remains OPEN. The planning baseline below is historical. Future task scope and release criteria remain unchanged; no next sprint was started.

**Historical planning baseline (before Sprint 8.1 execution):** 9 October 2026. Documentation only; no feature work is authorized by this pack.** Sprint 08 is complete locally; Sprint 8.1 is proposed, not started. Numbers describe execution order, not dates or delivery promises. The frozen source specifications and original prompt pack remain intact. For future work, this pack supersedes the earlier gap review and the future sections of the original ordered prompts; those prompts remain historical scope evidence. Completed reports retain their original meaning.

Read the [audit](SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](SPRINT_8_1_PLAN.md), [future roadmap](FUTURE_SPRINT_ROADMAP.md), [traceability](FEATURE_GAP_TRACEABILITY.md), and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) together. A later implementation session must read the latest handoff and current working tree before using these plans.

## Execution disposition

G-001 and G-003–009 are implemented and locally accepted; G-002 remains BLOCKED for real account email. G-010 is content-corrected and PARTIAL pending Word visual QA. G-035 is VERIFIED by the completed backend suite; G-034 remains UNVERIFIED hosted CI. G-036 now points to revised roadmap plus execution evidence; frozen historical prompt dependency conflicts remain documented rather than rewritten. [Report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md).

## Historical pre-execution baseline and evidence limits

Latest completed sprint: **08, accepted locally**. Normal migration head: **0007_durable_jobs**. Current branch: `main`; base commit `90564405bcacc8389e34f3b06d8ab8d00984c5c1`. Many existing changes, including Sprint 08, are uncommitted. No implementation sprint is in progress on behalf of this request. No existing Sprint 8.1 files were found before this pack. Future plans previously covered 09–23. Existing application source, migrations, source copies and completed reports are preserved; see the planning preservation record in `artifacts/local/sprint81-planning/`.

Current code was inspected alongside reports, contracts, original source extracts, future prompts, tests, runtime/configuration, CI definitions and the user guides. This is a code-and-evidence audit, not a new exhaustive live-browser or load certification. Successful local journeys are supported by the retained verification logs and test code. Individual source requirement status is reconciled in the traceability crosswalk; broad status labels below are scoped to the behavior named.

**Fresh safe check in this planning session:** `python -B -m pytest tests/test_ingestion_mapping.py tests/test_config_storage.py -q -p no:cacheprovider` finished **12 passed in 0.18s**; it did not use the normal database. The broader ASGI transaction rerun was interrupted without completion; its result is UNVERIFIED, not a reproduced defect. No normal database mutation, migration, reset, bootstrap or seed was run for this planning task.

**Prior recorded checks inspected:** `docs/verification/current-backend-after.txt` records 67 passed, one warning; `current-browser.txt` records nine passed. The broader verification report additionally records the enhanced mapping browser check, seven SQL assertions, contracts/types/lint/format/source/build checks and preservation of 60 current public tables. These are existing recorded results, not reruns claimed by this planning task. Sprint 07's auth correction has successful hosted CI evidence; Sprint 08 hosted execution is UNVERIFIED. Real Jira/GitHub and AI/audio/cloud providers have no acceptance evidence here.

## Status definitions

| Status | Meaning used here |
| --- | --- |
| VERIFIED COMPLETE | Named local behavior is implemented and backed by successful recorded checks; excludes wider production claims. |
| PARTIAL | Working foundation exists but named required or adopted completion work remains. |
| BROKEN | A demonstrated existing behavior or documented user instruction is wrong. |
| NOT IMPLEMENTED | Required or adopted feature is absent from the current implementation. |
| UNVERIFIED | Evidence is insufficient; not proof of failure. |
| BLOCKED | An explicit external prerequisite prevents verification or promotion. |
| NOT REQUIRED | Explicit scope decision excludes the item; original required features cannot receive this label silently. |

## Working behavior retained

| Area | Status and scope | Evidence / boundaries |
| --- | --- | --- |
| Login/session/activation/invitation acceptance/password reset mechanics | VERIFIED COMPLETE for locally tested mechanics | I; private mailbox only, no public signup or external delivery. Commit-before-response fix is present. |
| Admin/PM/Viewer, organization isolation, membership revocation | VERIFIED COMPLETE for covered current API flows | I,D,C,A,M,J; future storage/tool surfaces still need 22/23 regression. |
| Portfolio/program/project detail, work/sprints/milestones/dependencies/budgets/benefits/baselines/archive/history | VERIFIED COMPLETE for covered local core flows | D; project detail already exists and must be extended, not rebuilt. Ownership and access are distinct. |
| Resource profiles/calendars/leave/skills/allocations/effort/capacity snapshots | VERIFIED COMPLETE for covered local arithmetic/access | C; missing capacity is unknown; separate sensitive-effort grants; minimum team privacy rules. |
| Published framework versions/dynamic questions/autosave/review/return/completion/deterministic score/history | VERIFIED COMPLETE for covered local scoring | A; text evidence only, review score adjustments use 0–100; bars and accessible tables are valid current charts. |
| Four dashboards, risk register, metric drill-down/saved views/filters/JSON | VERIFIED COMPLETE for covered local behavior | M; risk = 40% schedule + 35% finance + 25% capacity when all inputs exist; health = 100 − risk. These are rules, not forecasts. |
| Durable jobs/outbox/leases/retry/SSE/reconnect and connector fixtures | VERIFIED COMPLETE for local fixture/recovery cases | J; bounded inputs and initiator permissions; live provider acceptance blocked. |
| Local Compose, schema/client contracts, migrations and CI definition | VERIFIED COMPLETE for recorded local checks and Sprint 07 hosted auth fix | R; no production deployment or measured 99.9% availability claim. |

Previously reproduced mapping overlap (`id` with `id.title`) is now rejected in both orders, with regression coverage. The auth response/transaction fix is also present. Neither is counted as an open BROKEN application gap. The only confirmed BROKEN entry below is documentation/readiness wording. No new P0 application defect was reproduced.

## Gap register

**32 confirmed completion gaps** (PARTIAL, BROKEN or NOT IMPLEMENTED), plus 4 blocked/unverified evidence items, give **36 tracked findings**. Counts represent grouped work areas, not a count of every future button. Prior review A01–A18 is incorporated, not a second backlog.

P0 = immediate security/data-loss blocker; P1 = required for the owning milestone; P2 = useful stabilization; P3 = optional. No P0 is assigned without reproduced evidence.

### G-001 — Public sign-up

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-81-001. **Evidence groups:** I.

**Expected versus current:** Login, bootstrap activation and invitation acceptance exist; there is no public registration page or endpoint. A first customer needs operator assistance.

**Action:** Add verified registration with organization creation separated from login and invitation acceptance. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-002 — Usable invitation and recovery delivery

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-002. **Evidence groups:** I.

**Expected versus current:** Challenges are written to a local filesystem mailbox; users cannot receive mail through a configured external provider. Pending invitation listing, resend and cancellation are absent.

**Action:** Add provider-independent delivery and invitation lifecycle screens; retain private local preview. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-003 — First-time setup and organization profile

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-003. **Evidence groups:** I, U.

**Expected versus current:** Organization membership and account/session screens work. No guided organization setup, editable organization profile or completion checklist is present.

**Action:** Add setup checklist and minimal profile editing with clear account versus resource explanations. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-004 — Browser access management

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-004. **Evidence groups:** I, D, C, A.

**Expected versus current:** Domain permissions exist; assessment access grants are API-only. Ownership does not itself grant access and sensitive effort requires a separate grant.

**Action:** Expose existing project/resource/assessment grants and understandable effective-access explanations. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-005 — Search actual records

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-81-005. **Evidence groups:** U, D, A.

**Expected versus current:** The command palette searches available page names only, not projects, work, risks or assessments.

**Action:** Add permission-filtered record search; document content search remains Sprint 09. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-006 — Complete lists and selectors

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-006. **Evidence groups:** A, C, J.

**Expected versus current:** Assessment UI explicitly loads the latest 100; selectors/import destinations are bounded to first 100. API pagination does not make browser records beyond that limit reachable.

**Action:** Add pagination and server search; make departmental comparison period and full cohort explicit. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-007 — My work and basic notifications

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-007. **Evidence groups:** U, J.

**Expected versus current:** No personal assigned-work inbox; the notification dialog states no feed is active. Durable jobs are implemented, but there is no user notification model.

**Action:** Provide assigned work/assessment views and a small in-app feed; timed reminders and external channels stay in 15/21. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-008 — Metadata needed by later analytics

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-008. **Evidence groups:** D, J.

**Expected versus current:** Dates, ownership, status, goals and budgets exist; project industry, methodology, size/category and work priority/type are absent. Fintech questions and compatible cohorts need these fields.

**Action:** Add optional controlled metadata with unknown values; never backfill invented categories. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-009 — Live refresh of manual changes

**Status:** PARTIAL. **Priority:** P2. **Owner:** PPM-81-009. **Evidence groups:** M, J.

**Expected versus current:** Job completion/degradation refreshes dashboards. General manual delivery/resource/assessment edits have no common change-event refresh.

**Action:** Publish bounded authorized change notices and show freshness; do not broadcast record content. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-010 — Guide and readiness wording

**Status:** BROKEN. **Priority:** P1. **Owner:** PPM-81-010. **Evidence groups:** U, D.

**Expected versus current:** The testing guide asks users to create an active sprint; delivery.py requires planned on creation. The system page contains obsolete dashboard readiness wording.

**Action:** Correct the guide steps and readiness descriptions; verify each documented route on the browser. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-011 — Document library and assessment evidence bridge

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-09-001. **Evidence groups:** A, R.

**Expected versus current:** Assessment text attachments exist, with manual quarantine release; PDF/DOCX/OCR/library/retrieval and shared document links do not.

**Action:** Build shared versioned documents; preserve existing assessment scores and attachment authority. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-012 — Governance policy lifecycle

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-09-003. **Evidence groups:** R.

**Expected versus current:** Architecture names governance entities; no structured registry of policy owner, effective dates and project applicability is implemented.

**Action:** Create policy registry in 09 and approval integration in 15. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-013 — Retention and pilot restore evidence

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-09-003. **Evidence groups:** A, J, R.

**Expected versus current:** Logical evidence removal prevents reads but old object bytes may remain. Event retention is bounded; no demonstrated full pilot restore or unified derived-data erasure exists.

**Action:** Establish scoped purge/hold rules and a non-destructive scratch restore before real documents; finish all surfaces in 22/23. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-014 — Document and AI dependency conflict

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-10-001. **Evidence groups:** R.

**Expected versus current:** Original 09 asks for embeddings before common provider budgeting in 10; extraction and semantic assessment need 11.

**Action:** Stage keyword retrieval/contracts in 09, budgeted embedding adapter in 10, reviewed extraction in 11. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-015 — AI gateway and operations

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-10-001. **Evidence groups:** R.

**Expected versus current:** No provider runtime, typed AI run store, budget controls or AI operations page is wired into main.py.

**Action:** Implement shared adapters, bounded orchestration and evaluation before agents. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-016 — Nine agents and semantic maturity scoring

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-11-001. **Evidence groups:** A, M, R.

**Expected versus current:** Only deterministic metrics and maturity scores exist; no agent implementation or model-generated score is present.

**Action:** Build all nine agents with evidence and distinct suggested/reviewer scores. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-017 — Recommendation review versus application

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-11-003. **Evidence groups:** R.

**Expected versus current:** No recommendation center or execution workflow exists. Original 11 review precedes general workflows 15.

**Action:** Separate accepted recommendation from applied change; no generic mutation before 15. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-018 — Repeat assessments, due dates and trend/export

**Status:** PARTIAL. **Priority:** P2. **Owner:** PPM-15-002. **Evidence groups:** A.

**Expected versus current:** History and version-compatible department comparisons work. Due dates, reassignment, repeat scheduling and explicit longitudinal/export views are missing.

**Action:** Extend the existing assessment lifecycle and connect workflow reminders, keeping published score history immutable. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-019 — Unattended connector identity and conflict resolution

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-12-001. **Evidence groups:** J.

**Expected versus current:** Connector jobs act as initiating users; sessions expire after seven days. Source/local edit conflicts are rejected; no browser diff/resolve flow. Connections can duplicate a logical source if configured twice.

**Action:** Add narrow renewable connector authority, source identity uniqueness and reviewable conflict resolution. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-020 — Live Jira/GitHub acceptance

**Status:** BLOCKED. **Priority:** P1. **Owner:** PPM-12-001. **Evidence groups:** J, R.

**Expected versus current:** Fixture adapter tests pass; real credentials and live authentication/sync are unavailable.

**Action:** Run authorized read-only provider checks and controlled import with scoped credentials in 12; preserve fixtures and mark blocked until supplied. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-021 — Historical features, labels and models

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-12-002. **Evidence groups:** D, J, R.

**Expected versus current:** Imports do not capture bug/scope histories or notes needed by all model targets; no dataset manifest, training pipeline or tracked models.

**Action:** Capture justified historical fields and consented notes, validate labels and evaluate baseline models. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-022 — Production model promotion evidence

**Status:** BLOCKED. **Priority:** P1. **Owner:** PPM-13-001. **Evidence groups:** R.

**Expected versus current:** No eligible model or genuine labeled history is available; source datasets are candidates, not proof of suitability.

**Action:** Require real temporal evaluation and suitability evidence; demo fixtures cannot satisfy promotion. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-023 — Forecast serving

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-13-002. **Evidence groups:** M, R.

**Expected versus current:** Risk is a transparent rule score, not a probability or trained forecast. No forecast routes, history or monitoring exist.

**Action:** Serve eligible versions with uncertainty and honest unavailable/fallback states. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-024 — Copilot, scoped context and natural language analytics

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-14-001. **Evidence groups:** R.

**Expected versus current:** No chat, conversations, semantic query model or source-grounded multi-project answers are implemented.

**Action:** Build bounded authorized tools and cited conversation UI after evidence runtime. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-025 — Approvals, escalation, due-event reminders

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-15-001. **Evidence groups:** R, J.

**Expected versus current:** Manual risk and assessment review exist; configurable versioned flows, SLA timers and action execution do not.

**Action:** Implement inbox, calendars, authority checks and repeat-safe approved actions. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-026 — Transformation and decisions

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-16-001. **Evidence groups:** R.

**Expected versus current:** No transformation initiative model, six planning outputs, KPI roadmap or decision log exists.

**Action:** Build evidence-linked roadmaps and approval-based project conversion; consume copilot drafts. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-027 — Resource and budget scenarios

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-17-001. **Evidence groups:** C, M, R.

**Expected versus current:** Capacity snapshots and baselines exist; no scenario workspace or authorized apply function exists.

**Action:** Simulate immutable copies with conservation and stale-apply rejection. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-028 — Knowledge graph and impact paths

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-18-001. **Evidence groups:** R.

**Expected versus current:** Neo4j is a planned derived projection; no graph service, rebuild or graph UI exists.

**Action:** Build scoped projection and bounded impact paths without changing source authority. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-029 — Comparable benchmarks

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-19-001. **Evidence groups:** A, M, R.

**Expected versus current:** Department assessment comparison exists. Broader period/cohort normalization and portfolio/team benchmarks are absent.

**Action:** Compare compatible cohorts with counts, denominators and privacy suppression. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-030 — Meeting intelligence

**Status:** NOT IMPLEMENTED. **Priority:** P1. **Owner:** PPM-20-001. **Evidence groups:** R.

**Expected versus current:** No audio/transcript jobs, minutes editor or approved action conversion exists.

**Action:** Add authorized uploads, transcription and evidence-linked review. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-031 — Reports, alerts and daily audio

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-21-001. **Evidence groups:** M, J, R.

**Expected versus current:** Metrics JSON download exists. Scheduled weekly email/Slack, rendered PDF/HTML and daily TTS briefing do not.

**Action:** Ship exports and authorized subscriptions; account emails remain 8.1. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-032 — Passkeys and account lifecycle settings

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-22-001. **Evidence groups:** I, R.

**Expected versus current:** Password/session recovery works locally. Passkeys, safe email change, leaving organization, retention/provider settings and full-surface audit search are missing.

**Action:** Implement passkeys and settings, preserving last-admin protection and all-surface revocation. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-033 — Release engineering and production configuration

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-23-001. **Evidence groups:** R.

**Expected versus current:** Local Docker and hosted Sprint 07 CI are evidenced. Current settings accept only local/test/demo; Terraform/Kubernetes/production config and measured release/recovery evidence are absent.

**Action:** Integrate all journeys and prepare deployment profiles; live deployment requires credentials and authorization. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-034 — Sprint 08 hosted CI

**Status:** UNVERIFIED. **Priority:** P1. **Owner:** PPM-81-010. **Evidence groups:** R.

**Expected versus current:** Sprint 07 auth-fix hosted CI passed; Sprint 08 workspace is uncommitted and no hosted run for those changes is established.

**Action:** Record a reviewed checkpoint and hosted checks during implementation closure without discarding existing changes. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-035 — Current direct ASGI rerun

**Status:** UNVERIFIED. **Priority:** P2. **Owner:** PPM-81-010. **Evidence groups:** R.

**Expected versus current:** A planning-session rerun combining two pure-unit files with transaction-boundary ASGI tests stopped after twelve tests without completion; it was interrupted. Prior full-suite log records 67 passing.

**Action:** Repeat transaction-boundary checks in the established isolated environment and capture completion; do not infer an application bug from an interrupted run. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

### G-036 — Planning consistency and source reconciliation

**Status:** PARTIAL. **Priority:** P1. **Owner:** PPM-81-010. **Evidence groups:** R.

**Expected versus current:** Roadmap intro still says only Sprint 00 completed; frozen original prompts and evolving coverage disagree on 13/14 dependencies and 14/16 decision-log dependencies.

**Action:** Make the new future roadmap authoritative, preserve originals and reconcile every requirement at release. The owning task's acceptance and tests in the plan/roadmap define proof of closure.

## Evidence index

Paths below are existing inspected files, relative to the repository root. New implementation paths elsewhere in this pack are explicitly proposed.

### I — Identity and account setup

- [services/api/ppm_api/identity.py](../../services/api/ppm_api/identity.py)
- [services/api/ppm_api/identity_tables.py](../../services/api/ppm_api/identity_tables.py)
- [services/api/ppm_api/identity_schemas.py](../../services/api/ppm_api/identity_schemas.py)
- [apps/web/app/account/identity-client.tsx](../../apps/web/app/account/identity-client.tsx)
- [scripts/bootstrap_identity.py](../../scripts/bootstrap_identity.py)
- [scripts/local_mailbox.py](../../scripts/local_mailbox.py)
- [tests/test_identity.py](../../tests/test_identity.py)
- [tests/browser/identity.spec.ts](../../tests/browser/identity.spec.ts)

### D — Delivery and project workspace

- [services/api/ppm_api/delivery.py](../../services/api/ppm_api/delivery.py)
- [services/api/ppm_api/ppm_tables.py](../../services/api/ppm_api/ppm_tables.py)
- [services/api/ppm_api/ppm_schemas.py](../../services/api/ppm_api/ppm_schemas.py)
- [apps/web/components/delivery.tsx](../../apps/web/components/delivery.tsx)
- [tests/test_delivery.py](../../tests/test_delivery.py)
- [tests/browser/delivery.spec.ts](../../tests/browser/delivery.spec.ts)
- [docs/contracts/delivery.md](../contracts/delivery.md)

### C — Capacity

- [services/api/ppm_api/capacity.py](../../services/api/ppm_api/capacity.py)
- [services/api/ppm_api/ppm_tables.py](../../services/api/ppm_api/ppm_tables.py)
- [services/api/ppm_api/capacity_schemas.py](../../services/api/ppm_api/capacity_schemas.py)
- [apps/web/components/capacity.tsx](../../apps/web/components/capacity.tsx)
- [tests/test_capacity.py](../../tests/test_capacity.py)
- [tests/browser/capacity.spec.ts](../../tests/browser/capacity.spec.ts)
- [docs/contracts/capacity.md](../contracts/capacity.md)

### A — Assessments

- [services/api/ppm_api/assessment.py](../../services/api/ppm_api/assessment.py)
- [services/api/ppm_api/assessment_tables.py](../../services/api/ppm_api/assessment_tables.py)
- [apps/web/components/assessments.tsx](../../apps/web/components/assessments.tsx)
- [tests/test_assessment.py](../../tests/test_assessment.py)
- [tests/browser/assessment.spec.ts](../../tests/browser/assessment.spec.ts)
- [docs/contracts/assessment.md](../contracts/assessment.md)

### M — Metrics and dashboards

- [services/api/ppm_api/command.py](../../services/api/ppm_api/command.py)
- [services/api/ppm_api/metric_math.py](../../services/api/ppm_api/metric_math.py)
- [services/api/ppm_api/command_tables.py](../../services/api/ppm_api/command_tables.py)
- [apps/web/components/command-center.tsx](../../apps/web/components/command-center.tsx)
- [tests/test_command.py](../../tests/test_command.py)
- [tests/browser/command.spec.ts](../../tests/browser/command.spec.ts)
- [docs/contracts/metrics.md](../contracts/metrics.md)

### J — Jobs and imports

- [services/api/ppm_api/jobs.py](../../services/api/ppm_api/jobs.py)
- [services/api/ppm_api/ingestion.py](../../services/api/ppm_api/ingestion.py)
- [services/api/ppm_api/job_tables.py](../../services/api/ppm_api/job_tables.py)
- [services/worker/ppm_worker/app.py](../../services/worker/ppm_worker/app.py)
- [apps/web/components/integrations.tsx](../../apps/web/components/integrations.tsx)
- [apps/web/components/live-jobs.ts](../../apps/web/components/live-jobs.ts)
- [tests/test_jobs.py](../../tests/test_jobs.py)
- [tests/test_ingestion_mapping.py](../../tests/test_ingestion_mapping.py)
- [docs/contracts/jobs-integrations.md](../contracts/jobs-integrations.md)

### U — Navigation and usability

- [apps/web/components/shell.tsx](../../apps/web/components/shell.tsx)
- [apps/web/components/workspace-home.tsx](../../apps/web/components/workspace-home.tsx)
- [apps/web/app/system/page.tsx](../../apps/web/app/system/page.tsx)
- [docs/learning/Enterprise PPM Website User Testing Guide.docx](../learning/Enterprise PPM Website User Testing Guide.docx>)
- [docs/AI_PPM_FUTURE_PRODUCT_VISION_AND_USER_GUIDE.md](../00-overview/AI_PPM_FUTURE_PRODUCT_VISION_AND_USER_GUIDE.md)

### R — Runtime, source scope and verification

- [services/api/ppm_api/main.py](../../services/api/ppm_api/main.py)
- [services/api/ppm_api/config.py](../../services/api/ppm_api/config.py)
- [services/api/ppm_api/storage.py](../../services/api/ppm_api/storage.py)
- [services/api/migrations/versions/0007_durable_jobs.py](../../services/api/migrations/versions/0007_durable_jobs.py)
- [compose.yaml](../../compose.yaml)
- [.github/workflows/ci.yml](../../.github/workflows/ci.yml)
- [docs/requirements/coverage.md](../requirements/coverage.md)
- [docs/prompts/02-ORDERED-SPRINT-PROMPTS.md](../prompts/02-ORDERED-SPRINT-PROMPTS.md)
- [docs/SPRINT_VERIFICATION_REPORT.md](../04-testing/SPRINT_VERIFICATION_REPORT.md)
- [docs/verification/current-backend-after.txt](../verification/current-backend-after.txt)
- [docs/verification/current-browser.txt](../verification/current-browser.txt)
- [docs/verification/current-runtime.txt](../verification/current-runtime.txt)
- [docs/verification/SPRINT-07-CI-FIX.md](../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md)

## Candidate decisions and exclusions

The requested candidates for project detail, dashboards/comparison drill-down, explainable health, milestones/dependencies, risk register, capacity conflicts, metric evidence, audit history and basic imports already have useful implementations. Extend missing portions under their gap tasks; do not schedule duplicate systems. Decisions, AI assistant/recommendations, broader comparisons and reporting remain original required future work.

Adopted additions are verified signup, invitation lifecycle, onboarding, browser grants, record search/paging, personal work/feed, analytics metadata, general freshness, assessment follow-through, policy lifecycle, unattended connector conflict review and early retention/restore evidence. They are plan recommendations authorized for documentation, not implemented or formally accepted by users. Business benefit, intended users, complexity and milestones are mapped in traceability.

NOT REQUIRED for the current release: SSO/SCIM/custom roles, cross-customer benchmark sharing, live meeting recording, biometric speaker identification, a second UI chart solely to replace working bars with a radar, and every possible alternate provider/database/cloud/model framework. A task-comment/checklist collaboration extension is optional P3; work priority/type and the existing blocker/risk records cover essential capture first. These exclusions do not remove the original graph, forecasts, meetings, transformation, scenarios, passkeys or TTS requirements.

## Assumptions to confirm before implementation

- Public signup is adopted as a desired product completion improvement following the user's account-setup concern. Organization creation must be controlled (verified creator; no global role). If commercial signup is invitation-only by policy, retain a clear request-access entry and explicitly amend G-001 acceptance before implementation.
- Keep the current Admin/PM/Viewer model; no complex enterprise-role engine. Membership revocation and sensitive effort remain explicit.
- Select mail/provider/retention limits and approved storage deployment during the owning task, with no purchase assumed here. Default no-provider mode is honest and usable locally.
- Metadata vocabularies, demo isolation, model eligibility thresholds, SLA calendar and retention/hold policy need a written decision at their task entry; this does not authorize fabricated defaults or history.
- Current reports conflict with stale historical coverage wording. The new crosswalk is the active planning disposition, not a claim that all original acceptance has been independently rerun.
- Calendar estimates require actual team capacity and task sizing. No delivery date can be inferred from sprint numbers.
