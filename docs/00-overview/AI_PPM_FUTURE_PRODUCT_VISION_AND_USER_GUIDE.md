# AI-PPM Future Product Vision and User Guide

Availability update, 15 October 2026: [current status](CURRENT_STATUS.md) and
[the document library guide](../03-sprints/completed/sprint-09/USER_GUIDE.md) record
implemented Sprint 09 intake/OCR/keyword/policy controls. Future-tense semantic
findings, embeddings, AI answers and later workflows in this vision remain planned.
This document is a product vision; source behavior and executed checks govern availability.

**Current canonical availability (9 October 2026):** [current status](CURRENT_STATUS.md), [feature catalogue](FEATURE_CATALOGUE.md) and [executable user steps](../06-user-guides/USER_GUIDE.md). This long-form product vision retains future business explanations and its dated baseline; Sprint 8.1 is locally implemented with open mail/CI/Word gates. Any older planned statement about core pilot controls is historical, not current availability. Detailed section-by-section reconciliation remains tracked; do not use a future journey as an executable demo.


**Scope reviewed: 9 October 2026 · Latest local implementation: Sprint 8.1; external/visual gates open**

This guide explains the complete product described in the existing plans through Sprint 23. It is for executives, project managers, Project Management Office (PMO) leaders, department heads, resource managers and new users. It describes what people will see, do and achieve. It does not promise a delivery date.

The working application is branded **Enterprise PPM**. This guide uses **AI-PPM** for the product described in the request; a final commercial name has not been selected.

### How to read availability

| Category | Meaning in this guide |
| --- | --- |
| **Available Today** | A connected implementation has supporting local verification records. Availability is limited to the tested local application and the restrictions stated here; it does not establish production readiness. |
| **PLANNED** | A capability is explicitly included in the requirements or ordered sprint plans, but its complete user workflow is not implemented and verified at the current checkpoint. |
| **IMPLEMENTED BUT UNVERIFIED** | A mentioned capability has unresolved behavior, final scope, design or real-environment verification. The guide states what needs confirmation rather than filling in the gap. |

Read the feature explanations in Sections 4–6 for the intended experience, the journeys in Section 7 for practical steps, and the catalogue in Section 12 for the full scope. Section 13 explains the evidence and resolves conflicting documents.

## 1. AI-PPM at a Glance

AI-PPM is an intended workspace for **Project and Portfolio Management (PPM)**. Project management concerns an individual initiative: its work, people, dates, costs and problems. Portfolio management concerns a collection of projects: whether they support business goals, how they compete for resources, and where management attention is needed.

The completed product will connect project records, resource plans, maturity assessments, supporting documents, dashboards and reviewed AI advice. A manager should be able to move from “Which projects need attention?” to “What evidence explains the problem?” and then to “Who should decide what to do?”

An organization might use it to manage a customer portal, a billing upgrade and a reporting improvement together. Each project has its own plan. The portfolio view helps leaders see shared constraints, spending and strategic purpose. The resource view shows that the same specialist has been assigned to more work than their recorded availability allows.

Artificial intelligence (AI) is intended to help people interpret authorized information, investigate possible causes, draft recommendations and prepare summaries. People will still decide priorities, approve material changes and check whether advice fits their circumstances.

**Today:** the local application supports project and portfolio records, delivery tracking, capacity planning, reviewed assessments, four command-center views, a risk register and bounded imports. **Today also:** Sprint 09 versioned source intake, English OCR, keyword citations and policy/retention. **Planned:** connected AI interpretation, embeddings, forecasts and later enterprise workflows. No AI capability is verified as available at Sprint 08.

## 2. The Problem It Solves

Organizations often hold the project plan in one spreadsheet, spending in another, staffing in email, risks in meeting notes and progress in a separate task tool. Different people may be working from different versions. An executive receives a reassuring status report while a critical milestone is already overdue.

AI-PPM is intended to bring these facts into a consistent, permission-controlled workspace. It retains the manager's reported status alongside calculated indicators. It helps users investigate a disagreement instead of quietly replacing the manager's report.

The product also addresses inconsistent project-management practices. Two departments may both say they use an agreed process, but their answers and supporting evidence may reveal different levels of adoption. A common assessment framework makes those differences easier to discuss.

The intended difference from scattered spreadsheets and messages is the connection between information: the warning links to project facts, the allocation links to a shared person, the assessment links to its published questions, and future AI findings link to their supporting material. The product will still depend on accurate records, appropriate access, regular updates and people following through.

## 3. Who Will Use AI-PPM?

### The three defined access roles

An access role determines what a person may do. A job title describes their workplace responsibility. They are not interchangeable. The current role model defines **Admin**, **Project Manager** and **Viewer**. Additional enterprise roles are possible extensions whose approval and behavior need confirmation.

| Defined role | Responsibility and information needed | After sign-in and main actions | Decisions and restrictions | Benefit |
| --- | --- | --- | --- | --- |
| Admin | Organization setup, membership, access and shared rules; needs organization-wide configuration and authorized records. | Account and workspace navigation; organization setup, member management, project access, resources, framework publishing, dashboard policies and integrations. Planned AI Operations and delivery settings add oversight of usage and recipients. | Can administer the organization. Sensitive effort still needs an explicit grant. Assessment answering/review requires the named assignment, even for Admin. An Admin cannot read another user's personal saved view. | Establishes a consistent working environment and controls who receives information. |
| Project Manager | Delivery and planning within assigned scope; needs project facts, authorized resources, risks and relevant evidence. | Workspace and authorized projects; edits work, dates, budgets and risks when granted; uses resource planning and assessments when assigned. Planned analysis, recommendations and approvals require appropriate authority. | Project creation requires management access to the portfolio. Staffing edits require resource-management permission and edit access to the affected project. Cannot administer members or publish frameworks. | Keeps planning and progress together and investigates problems with shared evidence. |
| Viewer | Oversight or stakeholder review; needs explicitly shared dashboards, records and results. | Same workspace navigation, with permitted read views; can maintain personal dashboard filters. Planned assistant supports scoped reading and report exports require an export grant. | Cannot edit business records, answer/review assessments or approve material actions. Cannot read sensitive actual effort. No access is implied by an executive title. | Reviews relevant information without changing it. |

### Workplace responsibilities mapped to those roles

These audiences are supported personas, not additional implemented role names. Their initial screens use the shared workspace; a dedicated home page for each job title is not defined.

| Person | What they need and use most | Decisions supported | Access arrangement and limits |
| --- | --- | --- | --- |
| Organization administrator | Members, departments, teams, configuration, frameworks and integration health. | Who has access; which shared definitions and connections are permitted. | Admin. Restricted data and independent review rules still apply. |
| PMO leader | Portfolio patterns, risks, assessment dimensions, improvement priorities and planned transformation roadmaps. | Which delivery practices need improvement and which proposals should advance. | Admin or scoped Project Manager according to duties. Publishing remains Admin-only. |
| Portfolio manager | Project health, alignment, benefits, budget and shared dependencies. | Which projects warrant attention and proposed reprioritization. | Persona consistent with portfolio management; no separate role. Granted scope is required. A complete portfolio-ranking workflow is not yet defined. |
| Project manager | Owners, work status, milestones, blockers, spending and plan history. | Delivery updates, mitigation actions and proposed plan changes. | Project Manager with relevant project edit/manage grants. Being recorded as owner alone does not grant access. |
| Resource manager | Skills, calendar availability, allocations, capacity and permitted effort. | Staffing options and allocation changes. | Admin or Project Manager with explicit resource-management grants and affected-project access. Only Admin has verified whole-organization allocation totals today. |
| Department head | Department/team assessments, relevant delivery information and workload. | Where to support teams and improve practices. | Persona; assigned assessments and relevant grants. Department ownership does not automatically grant every project or attachment. |
| Team member or assessment respondent | Assigned assessment questions and evidence; project work if appropriately granted. | Completes assigned responses and authorized updates. | No separate Team Member role is approved. Current assessment respondents must be assigned Admin/Project Manager members; a dedicated personal task inbox needs confirmation. |
| Executive or sponsor | Portfolio health, significant exceptions, costs, benefits and future briefings. | Funding, priority and management intervention using available evidence. | Viewer by default. Approval needs an eligible Admin/Project Manager role and a separate named approver assignment; Viewer cannot approve. |
| Auditor or stakeholder | Permitted reports, completed results, source support and appropriate history. | Reviews consistency and accountability. | Viewer for shared reading; private evidence is separately restricted. The product does not certify legal compliance. |

## 4. What the Completed Product Will Offer

The plans describe a connected experience with five kinds of work:

1. **Manage the facts.** Organize portfolios, programs, projects, work, budgets, goals, risks, people and capacity.
2. **Understand organizational practices.** Publish assessment frameworks, collect evidence, review scores and compare compatible results.
3. **Investigate with evidence.** Use dashboards, documents, eligible forecasts and an AI assistant to understand concerns and possible explanations.
4. **Review and act.** Use planned approvals, transformation initiatives, decision logs and simulations to consider changes before making commitments.
5. **Keep people informed.** Use planned reports, configured reminders, risk alerts and executive audio briefings.

The future design includes connected areas for Documents, Copilot, Workflows, Transformation, Scenarios, Knowledge Graph, Benchmarks, Meetings and Reports. Their exact final arrangements remain subject to implementation. A named destination in a plan is not evidence that its screen works today.

The completed application is expected to support an organization selector, clear navigation, project detail views, accessible chart tables, light/dark themes and useful explanations when data is missing or access is restricted. The local application already provides a shared shell; release-wide accessibility, performance and deployment acceptance remain later work.

## 5. The Main Features Explained

### 5.1 Find your starting point and see what needs attention

**Available Today:** Workspace overview shows your active membership, connected organizations, sessions and account actions, with a link to projects. It is not the same page as the portfolio dashboard. The **Command center** provides **Executive, Delivery, Risk and Resource** views.

Choose a date range and, where appropriate, a portfolio. Review visible project health, budget, strategic alignment, delivery variance, milestones, blockers and resource information. Save personal filters to return to a useful view. Open a metric's evidence to see contributing facts, missing inputs and source age, then open the relevant project to investigate further.

**Planned for the Complete Product:** eligible forecasts, specialist findings, reviewed recommendations and workflow/report information will extend this experience. Assessment results currently have their own assessment area; a particular maturity tile on the home page is not confirmed. There is no verified general “latest updates” feed or personal deadline inbox to describe today.

For example, the dashboard may show that a project reported Green has an overdue critical milestone. The manager opens the evidence, checks the milestone and discusses the obstacle. This warning is useful even when other missing inputs prevent a combined health score.

### 5.2 Set up organizations, departments, teams and access

