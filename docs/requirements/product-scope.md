# Product scope and user journeys

## Product purpose

Provide enterprise project portfolio intelligence, maturity assessments, governance improvement and evidence-backed decisions. The platform should expose a project reported as healthy when delivery, cost, capacity or policy evidence indicates trouble. It combines transactional PPM data, documents, analytics, workflows and transformation planning; it is not solely a chatbot or a ticket tracker.

## Personas and role mapping

| Persona | Initial role | Main decisions and journeys |
| --- | --- | --- |
| Organization administrator | Admin | Configure organization, invite users, publish frameworks/policies, authorize integrations and review audit history |
| PMO lead or project manager | Project Manager | Manage assigned projects/resources, review risks, run assessments, propose changes and track benefits |
| Executive sponsor | Viewer by default | Read explicitly shared portfolios, evidence, forecasts and briefings; needs a separate authorized approver assignment and an eligible role to approve |
| Assessment respondent | Project Manager in initial role model | Answer assigned assessments and upload evidence within permitted scope |
| Auditor or stakeholder | Viewer | Inspect permitted reports and evidence without changing domain records |

The initial three roles are from S4.1. Custom enterprise roles, SSO and SCIM are future extensions, not hidden requirements. Executive is a persona and agent name, not an automatic administrator role. A user may have different memberships/roles in different organizations.

## Primary journeys

1. Admin creates an organization and scoped memberships; PM creates a portfolio, program/project, goals, baseline and budget.
2. PM allocates resources and records delivery progress. Dashboards reconcile facts and show reported-versus-computed health.
3. Admin publishes a framework; assigned PM submits department evidence; reviewer approves maturity results without changing historical versions.
4. Authorized documents/integrations feed ingestion, retrieval and agents. Findings link to source evidence; users accept or reject proposed risks/actions.
5. A stakeholder asks why a project is delayed. The copilot combines authorized metric tools with retrieval and displays factual support and uncertainty.
6. PM proposes a transformation initiative or a scenario. Approval checks current authority and baseline versions before applying a live change.
7. Approved recipients receive scheduled summaries/alerts/audio; revoked access prevents subsequent delivery and source retrieval.

## Terminology

| Term | Definition |
| --- | --- |
| Organization or tenant | Security and data ownership boundary; not a department |
| Portfolio | Collection of related investments/projects aligned to business goals |
| Program | Optional grouping of projects inside one portfolio |
| Project | Delivery initiative with owners, baseline, budget and explicit access scope |
| Resource | Capacity/skills profile; may exist without a login identity |
| Baseline | Immutable approved plan version; revised plans create a new version |
| Reported health | Human-submitted assessment, retained separately from computed indicators |
| Risk score | Versioned rule/model output in 0–100 units; not automatically a probability |
| Evidence | Access-controlled, versioned source reference for a finding or calculation |
| Recommendation | Proposed action awaiting an authorized decision, not an executed command |
| Forecast | Time-stamped output with horizon, model/data version and uncertainty/eligibility |
| Scenario | Hypothetical snapshot and parameter changes separate from live records |
| MOM | Minutes of meeting with referenced decisions/actions and review history |

## Navigation and interaction

Primary sidebar: Command Center; Portfolios; Projects; Resources; Assessments; Risks; Documents; Copilot; Workflows; Transformation; Scenarios; Knowledge Graph; Benchmarks; Meetings; Reports. Settings contains Members, Frameworks, Policies, Integrations, AI Operations, Audit and Account/Passkeys. Show modules as unavailable until implemented, not misleading working links.

Persistent organization selector, breadcrumbs, scoped search, command palette and notification entry. Project detail tabs: Overview, Work, Timeline, Budget, Resources, Risks, Evidence and Activity. Use slate/navy surfaces, restrained accent color, accessible light/dark modes, limited translucent effects and shared tokens. Target WCAG 2.2 AA; every screen needs loading, empty, forbidden, error, stale and partial-data states. UI screenshots and accessibility evidence start in Sprint 03.

## Boundaries

All eight Word modules and the advanced product features remain in scope. No cloud deployment, real messages, training run, application code or spending occurs in Sprint 00. Names listed in the source are suggestions; use `enterprise-ppm` as a working identifier. Marketing comparisons and resume statements are not acceptance evidence.
