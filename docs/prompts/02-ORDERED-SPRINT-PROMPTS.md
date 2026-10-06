# Ordered module implementation prompts

Run these prompts in numerical order. Every prompt inherits `01-MASTER-PROMPT.md` and its definition of done. Every sprint must produce both documents defined in `03-SPRINT-REPORT-TEMPLATE.md` and `04-FOLLOW-UP-HANDOFF-TEMPLATE.md`. The labels are work packages, not promises that each can be completed within a fixed number of days.

## Sprint 00 Scope reconciliation and architecture contracts

```text
Apply the master build instruction. Execute Sprint 00 only.
Read the full Word specification and supplementary pasted specification before
designing the system. Inspect the repository and preserve existing work.

Create docs/requirements/coverage.md with atomic requirement IDs, exact source
headings, source feature, acceptance criteria, owning sprint, dependencies,
status and evidence columns. Include every core and advanced feature from both
sources. Separate required product behavior, proposed enhancements, alternative
technology suggestions and measurable nonfunctional targets. Keep incomplete
source sections visible rather than guessing missing requirements.

Define the product personas, Admin/PM/Viewer permission matrix, organization
boundaries, project visibility rules, terminology, navigation and module map.
Create an ER diagram covering organizations, memberships, departments,
portfolios, programs, projects, goals, teams, resources, skills, allocations,
milestones, work items, budgets, risks, dependencies, assessment framework
versions, assessments, maturity scores, KPIs, policies, documents, evidence,
recommendations, workflows, scenarios, notifications and AI runs. Group future
entities by their owning module; do not prematurely implement every table.

Record architecture decisions for the proposed stack and source alternatives,
module ownership, queue delivery semantics, tenant isolation, JWT revocation,
vector storage, graph projection, AI provider boundaries and deployment. Define
API/error/event conventions and a versioned metric dictionary. Define reporting
periods, business calendars, status transitions, budget units and risk thresholds.

Acceptance: each source feature has an implementation destination; each module
has inputs, outputs, ownership and dependencies; material contradictions have
an explicit proposed resolution. Write the first report and handoff, clearly
stating that implementation has not yet begun. Do not claim architecture review
or owner approval that has not occurred.
```

## Sprint 01 Repository foundation and reproducible runtime

```text
Apply the master instruction. Prerequisite: Sprint 00 contracts are coherent.
Implement the repository foundation using the approved versions and layout.

Create the Next.js application, FastAPI application, worker entry point, shared
contract generation, PostgreSQL/Redis development services, and local object
storage adapter. Configure exact dependency locks, formatting, linting, types,
structured errors, request correlation IDs and environment validation. Add
health/readiness endpoints that distinguish process health from dependencies.
Create the initial Alembic migration chain and database test infrastructure.

Provide Docker Compose, .env.example with placeholders, clear setup commands,
separate test configuration, and CI for changed application code. Generate the
TypeScript client from OpenAPI and fail CI on contract drift. Add a small real
database round-trip and API-to-web integration check rather than mock-only
health screens. Create secret-safe logging and separate demo configuration.

Acceptance: a fresh checkout can install, start services, apply migrations,
call readiness, load the frontend and run documented checks. Missing environment
values produce actionable errors. API types regenerate deterministically.
Restarting the stack retains persisted data. No production secrets are present.
Document exact commands, ports, dependencies, migration head and known setup
limitations in both required sprint records.
```

## Sprint 02 Organization identity and authorization

```text
Apply the master instruction. Prerequisite: Sprint 01 runtime and migrations.
Implement secure identity and multi-tenant access before other domain modules.

Build organizations, users, memberships, Admin/Project Manager/Viewer roles,
invitation acceptance, verified account activation, login, logout, password
reset and session revocation. Bootstrap the first admin through a controlled
development/admin flow. Prevent removal of the final active organization admin.
Use short-lived JWT access credentials, rotated refresh sessions, secure browser
cookies, CSRF protection, rate limits and bcrypt with explicit input limits.
Password reset tokens must expire, be single-use, and be stored safely.

Implement request-scoped tenant context, permission dependencies, PostgreSQL
row policies with a non-bypass application role, tenant-safe foreign keys and
audit events. Users with multiple memberships can switch only to authorized
organizations. Specify project scope now and enforce it as project data arrives.
Create login, invite, reset, organization switcher, member management and account
settings screens with validation and accessible error messages.

Acceptance: exercise all three roles; reject forged tenant IDs, ID guessing,
expired/replayed tokens and unauthorized role changes. Test logout/revocation,
concurrent refresh behavior, pooled database tenant context, and two organizations
with overlapping names. Invitations never grant membership in another tenant.
Record any unverified real email integration; use a local mailbox for development.
Update the permission matrix, report and handoff.
```

