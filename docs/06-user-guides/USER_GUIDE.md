# Current user guide

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

Use the local history/dataset/baseline walkthrough linked from the closeout and
`/integrations` for authority/conflict review. Synthetic results are not real accuracy;
existing guided-provider quotas, access and $0 controls remain unchanged.

## Local history and baseline lab

[Use Sprint 12](../03-sprints/completed/sprint-12/USER_GUIDE.md): connector approval/conflict review in `/integrations`; versioned manual history, isolated synthetic examples, as-of datasets and reproducible baseline model cards in `/ml`. Research actions require Admin; no external data scope or business permission expands.

Sprint 11 adds **Agents & recommendations** at `/agents`: [role-specific steps](../03-sprints/completed/sprint-11/USER_GUIDE.md). Inspect exact evidence, compare original/suggested/approved maturity and record independent accept/reject decisions. Acceptance never applies a project change. Missing providers/agents/evidence remain explicit; real-model quality is unverified. Normal runtime adoption requires the tested forward 0013 migration; this task does not deploy it.

## Historical checkpoints before Sprint 11

Availability: **IMPLEMENTED AND VERIFIED** within retained local checks. Production acceptance remains open. Use [current status](../00-overview/CURRENT_STATUS.md) and [the catalogue](../00-overview/FEATURE_CATALOGUE.md) for exact scope. For complete Sprint 8.1 steps and recovery limits, use [the pilot tester guide](../03-sprints/completed/sprint-8.1/SPRINT_8_1_USER_GUIDE.md).

For a self-contained organization, member, project and assessment exercise, use the [detailed website manual](WEBSITE_WALKTHROUGH.md). Development Gmail SMTP signup, existing-account invitation acceptance and recovery are verified. Personal signup arrived in Spam; test-Admin signup arrived in Inbox. The accepted invitation created the correct Viewer membership without changing the account's Admin role in its original organization. Check Inbox and Spam; provider acceptance alone does not prove inbox arrival. See [email verification](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md).

To add a Project Manager, sign in as the intended organization's Admin, open Account & access → Invite a member, enter their accessible email, select **Project Manager** and create the invitation. They accept the email privately and then sign in. To promote an existing Viewer instead, change their role in Organization members, keep Active checked, save and confirm. Give the PM the relevant work grants afterward: portfolio manage for project creation, project edit/manage for delivery, Resource access for staffing, and framework/assessment permissions for assessment work. Follow the [detailed role and access guide](MEMBERS_ROLES_AND_ACCESS.md) for every website step, access tests and revocation.

Ordinary members need no terminal or Docker. The person running the application uses the separate [Gmail SMTP setup document](../07-setup-and-deployment/GMAIL-SMTP-SETUP.md).

| User / purpose | What to do | Needed information | Expected result and limitation |
| --- | --- | --- | --- |
| New user: join/create organization | Open `/signup`, request verification, open the email privately, choose name/password, sign in | Accessible email and organization name; check Inbox and Spam | Organization created only after verification; Gmail delivery is verified on this development instance |
| Admin: configure access | Open `/account`, edit organization profile; invite/manage members; use project Grants/resource access/framework or completed-result Access | Correct organization and grant scope | Saved membership/grants; ownership alone never grants access; private effort remains separately scoped |
| PM: plan delivery | Admin creates portfolio and grants portfolio manage; PM creates a project at `/projects`, then opens its name and tabs | Name, portfolio, valid dates/currency, optional metadata; project grants for existing projects | Stored project/work/milestones/risks; archive checks active dependents; stale revision must be reloaded |
| PM: manage staffing | Admin creates resource/calendar/access; PM opens `/resources` to manage permitted availability/allocations and explicitly granted effort | Resource profile, working dates/hours and project permission | Deterministic capacity or Unknown for missing schedule/scope; login account and workforce profile differ |
| Assessor/reviewer: evaluate maturity | Admin creates/publishes framework and assigns different active Admin/PM members; named respondent saves/submits; named reviewer reviews/completes | Published version, assignment, required answers/evidence | Preserved results/history; adjustments require reasons; Viewer cannot submit evidence or assess; no AI scoring |
| Executive/Viewer: inspect portfolio | Open `/command-center`, choose permitted scope/period/view and inspect source drawer | Authorized records and compatible currency/period | Explainable deterministic measures with coverage/Unknown; not a predictive probability or complete historical reconstruction |
| All permitted users: find work | Ctrl K / search button → Find a record → type/query → page → open | Active organization, record query/type | Older permitted records discoverable; owning page rechecks access |
| Assigned user: follow up | Workspace My work; Notifications → mark read/preferences | Assignment and permitted target | Persistent in-app receipts shown for 30 days; scheduled/external notifications PLANNED |
| Import operator: load supported data | Open `/integrations`; choose configured fixture/CSV destination and mapping, preview/run/check job | Authorized project, supported columns, file and adapter mode | Durable job outcomes/rejected rows; real Jira/GitHub credentials are BLOCKED external acceptance |

