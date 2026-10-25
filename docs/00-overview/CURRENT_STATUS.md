# Current implementation and acceptance

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

**25 October 2026 quota update:** verified Gemini's configured free quota and Puter's
remaining monthly credit, then activated 50 requests/day per provider account in
the local pilot. All nine role routes passed in the running API and worker. Scope,
usage history, pacing and $0 policy are preserved. Puter throughput remains subject
to token costs and monthly credit. [Evidence](../limitations/QUOTA_REVIEW.md).

**Latest access update, 24 October 2026:** normal schema **0016** is deployed and
healthy. Alok Gupta, Hement, Blaze and Ashu have demo membership and project-scoped
guided permission; existing business roles are preserved. Explicit bounded data
approval was received and cloud scope now includes Customer Onboarding Portal
plus the synthetic demo.
[Access and verification](../limitations/USER_ACCESS.md) supersedes the schema/test
counts in the preceding limited-mode checkpoint below. Broad AT17 stays blocked.

**24 October 2026:** [limited guided review](../limitations/IMPLEMENTATION_REPORT.md)
is deployed locally on schema 0015 with preserved existing data and a separate
synthetic demo. Nine manual checklists work immediately; one optional API selection
per run is enabled for the explicitly approved synthetic demo only. One live request
each to Gemini/Puter/Groq succeeded; [receipt](../limitations/LIVE_API_VERIFICATION.md). Backend
509 passed/one skipped; two browser journeys passed. Broad accuracy AT17 remains
blocked. See [usage](../limitations/TRY_IT_NOW.md) and
[known limits/future solutions](../limitations/LIMITS_AND_FUTURE_SOLUTIONS.md).
Earlier versions and deployment states below are historical.

PR #3 review follow-up — 16 October 2026: [four review fixes and CI corrections](../04-testing/sprint-based/sprint-11/REVIEW_FIXES.md)
are on `sprint-11-specialist-review`. Forward 0014 preserves existing migrations;
normal database remains 0012. The requested output-budget increase is deferred
under the unchanged-limits constraint. Earlier checkpoint statements follow.

Current — 16 October 2026: Sprint 11 specialists, separate semantic maturity suggestions and recommendation review are implemented for deterministic local acceptance. [Report](../03-sprints/completed/sprint-11/SPRINT_REPORT.md) and [fresh validation](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) are authoritative. Real-provider semantic quality UNVERIFIED/BLOCKED; production/scale remain open. Normal database 0012 preserved, additive 0013 tested in disposable databases. No deployment/commit; stop before Sprint 12.

## Historical checkpoints before Sprint 11

**16 October 2026 update:** [Gemini free-tier support](../07-setup-and-deployment/GEMINI-FREE-TIER.md)
is authorized at $0 on a user-confirmed project with no linked billing account.
A real synthetic exact-excerpt completion and 256-dimension embedding smoke passed.
This supersedes the authorization restriction in the original checkpoint below;
general model-quality and production acceptance remain open. No new migration.

Current checkpoint — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope at `0012_ai_runtime`. Reviewed application checkpoint `631c149` passed hosted CI; 201 backend tests and the document browser regression passed. A current pilot Word guide is rendered and visually verified. Gemini bounded completion/embedding smoke passed at maximum spend $0; confirmation does not expire daily. Production deployment, scale and broad agent/model quality remain OPEN release/successor gates. Sprint 11 is not started. Stop before 11.

| Capability | Status | Evidence and limits |
| --- | --- | --- |
| Identity, scoped delivery, resource capacity, rubric assessments, deterministic dashboards | IMPLEMENTED AND VERIFIED | Current modules and retained local sprint checks; broader production claims excluded. |
| Durable jobs, CSV imports, labeled Jira/GitHub fixtures | IMPLEMENTED AND VERIFIED | Sprint 08 report and job tests; fixture success is not live-provider acceptance. |
| Signup, setup/profile, browser grants, scoped record search, paging/comparison, My work/notifications, optional metadata, authorized refresh | IMPLEMENTED AND VERIFIED | PPM-81-001 and 003–009 have current source and recorded local acceptance. |
| SMTP delivery to a real inbox | VERIFIED IN DEVELOPMENT | Development SMTP enabled; verified STARTTLS/authentication pass and signup reached provider_accepted. Signup receipt in Spam and verified Admin activation confirmed; recovery accepted by provider, with recovery completion confirmed by recipient; existing-account invitation acceptance and correct Viewer membership are confirmed. |
| Sprint 8.1 closure | COMPLETED DEVELOPMENT SCOPE | Ten work packages accepted for the pilot; retained local checks, development Gmail journeys, hosted CI and current Word-guide visual QA. See [closeout](../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md). |
| Reviewed hosted CI and current pilot Word layout | VERIFIED | CI run 38885041673 succeeded at `631c149`; the current pilot Word edition was rendered and every page visually inspected. Older Word snapshots retain their historical status. |
| Live Jira/GitHub sync | BLOCKED | Explicit credentials/provider acceptance required; do not present fixtures as customer integration. |
| Versioned document library, English OCR, keyword retrieval/citations | IMPLEMENTED AND VERIFIED LOCALLY | `/documents`, source versions/locations, real ClamAV, scoped history/downloads and same-byte assessment links; [guide](../03-sprints/completed/sprint-09/USER_GUIDE.md). |
| Policy registry and document retention/pilot restore | IMPLEMENTED AND VERIFIED LOCALLY | Admin owner/applicability/dates/state, holds, deletion/eligible purge and synthetic scratch recovery; approvals remain 15, production backup erasure/recovery remain 22/23. |
| Shared AI gateway, bounded embeddings/hybrid, orchestration, Admin controls | IMPLEMENTED AND VERIFIED LOCALLY | Recorded 150 backend / 16 browser / 12 offline baseline cases; Gemini free-tier smoke and later 63 AI/provider regressions passed. $0, no daily renewal; broad retrieval/model quality unverified. |
| Agents/copilot and predictive models | PLANNED | Sprints 11–14; no semantic findings or automatic edits. |
| Approvals, transformation, simulations, graph, broad benchmarking, meetings, reports/alerts/passkeys, production release | PLANNED | Sprints 15–23; current departmental comparison is a narrow local capability. |
| Optional unadopted additions and alternative stacks | NOT IN SCOPE | Only adopted required scope counts toward release; see the release criteria. |