## Sprint 03 Enterprise design system and application shell

```text
Apply the master instruction. Prerequisite: Sprint 02 authenticated sessions.
Build the shared enterprise frontend before separate module-specific screens.

Implement a responsive sidebar, organization switcher, breadcrumbs, top search
entry, keyboard command palette, account controls, notification shell and light/
dark themes. Define tokens for typography, spacing, colors, density, elevation,
focus and motion. Use subtle translucent surfaces selectively. Build reusable
data tables, filters, pagination, forms, dialogs, drawers, metric cards, status
badges, chart frames, skeletons, empty states and permission/error states.

Use real authenticated organization/member data to demonstrate the shell. Keep
future navigation destinations explicitly unavailable rather than adding dead
links. Add a component gallery for development with small, realistic examples.
Define chart/table alternatives, keyboard interaction, responsive breakpoints,
reduced-motion behavior and consistent destructive-action confirmation.

Acceptance: verify keyboard-only navigation, visible focus, screen-reader names,
contrast, readable dark/light themes and layouts around 360, 768 and 1440 pixels.
Avoid horizontal page overflow; large tables may scroll within their own region.
Use automated accessibility checks plus manual review of core flows. Capture
screenshots and record intentional design choices in the sprint report. The
handoff must identify the shared components and tokens later modules must reuse.
```

## Sprint 04 Portfolio and delivery system of record

```text
Apply the master instruction. Prerequisites: Sprints 02 and 03.
Implement transactional PPM entities and workflows used by later intelligence.

Build departments, strategic goals, portfolios, programs, projects, project
membership, teams, owners, work items, sprints, milestones, blockers, dependencies,
status updates, versioned plan baselines, budget lines and actual expenditure.
Support direct portfolio projects and program-linked projects with consistent
ownership. Implement CRUD/archive, validated transitions, search/filter/sort,
pagination, optimistic concurrency and audited changes. Keep reported health
separate from later computed health. Define rules for dependency cycles and
historical baselines. Do not overwrite baseline dates when forecasts change.

Build portfolio and project lists, project overview, timeline/Gantt, work board,
milestone editor, dependency view, budget overview and goal alignment editor.
Use decimal monetary values and currency; do not sum unlike currencies. Add
deterministic tenant-isolated demo fixtures with healthy and troubled projects.

Acceptance: create a goal-to-portfolio-to-project hierarchy, update a work item,
track spending, rebaseline a plan with history and archive a project. Reject
invalid dates, cross-tenant parents, forbidden edits and stale concurrent writes.
Test dependency rules, project visibility and totals against known fixtures.
Dashboard consumers must receive documented DTOs rather than querying arbitrary
tables. Update ER/schema contracts, report and handoff.
```

## Sprint 05 Resource capacity and workload intelligence foundations

```text
Apply the master instruction. Prerequisite: Sprint 04 projects and teams.
Implement resources, skills, availability, calendars, time off, allocations and
actual effort. Clearly distinguish a resource profile from a login identity.

Represent allocations over date ranges in explicit hours or normalized capacity
units. Define working days, part-time schedules, timezones, holidays and how
overlapping allocations combine. Compute planned/actual utilization with zero-
capacity and incomplete-timesheet handling. Flag over-allocation across projects
instead of assuming each project owns the same capacity. Preserve allocation
history so future models can reconstruct the past without future leakage.

Build a staffing matrix, resource profile, skills filters, capacity heatmap,
allocation editor and project/team utilization views. Add supported team-level
workload indicators for sustained overload and overtime. Label these as support
signals; do not diagnose burnout or rank individuals from notes or commit counts.
Add access restrictions for sensitive effort details.

Acceptance: verify a resource split across two projects, leave spanning a
milestone, part-time availability, zero capacity, DST/date boundaries and a
concurrent allocation edit. Cross-project totals reconcile with daily/weekly
capacity. Viewer access cannot mutate allocations. Report formulas, units,
calendar assumptions, privacy controls and data-quality limitations; hand off
the immutable allocation snapshot contract for simulations and ML.
```

