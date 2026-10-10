> Planning update (2026-10-09): this review is retained as audit history. The authoritative proposed execution plan is [Sprint 8.1](../09-planning/SPRINT_8_1_PLAN.md) and [future roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md); A01–A18 are reconciled in [traceability](../09-planning/FEATURE_GAP_TRACEABILITY.md). No feature implementation is implied.

**Historical/proposed reference:** Current availability is [CURRENT_STATUS](../00-overview/CURRENT_STATUS.md); current architecture is [SYSTEM_ARCHITECTURE](../01-architecture/SYSTEM_ARCHITECTURE.md); future execution order is [the revised roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md). Preserve dated decisions/scope below; proposed components are not implementation claims.


# Review of all sprint plans

Reviewed on 9 October 2026. Covers Sprints 00 through 23.

The plan includes the eight main modules and the advanced features in the original specifications. The bigger weakness is the complete user journey: creating an account, setting up an organization, inviting people, finding records, receiving reminders and sharing results. Some of these steps have no clear owner; others arrive much later than the features that need them.

Public sign-up is a recommended addition. The original specifications required authentication and organization access, but did not explicitly request open registration. The Sprint 02 prompt deliberately chose a controlled first-Admin setup. Its absence is a product usability gap, not evidence that an explicit original sign-up requirement was dropped.

This is a planning review, not a new application test or implementation. The latest handoff reports Sprint 08 complete locally. Future features remain planned. The existing roadmap, sprint prompts and completion records have not been rewritten by this review.

## What was checked

- Both preserved source specifications, including all named modules, agents and advanced features.
- Every ordered sprint prompt, 00 through 23, and the master instruction.
- The roadmap, requirement coverage, product journeys, decisions, data model and quality plan.
- Relevant current account, navigation, assessment and integration contracts and code to distinguish a missing plan from a known implementation boundary.
- The separate prompt-pack copy and repository copy of the ordered sprint prompts. Their file hashes match.

The review uses three labels:

- **Missing or unclear:** no explicit complete user flow or owning sprint was found.
- **Already planned but late or incomplete:** retain the feature and improve its timing or handoff.
- **Recommended addition:** useful product behavior beyond the explicit original requirements.

## Changes to prioritize

| Priority | Change | Why it matters | Suggested place |
| --- | --- | --- | --- |
| First | Sign-up and first organization setup | A new tester cannot start using the website independently | New 02A repair sprint |
| First | Working invitation and password recovery delivery | People should not need someone to retrieve private links from a terminal | 02A |
| First | Organization settings and understandable access setup | The Admin needs to finish setup and know who can use each project | 02A and 04A |
| First | Search actual records and show personal pending work | Users need to find projects and understand their next action | 03A and a small 08A usability sprint |
| Before Sprint 09 | Define how assessment evidence uses the document library | Avoid two disconnected upload systems | Add explicit scope to 09 |
| Before Sprints 09 and 10 | Clarify document processing versus shared AI calls | The current plan asks for embeddings before the shared AI runtime exists | Clarify the 09 to 10 handoff |
| Before Sprints 11 and 15 | Define what accepting a suggestion does | A reviewed suggestion must not become an unexplained or unauthorized record change | Clarify 11 and extend in 15 |
| Before Sprints 12, 14 and 19 | Add the information needed by models and comparisons | Some planned questions refer to fields the core app does not yet collect | 04A, 08A and 12 |
| Earlier than 21 | Basic downloadable reports | Users should be able to share current project and assessment results | 07A or 08A; retain scheduled reporting in 21 |
| Before real data and scheduled processing | Retention rules and unattended job ownership | Uploaded data and scheduled work need explicit lifecycle rules | 08A, 09 and 20; final audit in 22 and 23 |

02A, 03A, 04A, 07A and 08A are proposed repair labels. They are not existing completed sprints and have no approved dates. They preserve the original numbering and avoid rewriting accepted migrations or historical reports.

## Detailed findings

### A01 New account and first organization setup

**Missing complete user journey; recommended addition.** Sprint 02 contains login, invitations, activation and recovery, but uses a separate first-Admin setup. There is no planned browser journey that starts with Sign up.