**Available Today:** account activation, sign-in, invitations, password recovery, sessions and switching between active organization memberships. Admins maintain members and their roles. Organization setup includes timezone, currency, departments, teams and goals. Dated team memberships describe who belongs to a team over time.

Admins grant project/portfolio visibility and the authority needed to edit. A person who can read a portfolio does not automatically have permission to change every project. A resource profile can represent a person who has no application account.

The result is a workspace where the right people can maintain or inspect the relevant information. If a project is absent, the user should check the selected organization, filters and grants rather than assume the record was deleted.

**Planned:** passkeys, additional retention/provider settings and access checks across all future files, AI answers and reports. External invitation/reset email delivery is not established today; development uses a private local mailbox. Its production delivery arrangements need confirmation.

### 5.3 Manage portfolios, programs and business goals

**Available Today:** Admins create portfolios, optional programs and goals. A project belongs to one portfolio and may belong to a program within that portfolio. Authorized users can maintain records, inspect summaries and archive eligible records while retaining history.

Users link projects to strategic goals and record how strongly each contributes. The resulting alignment value reflects those declared links and weights; it does not prove the project is the best investment. Business benefits record a target, optional realized result, measurement unit and period.

For example, a “Better Customer Service” portfolio contains a customer portal project and a billing upgrade program. The reporting improvement may be a direct portfolio project. The executive can review the projects together while the individual managers maintain their own plans.

**Planned:** richer comparison through the assistant and internal benchmarking, transformation priorities and scenario analysis. The plans support informed prioritization; a universal automatic ranking or a dedicated project-priority scoring method is not defined.

### 5.4 Create projects and keep the plan understandable

**Available Today:** create a project in an authorized portfolio, optionally select a program, associate an owner, department and team, enter dates and currency, and maintain its lifecycle. Add work items, sprints, milestones, dependencies, blockers, status updates, budgets and expenditure.

Project details provide an overview, work board, initial timeline/date table, financial information, goal links and plan/change history. Use a **baseline** to keep a saved version of the plan. A later forecast date records a revised expectation without erasing that earlier plan.

The recorded owner helps establish responsibility. It is not a separate guaranteed “project manager” job-title field and it does not grant access. Assigning an owner requires an active eligible member where the record calls for one. An approved project-priority field or richer priority workflow needs confirmation.

To update spending, add an expenditure entry in the project's currency. Correct an accepted entry using a linked reversal rather than rewriting the old transaction. Budget usage requires a nonzero approved budget and an explicitly complete ledger. Portfolio money remains grouped by currency; there is no automatic exchange-rate conversion.

Archiving preserves the record. Archived projects must be restored before further editing. Reopening completed/cancelled projects or completed work requires a reason; a completed project also needs an actual finish date. The current timeline is bounded and is not a drag-and-drop scheduling engine.

### 5.5 Track delivery during a normal working week

**Available Today:** work items move through defined states such as backlog, ready, in progress and done. Users associate owners, dates, sprints and recorded estimates where provided. Milestones identify important delivery points. Dependencies record that one item or project relies on another, while blockers record obstacles already affecting progress.

A project manager might review ready work on Monday, update blocked items during the week, review approaching milestones and spending on Thursday, and close a completed sprint on Friday. The closed sprint preserves the completed work/points used for its velocity measure. Later work edits do not silently rewrite that result.

Velocity means completed estimated points within the team's own convention. It is not a universal productivity score. Earlier closed or imported sprints can have unknown historical coverage; the application must not manufacture past velocity.

Dependencies that would create a loop are rejected. Today, changes to dependencies across projects require Admin authority. This protects consistency when a manager cannot see the whole relationship network.

**Planned:** evidence-backed delay explanations and eligible sprint/project/milestone forecasts, milestone notifications, meeting-derived proposed actions and more extensive impact tracing. My work and in-app assignment/review/import receipts are locally implemented in Sprint 8.1; scheduled and external notifications remain planned.

### 5.6 Record risks and follow up on mitigation

**Available Today:** risks have a project, responsible member, severity and likelihood, review date, mitigation plan, status and resolution/acceptance explanation. Users can create, inspect and update risks when they have project edit access. Mitigating, accepting or closing risks requires the supporting responsibility and explanation appropriate to that transition.

A **risk** is something that could affect delivery. A **blocker** is an obstacle already holding up work. The current product records both. A separately specified general issue-management module is not established.

Example: the billing upgrade depends on a security review that has not finished. The manager records the dependency and the current blocker, creates a risk of missing the launch date, names an owner and records a mitigation such as arranging a review meeting. Managers can review authorized risks across projects through the command center and open affected project records.

The current risk register's severity/likelihood entries and the calculated dashboard risk are different measures. Dashboard risk uses schedule, finance and capacity inputs; it does not automatically recalculate from the risk register's severity fields.

**Planned:** AI risk findings and mitigation suggestions, a configured escalation matrix and workflow routing to authorized people. Today's escalation readiness is preparation, not an automatically sent escalation.

### 5.7 Understand skills, availability and shared workload

**Available Today:** resource profiles, skills, calendars, dated availability, reporting teams, approved time off, allocations, permitted actual effort, capacity views and saved planning snapshots. Resource planning provides a staffing matrix, exact skill filtering, daily heatmap/table, weekly reconciliation and team workload support signals.

Capacity is the working time recorded as available after calendar rules, holidays and approved leave. Allocation is planned time assigned to projects. The same person's time is shared across projects. Over-allocation remains visible instead of being clipped to make the plan look feasible.

Suppose a new project needs three people. The manager looks for the required skills and reviews each candidate's calendar and commitments. A full-scope view might reveal that two candidates are already heavily allocated. The manager can consider a different start date, another suitable resource or changing a permitted allocation. The application does not automatically hire staff, guarantee a skills match or resolve the conflict.

A simple supported calculation: someone has 20 available hours in a week and 30 allocated hours across two projects. Planned utilization is 150%. This is a planning conflict, not evidence that the person is less productive. Missing calendars make capacity unknown. Zero capacity does not produce a meaningful utilization percentage.

Actual utilization requires authorized effort and explicit completeness for the period. A scoped manager's visible allocations may cover only some projects. The application labels that limitation and cannot claim a complete workload from the subset. Today only Admin has verified full-organization allocation scope.

Sensitive effort needs an explicit grant, including for Admin. Sensitive team support signals require adequate scope and at least five resources throughout the selected dates. Time off records hours, not medical narratives. There is no current leave-request approval flow.

**Planned:** reviewed AI staffing recommendations, eligible team workload/sentiment trends and hypothetical resource transfers. A staffing gap can be investigated using current information, but a separately specified automatic vacancy forecast or optimizer is not confirmed.

### 5.8 Assess project-management maturity

**Available Today:** build and publish a framework, assign a version to an organization/department/team, collect autosaved answers and evidence, submit, review, return for changes and complete. Four editable product examples cover PMO capability, Agile practices, governance and delivery capability. They are examples, not certified industry frameworks.

**Maturity** means how consistently an organization follows the practices it has chosen to assess. A **dimension** is one area, such as governance. A **rubric** explains the permitted answer levels. Weights indicate which questions or dimensions contribute more to the overall score.

The respondent answers the questions and explains their practice. The named independent reviewer checks answers and evidence, may make numeric adjustments with reasons, and completes the result. Admin status does not bypass those named responsibilities.

Afterward, permitted users see overall and dimension scores, bars and tables, answer coverage, evidence coverage and history. Missing information is distinct from poor performance. Required missing answers or an uncomputable dimension prevent finalization. An evidence note or released file contributes to evidence coverage; it does not prove that an answer is true or automatically improve the score.

Published versions and completed results remain stable. Compare departments on the same published version; a changed framework cannot silently rewrite their earlier results. Retained assessments support reviewing progress over time, but a fully designed longitudinal trend screen needs confirmation. Today the comparison loads a bounded set of recent authorized records.

Current attachments are small UTF-8 plain-text files, held for independent review and release. General PDF/Word analysis and automated malware scanning are later work. Some assessment access-grant administration currently lacks a frontend and must be handled by an administrator through the existing supported administration interface outside these user walkthroughs.

**Planned:** AI interpretation of narrative answers, patterns, maturity gaps, suggested scores and improvement advice. The original calculated score, AI suggestion and approved result will remain distinguishable. The final chart choice, including the proposed radar-style view, needs confirmation; bars and tables work today.

### 5.9 Bring documents and connected work into the workspace

**Available Today:** Admins configure bounded imports, preview field mappings, queue processing, inspect row errors/source references, cancel work and monitor progress. Comma-separated values (CSV) imports use simple text arranged in rows and columns and work locally. Jira Cloud issues/sprints and GitHub issues/pull requests have verified local contract fixtures. Live adapters exist, but actual provider authentication and sync need confirmation.

These imports populate supported work/sprint information. They do not import arbitrary notes, people, resource allocations or all information from the connected tool. A source reference helps show where a record came from. Local changes are protected from silent source overwrites. Repeating the same source through the same connection avoids duplicating supported effects; separate duplicate connections are not guaranteed to merge.

**Planned:** a document library for software requirements, business requirements, product requirements, meeting minutes, sprint reports, risk logs, project charters and governance policies. Initial formats in the plan include PDF, Word DOCX, text, scanned PDF/images and CSV/Excel XLSX tabular logs. Final file-size/type limits and real-provider verification still need confirmation.

Users will upload permitted material, watch processing, preview extracted text and inspect proposed risks, blockers, dependencies or policy/practice gaps at their source location. Text recognition will help read scans, with confidence limitations shown. Retrieved passages will support answers rather than grant new access. Semantic interpretation follows the shared AI work; document intake alone does not prove AI extraction works.

A suggested risk from a document remains a proposal for review. It will not silently become a live risk or dependency. Document versions, restricted access and deletion/retention behavior are part of the planned experience.

### 5.10 Ask the AI PMO assistant questions

**Planned for the Complete Product:** a conversational Copilot, supported project/portfolio analytics, scoped conversation history, follow-up questions, source previews, result tables/charts and feedback. The intended inputs are authorized project records, shared calculations, assessment information, permitted documents, specialist findings and eligible forecasts.