## Sprint 06 Enterprise maturity assessment engine

```text
Apply the master instruction. Prerequisite: Sprint 04 organizational hierarchy.
Implement the Word document's full assessment engine before AI interpretation.

Create a custom framework builder with dimensions, questions, answer types,
weights, rubric levels, evidence attachments and versioned publishing. Include
editable starter frameworks for PMO capability, Agile maturity, governance and
delivery capability. Label them product examples, not certified industry models.
Validate weights and scoring bounds. Published framework versions are immutable;
new edits create a version and do not rewrite historical assessments.

Build assessment assignment by organization/department/team, draft autosave,
submission, review, return-for-change and completion states. Implement deterministic
scoring with explicit normalization, missing-answer rules and reviewer adjustments
with reasons. Display dimension scores, radar/chart plus table, evidence coverage,
history and department comparisons only for compatible framework versions.

Acceptance: create/publish a framework, complete two departmental assessments,
review one, change a framework and retain old scores. Verify weighting, all-
missing answers, invalid rubric values and unauthorized submissions. Explain why
scores differ with a worked fixture. AI semantic scoring remains an explicit
future extension in Sprint 11, not a fabricated implementation. Update scoring
contracts, requirements coverage, report and handoff.
```

## Sprint 07 Portfolio command center and metric consistency

```text
Apply the master instruction. Prerequisites: Sprints 04–06.
Implement the Executive, Delivery, Risk and Resource dashboards from the Word
document, using real stored data and one metric service.

Executive: portfolio health, business value, budget use, strategic alignment and
drill-down. Delivery: velocity, milestone variance, blockers and dependencies.
Risk: risk register, owners, severity/likelihood, mitigations and escalation
readiness. Resource: capacity, allocation, utilization and team workload signals.
Implement risk CRUD and lifecycle here if not yet present. Define business value
as recorded targets/realized benefits with units, not an invented AI score.

Add a reported-versus-evidence health comparison to expose the watermelon effect.
Use a versioned deterministic starter rule set, configurable thresholds and
explicit evidence coverage. Do not imply an untrained predictive model exists.
Every KPI shows period, units, source and freshness. Add saved views, date and
portfolio filters, keyboard-accessible drill-down, and an evidence drawer.

Acceptance: totals reconcile across source records, dashboard and export DTOs;
empty/partial/stale states are truthful. A seeded green-reported project with
overdue critical milestones shows a visible discrepancy with supporting facts.
Test filters, role-scoped views, responsive charts and accessible data tables.
Record baseline rendering measurements and query costs without claiming final
performance compliance. Update metric dictionary, report and handoff.
```

## Sprint 08 Durable jobs integrations and live progress

```text
Apply the master instruction. Prerequisite: Sprint 07 metric contracts.
Build the production-shaped asynchronous pipeline shared by ingestion, AI,
notifications, reports and document processing.

Implement a transactional outbox, durable job records, versioned event envelopes,
idempotency keys, retry/backoff, dead-letter handling, cancellation and worker
heartbeats. Use at-least-once delivery with idempotent effects; do not promise
exactly-once external delivery. Enforce tenant context in workers and retry paths.
Add authenticated SSE with event IDs, ordered per-run stages, reconnect/resume,
heartbeats and retention behavior. Show only processing status and evidence.

Create an ingestion adapter contract plus working CSV import, Jira issue/sprint
ingestion and GitHub issue/PR ingestion. Support explicit field mapping, preview,
validation errors, source timestamps, provenance, incremental cursors, API rate
limits, secret references and replay protection for signed webhooks. Never fetch
arbitrary internal URLs supplied by users. Separate fixtures from live connectors.

Build integration settings, sync history, data-quality errors and job activity
screens. Acceptance: crash/restart a worker, replay a webhook and repeat an import
without duplicating domain effects. Verify partial sync recovery and SSE reconnect.
Unauthorized users cannot subscribe to another tenant/run. If credentials are
absent, run contract fixtures and mark live authentication/sync unverified.
Document retry guarantees, connector support boundaries, report and handoff.
```

## Sprint 09 Document intelligence OCR and retrieval