Add Sign up, email verification, name and password entry, organization creation, timezone and currency setup, and a short welcome checklist. Keep joining an existing organization invitation-based. An invited person should land in the organization that invited them, rather than accidentally create another one. Allow an installation to disable open sign-up if it is intended for a closed company.

**Owner:** 02A, with the setup checklist in 03A/04A. **Done when:** a new person can create and enter their own test organization through the website; another person can accept an invitation without setup commands.

### A02 Account messages and invitation management

**Already partly planned, but delivery ownership is unclear.** Sprint 02 explicitly allows a local mailbox and leaves real email unverified. Sprint 21 owns report and alert email, but does not explicitly complete identity-message delivery. A local mailbox is useful for development; it is not a complete ordinary-user invitation experience.

Add an identity email delivery owner, delivery failure messages, resend verification, resend invitation, cancel invitation, pending invitation status and an expired-link recovery screen. Password reset must use the same usable delivery path. Keep a clearly labeled local demonstration option when real email is not configured.

**Owner:** 02A. **Done when:** an Admin can see pending invitations, resend or cancel one, and an invitee or password-reset user can complete the flow without a terminal operator. Real-provider checks must be recorded separately from local demonstrations.

### A03 Organization and account lifecycle

**Missing or unclear beyond basic setup.** Organization configuration stores timezone/currency and membership administration exists, but the plan does not clearly cover renaming the organization, leaving it, changing an account email or handing over responsibility when its administrator leaves.

Add organization-name editing, verified email change, leave-organization behavior and a guided Admin handover. Preserve the last-active-Admin protection already built. Explain the effect of archive or closure on retained history before offering organization closure. Organization closure can remain a release-stage feature; the everyday settings and handover should come earlier.

**Owner:** 02A/04A; closure policy before 23. **Done when:** Asha can hand over administration to another active member and leave without orphaning the organization; an email change preserves the correct memberships.

### A04 Permission setup that an Admin can understand

**Recommended usability addition.** Project grants, resource management and private effort access are already present. Assessment respondent/reviewer assignments are also explicit. These are not missing security features. The problem is that selecting someone as project Owner or adding them to a team does not necessarily give them the access a user expects.

Add an Access screen or guided step that shows who can view, edit and manage a project, who can plan a resource and who can see private hours. Show a short explanation when a person lacks access. Offer explicit access assignment while creating a project instead of requiring a later hunt through separate records.

**Owner:** 04A/05 follow-up. **Done when:** the Admin can give Rohan project edit access from the project screen and can see why a Viewer cannot edit. Owner selection must not silently grant private timesheet access.

### A05 Search actual project and document records

**Missing explicit ownership.** The product scope calls for scoped search. Sprint 03 builds a top search entry and command palette, but the current search finds destinations such as Projects, not project records. Individual list filters do not complete the global search journey.

Assign ordinary record search to a sprint. Start with projects, portfolios, resources and assessments. Add document search in 09. Show the record type and open the matching authorized record. Search should cover the permitted records, not just the currently loaded page. Keep navigation commands as a separate useful function.

**Owner:** 03A/08A, extended in 09. **Done when:** searching Customer Portal finds the actual project, while a person without ERP access cannot find ERP records or snippets.

### A06 Personal work and notification inbox

**Already partly planned, but late and underspecified.** Sprint 03 owns a notification shell, 15 owns an approval inbox and reminders, and 21 owns external delivery. The bell currently states that notifications are not connected. The plan does not explicitly define a shared feed with unread state and direct links to pending work.

Add My work for assigned tasks, assessments and reviews, plus a persistent notification feed with read/unread state and clear action links. Introduce basic assignment and due-date notices after the durable job system. Add configurable approval escalation in 15, and email/Slack delivery in 21. A simple assessment reminder should not wait for the AI agents.

**Owner:** 08A for the basic feed; 15 and 21 extend it. **Done when:** Rohan sees his assigned assessment and Meera sees the review waiting for her; reading a notification does not complete the task.

### A07 Everyday task collaboration

**Recommended addition, not an omitted original requirement.** Sprint 04 builds tasks and a work board, but does not explicitly include comments, mentions, checklist items or priority. An audit record tells users that a field changed; it is not a place to discuss the work.