| Intended use | Illustrative question | Expected kind of answer |
| --- | --- | --- |
| Portfolio attention | “Which projects have high risk this quarter?” | Scoped projects, timeframe, supporting indicators and missing-data limits. |
| Specific project progress | “What is the current position of the billing upgrade?” | Recorded work, dates, costs and relevant findings with source support. |
| Delays and blockers | “Why might the customer portal be late?” | Known dependencies/workload facts, possible explanations and clearly identified uncertainty. |
| Project comparison | “Compare the portal and billing projects. Which concerns should we investigate first?” | Comparable facts and review priorities; no universal ranking promised. |
| Resource constraints | “What resource commitments could be affecting this project?” | Authorized allocation/capacity evidence; partial scope remains explicit. |
| Assessment interpretation | “Summarize the governance gaps in our completed assessment.” | Permitted dimensions/answers and grounded improvement suggestions. |
| Recurring problems | “Do our recent delivery records suggest a recurring dependency problem?” | Patterns within accessible history, with coverage limits and hypotheses separated from facts. |
| Filtered analytics | “Show delayed fintech projects with budget overruns.” | A supported filtered table, provided the relevant category and data are recorded and accessible. |
| Recommendations | “What options could address this review bottleneck?” | Proposed actions, assumptions, supporting sources and tradeoffs for human review. |
| Follow-up | “Limit that comparison to this portfolio and show the sources.” | A narrowed authorized result without assuming access to other projects. |

Users will examine citations, check dates and distinguish recorded facts from interpretations. Questions outside the permitted information or supported analytics should produce a clarification, limitation or unavailable answer. The assistant is not connected today, and no final question-entry button or screen layout is asserted here.

### 5.11 Review forecasts and AI insights carefully

**Planned:** forecasts for sprint/project delay, missed milestones, budget overrun, portfolio concerns, risk trends, resource inefficiency, delivery confidence and evaluated risk categories. Team-level workload and sentiment support are included under privacy restrictions.

A forecast should state what it concerns, when it was made, the period it predicts, the source coverage and its uncertainty. Users may see an experimental label, a rules-based fallback or “unavailable” if no suitable model exists. Historical data quality and measured evaluation determine whether a prediction can be offered responsibly.

The plans distinguish a risk score from a probability of failure. A score of 70 does not mean a 70% chance of failure. A probability needs a defined outcome, suitable historical examples and evidence that the probability is meaningful. Those model-promotion details are not settled today.

AI may summarize unusual changes and possible causes, but associated events do not prove causation. Workload/sentiment signals are reasons to offer support and investigate; they are not medical diagnoses, employee rankings or proof of burnout.

### 5.12 Turn recommendations into reviewed actions

**Planned:** configurable approval flows, ordered steps, named eligible approvers, rejection, return for changes, reassignment, due dates, reminders, escalation, response-time tracking and milestone notifications. Users will review an approval inbox and the history of each request.

A recommendation becomes a live change only through an authorized supported action. The execution should check current permissions and whether the underlying plan has changed. A stale proposal or removed approver must not bypass those checks. Sensitive actions cannot be approved by their own proposer.

An **SLA**, or service-level agreement, is the agreed time allowed for a response/action. The workflow will state whether it counts elapsed time or working-calendar time. General approvals and timers are not available today, although assessment-specific independent review already works.

### 5.13 Plan transformation and measure improvement

**Planned:** draft PMO and Agile transformation roadmaps, process improvements, governance structures, reporting responsibilities, resource models, tooling recommendations, delivery optimization and Key Performance Indicator (KPI) frameworks.

A PMO leader could ask for a plan to improve delivery in a 300-person organization. The product should gather constraints and use available assessments, risks, goals and capacity. It should not assume the organization can add staff or promise a financial return.

Each initiative will record an objective, owner responsibility, evidence, dependencies, priority, effort/cost assumptions, quarterly milestones and measurement plan. A decision log will keep alternatives, reasons, approvals and follow-up outcomes. Approved initiatives may link to existing projects or become new projects; generating a roadmap alone creates no commitment.

The leader will compare expected benefits with observed results and revisit the plan. Numeric targets are proposals to validate, not guaranteed improvements.

### 5.14 Explore what-if scenarios and relationship impacts

**Planned:** the Time Machine simulator will compare an unchanged baseline with hypothetical resource transfers or budget cuts. Users will change exact inputs, inspect assumptions, save scenarios and compare justified schedule, cost, utilization, risk and dependency effects.

For example, moving two developers from Project A to Project B must consider both projects and their shared capacity. A 25% budget-cut scenario should retain the original live budget. Simulation does not prove what will happen; unsupported outputs remain unavailable. Applying a scenario requires approval and a check that the live plan still matches the baseline.

The planned **Knowledge Graph** is a connected map of portfolios, goals, projects, teams, skills, risks and dependencies. Users will trace an affected project back to related work and inspect supporting records through a graph or table. Inferred links will be marked differently from confirmed links, and refresh lag will be visible. A relationship path helps investigation; it does not prove the root cause.

### 5.15 Compare fairly and capture meeting decisions

**Planned:** internal benchmarking across departments, teams and portfolios. Users will select comparable periods, work types, project sizes, methodologies, currencies and assessment versions. Results will show sample counts, coverage and why a comparison is unavailable. Raw story points from different teams will not become a productivity leaderboard. Cross-customer benchmarking is not approved scope.

**Planned:** authorized transcript/audio intake, transcription, editable minutes, decisions, proposed actions, owners/dates, blockers, risks and dependency candidates. Findings will reference transcript passages or timestamps. Unclear owners or dates will remain unresolved for review; no fabricated commitment should be created.

After approval, supported meeting actions or risks can become project records without duplication on reprocessing. Supported audio formats, duration limits, provider and cost policies require confirmation. No biometric speaker identification is planned in the ordered scope.

### 5.16 Review reports, receive updates and retain accountability

**Available Today:** inspect project/portfolio summaries, capacity views, assessment results, command-center evidence and scoped business history. Download the current command-center snapshot as **JSON**, a structured data file. This is not a formatted executive report or a scheduled delivery service.

**Planned:** downloadable PDF/HTML reports, weekly executive summaries, configured email/Slack risk alerts, and an approximately two-minute daily audio briefing with a supporting transcript and text-only fallback. Reports will use shared facts with period, currency, freshness, owners, risks and supporting references. Source metrics must agree with the displayed report snapshot.

| Report or review output | Intended reader and decision | Availability / format boundary |
| --- | --- | --- |
| Project and portfolio summaries | Managers/sponsors review plan, costs, alignment and delivery position. | Available Today as on-screen summaries; a separate export template for every project/portfolio is not confirmed. |
| Assessment result and comparison | PMO/department leaders select improvement areas using compatible scores and coverage. | Available Today on screen; dedicated assessment report export needs confirmation. |
| Capacity/resource views | Resource managers investigate staffing conflicts and incomplete effort. | Available Today on screen; dedicated resource report export needs confirmation. |
| Dashboard snapshot | Authorized analysts reuse the permitted current overview. | Available Today as JSON; no CSV/XLSX dashboard export is specified. |
| Weekly executive summary and general report | Executives/PMO review key changes, risks, owners and recommended decisions. | Planned PDF/HTML downloads and configured delivery. Exact optional templates need confirmation. |
| Daily briefing | Executives quickly review portfolio concerns, then consult transcript/evidence. | Planned audio plus transcript; no specific audio file extension is promised. |
| Historical/benchmark comparison | Leaders inspect compatible changes and outcomes. | Planned broader trend/benchmark views; current dashboards do not reconstruct every past state. |
| Audit review/export | Authorized administrators examine accountability. | Scoped history works today; planned restricted audit search/export has no confirmed final file format. |

Admins will configure approved destinations and recipients; recipients can manage allowed briefing preferences. Preview and test-to-self are planned before general delivery. Users will act on review requests, rejected import rows and assigned responses. Configured background processing, reminders and report schedules can run automatically once implemented and authorized.

Sprint 8.1 adds manual saved-change dashboard refresh and a private in-app notification feed with read/preferences and live target access checks. No mobile push channel is specified, and email/Slack risk delivery is planned rather than working today. Broader automatic status-change or assigned-task notifications need confirmation.

History already helps users see important changes, saved plans, expenditure corrections, reviewer reasons and preserved assessment results. Future workflow, AI-run, scenario, meeting and decision histories will extend that accountability. History is permission-controlled and bounded; it is not a promise of unlimited or tamper-proof records.

## 6. How Users Will Use Each Feature

Use this as a quick starting guide. Exact future layouts and control labels are not defined here.

| User need | Where to begin / intended action | What to review before continuing | Result |
| --- | --- | --- | --- |
| Find work | Today: select the correct organization, open Projects or Portfolios, search/filter authorized records. | Scope, archive filters and loaded-record limits. | Open the intended project or collection. |
| Make a dependable plan | Today: project details; add work, milestones, budget and a saved baseline. | Dates, owners, dependencies and completeness. | A recorded plan and reference point for changes. |
| Update delivery | Today: project work/status records and Delivery dashboard. | Current obstacles, actual dates and sprint coverage. | Shared progress and visible exceptions. |
| Review a portfolio warning | Today: Command center, relevant view and evidence drawer. | Source age, coverage, currency, baseline and reported/computed differences. | Identify facts and affected projects. |
| Plan staffing | Today: Resource planning; skills, selected dates, calendar and allocations. | Full versus partial scope, leave, effort completeness and permissions. | Evaluate available options and make permitted edits. |
| Assess a department | Today: Maturity assessments; published version and named respondent/reviewer. | Required questions, evidence release and compatibility. | A reviewed result tied to stable rules. |
| Process outside work | Today: Admin uses Integrations & jobs to preview, queue and inspect errors. | Fixture/live label, field mapping, accepted rows and source conflicts. | Supported work/sprints with progress and provenance. |
| Investigate written evidence | Planned: permitted document upload, preview and finding review. | Extracted source passage, scan confidence and proposed versus accepted finding. | Reviewable evidence and proposals. |
| Ask for an explanation | Planned: scoped Copilot question and follow-up. | Citations, missing facts, hypotheses and model eligibility. | A supported answer or an honest limitation. |
| Change a plan from advice | Planned: proposal, independent approval and execution outcome. | Alternatives, authority, stale baseline and action scope. | A recorded decision and, if authorized, a supported change. |
| Improve organizational practices | Planned: Transformation initiative and KPI review. | Gaps, goals, constraints, assumptions and observed outcomes. | A measurable improvement plan. |
| Explore alternatives | Planned: saved scenario comparison or relationship map. | Shared capacity, dependencies, unsupported predictions and refresh lag. | A better-informed discussion before commitments. |
| Inform stakeholders | Today: permitted on-screen views/JSON snapshot; planned: report preview and approved delivery. | Recipient access, period, facts and protected material. | Appropriate information for a decision. |

## 7. Step-by-Step User Journeys

The examples use a fictional organization. They are walkthroughs, not claims that sample data exists in your workspace. Current steps use verified routes or functional descriptions. Planned steps deliberately avoid inventing final buttons.

### Journey 1: A project manager creates and manages a project

**Goal:** Set up and maintain a billing upgrade.

**Starting point:** Signed in as a Project Manager with management access to the chosen portfolio; the Admin has configured the organization and necessary grants.