```text
Apply the master instruction. Prerequisite: Sprint 08 durable jobs and storage.
Implement enterprise document upload and retrieval for SRS, BRD, PRD, MOM, sprint
reports, risk logs, project charters and governance policies.

Support PDF, DOCX and text initially, scanned PDF/image OCR, and CSV/XLSX tabular
logs with a documented format matrix. Quarantine unsupported/corrupt/oversized
files. Record document versions, content hashes, access scope, source page or
paragraph/sheet locations, extraction/OCR confidence and processing status.
Use bounded parsers, malware scanning/quarantine, tenant-scoped signed downloads
and retention controls. Reprocessing must not create duplicate active chunks.

Build versioned chunking/embeddings and hybrid retrieval through an interface.
Filter by tenant and project access before retrieval and revalidate citations.
Store original text separately from summaries. Extract candidate risks, blockers,
dependencies, compliance gaps and maturity evidence into a review queue; do not
silently turn document text into authoritative database changes.

Build a document library, upload progress, preview, extracted findings and source
highlight view. Acceptance: test scanned and text PDFs, Word files, tables,
duplicates, changed permissions, malicious instructions and deletion. Deleting
or revoking a source prevents future retrieval and handles derived indexes and
caches under the documented policy. Measure retrieval on a small labeled fixture
set. No missing source may become a fabricated citation. Record report/handoff.
```

## Sprint 10 AI gateway orchestration and evaluation harness

```text
Apply the master instruction. Prerequisites: Sprints 08–09.
Build the common AI runtime before introducing many independent agents.

Implement provider adapters for completion, embeddings and later audio, with one
real configured implementation, deterministic test doubles and disabled states
when credentials are absent. Version prompts, schemas, tools and model settings.
Create AI run records with input snapshots, evidence references, costs/token
usage when available, latency, status and redacted diagnostics. Add per-tenant
budgets, concurrency limits, deadlines, bounded retries, circuit breaking and
Pydantic output validation. Invalid output must fail safely or enter a clearly
labeled fallback; schema validation cannot guarantee factual correctness.

Implement a typed orchestration graph with bounded fan-out, partial results,
aggregation rules and cancellation. Allowlisted tools enforce authorization
independently. Untrusted retrieved text cannot select new tools, change tenant
scope or trigger arbitrary commands. Store concise rationale/evidence summaries,
not private model reasoning. Reuse SSE to expose observable run stages.

Build an AI operations page for admins with usage, errors and provider status.
Acceptance: test timeout, malformed output, over-budget runs, prompt injection,
provider failure, cancellation, partial agents and replay. Add versioned fixtures
for factual support, citation validity, task completion and access leakage.
Define release thresholds before evaluating production agents. Record results
and unresolved real-provider verification in both sprint documents.
```

## Sprint 11 Specialized agents and semantic assessments

```text
Apply the master instruction. Prerequisites: Sprints 06, 07 and 10.
Implement the specialized intelligence described across both specifications.

Create Financial (spend and overrun evidence), Schedule (milestones/dependencies),
Sentiment (team-level textual blockers), Risk (aggregate risks), Resource (capacity
and allocation), Governance (policy/rubric gaps), Agile Coach (delivery practice
improvements), PMO (portfolio synthesis), and Executive (concise briefing) agents.
Each has explicit inputs, allowed tools, typed output, evidence requirements,
fallback behavior, timeout and evaluation cases. Reuse metric services; agents
must not independently redefine budget or schedule formulas.

Add semantic evaluation of assessment answers against their published rubric.
Return suggested dimension scores, textual evidence, gaps and improvements.
Keep original deterministic score, suggested score and reviewer-approved score
distinct. Require a reason for overrides and preserve framework/prompt versions.
Aggregate multi-agent findings with deterministic precedence, duplicate merging,
conflict display and missing-agent indicators. Separate severity from confidence.

Build run details, live stage display, evidence drawer, recommendation review
and discrepancy views. Acceptance: verify every agent with supported and missing
data, contradictory notes, hidden-risk fixtures and malicious source text.
Failing one agent must produce partial/degraded results, not invented success.
No agent can approve its own recommendations or mutate plans. Record per-agent
evaluation evidence, schema contracts, report and handoff.
```

## Sprint 12 Historical data feature pipelines and model baselines

