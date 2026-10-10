# Current implementation and acceptance

Audited 9 October 2026 (Asia/Calcutta). Code checkpoint: base `9056440` plus the existing dirty working tree; not a committed Sprint 8.1 release. Schema source ends at `0008_pilot_completion`. No runtime/database mutation was performed by this documentation audit.

| Capability | Status | Evidence and limits |
| --- | --- | --- |
| Identity, scoped delivery, resource capacity, rubric assessments, deterministic dashboards | IMPLEMENTED AND VERIFIED | Current modules and retained local sprint checks; broader production claims excluded. |
| Durable jobs, CSV imports, labeled Jira/GitHub fixtures | IMPLEMENTED AND VERIFIED | Sprint 08 report and job tests; fixture success is not live-provider acceptance. |
| Signup, setup/profile, browser grants, scoped record search, paging/comparison, My work/notifications, optional metadata, authorized refresh | IMPLEMENTED AND VERIFIED | PPM-81-001 and 003–009 have current source and recorded local acceptance. |
| SMTP delivery to a real inbox | VERIFIED IN DEVELOPMENT | Development SMTP enabled; verified STARTTLS/authentication pass and signup reached provider_accepted. Signup receipt in Spam and verified Admin activation confirmed; recovery accepted by provider, with recovery completion confirmed by recipient; existing-account invitation acceptance and correct Viewer membership are confirmed. |
| Sprint 8.1 closure | PARTIALLY IMPLEMENTED | 8 of 10 tasks complete locally; 002 external mail gate and 010 CI/Word visual gates remain open. |
| Current hosted CI and regenerated Word layout | IMPLEMENTED BUT UNVERIFIED | Workflow/document artifacts exist; current revision CI and every-page visual acceptance are not established. |
| Live Jira/GitHub sync | BLOCKED | Explicit credentials/provider acceptance required; do not present fixtures as customer integration. |
| Versioned document library, OCR, retrieval, AI gateway/agents/copilot, predictive models | PLANNED | Sprints 09–14. Existing plain-text assessment evidence is a narrower implemented feature. |
| Approvals, transformation, simulations, graph, broad benchmarking, meetings, reports/alerts/passkeys, production release | PLANNED | Sprints 15–23; current departmental comparison is a narrow local capability. |
| Optional unadopted additions and alternative stacks | NOT IN SCOPE | Only adopted required scope counts toward release; see the release criteria. |

Verification means the named behavior has source plus **retained successful local evidence**, not a new full rerun or production certification. BROKEN requires demonstrated failure; an unrun check is not a defect. Read [Sprint 8.1 evidence](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md) for exact commands, counts and blockers; [catalogue](FEATURE_CATALOGUE.md) for feature-level scope.

## Current limits

10 October 2026 account-email update: message templates explain the organization/role, action, expiry and recovery path; SMTP configuration is validated, provider recipient refusals are failures, and website status separates local previews from provider acceptance. Expired pending invitations can be resent. See [verification report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) and [operator setup](../07-setup-and-deployment/EMAIL-DELIVERY.md). The user configured credentials privately and explicitly authorized the sender and sole recipient. Development services were rebuilt/restarted successfully in SMTP mode after confirming an empty queue. The initial incomplete credential caused Gmail authentication rejection (535); after private correction/reload, verified STARTTLS/authentication pass (235) and the existing website signup email reached provider_accepted. The queue is empty. The recipient confirmed signup arrival in Spam and completed activation; a scoped read confirms verified active Admin membership. Recovery was requested through the website and reached provider_accepted on attempt 1. The recipient confirmed successful recovery; the newest reset challenge is consumed. The separately authorized sender-inbox test Admin signup arrived in Inbox and was activated. It sent a Viewer invitation through the website; the personal recipient confirmed arrival in Spam and acceptance/sign-in. The website and scoped database read confirm the new active Viewer membership while the original organization retains Admin membership. Unrelated acceptance statuses are unchanged.

Command snapshots bound inputs to 200 projects, 100 assigned resources and 5,000 rows per loaded source kind, with 1–366-day periods. Sprint 8.1 selectors page on the server; that does not remove snapshot limits. Department comparison uses a selected framework version and the full authorized UTC creation-period cohort, not only the displayed page. SSE polls authorized revisions each second; this has a per-connection query cost and is not a production scalability proof.

Assessment evidence remains bounded UTF-8 text with manual release. Notification receipts show 30 days; this is presentation retention, not physical purge. Registration creates organization/membership only after verification; local mode needs private operator mailbox access. Production environment is rejected by configuration. Real data, provider credentials and deployment proof remain external acceptance obligations.


## 10 October 2026 account and website repair follow-up

Current local schema head is `0010_account_authority`. Global account status, organization-free personal sessions, organization profile editing, visible calendar navigation, trusted business errors and the scoped Hement correction are implemented. Guarded Northstar training data is provisioned independently of existing organizations. [Current verification and walkthrough inventory](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) give actual results. Production, live connector acceptance and the planned AI/document-intelligence phases retain their existing gates.