**Step 1:** Open **Projects** and start creating a project. Choose the authorized portfolio and optional program. Enter its name, dates, owner and other supported details. The saved project appears in the list.

**Step 2:** Open the project. Add work items with responsible members, dates and supported estimates. Create milestones and, if needed, sprints. The work board and timeline/date table show the loaded records.

**Step 3:** Record dependencies and blockers. Ask Admin to maintain any cross-project dependency. Check that the relationship is sensible and does not create a loop.

**Step 4:** Record approved budget lines and expenditure as they occur. Confirm ledger completeness only when warranted. The summary shows amounts in the project's currency and an eligible usage percentage.

**Step 5:** Save an initial baseline with a reason. Future date changes can be compared with that plan. Allocation edits need additional resource permissions; consult the resource manager where necessary.

**Step 6:** During the week, update work states, milestones, blockers and reported health. Record a revised forecast when expectations change. If another person has edited the record, reload and review the latest version before saving again.

**Step 7:** Review the command-center delivery/risk evidence. On completion, enter the actual finish and complete the project through the allowed lifecycle. Review retained plan and change history.

**Final result:** A project with a recorded plan, delivery facts, spending, obstacles and retained changes.

**Business benefit:** Colleagues can use the same records and discuss deviations from a known plan.

**Availability:** **Available Today** within current grants and bounded views. AI scheduling, automatic staffing and general approval flows are **PLANNED**.

### Journey 2: An executive reviews the organization's projects

**Goal:** Identify concerns that need management attention.

**Starting point:** Signed in with Viewer access to the relevant portfolio/projects; a complete organization view requires appropriate access.

**Step 1:** Open **Command center** and choose **Executive**. Set the period and portfolio. The application shows only authorized data.

**Step 2:** Review health coverage, budget by currency, declared strategic alignment and benefits. An unknown health score means insufficient information, not healthy delivery.

**Step 3:** Check any reported-versus-evidence discrepancy. Open its evidence to examine the underlying fact, such as an overdue critical milestone.

**Step 4:** Open the affected project and, where permitted, review Delivery, Risk or Resource information. Check whether the data is stale or the scope partial.

**Step 5:** Discuss an intervention with the project manager. Record changes through an authorized manager. Future workflow approval will capture the request and decision; Viewer does not approve it.

**Final result:** An evidence-based agenda of concerns and next discussions.

**Business benefit:** Leadership attention is directed by visible facts rather than status color alone.

**Availability:** Dashboard investigation is **Available Today**. Forecasts, AI summaries and formal action approval are **PLANNED**.

### Journey 3: A PMO leader performs a maturity assessment

**Goal:** Compare Engineering and Operations practices and choose improvements.

**Starting point:** An Admin can publish/assign; different eligible members are available as respondent and independent reviewer.

**Step 1:** Open **Maturity assessments**. Create a framework or load an editable example. Define dimensions, questions, allowed answers, weights and required explanations.

**Step 2:** Publish a version. Assign that exact version to Engineering and Operations with named respondents and independent reviewers.

**Step 3:** Each respondent opens their assigned assessment, answers questions and provides supporting explanations. Wait for successful autosave; unresolved save failures block submission.

**Step 4:** Add supported evidence if needed. Today only bounded UTF-8 plain-text attachments are accepted and held for review.

**Step 5:** Submit after required information and computable dimensions are present. The named reviewer examines the responses, previews/releases appropriate evidence with a reason, requests changes or makes reasoned adjustments.

**Step 6:** Complete the reviewed assessment. Inspect the overall/dimension bars, tables and coverage. Engineering scoring 75 and Operations scoring 0 in the documented fixture reflects different answers and a recorded adjustment, not an AI opinion.

**Step 7:** Compare completed department results on the identical framework version. Review weaknesses and agree improvement actions. Future Transformation planning can turn reviewed gaps into proposed initiatives.

**Step 8:** Reassess later, retain earlier results and check framework compatibility before interpreting a change as improvement.

**Final result:** Stable reviewed results, supporting reasons and a practical improvement discussion.

**Business benefit:** Departments can compare practices consistently and revisit progress without rewriting history.

**Availability:** Core assessment/review and compatible department comparison are **Available Today**. AI interpretation and transformation planning are **PLANNED**; final longitudinal trend presentation needs confirmation.

### Journey 4: A resource manager investigates team workload

**Goal:** Find a feasible staffing option for a project needing three people.

**Starting point:** Resource-management permission and access to the affected projects; use an Admin view when full allocation totals are required.

**Step 1:** Open **Resource planning**. Select the relevant dates and use recorded skills to identify candidates.

**Step 2:** Review calendar availability, approved leave and allocations. The heatmap and equivalent table show available/planned hours and eligible utilization.

**Step 3:** Check the scope label. If only some projects are visible, request an authorized full-scope review before concluding that someone has spare capacity.

**Step 4:** Inspect daily and weekly conflicts. A person with 20 available and 30 allocated hours has more planned work than available time. Check the dates causing the excess.

**Step 5:** Discuss options: another resource, adjusted dates or a permitted allocation change. Current edits are explicit; there is no atomic transfer or automatic optimizer. Preserve a planning snapshot when an authorized Admin needs a reference point.

**Step 6:** Recheck the resulting totals. Later Time Machine scenarios will support comparing a hypothetical transfer before approved application.

**Final result:** A staffing decision grounded in recorded availability and commitments, or a clearly identified information gap.

**Business benefit:** Avoids assuming the same person's capacity belongs independently to several projects.

**Availability:** Capacity investigation and permitted edits are **Available Today**. AI recommendations and cross-project scenario application are **PLANNED**.

### Journey 5: A user investigates a delivery problem with AI

**Goal:** Understand why the customer portal may miss its planned finish.

**Starting point:** Future Copilot enabled with authorized project data/evidence; forecasts are optional and must be eligible.

**Step 1:** Establish the project and timeframe, then ask: “Why might the customer portal miss its planned finish?” The assistant checks supported information within the user's access.

**Step 2:** Read the answer's distinction between facts, possible explanations and forecasts. For example, an overdue review is a fact; its contribution to a later delay may be a hypothesis.

**Step 3:** Open supporting project records or cited passages. Check source dates, baseline and scope. A missing cost forecast must remain missing.

**Step 4:** Ask a follow-up, such as “What options address the review bottleneck, and which evidence supports them?” Review the proposal and assumptions.

**Step 5:** Discuss feasibility with the responsible people. Save an appropriate decision draft or propose a supported action; obtain required approval before a live change.

**Final result:** A checkable explanation and reviewed next step, or an honest statement that the available evidence cannot answer the question.

**Business benefit:** Helps organize investigation without removing human accountability.

**Availability:** **PLANNED**. No current Copilot workflow or AI answer is verified.

### Journey 6: A manager reviews risks across multiple projects

**Goal:** Follow up on significant delivery risks within an authorized portfolio.

**Starting point:** Command-center access; project edit permission where risk updates are required.

**Step 1:** Open **Command center**, select the portfolio and use **Risk**. Review available risk records and known/unknown calculated indicators.

**Step 2:** Identify a concern and open the related evidence/project. Check the risk's owner, likelihood, severity, review date and mitigation plan.

**Step 3:** Inspect the associated blocker or dependency. Confirm whether it is still active and what information is missing.

**Step 4:** Agree follow-up with the owner. If permitted, update the mitigation/status, recording resolution or acceptance reasons where required.

**Step 5:** Revisit the risk at its review date. Future escalation workflows will route qualifying problems under configured policy; the current process does not automatically send them.

**Final result:** Updated responsibility and mitigation for visible risks across projects.

**Business benefit:** Helps management follow through on concerns instead of leaving them in scattered notes.

**Availability:** Register review/update is **Available Today**. AI risk analysis and automated escalation are **PLANNED**.

### Journey 7: A user generates or shares a report

**Goal:** Prepare a consistent portfolio update for authorized stakeholders.

**Starting point:** Today, command-center read access; in the completed product, the relevant export grant and approved delivery configuration.

**Step 1:** Select the correct organization, period and portfolio. Check freshness, coverage and currency grouping.

**Step 2:** Today, download the authorized dashboard snapshot as JSON if structured data is needed. This action rechecks current access and does not email a report.

**Step 3:** In the planned reporting area, generate/preview a supported PDF or HTML report from a versioned snapshot. Review project facts, risks, owners and recommendations against the evidence.

**Step 4:** Share only through permitted destinations and recipients. An Admin configures email/Slack delivery, validates recipients and can preview/test to self. Users should not assume that a public link exposes protected evidence.

**Step 5:** If a schedule is configured, review the delivery outcome and any failure. For an audio briefing, check its supporting transcript and text-only fallback.

**Final result:** A consistent authorized update, with its period and limitations visible.

**Business benefit:** Reduces repeated preparation and inconsistent executive messages while preserving review.

**Availability:** JSON snapshot download is **Available Today**. Formatted reports, scheduled delivery and audio are **PLANNED**. Dedicated assessment/resource export templates need confirmation.

## 8. Dashboards, Assessments, and AI Insights

### Understand which kind of information you are reading

| Information | What it means | How to check it |
| --- | --- | --- |
| Recorded fact | A saved date, work state, budget entry, allocation, answer or benefit declaration. | Open the underlying record, date, owner and history. A saved statement can still be inaccurate. |
| Calculated measure | A result from stated rules, such as budget usage, available hours or rubric score. | Check inputs, completeness, period, units and published definition. |
| AI explanation or suggested score | Planned interpretation of evidence, including possible gaps or causes. | Inspect citations and uncertainty; compare with original facts/calculated score. |
| Forecast | Planned estimate of a future outcome from an eligible evaluated model, or a clearly labelled fallback. | Check horizon, model eligibility, source age, uncertainty and experimental status. |
| Recommendation | A proposed next step. | Review assumptions, costs, alternatives and required authority. It has not necessarily been approved or executed. |

### What the four current dashboards tell you

| View | Main information | Important limit |
| --- | --- | --- |
| Executive | Covered portfolio health, reported/computed differences, budgets by currency, declared alignment and target/realized benefits. | Coverage matters; unlike currencies/benefit units are not silently summed. |
| Delivery | Closed-sprint velocity, baseline/working-calendar variance, critical milestones, blockers and dependencies. | Historical closure coverage can be unknown; current timeline dates and working-day variance are different presentations. |
| Risk | Register records, deterministic risk components, health discrepancies and escalation readiness. | Current calculated risk is a heuristic; escalation execution and prediction are planned. |
| Resource | Authorized capacity, allocation, utilization and eligible team workload signals. | Partial access and sensitive-data suppression restrict what can be concluded. |