```text
Apply the master instruction. Prerequisites: Sprints 05, 08 and 11.
Build reproducible ML datasets and evaluation before showing predictions as fact.

Define targets, horizons, observation cutoffs and labels for milestone/project/
sprint delay, budget overrun, risk category, delivery failure and team sentiment.
Failure needs a documented operational definition; do not manufacture labels
from the current risk score and then claim independent predictive success.
Create as-of feature snapshots from velocity, bug counts, scope change, spend,
dependencies, allocation and notes without including future information.

Create a dataset manifest with origin, license, permitted use, schema mapping,
label suitability, dates and privacy treatment. Assess PROMISE, licensed Jira
datasets and authorized public GitHub data individually; defect datasets are not
automatically suitable for project delay or failure prediction. Add seeded Faker
synthetic data for demonstration, isolated from real evaluation results.

Build deterministic baseline models and training/evaluation commands, MLflow
tracking, dataset hashes and temporal/entity-aware splits. Compare XGBoost/Random
Forest and a DistilBERT sentiment candidate when labels support them. Define MAE
for delay/overrun and PR-AUC, recall, calibration/Brier scores for relevant
classifiers, with class balance and sample-size context.

Acceptance: reproduce a run, test feature leakage and split overlap, reject an
incompatible dataset, and document missing-data behavior. If genuine historical
labels are insufficient, deliver the pipeline and clearly labeled demo results;
record production model promotion as blocked. Create model cards/report/handoff.
```

## Sprint 13 Forecast serving and predictive analytics views

```text
Apply the master instruction. Prerequisite: Sprint 12 evaluation artifacts.
Integrate approved model versions with the application; keep experimental models
clearly labeled and allow deterministic fallback when evidence is insufficient.

Implement asynchronous batch inference and bounded cached reads, feature schema
validation, model registry promotion/rollback, input freshness checks, prediction
history, drift monitoring and outcome feedback. Expose delay in days, overrun
with currency or percentage units, risk categories, and calibrated failure/delay
probabilities only when evaluation supports them. Define delivery confidence
precisely and display uncertainty/coverage. Do not present a heuristic as a 92%
probability simply because the frontend supports percentages.

Add forecast views for sprints, milestones, projects, budgets and portfolios.
Explain measured feature contributions and evidence limitations without claiming
causal explanations. Show team sentiment/workload trends only under the privacy
and minimum-group rules. Route predictions into existing dashboard DTOs, never
parallel dashboard-specific scoring code.

Acceptance: train/serve feature parity, missing/stale features, incompatible model
version, registry rollback, fallback, tenant boundaries and reproducible fixture
predictions. Measure inference latency with stated hardware/data size. Test UI
for no eligible model, low confidence and stale forecasts. Report which models
are production candidates versus experimental and what evidence is still needed.
Update metric/model contracts and both documentation records.
```

## Sprint 14 PMO copilot and natural language analytics

```text
Apply the master instruction. Prerequisites: Sprints 09–11; use Sprint 13 forecasts
only when eligible. Implement the conversational assistant and analytics explorer.

Support questions such as why projects are delayed, which projects have high
quarterly risk, and which fintech projects are delayed with budget overruns.
Route factual questions to authorized typed metric/query tools and document
questions to scoped RAG. Translate natural language into a validated query plan
over an allowlisted semantic model, not unrestricted SQL. Enforce row limits,
query budgets, allowed joins/aggregations, timeframe and currency semantics.

Build streaming chat with tenant/project-scoped conversation history, evidence
citations, source previews, result tables/charts, follow-up filters and feedback.
Explain ambiguity and missing data; offer clarification when the query cannot
be resolved reliably. Persist useful answers as decision-log drafts or saved
views with provenance. Proposed record changes remain reviewable drafts using
the existing recommendation contract; add approved actions only through workflows.

Acceptance: compare query answers with deterministic expected results, verify
citations and access after membership changes, and test prompt/SQL injection,
oversized queries, provider timeout and requests for unavailable facts. A cited
document cannot override the user's authorization. Evaluate multi-turn context
without cross-project/tenant leakage. Record tool contracts, examples, evaluation
results, report and handoff.
```

## Sprint 15 Workflow automation approvals and escalation