Verification means the named behavior has source plus **retained successful local evidence**, not a new full rerun or production certification. BROKEN requires demonstrated failure; an unrun check is not a defect. Read [Sprint 8.1 evidence](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md) for exact commands, counts and blockers; [catalogue](FEATURE_CATALOGUE.md) for feature-level scope.

## Current limits

10 October 2026 account-email update: message templates explain the organization/role, action, expiry and recovery path; SMTP configuration is validated, provider recipient refusals are failures, and website status separates local previews from provider acceptance. Expired pending invitations can be resent. See [verification report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) and [operator setup](../07-setup-and-deployment/EMAIL-DELIVERY.md). The user configured credentials privately and explicitly authorized the sender and sole recipient. Development services were rebuilt/restarted successfully in SMTP mode after confirming an empty queue. The initial incomplete credential caused Gmail authentication rejection (535); after private correction/reload, verified STARTTLS/authentication pass (235) and the existing website signup email reached provider_accepted. The queue is empty. The recipient confirmed signup arrival in Spam and completed activation; a scoped read confirms verified active Admin membership. Recovery was requested through the website and reached provider_accepted on attempt 1. The recipient confirmed successful recovery; the newest reset challenge is consumed. The separately authorized sender-inbox test Admin signup arrived in Inbox and was activated. It sent a Viewer invitation through the website; the personal recipient confirmed arrival in Spam and acceptance/sign-in. The website and scoped database read confirm the new active Viewer membership while the original organization retains Admin membership. Unrelated acceptance statuses are unchanged.

Command snapshots bound inputs to 200 projects, 100 assigned resources and 5,000 rows per loaded source kind, with 1–366-day periods. Sprint 8.1 selectors page on the server; that does not remove snapshot limits. Department comparison uses a selected framework version and the full authorized UTC creation-period cohort, not only the displayed page. SSE polls authorized revisions each second; this has a per-connection query cost and is not a production scalability proof.

Assessment evidence remains bounded UTF-8 text with manual release. Notification receipts show 30 days; this is presentation retention, not physical purge. Registration creates organization/membership only after verification; local mode needs private operator mailbox access. Production environment is rejected by configuration. Real data, provider credentials and deployment proof remain external acceptance obligations.


## 10 October 2026 account and website repair follow-up

The 10 October follow-up reached `0010_account_authority`; Sprint 09 subsequently advanced the normal head to `0011_document_sources`. Global account status, organization-free personal sessions, organization profile editing, visible calendar navigation, trusted business errors and the scoped Hement correction are implemented. Guarded Northstar training data is provisioned independently of existing organizations. [Current verification and walkthrough inventory](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) give actual results. Production and live connector acceptance retain their gates. Document intake/OCR/keyword retrieval are now local Sprint 09 capabilities; AI interpretation remains planned.

## Sprint 09 evidence and limits

The full backend/lifecycle run passed 123 cases. Focused source/parser acceptance passed
24, final security passed nine and the final chunk boundary passed one. Fourteen browser
regressions passed in the full run; after repairing the new document flow, its affected
scenario passed separately. This is not a claim of a single all-green combined browser run.
Static/contract checks and npm/locked Python vulnerability audits passed. Local data
preservation used a fresh quiesced checkpoint after one legitimate refresh-token row
appeared while the previous stack was live; that row was retained. Recovery used new
scratch targets only. [Exact evidence and failures](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md).

The optional ClamAV override must be healthy for intake; unavailable scanning quarantines
without a manual bypass. Sources are bounded to 8 MiB, with strict parser limits and
English OCR. Only latest ready versions participate in keyword search. Workforce notes
are excluded; private assessment evidence keeps independent authority. Policy labels use
UTC calendar dates, not a compliance certification. Pilot retention is 30 days; production
storage, backup erasure, performance/availability, hosted CI and Word visual QA remain open.