The current combined risk rule uses schedule, financial and capacity components. Health is derived from that risk rule. If required components are missing or outside the user's scope, the combined value is unknown. Admins can configure operational thresholds; they are not validated promises of project outcomes.

The date filter selects relevant period facts, such as spending and closed sprints, while some measures reflect current state. It does not turn the dashboard into a reconstruction of the organization on a past date. Reloading also does not make old source information fresh.

Assessment scores answer a different question: how the answers fit a published framework. Review the score together with answer/evidence coverage. A high score with weak evidence warrants investigation, and comparisons require compatible versions. Future AI interpretation can suggest gaps or improvements, but approval remains separate.

## 9. Benefits for the Organization

| Business problem | How AI-PPM will help | Expected benefit |
| --- | --- | --- |
| Project information is scattered | Available project/work/cost/risk records and planned document/meeting evidence connect in one authorized workspace. | Easier access to consistent information and its source. |
| A reassuring status hides delivery trouble | Available reported-versus-evidence comparison highlights supported discrepancies. | Earlier investigation of contradictory facts. |
| People are committed to several projects | Available shared calendars, allocations and capacity show eligible conflicts. | Better-informed staffing discussions. |
| Spending reports disagree | Available expenditure history and same-currency summaries; planned reports reuse shared calculations. | Easier reconciliation and fewer incompatible totals. |
| Departments assess themselves differently | Available published frameworks and independent review preserve comparable results. | Clearer discussions about improvement areas. |
| Leaders struggle to connect projects to goals | Available declared goal alignment and benefit targets/results. | More transparent discussion of strategic purpose. |
| Managers repeat investigations | Planned cited Copilot answers, specialist findings and relationship tracing organize evidence. | Less repeated searching and clearer questions for responsible people. |
| Recommendations lose accountability | Planned approvals and decision logs retain owners, reasons and outcomes. | More visible follow-through. |
| Proposed changes have wider consequences | Planned scenarios compare resource/budget changes against a preserved baseline. | Better examination of tradeoffs before commitment. |
| Meeting actions get lost | Planned reviewed minutes/actions link statements to project records. | Clearer responsibilities and fewer unconfirmed commitments. |
| Executive updates take repeated preparation | Planned shared report snapshots, summaries and audio briefing. | More consistent updates for authorized recipients. |
| Improvement programs lack measures | Planned transformation initiatives link gaps, owners, milestones and KPIs. | Easier review of expected versus observed benefits. |

These benefits depend on accurate and timely data, adoption, suitable access, appropriate interpretation and sound decisions. The project evidence does not establish guaranteed savings, productivity increases or perfect predictions.

## 10. A Typical Day with AI-PPM

This scenario describes the completed intended product. The AI, generic workflows and reports mentioned here are planned.

**Morning:** An executive opens the portfolio view. The billing upgrade is reported Green, but a critical review milestone is overdue. The executive opens the source evidence and asks the manager to investigate. The warning does not prove failure; it provides a specific discussion point.

**Mid-morning:** The project manager updates the blocked work and records the current forecast. A resource manager checks the review team's availability and finds a conflict with another project. They discuss options using the authorized allocation information. If their view is partial, they seek a full-scope review.

**Before lunch:** A PMO leader reviews completed departmental assessments. Both use the same framework version, so differences can be investigated fairly. The leader proposes an improvement initiative for inconsistent review practices, with an owner and measurable target.

**Afternoon:** A manager asks the future assistant to summarize the evidence behind the billing delay. The answer identifies known blockers, a possible capacity explanation and missing information. The manager checks the citations. A hypothetical resource transfer is compared in a scenario; the live allocation stays unchanged during exploration.

**Later:** Responsible people review a proposed change through the planned approval workflow. Execution checks the current plan before applying an authorized action. A meeting's proposed follow-up tasks are checked against its transcript before acceptance.

**End of day:** An authorized report or briefing reflects the same recorded facts, with source age and uncertainty visible. It does not automatically claim the approved intervention solved the problem. The project manager will update outcomes when evidence is available.

## 11. What AI Can and Cannot Do

**Current position:** no connected AI inference, conversational assistant, semantic assessment, document retrieval or predictive model is verified through Sprint 08. Existing calculations, autosave and import processing are ordinary application features.

The planned intelligence includes nine specialist areas: portfolio/PMO, risk, governance, Agile practice, executive reporting, resources, finance, schedule and team sentiment. These are analysis responsibilities, not nine new user roles. They should reuse shared facts and show incomplete/conflicting findings when specialists disagree or fail.

| User question | Intended answer |
| --- | --- |
| What kinds of questions can AI help with? | Supported project/portfolio progress, risks, delays, resource constraints, assessments, documents, recommendations and comparable analytics. |
| What can it use? | Information within the user's current permissions, through supported records, documents and tools; eligible forecasts when available. External connections do not imply access to everything in a third-party tool. |
| How will it help? | Summarize evidence, organize possible explanations, suggest next steps and make complex information easier to inspect. |
| How do I judge reliability? | Open citations, check periods/versions/source age, compare numerical facts with records, and inspect uncertainty and missing inputs. A citation is support to inspect, not proof of correctness. |
| Which decisions remain mine? | Priorities, funding, staffing, risk acceptance, assessment approval, policy adoption and material live changes. Appropriate people must review feasibility and consequences. |
| What if information is missing? | Show unknown/partial results, ask for clarification or decline unsupported claims. A clearly labelled rules fallback may be available; missing data must not become a fabricated answer. |
| What if the AI service fails or exceeds its budget? | Planned visible unavailable/degraded states, bounded attempts and useful partial results where justified. No invented successful analysis. |
| What limits should I expect? | Errors, incomplete evidence, out-of-date sources, restricted scope, ambiguous questions, unsupported analytics and model-specific eligibility. Hypotheses and scenarios do not establish causation. |

Progress displays will describe observable stages and concise evidence summaries. The source phrase “AI thought streaming” has been reconciled to this behavior; it does not promise a display of private internal reasoning.

AI Operations is planned for Admins to inspect configured provider availability, usage, costs where available, errors and organization budgets. Exact provider/model, production data-handling policy and spend caps need confirmation. A successful demonstration using examples would not establish real-world forecast accuracy.

## 12. Complete Feature Catalogue

This catalogue was established from the preserved specifications, coverage matrix, ordered sprint prompts, reports, contracts, current screens and verification evidence before the narrative was written. It covers user-facing scope; model-training tools, runtime diagnostics and code-generation tools are not product features. Source requirement IDs are included for traceability, not instructions for business users.

### Access and everyday navigation

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Accounts and sessions (F-001) | Activate, sign in/out, recover access and review/revoke sessions. | Controls personal access. | All members | Available Today; delivery uses a local mailbox. |
| Memberships and three roles (F-002–003) | Admin invites/changes members; users switch active organizations. | Separates organization information and responsibilities. | Admin; all members | Available Today within implemented modules. |
| Project/portfolio and restricted-data grants | Inspect/edit only granted information; separately authorize sensitive effort/results. | Makes access match the task. | Admin; granted members | Available Today; some assessment grant administration has no frontend. |
| Organization hierarchy/settings | Maintain departments, teams, dated memberships, timezone and currency. | Provides consistent organization context. | Admin | Available Today. |
| Workspace overview and navigation (E-004) | Open functioning modules, page command search, breadcrumbs and account actions. | Helps users find their work. | All members | Available Today; command search is navigation search. |
| Light/dark and accessible presentations | Change theme; use keyboard controls and chart/table alternatives. | Supports different viewing needs. | All members | Available Today for tested flows; complete release coverage needs confirmation. |
| Passkeys (F-004) | Enroll/name/revoke supported credentials and sign in/recover. | Adds a planned account-access option. | All members | Planned for the Complete Product. |
| Retention/provider settings and restricted audit export | Configure later data/AI policies and inspect authorized exported history. | Supports operational oversight. | Admin | Planned for the Complete Product; final policies/formats need confirmation. |
| Custom enterprise roles and identity extensions | Possible richer roles, company single sign-on (SSO) and automated account provisioning (SCIM). | Could fit future enterprise needs. | Admin | Completion Still Needs Confirmation; extensions, not approved core deliverables. |

### Portfolios, projects and delivery

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Portfolio lifecycle (F-005) | Create/edit/archive portfolios and review authorized projects. | Groups investment and delivery information. | Admin; granted managers/readers | Available Today. |
| Programs (F-006) | Group projects inside their portfolio. | Keeps related initiatives together. | Admin; granted readers | Available Today. |
| Goals/alignment (F-009) | Record weighted project contributions and inspect coverage. | Explains stated strategic purpose. | Admin; granted managers/readers | Available Today. |
| Benefits (F-027) | Record target/realized benefit, unit and period. | Compares intended and observed value. | Granted managers/readers | Available Today. |
| Project creation and lifecycle (F-007) | Save owners/dates/context, edit, complete, archive/restore and reopen with reasons. | Keeps a dependable project record. | Admin; granted Project Manager | Available Today. |
| Lists and details | Search/filter/page authorized records and open a project. | Finds relevant work. | Granted members | Available Today; bounded selectors/views. |
| Work items and board | Maintain owners, states, dates and supported estimates. | Makes delivery progress visible. | Granted managers/readers | Available Today; board shows loaded page. |
| Sprints and closure measures (F-011,030) | Plan/track sprints and inspect frozen completed points. | Preserves team-specific delivery facts. | Granted managers/readers | Available Today; missing historical coverage is unknown. |
| Milestones and timeline (F-011,031) | Track key dates through timeline/table and eligible variance. | Helps investigate timing. | Granted managers/readers | Available Today; initial bounded timeline. |
| Dependencies (F-012,032) | Link permitted predecessors/successors and inspect relationships. | Shows reliance between work. | Granted managers; Admin for cross-project changes | Available Today. |
| Blockers (F-012,032) | Record obstacles and inspect affected work. | Makes current impediments visible. | Granted managers/readers | Available Today. |
| Reported status and health | Append status reports without hiding computed disagreement. | Preserves the manager's stated position. | Granted managers/readers | Available Today. |
| Plan baselines and metric plans | Preserve plan versions; select baseline/calendar and recorded cost forecast. | Anchors comparisons without rewriting earlier plans. | Granted managers/readers | Available Today; entered forecasts are not AI predictions. |
| Budgets/expenditure/reversals (F-010,028) | Record approved budget, spend and exact corrections by currency. | Supports reconciliation. | Granted managers/readers | Available Today. |
| Business change history | Inspect permitted changes and saved versions. | Explains how a plan evolved. | Admin; authorized actors/readers as permitted | Available Today; scope and latest-entry limits apply. |
| Rich scheduling and priority design | Possible later scheduling interactions and project ranking controls. | Could support more detailed planning. | Project/portfolio managers | Completion Still Needs Confirmation; no drag-and-drop optimizer or exact priority method confirmed. |