```text
Apply the master instruction. Prerequisites: Sprints 08 and 11.
Implement configurable, versioned approval flows and state machines for risk
escalations, assessment review, recommendations and proposed plan changes.

Support role/person approvers, ordered approval steps, rejection, return for
changes, explicit reassignment, due dates, reminders, SLA clocks and milestone
notifications. Define business-calendar versus elapsed-time SLA behavior.
Prevent self-approval for configured sensitive actions, permission bypass,
duplicate transitions and actions on stale source versions. Revalidate authority
and current data at execution, not just when a request is created.

Use the outbox and job system for due events; add reminder deduplication,
escalation cooldown and audit history. An approved AI action executes only its
typed allowlisted operation. Delivery adapters are connected in Sprint 21; now
provide an in-app approval inbox, workflow builder/editor and timeline with
meaningful empty/failure states. Published workflow changes affect new instances
unless an explicit migration is designed for existing ones.

Acceptance: approval/rejection, two concurrent approvers, approver removed from
organization, failed action execution, worker restart, late reminder and timezone
boundary. Replay events without duplicate business changes. Viewers cannot
approve actions. Document transition diagrams, SLA formulas, delivery assumptions,
test evidence and both required sprint records.
```

## Sprint 16 Strategic transformation and decision tracking

```text
Apply the master instruction. Prerequisites: Sprints 06, 11 and 15.
Implement the strategic transformation engine as evidence-backed planning.

Combine assessment gaps, portfolio risks, governance policies, capacity, goals
and approved recommendations into draft PMO and Agile transformation roadmaps.
Generate process improvement plans, governance structures, reporting hierarchy,
resource models, tooling recommendations, delivery optimization strategies and
KPI frameworks. A request such as improving a 300-member organization's delivery
must capture constraints, timeframe and available evidence rather than assume
staffing or invent savings.

Each initiative needs an owner role, objective, evidence, dependencies, priority,
effort/cost assumptions, quarterly milestones, KPI baseline, target, measurement
method and review cadence. Distinguish expected benefits from observed benefits.
Build roadmap timeline, initiative editor, comparison/history and a decision log
recording alternatives, approver, rationale and follow-up outcomes. Approved
initiatives may link to new or existing projects through idempotent workflow
actions; generation alone must not create live commitments.

Acceptance: trace each roadmap initiative to a gap or stated objective, detect
dependency cycles, preserve edited versions and reject unsupported numeric claims.
Test missing assessments, incompatible frameworks, restricted policy documents
and duplicate project conversion. Document agent/tool reuse, explanation examples,
requirements coverage, report and handoff.
```

## Sprint 17 Time Machine scenario simulator

```text
Apply the master instruction. Prerequisites: Sprints 05, 07, 13 and 15.
Implement the resource-transfer and budget-cut simulations from both sources.

Create immutable baseline snapshots with source versions, capacity/calendars,
dependencies, budgets, risk rules and eligible model versions. Accept typed
changes such as moving two backend developers between projects or cutting a
budget by 25%. Define how skill match, effective dates, resource capacity, task
dependencies and funding constraints affect computed scenarios. Preserve capacity
conservation across all affected projects; do not duplicate shared resources.

Use deterministic scenario rules initially and evaluated prediction models only
within their validated range. Observational ML does not prove the causal impact
of staffing changes: label extrapolation and assumptions explicitly. Return
before/after schedule, cost, utilization, risk, affected dependencies and intervals
only when justified. Explain unavailable metrics instead of fabricating them.

Build sliders plus exact numeric inputs, baseline/scenario comparison, saved
versions and an assumptions drawer. Live data never changes during simulation.
Applying a scenario requires approval, stale-baseline detection and atomic,
idempotent domain updates. Acceptance: no-op, zero budget, invalid headcount,
cross-project effects, repeated run reproducibility, stale snapshot and rollback
on failed application. Document formulas, limitations, report and handoff.
```

## Sprint 18 Enterprise knowledge graph and impact tracing

```text
Apply the master instruction. Prerequisites: Sprints 04, 09 and 11.
Implement the advanced knowledge graph specified in the Word document.

Use Neo4j as a derived projection of PostgreSQL-authoritative entities and
approved extracted relationships. Model Portfolio-to-BusinessGoal, Project-to-
Team, Team-to-Skill, Project-to-Risk and Risk-to-Dependency relationships with
tenant scope, source entity IDs, evidence, timestamps and relationship types.
Keep inferred edges distinguishable from confirmed records. Do not permit a
graph-derived inference to silently modify transactional data.

Implement outbox-driven idempotent projection, delete/tombstone handling,
reconciliation, lag metrics and a full rebuild command. Access Neo4j only through
allowlisted parameterized services that enforce tenant and project permissions;
the client/copilot cannot submit arbitrary Cypher. Limit traversal depth and size.

Build organizational map, project dependency graph, impact path tracing and
source/evidence drill-down, with accessible list/table equivalents. Root-cause
paths show relationships and hypotheses, not proof of causation. Graph failure
must not break core project operations.

Acceptance: rebuild reproduces the graph, repeated events create no duplicates,
deleted/restricted records disappear, and cycles/large graphs remain bounded.
Test cross-tenant traversal attacks, projection lag and recovery. Explain data
ownership and graph query contracts in the report and next-sprint handoff.
```