## Recovery and unavailable experiences

Account email: after a verified real-email setup, check Inbox and Spam; verification/invitations expire in 24 hours and recovery in 30 minutes. Admin uses Pending invitations → Refresh invitations to see queued, provider-accepted, failed or local-preview status. Resend invalidates the old invitation; Cancel blocks acceptance; expired invitations can be resent. An invalid completion link offers signup/recovery replacement links and instructions to ask Admin for a new invitation. In local mode users still require private operator assistance. Operator configuration is in [Email delivery](../07-setup-and-deployment/EMAIL-DELIVERY.md).

Wrong organization or absent grant can hide a row; recheck Account and access rather than changing IDs. Keep separate browser profiles for different users. On 401 sign in/refresh; on stale revision reload before editing. Unknown metrics need source/calendar/coverage corrections, not invented zeros. Failed imports expose bounded diagnostics through their job surface. Local challenge links are private, expire and cannot be replayed.

**IMPLEMENTED, verification in progress:** /ai disabled source previews and Admin controls (10), Gemini free-tier smoke verified; broader quality unverified. **PLANNED:** agents (11), predictive models (12–13), project/multi-project copilot (14), approvals/reminders (15), transformation/scenarios/graph/benchmarks/meetings (16–20), reports/exports/alerts/audio (21), passkeys/lifecycle (22), production recovery/deployment (23). There is no executable AI assistant or report-export demo at this checkpoint. Follow [approved future scope](../09-planning/FUTURE_SPRINT_ROADMAP.md); optional additions are not guaranteed.


## Account and setup repair — 10 October 2026

The organization profile now shows read-only name, saved description/industry/website, live administrators, member counts and operating settings. Use **Edit name** to enter Save/Cancel mode. Resource planning exposes **Working calendars** directly; create immutable schedule versions and reference them from dated availability. Field and business-rule errors retain their specific explanations.

Membership removal denies only that organization and preserves the global account; no-membership accounts can sign in and manage their own profile/sessions. Existing-project sprint writes need explicit project edit/manage access. See [the full walkthrough](WEBSITE_WALKTHROUGH.md), [training provisioning](../05-demos/WALKTHROUGH_DATA.md), and [current verification](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md).

## Document library — Sprint 09

Open **Document library** (`/documents`). Admin or a PM with project edit/manage can
upload categorized PDF/scans, DOCX, TXT/CSV/XLSX or PNG/JPEG up to 8 MiB. Viewer reads
only permitted sources; ownership grants no access. Wait for Ready, open a paged source
location, search keywords, verify a citation, download the original or append a version.
Missing scanner quarantines; ask the operator to restore health and explicitly reprocess.
Follow the [canonical library guide](../03-sprints/completed/sprint-09/USER_GUIDE.md) for
every step, private assessment references, Admin policy/hold/deletion/purge and recovery.
Semantic extraction, embeddings and policy approval are not available in this slice.
## AI evidence preview — Sprint 10

Open AI operations & evidence as Admin to retrieve a permitted project source
preview, inspect no-key diagnostics and manage a zero-spend tenant budget. Follow
[the current steps](../03-sprints/completed/sprint-10/USER_GUIDE.md). Keyword excerpts are labeled source_fallback; no match
stays unavailable. Index embeddings and real model answers remain disabled until
explicit provider/model/spend authorization. PM/Viewer use the document library;
restricted Admin diagnostics are inaccessible. No semantic agents or plan edits.