### Resources and capacity

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Independent resources and teams (F-008) | Maintain profiles without requiring logins and dated reporting teams. | Describes the workforce separately from accounts. | Admin; resource-granted Project Manager | Available Today. |
| Skills search | Record skills and filter exact matches. | Helps identify candidates. | Resource planners | Available Today. |
| Calendars, availability and leave | Record schedules/holidays/approved leave over dates. | Establishes recorded working capacity. | Authorized resource managers | Available Today; no leave-request workflow. |
| Allocations (F-013) | Plan hours across authorized projects. | Makes shared commitments explicit. | Authorized resource/project managers | Available Today. |
| Staffing matrix/heatmap | Inspect daily/weekly plans and equivalent tables. | Makes conflicts easier to locate. | Authorized planners/readers | Available Today. |
| Planned utilization/excess (F-014,036) | Review eligible full or qualified subset measures. | Identifies overload and apparent spare capacity with scope limits. | Authorized planners/readers | Available Today. |
| Actual effort and completeness | Enter permitted effort and review attested eligible utilization. | Separates reported actual work from plans. | Explicit effort-granted members | Available Today; Viewer cannot read sensitive effort. |
| Team workload/overtime support | Review eligible, sufficiently large team signals. | Supports discussion of sustained strain. | Full-scope authorized managers | Available Today as deterministic signals. |
| Planning snapshots | Preserve Admin-captured allocations/calculations before changes. | Supplies a stable planning reference. | Admin | Available Today; not automatic history of every edit. |
| AI staffing recommendations (F-045) | Review proposed options grounded in skills/capacity. | Helps investigate constraints. | Authorized resource managers | Planned for the Complete Product. |
| Automatic staffing-gap detection | Possible richer demand/vacancy identification. | Could support recruitment/planning discussions. | Resource managers | Completion Still Needs Confirmation; exact demand model unspecified. |

### Assessments

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Framework builder/publishing (F-016) | Define weighted dimensions, questions, rubrics and immutable versions. | Makes scoring rules stable and inspectable. | Admin; delegated draft editors | Available Today. |
| PMO example (F-019) | Adapt a labelled capability framework. | Starts a structured PMO discussion. | PMO/Admin | Available Today. |
| Agile example (F-020) | Adapt questions about Agile practices. | Reviews consistency of delivery practices. | PMO/department leaders | Available Today. |
| Governance example (F-021) | Adapt questions about agreed oversight practices. | Highlights gaps against chosen rules. | PMO/Admin | Available Today; no certification. |
| Delivery example (F-022) | Adapt delivery capability questions. | Supports practical improvement review. | PMO/project leaders | Available Today. |
| Assignment/autosave/submission (F-017) | Answer a published version within named assignment. | Collects accountable responses. | Assigned Admin/Project Manager | Available Today. |
| Independent review/return/adjustment | Review, release evidence, adjust with reasons and complete. | Keeps approval separate from self-assessment. | Named independent reviewer | Available Today. |
| Evidence notes/plain-text attachments | Explain answers and submit restricted files for release. | Supports checking the response. | Respondent/reviewer | Available Today within narrow text limits. |
| Scores/coverage/history | Inspect bars, tables, approved results and preserved definitions. | Distinguishes result quality and completeness. | Assigned/permitted result readers | Available Today. |
| Compatible departmental comparison (F-018) | Compare completed results on the same version. | Avoids misleading comparisons. | Permitted PMO/department readers | Available Today for the full permitted completed cohort within the selected version and UTC creation period. |
| Semantic evaluation (F-023) | Review AI interpretation/suggested scores beside calculated/approved scores. | Adds narrative interpretation for review. | Assigned reviewers | Planned for the Complete Product. |
| Pattern/gap detection and suggestions (F-024–025) | Inspect supported maturity gaps and improvements. | Connects answers to practical next steps. | PMO/department leaders | Planned for the Complete Product. |
| Longitudinal assessment presentation/radar | Possible specialized charts for change over time. | Could aid recurring assessments. | PMO leaders | Completion Still Needs Confirmation; current bars/tables and preserved results verified. |

### Command center, risks and imports

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Executive view (F-026–029) | Review covered health, money, benefits and alignment. | Supports portfolio oversight. | Executives/PMO within scope | Available Today. |
| Delivery view (F-030–032) | Inspect velocity, variance, blockers and dependencies. | Locates delivery concerns. | Authorized project/PMO readers | Available Today. |
| Risk register/view (F-015, F-033) | Maintain owners, seriousness, mitigation/review/lifecycle and inspect rule components. | Supports accountable risk handling. | Granted managers/readers | Available Today. |
| Resource view (F-036) | Review shared capacity and eligible team support signals. | Connects delivery with staffing. | Authorized managers/readers | Available Today. |
| Reported/evidence discrepancy (F-037) | Investigate a reassuring status contradicted by facts. | Reveals a specific reason for attention. | Authorized managers/readers | Available Today. |
| Filters/saved views (E-003) | Save personal period/portfolio/view choices. | Makes repeated reviews easier. | Granted members | Available Today. |
| Evidence/freshness/coverage (E-001–002) | Open contributing facts and missing/stale indicators. | Helps judge a number's usefulness. | Granted readers | Available Today. |
| JSON snapshot download | Download current authorized dashboard data. | Reuses a consistent snapshot. | Granted readers | Available Today. |
| CSV mapping/preview/import (E-009) | Preview mapped rows, queue and repeat supported imports. | Brings work information into projects. | Admin | Available Today within CSV bounds. |
| Jira/GitHub local fixtures (E-009) | Demonstrate issue/sprint/PR mappings with labelled supplied data. | Tests the supported adapter behavior. | Admin | Available Today as fixtures. |
| Live Jira Cloud/GitHub and native hook | Connect real authorized sources and receive supported source events. | Could reduce repeated manual entry. | Admin/operator | Completion Still Needs Confirmation; real authentication/sync/external hook delivery unverified. |
| Data-quality/sync history (E-007) | Inspect rejected rows, source conflicts and corrected sync outcomes. | Makes import problems actionable. | Admin/authorized initiator | Available Today. |
| Background progress/recovery (F-038) | Observe stages, reconnect, cancel and inspect partial/failure outcomes. | Avoids losing progress or hiding rejected work. | Authorized run readers | Available Today for supported imports; not all edits broadcast live. |

### Documents, specialist intelligence and forecasts

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Requirements document library (F-065) | Upload/classify software, business and product requirements. | Makes requirements available as authorized evidence. | Authorized document managers/readers | Planned for the Complete Product. |
| Minutes/sprint reports (F-066) | Process written meeting minutes and delivery reports. | Adds attributable delivery evidence. | Authorized document managers/readers | Planned for the Complete Product. |
| Risk logs, charters, policies (F-067–069) | Preserve versions/types and inspect source locations. | Supports risk and governance investigation. | Authorized managers/readers | Planned for the Complete Product. |
| Scan recognition and retrieval (F-073–074) | Read scans, search permitted passages and inspect confidence/citations. | Makes evidence easier to find. | Authorized readers/Copilot users | Planned for the Complete Product. |
| Proposed extracted findings (F-070–072) | Review risks, blockers, dependencies, policy gaps and maturity indicators. | Turns evidence into checkable proposals. | Authorized managers/reviewers | Planned for the Complete Product. |
| AI run stages/operations (F-039, E-008) | Monitor observable analysis progress, provider status, errors and budgets. | Shows availability and usage honestly. | Users for own runs; Admin for oversight | Planned for the Complete Product. |
| PMO/Risk specialists (F-040–041) | Review portfolio synthesis and supported risk/mitigation findings. | Organizes cross-project concerns. | PMO/project leaders | Planned for the Complete Product. |
| Governance/Agile specialists (F-042–043) | Review policy/rubric gaps and practice improvements. | Supports organizational improvement. | PMO/department leaders | Planned for the Complete Product. |
| Executive/Resource specialists (F-044–045) | Review briefings and capacity-aware staffing proposals. | Makes evidence useful for different decisions. | Executives/resource managers | Planned for the Complete Product. |
| Financial/Schedule specialists (F-046–047) | Review costs, milestones, baseline and dependency findings. | Helps investigate budget/timing concerns. | Authorized managers | Planned for the Complete Product. |
| Sentiment specialist (F-048, F-060) | Inspect team-level textual support signals with uncertainty/privacy controls. | May surface themes worth discussing. | Authorized managers | Planned for the Complete Product; no diagnosis or individual ranking. |
| Combined specialist findings (F-049) | See disagreements, missing analyses and merged supported proposals. | Prevents a failed analysis appearing complete. | Authorized managers | Planned for the Complete Product. |
| Sprint/project/milestone delay (F-050–052) | Review eligible estimates of future timing. | Supports earlier investigation/planning. | Project/PMO leaders | Planned for the Complete Product; eligibility needs evidence. |
| Budget overrun and risk trends (F-053–054) | Inspect forecasts by currency/horizon and comparable changes. | Supports financial review. | Authorized leaders | Planned for the Complete Product. |
| Resource inefficiency/team strain trends (F-055–056) | Review eligible workload/overtime/velocity/sentiment indicators. | Supports planning and team support. | Authorized resource/PMO leaders | Planned for the Complete Product. |
| Predictive failure indicators/probability/delivery confidence/risk categories (F-035, F-057–059) | View evaluated outcomes, confidence and categories when eligible. | Adds qualified forward-looking information. | Authorized leaders | Planned for the Complete Product; final labels/calibration/promotion need confirmation. |
| Copilot and follow-ups (F-075–076) | Ask scoped questions, check cited explanations and possible impact. | Helps connect facts and investigations. | Authorized members | Planned for the Complete Product. |
| Natural-language analytics (F-077) | Request supported filters/tables/charts in ordinary language. | Makes permitted analytics easier to use. | Authorized members | Planned for the Complete Product. |