## Sprint 19 Benchmarking and comparable performance views

```text
Apply the master instruction. Prerequisites: Sprints 06, 07 and 13.
Implement comparisons across departments, teams and portfolios without creating
misleading leaderboards or leaking private data.

Define comparison cohorts by reporting period, delivery methodology, project size,
work type, currency and framework version. Compare delivery reliability, schedule
variance, budget outcomes, utilization and maturity only where denominators and
scales are compatible. Never compare raw story-point velocity between teams as
if story points were a universal productivity unit. Show sample counts, missing
data, coverage and reasons a comparison is unavailable.

Provide median/percentile summaries where appropriate, trend views, accessible
charts/tables, saved cohort filters and drill-down to authorized evidence. Apply
minimum-group thresholds to sensitive workload/sentiment information. Default
to comparisons within one organization. Do not expose cross-customer benchmarks
without a separately authorized data-sharing design.

Acceptance: incompatible maturity frameworks and mixed currencies do not silently
merge; small samples and zero denominators show truthful states. Verify filters,
aggregation arithmetic, access permissions and reproducibility for a fixed period.
Add explanation text stating what comparisons can and cannot establish. Document
cohort definitions, formulas, suppression rules, evidence, report and handoff.
```

## Sprint 20 Meeting intelligence and action extraction

```text
Apply the master instruction. Prerequisites: Sprints 09, 10 and 15.
Implement meeting transcript and authorized audio upload intelligence.

Support transcript files and a documented audio format/duration/size matrix.
Record upload consent/authority, access scope and retention. Transcribe audio
through a provider adapter with timestamps and uncertainty. Do not identify
speakers by biometrics; allow user-supplied speaker labels and corrections.
Process jobs asynchronously with retry-safe chunks, cancellation and clear cost
estimates/limits. Keep original transcript and edited transcript versions.

Generate MOM, decisions, action items, proposed owners/due dates, blockers,
risks and dependency candidates with timestamp or transcript-span references.
Mark ambiguous assignments and dates for confirmation; do not invent commitments.
Build transcript/audio view, generated minutes editor, source jump links and
review/approve workflow. Convert approved actions to work items and approved
risks to the register idempotently. Reprocessing a transcript must not duplicate
previously accepted actions.

Acceptance: multiple speakers, unclear audio, missing owner, contradictory dates,
malicious transcript instructions, cancellation, deleted audio and restricted
meetings. Test no-credential mode transparently with fixtures; distinguish fixture
tests from real transcription verification. Document supported formats, privacy,
evaluation examples, report and handoff.
```

## Sprint 21 Reporting alerts and daily executive audio

```text
Apply the master instruction. Prerequisites: Sprints 08, 11, 13 and 15.
Implement scheduled reporting and delivery, including the daily executive podcast.

Create versioned report snapshots using shared metrics and evidence. Generate
weekly executive summaries and downloadable PDF/HTML reports with period,
currency, freshness, key changes, risks, owners and recommended decisions.
Generate a daily executive script with citations available in its transcript and
an approximately two-minute TTS briefing. Measure duration, allow a text-only
fallback, protect audio access and enforce retention. Do not synthesize a named
person's voice; use a configured standard provider voice.

Implement authorized email and Slack channel configuration, recipient validation,
template previews, test-to-self capability, subscription preferences and delivery
audits. Add threshold-crossing and risk-spike alerts with prior/current evidence,
severity, cooldown, deduplication, recovery behavior and quiet hours. Revalidate
recipient authorization at delivery; avoid leaking sensitive detail in messages.
Use timezone-aware schedules and the durable outbox/queue. Handle ambiguous
provider timeouts using provider idempotency where supported and recorded retry
policy; do not claim universal exactly-once delivery.

Acceptance: weekly and daily schedules, daylight/timezone changes, duplicate
events, provider outage, revoked recipient, unsubscribe and inaccessible evidence.
Inspect generated reports and audio/transcript alignment. Define worker availability
SLI toward the source's 99.9% target; do not claim achieved uptime from a unit test.
Document real-provider versus fixture verification, report and handoff.
```