Add task priority and comments first. Add mentions through the notification system. Checklists and task attachments are useful later additions; avoid expanding into a full ticketing product unless needed. Link attachments to the document system rather than creating another upload store.

**Owner:** 04A for priority/comments; mentions after 08A; attachments after 09. **Done when:** a user can ask a question on Build Sign In, mention its assignee and retain the discussion with that task.

### A08 Information required by later questions and comparisons

**Missing cross-sprint data requirements.** Sprint 14 explicitly promises a question about delayed fintech projects. Sprint 19 compares by methodology, project size and work type. Sprint 12 uses bug counts and scope changes. The current typed project/work-item forms do not collect explicit industry, methodology, size category or issue type. The future prompts do not clearly assign all those fields or their mapping rules.

Define a small set of needed fields: industry, delivery methodology, project size category, work type and issue type where used. Define how scope-change history is measured rather than assuming ordinary current task records reconstruct the past. Add field choices to forms and connector mappings. If a field is unavailable, the assistant must say so instead of guessing it from a project name.

**Owner:** 04A/08A; historical definitions in 12. **Done when:** an authorized fintech project can be filtered correctly, and benchmarking can explain which recorded fields made projects comparable.

### A09 Connect assessment evidence to the document library

**Missing integration handoff.** Sprint 06 has assessment-specific text uploads. Sprint 09 adds PDF, Word, spreadsheet and OCR document handling. The plan does not explicitly say how an assessment chooses an approved library document, how older attachments remain usable or how a completed assessment preserves its exact evidence version.

Add Attach existing document and Upload new evidence through a common reviewed document flow. Preserve the original text evidence and permissions. Completing an assessment should depend on the attached document being approved for that use, not merely on a file having uploaded successfully. Define the behavior when source access changes or a document is deleted.

**Owner:** 09 with assessment regression checks. **Done when:** Rohan can attach a permitted Word charter to an assessment, Meera can inspect it, and the completed result retains the exact reviewed version.

### A10 Assessment dates and repeated measurement

**Recommended addition.** Sprint 06 covers assignment, answers, review and compatible department comparisons. Sprint 19 adds broader comparisons. Neither clearly owns recurring assessments, due dates, reassignment or a simple view of improvement over time.

Add a due date and explicit reassignment first. Add a repeat-assessment action that creates a new assessment, plus a history view comparing compatible results over time. Label framework changes so users do not mistake unlike question sets for a genuine improvement or decline. Use the shared reminders instead of a separate assessment scheduler.

**Owner:** assessment follow-up with 08A/15 reminders; trends can extend 19. **Done when:** Engineering can repeat the same framework next month and compare approved results without modifying the earlier assessment.

### A11 Governance policy management

**Missing clear feature owner.** The original specification names GovernancePolicies; the data model says a policy has immutable versions and may be represented by a document. Sprint 09 handles policy documents, and 11/16 use policies and propose governance structures. Those do not fully define an Admin's policy management screen or lifecycle.

Add policy name, owner, draft/published/retired state, version, effective date, next review date, applicable departments and linked evidence. Decide whether employee acknowledgment is actually needed; it is an optional extension, not an original requirement. Agents should use an identified applicable policy version, not simply any uploaded file that looks like a policy.

**Owner:** 09 for the policy library and versions; approval rules in 15; intelligence in 11/16. **Done when:** an Admin publishes a policy and a Governance finding points to the applicable version.

### A12 Document processing before the shared AI runtime

**Sequencing ambiguity.** Sprint 09 asks for versioned embeddings, hybrid retrieval and extracted candidates. Sprint 10 depends on 09 and introduces the common completion/embedding provider runtime. The coverage matrix correctly places semantic extraction in 11, but the Sprint 09 wording is broader than that distinction.

Make the handoff explicit: 09 owns uploads, parsing, OCR, document versions, access and keyword retrieval, with a defined embedding/candidate interface. 10 wires provider-backed embedding calls through the common usage and budget controls. 11 supplies semantic candidate extraction. Alternatively, establish the minimal shared embedding adapter before 09 and reuse it in 10. Do not create two unrelated provider-call systems.