### Decisions, transformation and advanced tools

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Approval flows (F-084) | Propose, review, reject/return/reassign and authorize supported actions. | Preserves accountable decisions. | Eligible assigned managers/approvers | Planned for the Complete Product. |
| Escalation/reminders/SLA/milestone updates (F-034, F-085–088) | Track due actions and receive configured in-app follow-up. | Supports timely handling under agreed policy. | Responsible members/approvers | Planned for the Complete Product. |
| PMO/Agile roadmaps (F-078, F-083) | Review evidence-linked improvement initiatives. | Connects gaps with an actionable plan. | PMO/department leaders | Planned for the Complete Product. |
| Process/governance improvement (F-079–080) | Draft practices and decision/reporting structures. | Supports consistent responsibilities. | PMO/Admin | Planned for the Complete Product. |
| KPI frameworks/delivery strategy (F-081–082) | Define measures, targets, owners, resource/tooling assumptions and review cadence. | Makes improvement testable. | PMO/leadership | Planned for the Complete Product. |
| Decision log and initiative history (E-005) | Record alternatives, reasons, approvals and observed outcomes. | Retains the thinking behind decisions. | Authorized decision-makers | Planned for the Complete Product. |
| Approved initiative conversion | Link an initiative to existing/new project work after authorization. | Connects strategic planning and delivery. | Eligible approvers/managers | Planned for the Complete Product. |
| Budget/resource scenarios (F-099–100, E-006) | Compare budget cuts/transfers with preserved baseline and assumptions. | Examines tradeoffs before live changes. | Authorized project/resource leaders | Planned for the Complete Product. |
| Relationship map (F-089–093, F-095) | Explore project/team, team/skill, project/risk, risk/dependency and portfolio/goal links. | Explains organizational connections. | Authorized readers | Planned for the Complete Product. |
| Impact/root-cause paths (F-094) | Trace supported links and inferred hypotheses to evidence. | Organizes investigation of wider effects. | Authorized managers | Planned for the Complete Product. |
| Internal benchmarks (F-101–104) | Compare compatible departments, teams, portfolios and delivery maturity. | Supports fairer comparisons. | Authorized leaders | Planned for the Complete Product. |
| Meeting audio/transcripts (F-096) | Upload authorized material, inspect transcription and corrections. | Preserves meeting evidence. | Authorized meeting managers/readers | Planned for the Complete Product; format/provider limits need confirmation. |
| Minutes/actions/blockers (F-097–098) | Review cited drafts and approve supported conversion to project records. | Keeps commitments checkable. | Authorized managers/approvers | Planned for the Complete Product. |

### Reports and communication

| Feature | What the user can do | Why it is useful | Intended user | Status |
| --- | --- | --- | --- | --- |
| Weekly executive summaries (F-105) | Review scheduled snapshot-based updates. | Provides a consistent management briefing. | Authorized executives/PMO | Planned for the Complete Product. |
| Email/Slack risk alerts (F-106–107) | Receive authorized qualifying threshold/spike alerts. | Directs attention to material changes. | Approved recipients | Planned for the Complete Product. |
| Daily executive audio (F-108) | Listen to an approximate two-minute briefing and inspect its transcript. | Adds a convenient review option. | Authorized executives | Planned for the Complete Product. |
| PDF/HTML reports (F-109) | Preview/download supported rendered reports with shared facts/evidence. | Supports readable stakeholder review. | Export-granted members | Planned for the Complete Product. |
| Delivery controls/preferences | Configure recipients, previews, test-to-self, schedules, quiet hours and allowed subscriptions. | Helps deliver the right information. | Admin; recipients within allowed choices | Planned for the Complete Product. |
| Dedicated exports/other notification channels | Possible separate assessment/resource templates, CSV/XLSX exports, status/assignment feed or mobile push. | Potential sharing/coordination uses. | Relevant users | Completion Still Needs Confirmation; do not treat these as promised formats/channels. |

Requirements F-061–064 concern assessing training-data suitability and creating controlled test data. They support forecast validity but are not business-user features. Their relevance is the distinction between a tested demonstration and a model that is eligible for real organizational predictions.

## 13. Current Features vs Planned Features

### The evidence-backed checkpoint

The latest handoff and 9 October verification report identify Sprint 08 as the current implemented checkpoint. Recorded fresh checks include **67 passing backend tests**, **nine existing browser workflows**, a further enhanced focused import workflow and persisted-record checks. Current implementation/source inspection agrees with the delivery, capacity, assessment, command-center and import boundaries described above.

This documentation task reviewed those records and relevant source/tests; it did not rerun application tests, authenticate to providers or certify a deployment. The evidence supports bounded local behavior, not every intended capability end to end.

| Available Today | Planned for the Complete Product | Completion Still Needs Confirmation |
| --- | --- | --- |
| Accounts/organizations/roles; shared navigation; portfolios/programs/projects/goals/work/budgets/baselines/history. | General document library, scan recognition and scoped retrieval. | Real invitation/reset email delivery configuration and verification. |
| Calendars/resources/skills/allocations, scoped capacity/effort, team support signals and Admin planning snapshots. | AI gateway, nine specialist analyses, semantic assessment/document findings and Copilot. | Actual Jira/GitHub authentication/sync and externally delivered GitHub events. |
| Versioned frameworks, assignments, autosave, text evidence/review, scores/bars/tables and compatible departmental comparison. | Eligible forecasts, broader trends and internal benchmarks. | Production forecast eligibility, precise failure labels, provider/model/budget choices. |
| Four command-center views, risk lifecycle, benefits, evidence/coverage/freshness, saved views and JSON snapshot. | General workflows, escalations, reminders, response-time tracking and transformation decisions. | Final advanced screen layouts, dedicated role homes, radar chart, longitudinal assessment design and some administration screens. |
| CSV import, labelled Jira/GitHub fixtures, provenance/errors, durable recovery, cancellation and import progress refresh. | Simulations, relationship mapping, meeting intelligence, PDF/HTML reports, email/Slack alerts, audio and passkeys. | Dedicated report templates, extra export formats, generic status/task notifications, workforce/retention policies and production/release acceptance. |

### Source discrepancies and the interpretation used

| Discrepancy or uncertainty | Reliable interpretation | Basis |
| --- | --- | --- |
| Roadmap opening says only Sprint 00 is complete; older handoffs, reuse plan and agent entry point name earlier next sprints. | These are historical checkpoint statements. Use the latest handoff/fresh report for current implementation; retain the roadmap table for future scope/order. | Latest handoff, verification report and current modules. |
| Older AI chapter describes durable jobs as future Sprint 08 work. | Its no-AI conclusion remains correct; its job status is superseded by the Sprint 08 contract, source and checks. | Jobs contract and current import workflow. |
| Plans mention `/dashboard` or `/assistant`. | Current verified dashboard is `/command-center`; future Copilot's exact final route is not assumed. | Current navigation/components versus proposed screen plan. |
| Original source requests radar/Gantt-style displays. | Current assessments have bars/tables; current timeline is an initial bounded date view. Do not claim radar, full scheduling or drag-and-drop exists. Final richer presentation needs confirmation. | Assessment/delivery source and fresh verification. |
| Source describes AI “thought process” streaming. | Show observable stages and concise support summaries, not private internal reasoning. | Decision D06, AI decision record and ordered Sprint 10. |
| Source calls for semantic assessment and predictive intelligence; reports describe scores and warnings today. | Current scores/warnings use defined calculations. Semantic suggestions and evaluated forecasts are separate future deliverables. | Assessment/command contracts, current source and Sprints 11–14. |
| Supplement emphasizes burnout detection and says validation prevents malformed AI outputs. | Use privacy-controlled team support signals without diagnosis. Validate/fail safely; validation cannot guarantee truthful AI answers. | D07–D09 and AI governance plan. |
| Local Jira/GitHub fixture acceptance appears in a completed sprint. | Local adapter behavior is verified; real provider authentication/sync remains unverified. | Fresh report and jobs support boundaries. |
| Source lists six specialist agents; supplement adds finance/schedule/sentiment. | Preserve all nine planned analysis responsibilities. They are not separate access roles. | Coverage F-040–049 and ordered Sprint 11. |
| General permission matrix is broader than current assessment behavior. | Use the implemented named-assignment/result-grant rules today; Admin alone cannot answer/review or bypass private evidence. | Assessment contract and negative verification cases. |
| A named “Reports” area implies every specialized export exists. | JSON snapshot works today; PDF/HTML and weekly/audio delivery are planned. Dedicated assessment/resource templates and other formats remain unspecified. | Command contract, coverage F-105–109 and Sprint 21. |
| Final name, custom roles and enterprise identity extensions are mentioned as possibilities. | AI-PPM/Enterprise PPM is a working name; Admin/Project Manager/Viewer is the approved initial role model. SSO/SCIM/custom roles remain extensions requiring confirmation. | Product scope, source index and Sprint 22. |

### References for checking scope and status

The business narrative above is grounded in these local project sources:

- [Original specification index](../source/INDEX.md), [readable Word specification](../source/Word-Specification-Extract.txt) and [supplementary specification](../source/Supplementary-Specification.txt): full product intent, including all eight modules and advanced features.
- [Product scope and personas](../requirements/product-scope.md), [coverage matrix](../requirements/coverage.md), [decision register](../requirements/decisions-and-assumptions.md), [roadmap](../requirements/roadmap.md) and [ordered Sprint 00–23 plans](../prompts/02-ORDERED-SPRINT-PROMPTS.md): reconciled scope, responsibilities and planned behavior.
- [Latest handoff](../handoffs/LATEST.md), [Sprint 08 report](../03-sprints/completed/sprint-08/SPRINT_REPORT.md), [fresh verification report](../04-testing/SPRINT_VERIFICATION_REPORT.md) and [current limitations](../02-learning/08-deployment-and-operations/OPERATIONS_AND_LIMITS.md): present evidence and unresolved environments. Earlier reports 00–07 were reviewed as history, with subsequent verification notes considered.
- [Delivery](../contracts/delivery.md), [capacity](../contracts/capacity.md), [assessment](../contracts/assessment.md), [command center](../contracts/command-center.md), [jobs/integrations](../contracts/jobs-integrations.md), [permissions](../contracts/permissions.md), [metrics](../contracts/metrics.md) and [frontend](../contracts/frontend.md): exact current behavior and restrictions.
- [Screen/reuse plan](../planning/PRODUCT-REUSE-AND-SCREEN-PLAN.md), [AI governance decision](../architecture/adr/005-ai-and-model-governance.md) and [quality plan](../requirements/quality-plan.md): proposed experience, intelligence boundaries and release evidence requirements.

Current interface/source cross-checks included workspace/navigation, delivery forms, resource planning, assessments, command center and integrations, together with their browser workflows and owning behavior contracts. Proposed screens and example data were not counted as implementation proof.

## 14. Product Boundaries and Limitations

### Information and decisions

AI-PPM is intended to manage connected project/portfolio facts, staffing plans, assessments, evidence, risks and improvement decisions. Users or authorized connected systems must supply dates, work progress, budgets/spend, calendar availability, allocations, responses and relevant evidence. An import does not establish that its contents are complete or correct.

Human responsibility remains necessary for strategy, funding, staffing, risk acceptance, review and material changes. AI generation does not approve a decision. Forecasts, scenario assumptions and policy-gap findings require appropriate interpretation.

The documented scope does not provide automatic currency conversion, an unrestricted analytics query engine, autonomous hiring, medical diagnosis, individual workforce ranking or compliance certification. It does not establish a complete accounting/payroll system or a general-purpose issue/service desk; any broader replacement claim needs confirmation.