## Sprint 22 Passkeys and enterprise access hardening

```text
Apply the master instruction. Prerequisites: Sprint 02 identity and all protected
data surfaces. Implement WebAuthn/passkeys using a maintained library.

Build registration, sign-in, credential listing/naming/revocation and account
recovery. Require authenticated recent verification for enrollment and sensitive
changes. Validate challenge expiry and single use, relying-party ID, origin,
user verification and credential ownership. Support multiple credentials and
handle library-reported authenticator/sign-counter behavior appropriately.
Define safe password/passkey recovery policies without weaker support bypasses.
Show usable browser/device compatibility and cancellation/error states.

Review organization membership revocation across sessions, SSE, exports,
retrieval, graph, meeting files, cached answers and queued delivery. Add tenant
settings for retention and AI provider usage; provide audit search/export with
restricted access. SSO/SCIM are possible future extensions, not substitutes for
the requested passkey feature or silently added scope.

Acceptance: use a browser virtual authenticator for repeatable tests and record
any available real-device check. Reject wrong origin, replayed challenge and
foreign credentials. Test revoked credentials, recovery, role changes and
authorization after existing sessions have been established. Repeat cross-tenant
negative tests on every storage/search/stream surface. Document remaining device
coverage, access policy, report and handoff.
```

## Sprint 23 Integrated verification deployment and release handoff

```text
Apply the master instruction. Prerequisite: Sprints 00–22 have traceable status.
Perform the release integration sprint; do not disguise missing scope as done.

Run end-to-end journeys from organization onboarding through projects/resources,
assessment, document/meeting ingestion, agents, forecasts, copilot, approval,
transformation plan, simulation, graph, benchmarking and delivered reports/audio.
Verify Admin/PM/Viewer behavior and at least two isolated tenants. Reconcile every
source requirement with implemented code and acceptance evidence. Repair gaps or
list explicit release blockers; advanced features cannot quietly disappear.

Run measured performance tests with stated hardware, dataset size, concurrency,
network profile and percentile. Evaluate the source targets: sub-second login,
FCP under two seconds, and near-60fps representative chart interaction. Define
realistic p95 budgets in the test plan and record actual results. Use query plans,
indexes, bounded payloads, caching and chart virtualization where evidence shows
need. Test rate limits, accessibility, secrets/dependency scanning, upload abuse,
queue crash/replay, provider failure, backup restore and tenant isolation.

Create production containers, Terraform for the approved AWS ECS/RDS/S3 design,
network/TLS/secrets configuration, migration jobs, least-privilege roles,
observability, cost budgets and CI/CD with rollback. Also supply a documented
Kubernetes deployment profile for the Word document's deployment option, reusing
the same images/configuration; validate locally or mark unverified explicitly.
Define availability/delivery SLIs, monitoring and an error budget for the 99.9%
alerting target. Record recovery time and data-loss objectives as proposed targets
until restore tests establish actual evidence. Live cloud deployment requires
configured credentials, budget and any necessary user authorization.

Deliver administrator/user guides, operations and incident runbooks, backup/
restore and rollback instructions, model/data cards, threat model, API docs,
complete requirement matrix and a ten-minute demo script. Produce the final
sprint report and release handoff with exact revisions, verification evidence,
unverified environments and release decision. Never claim production reliability
or model accuracy that has not been measured.
```

## Final independent review prompt

Use this after Sprint 23, or whenever you want a review without new feature work.

```text
Review this repository against both original PPM specifications and the full
requirement coverage matrix. Do not assume that report status proves completion.
Trace each requirement to working UI/API/data flows and test evidence. Review
cross-tenant access, migration compatibility, model/data validity, citations,
durable job behavior, simulation isolation, accessibility and deployment recovery.
Identify missing features, unsupported claims and integration defects, ranked by
impact, with exact file references and reproducible checks. Separate confirmed
defects from unverified concerns. Update the release checklist and recommend
specific repair sprints; do not call the project complete with unresolved required
scope or critical defects. Produce a concise review report and updated handoff.
```