**Owner:** revise the scope notes for 09, 10 and 11 before implementing 09. **Done when:** each promised 09 capability has an available dependency or is explicitly identified as the later 10/11 extension.

### A13 Accepting a recommendation before general workflows exist

**Missing explicit handoff, not permission to skip approval.** Sprint 09 puts findings in a review queue; 11 builds recommendation review; 15 supplies general approved actions. What Accept means in the earlier screens needs to be stated.

Define Draft, Accepted, Rejected and Applied separately. In 09/11, acceptance can record a review decision while leaving application to a clearly identified later action, or support a narrowly specified manual conversion with existing access checks. In 15, approved actions may create or update live records. Review acceptance alone must not be shown as successful execution.

**Owner:** 11, extended in 15. **Done when:** accepting a proposed risk shows exactly whether it is only accepted or has become a real risk record, and repeating the action does not create duplicates.

### A14 Unattended integrations and useful conflict recovery

**Known incomplete production flow.** Sprint 08 protects connector writes by rechecking the initiating Admin's session. This is intentional and documented, but jobs stop when that session expires or is revoked. Local edits to imported records are correctly rejected as conflicts. The plan needs a complete long-running owner and resolution journey before promising unattended sync.

Define who owns an integration after its creator leaves, how authorized credentials are renewed and which permission governs scheduled runs. Add a connect/test/disconnect experience where supported, without making a specific OAuth method mandatory for every provider. Explain conflicts with a comparison of source and local values, and offer an explicitly authorized resolution. Keep existing protection against silent overwrites.

**Owner:** 08A; required before unattended integrations or schedules are released. **Done when:** a connector can be safely handed over, an expired owner is clearly reported, and a user can resolve an import conflict through a documented flow. Live providers still need their own verification.

### A15 Live updates for ordinary edits

**Already planned at the product level; current scope is narrower.** The Sprint 08 coverage row explicitly limits acceptance to authorized sync-stage dashboard refresh. It states that other mutation broadcasts are outside that slice. A work-item or budget edit is not necessarily an integration job.

Assign general refresh/invalidation to an owner. Cover manual project edits, resource allocations, assessment completion and risk changes, not only imported data. Each later sprint must publish or invalidate the relevant visible information. Full reload should remain a reliable fallback.

**Owner:** 08A shared contract, adopted by subsequent modules. **Done when:** an authorized dashboard updates after another user edits a relevant source record; hidden-project events reveal no record details.

### A16 Basic sharing and reports arrive too late

**Already planned but late.** Sprint 21 includes PDF/HTML reports, weekly summaries and audio. Current command-center JSON download is not the simple project or assessment report most users expect. User/admin guides are also explicit final deliverables in 23, despite usability being needed much earlier.

Add an on-demand project summary and an approved assessment result download before the AI layer. Add printable dashboard or CSV export where it helps the actual user. Keep scheduled email, Slack and audio in 21. Maintain a short user guide and demo walkthrough when a feature ships, with fictional data and actual account-activation instructions.

**Owner:** 07A/08A; advanced delivery stays 21. **Done when:** a user can share the authorized current project summary and approved assessment results without exporting raw technical data.

### A17 Data retention and deletion before real intake

**Already planned, but the defaults and ownership must arrive earlier.** Upload deletion and retention are in 09/20; tenant retention settings and a broad audit are in 22; restore checks are in 23. Existing contracts explicitly retain local objects and job history. This is not a finding that all deletion controls are absent.

Define archive versus permanent removal, evidence retention, document/audio removal and cleanup of derived search results before real intake. State what remains for history and why. Add a restore exercise before a real-user pilot rather than relying only on the final release sprint. Preserve immutable financial and completed-assessment history; a generic Delete everything button is not a suitable replacement.

**Owner:** per-module rules in 08A/09/20; full verification in 22/23. **Done when:** a removed document stops appearing in retrieval, authorized history follows the recorded policy, and a backup can be restored before real users depend on the data.

### A18 Keep the roadmap and status records coherent