### Integrations actually supported or planned

The named work connectors are CSV, **Jira Cloud** issue/sprint data and **GitHub** issue/pull-request data. Current provider host/input limits apply; arbitrary self-hosted Jira, GitHub Enterprise hosts, commit-history imports and raw workforce notes are not supported by the current adapters. Research/training references to repository data do not create a general product connector.

Planned outbound delivery uses configured **email and Slack**. Planned AI, transcription and speech services use selected configured providers; a specific final provider is not promised. Versioned document upload is now local Sprint 09 scope; meeting uploads remain planned. Neither is not evidence of SharePoint, Drive, Teams, Outlook or other named integrations. Additional integrations need explicit scope confirmation.

### Current practical boundaries

- Dashboard snapshots are bounded to 200 visible projects, 100 assigned resources and 5,000 rows per project-source kind. Exceeding a bound fails explicitly rather than silently returning incomplete totals. Selected capacity/dashboard intervals are 1–366 days.
- Some lists/selectors show at most 100 records; work boards and timelines have stated loaded-item limits. A visible page is not automatically a whole-organization total.
- Assessment attachments are UTF-8 `.txt`, up to 512 KiB each and at most 50 per assessment. Independent release is human attestation, not automated antivirus verification.
- CSV imports allow up to 500 rows within the documented input limit. Live provider adapters use bounded pages/jobs. Partial processing retains accepted effects; cancellation does not roll back committed rows. Fix rejected input and start a corrected sync.
- Connector definitions are immutable. Source/local-edit collisions require review, and separately configured connections can create separate effects. Current background authority depends on an initiating authorized session; unattended production identity needs a settled design.
- Restricted/partial views must not expose hidden project names or imply complete resource utilization. Team-sensitive aggregates have scope and minimum-group rules.
- Current history and snapshots preserve important records, but do not reconstruct every past dashboard. Automatic physical evidence/job purge and production retention policy are not configured.

### Conditions for a completed release

The plans contain performance, accessibility, security, availability, backup and recovery targets. A target is not a measured guarantee. Production readiness requires integrated journeys, real-provider checks where relevant, suitable prediction evidence, approved data/provider policies and measured deployment/recovery results.

Final cloud environment, retention rules, workforce evidence policy, budget and release decision still need confirmation. The product can deliver much of its operational value while a model remains ineligible; the interface must clearly label the unavailable prediction. Completion of a sprint prompt alone does not establish the entire product is finished.

## 15. Expected Experience of the Completed Product

After activation/sign-in, users will select an organization and see available navigation appropriate to their role and grants. Passkeys are intended to add another supported sign-in option. The final default landing choice for every persona is not yet defined; today sign-in leads to account access and the workspace is separately available.

Users will find projects through authorized lists/search and move between their details and portfolio views. A manager will maintain the work and plan, then inspect an overall warning and its supporting facts. Indicators will explain insufficient evidence, stale information or partial access rather than hide the limitation behind a color.

Assessment respondents will resume assigned questions and see whether saving succeeded. Reviewers will check evidence and approve/return results. Resource planners will inspect skills, calendar-based availability and shared commitments with appropriate privacy controls.

The planned assistant will help connect evidence in ordinary language. Documents, relationship paths and forecasts will be checkable at their source. Recommendations will move into reviewable proposals. Scenario exploration will preserve live plans until an authorized decision is applied.

Meeting findings and transformation initiatives will connect to project work after review. Reports and permitted updates will use the same facts rather than another set of totals. Decision and change history will help people follow up on what was agreed and what happened afterward.

The intended experience is continuous investigation and accountable action. Specific advanced menu labels, screen arrangements and every possible dashboard widget are still subject to implemented design and acceptance.

## 16. Future Roadmap

The following stages preserve the numbered dependency plan. Sprint numbers identify work packages, not dates or guaranteed durations. Latest evidence supersedes historical introductory checkpoint wording in the roadmap.

| Stage / planned sprints | User problem addressed | Intended deliverables and overall improvement | Current standing |
| --- | --- | --- | --- |
| Scope and foundation, 00–03 | No dependable shared workspace/access model. | Reconciled requirements, account/organization controls and usable shared navigation/themes. | Implemented local foundation; production/release targets remain later. |
| Operational PPM, 04–07 | Project, people, assessment and risk information is disconnected. | Portfolios/programs/projects, delivery/budgets/baselines, capacity, reviewed assessments, four dashboards and evidence-backed exceptions. | Available Today within stated local limits. This operational milestone is not AI-complete. |
| Connected input/progress, 08 | Imports and background work are hard to inspect or recover. | CSV/Jira/GitHub mappings, preview/errors, provenance, durable recovery and visible progress. | Local scope verified; live provider environment still needs confirmation. |
| Document evidence and managed AI, 09–11 | Written evidence and narrative practices are difficult to investigate consistently. | Document formats/scans/retrieval, shared AI controls, nine specialists and semantic assessment/document suggestions. | Planned. Intake/retrieval precede shared AI and semantic integration. |
| Forecast evidence and conversation, 12–14 | Leaders need qualified forward-looking analysis and understandable answers. | Historical data/evaluation, eligible forecasts with fallback/uncertainty, Copilot and natural-language analytics. | Planned. Genuine data may block model promotion even when a labelled demonstration works. |
| Accountable improvement and alternatives, 15–17 | Advice and plan changes lack clear review and outcome tracking. | Workflows, escalation/reminders/SLA, transformation/KPIs/decision log, resource/budget scenarios with approved application. | Planned. No automatic live commitment from generated advice. |
| Relationships, fair comparison and meetings, 18–20 | Wider effects, incomparable measures and lost meeting actions obscure decisions. | Relationship/impact maps, internal compatible benchmarks, transcripts/audio, reviewed minutes/actions. | Planned; final cohort/provider/file policies require implementation decisions. |
| Briefings and all-surface access, 21–22 | Stakeholders need consistent authorized updates and stronger access options. | PDF/HTML/weekly reports, email/Slack alerts, daily audio, passkeys, retention/provider settings and access hardening. | Planned; the end of 22 is a functional-scope candidate, not automatic release acceptance. |
| Integrated release acceptance, 23 | Working pieces alone do not prove a dependable whole product. | Complete user journeys, release-wide access/accessibility/performance checks, backup/recovery and configured deployment verification. | Planned. Real release depends on evidence, configuration and unresolved blockers. |

Sprint 09 intake/OCR/keyword retrieval is now locally verified; the next planned capability is the separately authorized Sprint 10 AI gateway/embeddings. See [the current Sprint 09 hub](../03-sprints/completed/sprint-09/README.md). This guide does not execute or authorize a development sprint. No application code was changed to produce it.

## 17. Glossary of Simple Terms

| Term | Simple meaning |
| --- | --- |
| AI | Artificial intelligence: software used here to interpret information and generate advice that people should check. |
| PPM | Project and Portfolio Management: managing individual projects and their collective goals, costs, resources and priorities. |
| PMO | Project Management Office: the group responsible for common project practices and organizational delivery oversight. |
| Organization | The workspace's ownership/access boundary. A department is a subdivision, not another organization by default. |
| Portfolio | A collection of projects/investments considered together. |
| Program | An optional group of related projects within one portfolio. |
| Project | An initiative with a plan, people, work, dates and expected outcomes. |
| Work item | A recorded piece of work within a project. |
| Milestone | An important delivery point or date. |
| Sprint | A defined work period whose closure can preserve team delivery measures. |
| Story points / velocity | A team's estimate units and the completed units in a sprint; not comparable universal productivity units. |
| Dependency | A recorded relationship in which one item relies on another. |
| Blocker | An obstacle currently preventing progress. |
| Risk / mitigation | A possible problem / an action intended to reduce its likelihood or impact. |
| Baseline | A saved version of a plan used as a reference for change. |
| Forecast | An estimate of a future outcome, with its date, assumptions and limitations. A manually entered forecast is not automatically AI-generated. |
| Reported / computed health | The manager's stated condition / an indicator calculated from available inputs. |
| Capacity / allocation | Recorded available working time / planned time committed to work. |
| Utilization | Allocated or eligible actual hours as a proportion of available hours; not an employee performance judgment. |
| Over-allocation | More work is allocated than the recorded capacity supports. |
| Maturity / dimension | Consistency of assessed practices / one area within an assessment. |
| Framework / rubric | The assessment questions and rules / the defined permitted answer levels. |
| Coverage / freshness | How much required information is present / how old the source information is. |
| Evidence | A permitted record, explanation or source passage that supports checking a claim. |
| Copilot / agent | The planned conversational assistant / a specialist analysis responsibility. Neither is a user access role. |
| Recommendation | A proposed action for review; it is not necessarily approved or executed. |
| Scenario | A hypothetical change examined separately from the live plan. |
| Knowledge Graph | A connected map of related projects, teams, skills, risks, dependencies and goals. |
| Benchmark | A comparison with a compatible group using the same meaningful definitions. |
| KPI | Key Performance Indicator: a defined measure with a baseline, target, owner and review schedule. |
| SLA | Service-Level Agreement: an agreed response/action time using the workflow's stated clock. |
| MOM | Minutes of Meeting: the recorded discussion, decisions and actions. |
| OCR | Optical Character Recognition: converting scanned text into readable text, with possible recognition errors. |
| RAG | Retrieval-Augmented Generation: finding permitted relevant passages to support an AI answer. |
| CSV / JSON | A simple tabular text format used for supported imports / a structured data format used by today's dashboard download. |
| PDF / DOCX / XLSX / HTML | Common document, Word, Excel and web-document formats. Only the specific intake/export uses described in this guide are supported or planned. |
| Passkey | A device/browser-supported sign-in credential, planned with enrollment, revocation and recovery controls. |
| SSO / SCIM | Company single sign-on / automated account provisioning; possible extensions requiring confirmation. |

### Documentation quality review

This guide was checked for plain-language explanations, the eight original modules and advanced features, all user-facing requirement groups, realistic journeys, status boundaries, role/grant accuracy, supported formats and the Sprint 00–23 sequence. Unsupported screen details and guarantees were removed or explicitly marked for confirmation. Application tests and production/provider verification were not performed during this documentation-only task.

## Sprint 8.1 execution addendum

Verified signup, first organization setup, profile editing, private delivery lifecycle, existing grant controls, record search, server-paged selectors, full-period comparison, My work, notification receipts, nullable metadata and manual freshness are implemented locally. See the [current tester guide](../03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md) and [acceptance report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md). Earlier general availability descriptions should be read with this addendum. Real SMTP inbox checks, hosted CI and regenerated Word-guide layout remain open; full operational pilot release is not accepted.