**Confirmed planning/documentation inconsistencies.** The roadmap introduction still says only Sprint 00 is authorized and completed, while the latest handoff reports Sprint 08 complete locally. This is historical text presented too close to current status. Coverage F-075 to F-077 lists Sprint 13 as a dependency, while the Sprint 14 prompt allows forecasts only when eligible. Coverage E-005 includes Sprint 14 for the decision log, while the Sprint 16 prompt lists 06, 11 and 15. These differences need explicit resolution.

Use a current status block that links to the latest handoff; mark old authorization statements as dated history. Distinguish required prerequisites from optional enrichments. Keep copilot answers available when eligible prediction models are absent, if that is the chosen contract. Give decision-log ownership and its prior draft producers a consistent statement. Add user journey requirements to coverage so they cannot disappear between modules.

**Owner:** documentation follow-up now; maintained in every sprint. **Done when:** the roadmap, ordered prompts, coverage and latest handoff agree about what is implemented, what is required next and what remains optional or unverified.

## Review of each sprint

| Sprint | Existing purpose | Review and recommended addition |
| --- | --- | --- |
| 00 | Requirements and architecture | Main source modules are mapped. Add explicit complete user journeys and owners for A01–A18; separate original requirements from new suggestions. |
| 01 | Local runtime and project foundation | Core setup is specified. Add a clear first-use handoff to account setup, a labeled demo launch path and early recovery instructions. A working server alone is not a usable account. |
| 02 | Accounts and organization access | Major usability gap. Add 02A for website sign-up/onboarding, identity-message delivery, pending invitations and account/organization lifecycle. Keep existing isolation and last-Admin controls. |
| 03 | Navigation and shared interface | Search and notifications are shells. Add actual record search, the setup checklist, My work and contextual help with named later owners. |
| 04 | Portfolios, projects and delivery | Core records are planned. Add guided access setup and the fields required by later queries/cohorts. Task comments/priority are recommended additions. |
| 05 | Resources and workload | Capacity rules and privacy are already covered. Improve resource-access discovery and explain the difference between a resource profile and a login; reuse shared reminders for staffing changes if needed. |
| 06 | Maturity assessments | Core scoring/review is covered. Add evidence-library handoff, due dates and reassignment. Repeat assessments/trends are useful extensions rather than missing original scoring. |
| 07 | Dashboards and common measures | Source-backed dashboards are covered. Bring forward simple downloadable summaries and give global search/live refresh a clear integration owner. |
| 08 | Imports, connectors and durable jobs | Local slice is reported complete. Add unattended ownership, conflict-resolution flow, shared notifications and general manual-edit refresh. Keep live-provider verification separate. |
| 09 | Documents, OCR and retrieval | Add the assessment evidence bridge and policy lifecycle. Resolve the embedding-provider handoff before starting. Define deletion rules before real documents are accepted. |
| 10 | Shared AI runtime | Usage limits, errors and evaluations are covered. Reuse the agreed document embedding path and clearly expose disabled/no-provider states. Do not introduce duplicate document AI calls. |
| 11 | Nine agents and suggested assessment scores | All nine source agents are represented. Define accepted versus applied recommendations and confirm the policy/data versions each agent uses. |
| 12 | Historical data and model evaluation | Data quality and honest model claims are covered. Specify missing issue/category/history fields, collection rules and usable outcome-label entry or import. |
| 13 | Predictions and forecast screens | Forecast eligibility/fallback is already covered. Make the recorded-outcome feedback journey and model approval responsibility explicit; the app must still work when a model cannot be promoted. |
| 14 | Copilot and natural language questions | Chat history, citations and safe queries are covered. Add the promised query metadata and reconcile required versus optional Sprint 13 dependency. |
| 15 | Approvals, reminders and escalation | Features are covered but basic reminders arrive late. Extend an earlier personal inbox; define absence/deactivation/reassignment so approvals do not remain stuck. |
| 16 | Transformation roadmaps and decisions | Original transformation outputs are covered. Resolve decision-log ownership and connect approved initiatives to existing project/benefit records with explicit status. |
| 17 | Resource and budget scenarios | Source examples, saved comparisons and safe application are covered. Keep scenarios usable with deterministic rules when prediction models are unavailable; explain which outputs cannot be calculated. |
| 18 | Knowledge graph and impact tracing | All named relationships and advanced tracing are covered. Connect ordinary dependency screens to graph views and preserve a usable list when the graph service is unavailable. |
| 19 | Comparisons and benchmarks | Source comparison types are covered. Ensure the cohort fields exist; add compatible repeated-assessment trends if included in the product scope. |
| 20 | Meetings, transcripts and extracted actions | Core intake, minutes and reviewed actions are covered. Use the shared evidence/retention rules and keep optional meeting-template or calendar integration separate from required scope. |
| 21 | Scheduled reports, alerts and executive audio | Original reporting and audio features are covered. Reuse the earlier report snapshots and notification preferences. Complete unattended authority before enabling schedules. Identity email must have its own earlier owner. |
| 22 | Passkeys and complete access audit | Passkeys are already planned, not missing sign-up. Bring retention settings forward where needed; keep the final all-module access audit here. SSO/custom roles remain optional extensions. |
| 23 | Full verification and deployment | Release checks, backup/restore and guides are covered. Include a fresh-user journey with no setup commands and an ordinary-user pilot. Do not postpone all usability discovery to this sprint. |

## Suggested delivery order

1. Complete 02A: browser account creation, first organization setup, invitations and recovery.
2. Complete a focused 03A/04A usability pass: setup checklist, understandable access, actual record search and the minimum fields needed later.
3. Complete 08A: personal pending work, basic notifications, general refresh and connector ownership/recovery. Add basic result downloads if included in this pass.
4. Agree and record the 09/10/11 boundaries, then continue the original roadmap with the evidence-library and governance-policy additions.
5. Keep advanced reporting, passkeys, graphs and predictive features in their existing modules. They are already represented; adding them again would duplicate scope.

Each repair should remain small enough to demonstrate one complete user journey. Existing accepted sprint reports should remain historical evidence. Record new work in new reports and handoffs, and update all maintained prompt copies together if the plan is subsequently amended.

## Pilot acceptance journey

Before calling the operational app ready for ordinary users, demonstrate this sequence without asking the user to run setup commands:

1. Asha signs up, verifies her address and creates Northstar Demo Services.
2. She sets timezone/currency and invites Rohan, Meera and Kiran.
3. Each person joins from the invitation; Asha can resend or cancel an unused invitation.
4. Asha creates a project and assigns understandable access. Rohan finds it through search and updates its work.
5. Rohan finds his assessment in My work, completes it and attaches permitted evidence.
6. Meera sees a pending review, returns it for changes if needed and approves the final result.
7. A dashboard reflects relevant changes, explains missing information and offers a useful result download.
8. Kiran can view permitted results but cannot edit, approve or see private hours.
9. A forgotten password and an expired invitation can be recovered through visible user flows.

Document-library steps belong to Sprint 09. Before that, disclose the existing plain-text evidence limit instead of pretending Word/PDF evidence works.

## Source references

- [Original Word specification extract](../source/Word-Specification-Extract.txt) and [supplementary specification](../source/Supplementary-Specification.txt).
- [All ordered sprint prompts](../prompts/02-ORDERED-SPRINT-PROMPTS.md), especially 02, 03, 09–15 and 21–23.
- [Master instruction](../prompts/01-MASTER-PROMPT.md), particularly complete slices, frontend states and feature traceability.
- [Roadmap](../requirements/roadmap.md) and [coverage](../requirements/coverage.md), including F-038, F-070–F-077, E-005 and N-016–N-018.
- [Product journeys](../requirements/product-scope.md), [decisions](../requirements/decisions-and-assumptions.md) and [data model](../architecture/data-model.md).
- [Identity setup](../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md), [frontend contract](../contracts/frontend.md), [assessment contract](../contracts/assessment.md) and [jobs and integrations contract](../contracts/jobs-integrations.md).
- [Latest handoff](../handoffs/LATEST.md) and [Sprint 08 report](../03-sprints/completed/sprint-08/SPRINT_REPORT.md).
- Current forms/navigation: `apps/web/app/account/identity-client.tsx`, `apps/web/components/shell.tsx`, `apps/web/components/delivery-fields.ts` and `services/api/ppm_api/ppm_schemas.py`.

No delivery dates or new implementation completion are claimed by this review.
