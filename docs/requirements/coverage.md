# Requirement coverage matrix

Source keys resolve to exact headings in [source index](../source/INDEX.md). Each row names an independently reviewable capability or constraint. Type: F required feature; N nonfunctional/control requirement; E proposed enhancement; T technology choice; P planning deliverable. Owners are sprint numbers. Dependencies are prerequisite sprint checkpoints, not claims of current completion. `Planned` means not implemented; evidence is deliberately absent until verified. Technical alternatives are resolved in ADRs rather than silently classified as completed product features.

## Sprint 00 planning

| ID | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | User request | Preserve originals and prompts | 00 | None | Both source and all five prompt copies hash-match originals | Complete | source-manifest.json; verification report |
| P-002 | Sprint 00 prompt | Trace scope and source conflicts | 00 | None | Each source capability mapped with acceptance and owner | Complete | This matrix; decisions register |
| P-003 | Sprint 00 prompt | Architecture and domain model | 00 | None | Boundaries, flows, entity relationships and choices documented | Complete | architecture/overview.md; data-model.md; ADRs |
| P-004 | Sprint 00 prompt | Permissions and shared contracts | 00 | None | Roles, project scope, API/events/metrics/versioning specified | Complete | contracts/ |
| P-005 | User request | Explain work and provide continuity | 00 | None | Separate report and latest handoff identify next step | Complete | sprints/SPRINT-00-REPORT.md; handoffs/LATEST.md |

## Identity and core PPM

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | F | S4.1 | JWT login and session lifecycle | 02 | 01 | Valid login succeeds; expired, revoked and replayed credentials rejected | Accepted for local identity | [Sprint 02 checks](../verification/SPRINT-02-CHECKS.md); activation/invite/reset and refresh concurrency included; external email unverified |
| F-002 | F | S4.1 | Admin PM Viewer RBAC | 02 | 01 | Permission matrix passes positive/negative API checks | Accepted for identity/member scope | [Sprint 02 checks](../verification/SPRINT-02-CHECKS.md); future domain actions remain their owning sprint's responsibility |
| F-003 | F | S4.1 | Organization isolation | 02 | 01 | Two-tenant read/write and pooled-connection tests prevent leakage | Accepted for implemented identity surfaces | [Sprint 02 checks](../verification/SPRINT-02-CHECKS.md); RLS/composite references/live membership/selector tests; future surfaces still planned |
| F-004 | F | S4.1 | Passkey enrollment and login | 22 | 02 | Origin/challenge validation and revoked-credential tests pass | Planned | — |
| F-005 | F | WD; WP | Portfolios | 04 | 02,03 | Create/edit/archive portfolio with scoped projects and history | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-006 | F | WD | Programs | 04 | 02,03 | Program and project portfolio membership remain consistent | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-007 | F | WD; WP | Project tracking | 04 | 02,03 | Persist owner, work, status and baseline with concurrency checks | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-008 | F | WD; W3 | Teams and resources | 05 | 04 | Resource may exist without login; team membership/history persisted | Implemented locally | [Sprint 05 checks](../verification/SPRINT-05-CHECKS.md); [capacity contract](../contracts/capacity.md) |
| F-009 | F | W3; W8 | Goals and strategic alignment | 04 | 02,03 | Goal links have explicit weights and drill-down evidence | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-010 | F | W3; S4.2 | Budgets and expenditure | 04 | 02,03 | Decimal/currency totals reconcile without mixed-currency sums | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-011 | F | W4; W7 | Sprints and milestones | 04 | 02,03 | Baseline/forecast/actual dates retained with validated transitions | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-012 | F | W3; W8 | Blockers and dependencies | 04 | 02,03 | Track blockers and reject prohibited schedule dependency cycles | Implemented locally | [Sprint 04 checks](../verification/SPRINT-04-CHECKS.md); [delivery contract](../contracts/delivery.md) |
| F-013 | F | W3 | Resource allocation | 05 | 04 | Date-ranged allocations conserve resource capacity across projects | Implemented locally | [Sprint 05 checks](../verification/SPRINT-05-CHECKS.md); additive allocation hours, shared capacity and explicit excess |
| F-014 | F | W3; S4.2 | Utilization efficiency | 05 | 04 | Capacity/effort formula handles part-time, leave and zero capacity | Implemented locally | [Sprint 05 checks](../verification/SPRINT-05-CHECKS.md); [capacity contract](../contracts/capacity.md) |
| F-015 | F | WD; W3 | Risk register | 07 | 04 | Track owner, severity, likelihood, mitigation and lifecycle | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |

## Assessment and dashboards

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-016 | F | W1/Features | Custom maturity framework builder | 06 | 04 | Publish immutable weighted rubric version with valid question types | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-017 | F | W1/Features | Dynamic assessments | 06 | 04 | Assign, autosave, submit, return and review assessment | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-018 | F | W1/Features | Department scoring | 06 | 04 | Compatible department scores reproduce fixture arithmetic | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-019 | F | W1/Features | PMO capability analysis | 06 | 04 | PMO dimension results link to answers and rubric | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-020 | F | W1/Features | Agile maturity analysis | 06 | 04 | Agile dimension results retain framework version and evidence | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-021 | F | W1/Features | Governance evaluation | 06 | 04 | Governance dimension scores and gaps are reviewable | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-022 | F | W1/Features | Delivery capability scoring | 06 | 04 | Delivery dimension score handles incomplete answers explicitly | Accepted locally | [Sprint 06 checks](../verification/SPRINT-06-CHECKS.md) |
| F-023 | F | W1/AI Features | Semantic answer evaluation | 11 | 06,10 | AI interpretation cites answer/rubric and remains separate from approved score | Planned | — |
| F-024 | F | W1/AI Features | Pattern and maturity gap detection | 11 | 06,10 | Fixture inconsistency produces supported gap without fabricated evidence | Planned | — |
| F-025 | F | W1/AI Features | Improvement suggestions | 11 | 06,10 | Suggestions map to identified dimensions and human review | Planned | — |
| F-026 | F | W3/Executive Dashboard | Portfolio health | 07 | 04,05,06 | Weighted health reconciles to covered projects with unknowns displayed | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-027 | F | W3/Executive Dashboard | Business value | 07 | 04,05,06 | Target/realized benefits show explicit units and source records | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-028 | F | W3/Executive Dashboard | Budget usage | 07 | 04,05,06 | Dashboard spend/budget agrees with ledger by currency | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-029 | F | W3/Executive Dashboard | Alignment dashboard | 07 | 04,05,06 | Goal-weight metric and per-project contribution visible | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-030 | F | W3/Delivery Dashboard | Sprint velocity | 07 | 04,05,06 | Count completed points using team-specific definitions and periods | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-031 | F | W3/Delivery Dashboard; S4.2 | Delay and timeline variance | 07 | 04,05,06 | Baseline/actual/forecast variance units and dates are consistent | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-032 | F | W3/Delivery Dashboard | Blocker and dependency visualization | 07 | 04,05,06 | Accessible graph/table drill-down respects project scope | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-033 | F | W3/Risk Dashboard | Project risk score | 07 | 04,05,06 | Versioned deterministic score matches fixtures, no probability claim | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-034 | F | W3/Risk Dashboard | Escalation matrix | 15 | 07,08,11 | Risk severity/role policy routes to correct authorized approver | Planned | — |
| F-035 | F | W3/Risk Dashboard | Predictive failure indicators | 13 | 12 | Eligible model output shows horizon, uncertainty and evidence | Planned | — |
| F-036 | F | W3/Resource Dashboard | Allocation workload dashboard | 07 | 05,06 | Capacity and team workload values reconcile with source allocations | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-037 | F | S1 | Reported versus evidence health | 07 | 04,05,06 | Reported-green troubled fixture displays evidence discrepancy | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| F-038 | F | S4.2 | Live project visibility | 08 | 07 | Authorized event updates dashboard; reconnect resumes or requests snapshot | Planned | — |
| F-039 | F | S4.2 | AI progress streaming | 10 | 08,09 | SSE exposes observable stages, not hidden reasoning or secret inputs | Planned | — |

## Agents and predictive analytics

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-040 | F | W2/Agents | PMO agent | 11 | 06,07,10 | Portfolio synthesis links to scoped metrics and findings | Planned | — |
| F-041 | F | W2/Agents | Risk agent | 11 | 06,07,10 | Structured risks/mitigations validate and missing evidence stays unknown | Planned | — |
| F-042 | F | W2/Agents | Governance agent | 11 | 06,07,10 | Gaps reference policy versions; no unsupported compliance certification | Planned | — |
| F-043 | F | W2/Agents | Agile coach agent | 11 | 06,07,10 | Practice suggestions connect to maturity/delivery evidence | Planned | — |
| F-044 | F | W2/Agents | Executive agent | 11 | 06,07,10 | Concise summary preserves source values and limitations | Planned | — |
| F-045 | F | W2/Agents | Resource agent | 11 | 06,07,10 | Staffing proposals honor capacity and remain unexecuted drafts | Planned | — |
| F-046 | F | S4.3 | Financial agent | 11 | 06,07,10 | Costs match metric service and currency grouping | Planned | — |
| F-047 | F | S4.3 | Schedule agent | 11 | 06,07,10 | Schedule findings reference baseline/dependency versions | Planned | — |
| F-048 | F | S4.3 | Sentiment agent | 11 | 06,07,10 | Team-level blockers include source support and uncertainty | Planned | — |
| F-049 | F | W2; S4.3 | Multi-agent aggregation | 11 | 10 | Partial failure, disagreement and duplicates handled deterministically | Planned | — |
| F-050 | F | W4/Delay Prediction | Sprint delay model | 13 | 12 | As-of sprint labels and out-of-time evaluation precede model promotion | Planned | — |
| F-051 | F | W4/Delay Prediction; S5M | Project delay regression | 13 | 12 | Delay-day MAE versus baseline and horizon documented | Planned | — |
| F-052 | F | W4/Delay Prediction | Missed milestone model | 13 | 12 | Eligible milestone forecast has explicit baseline date and horizon | Planned | — |
| F-053 | F | W4/Budget Overrun Prediction | Budget overrun forecast | 13 | 12 | Forecast spend/overrun values specify currency, horizon and model eligibility | Planned | — |
| F-054 | F | W4/Budget Overrun Prediction | Risk trends | 13 | 12 | Compare versioned time snapshots, flag model/rule changes | Planned | — |
| F-055 | F | W4/Budget Overrun Prediction | Resource inefficiency indicators | 13 | 05,12 | Indicators derive from explicit capacity/effort assumptions | Planned | — |
| F-056 | F | W4/Team Burnout Detection | Team overload signals | 13 | 05,12 | Workload, overtime and velocity-drop signals suppress small groups and avoid diagnosis | Planned | — |
| F-057 | F | W4/Portfolio Failure Prediction | Project failure probability | 13 | 12 | Defined outcome labels and calibration required before probability display | Planned | — |
| F-058 | F | W4/Portfolio Failure Prediction | Delivery confidence | 13 | 12 | Meaning/horizon distinct from risk score and source uncertainty shown | Planned | — |
| F-059 | F | S5M | High Medium Low risk classifier | 13 | 12 | Held-out classification results and threshold policy recorded | Planned | — |
| F-060 | F | S5M | NLP sentiment pipeline | 12 | 05,08,11 | Candidate evaluated on labeled text, not treated as workforce truth | Planned | — |
| F-061 | F | S5D/PROMISE | PROMISE dataset suitability | 12 | 08,11 | License/labels/schema assessed; reject unsuitable task mapping | Planned | — |
| F-062 | F | S5D/JIRA | Jira dataset suitability | 12 | 08,11 | Lineage/permission and temporal splits recorded | Planned | — |
| F-063 | F | S5D/Git Commit Logs | Authorized public repository data | 12 | 08,11 | Source/license/rate limits and as-of feature mapping recorded | Planned | — |
| F-064 | F | S5D/Synthetic Project Data | Synthetic dataset generator | 12 | 08,11 | Seeded schema-valid fixtures isolated from real accuracy claims | Planned | — |

## Documents copilot and transformation

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-065 | F | W5/Supported Documents | SRS BRD PRD classification | 09 | 08 | Each document category retains type, version and source locations | Planned | — |
| F-066 | F | W5/Supported Documents | MOM and sprint report ingestion | 09 | 08 | Both categories yield attributable text/findings | Planned | — |
| F-067 | F | W5/Supported Documents | Risk log ingestion | 09 | 08 | Tabular/text risk candidates enter review without duplicate live risks | Planned | — |
| F-068 | F | W5/Supported Documents | Project charter ingestion | 09 | 08 | Charter evidence links to project and source version | Planned | — |
| F-069 | F | W5/Supported Documents | Governance policy ingestion | 09 | 08 | Restricted policy version used only by authorized consumers | Planned | — |
| F-070 | F | W5/AI Processing | Extract risks and blockers | 11 | 08,09,10 | Sprint 09 candidate interfaces integrate with shared AI gateway; schema and evidence validate | Planned | — |
| F-071 | F | W5/AI Processing | Extract dependencies | 11 | 08,09,10 | Semantic extraction integrates with gateway; proposed edges require review | Planned | — |
| F-072 | F | W5/AI Processing | Compliance gaps and maturity indicators | 11 | 08,09,10 | Semantic findings cite sources and remain provisional until reviewed | Planned | — |
| F-073 | F | W5/Add OCR + RAG | OCR | 09 | 08 | Scanned fixture extracts text with page references/confidence | Planned | — |
| F-074 | F | W5/Add OCR + RAG | Scoped RAG | 09 | 08 | Retrieval prevents access leakage and invalid/deleted citations | Planned | — |
| F-075 | F | W2/Capabilities; WA1 | Conversational copilot | 14 | 09,10,11,13 | Scoped multi-turn answers contain valid evidence or abstain | Planned | — |
| F-076 | F | W2/Capabilities | Root causes and predicted impact | 14 | 09,10,11,13 | Distinguish supported associations, hypotheses and measured predictions | Planned | — |
| F-077 | F | WA2 | Natural language analytics | 14 | 09,10,11,13 | Allowlisted query plan matches deterministic expected answer | Planned | — |
| F-078 | F | W6/AI Generates | PMO transformation roadmap | 16 | 06,11,15 | Initiatives trace to gaps/goals with owner and quarterly milestones | Planned | — |
| F-079 | F | W6/AI Generates | Process improvement plans | 16 | 06,11,15 | Steps, assumptions and measurable outcomes documented | Planned | — |
| F-080 | F | W6/AI Generates | Governance structures | 16 | 06,11,15 | Proposed decision/reporting hierarchy reviewed before adoption | Planned | — |
| F-081 | F | W6/AI Generates | KPI frameworks | 16 | 06,11,15 | Each KPI has baseline, target, unit, owner and cadence | Planned | — |
| F-082 | F | W6/AI Generates | Delivery optimization strategy | 16 | 06,11,15 | Resource/tooling recommendations state evidence and constraints | Planned | — |
| F-083 | F | W6/AI Generates | Agile transformation roadmap | 16 | 06,11,15 | Sprint/process changes map to approved improvement initiatives | Planned | — |

## Workflows graph and advanced capabilities

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-084 | F | W7/Features | Approval flows | 15 | 08,11 | Versioned state machine rejects unauthorized/stale/self-approved actions | Planned | — |
| F-085 | F | W7/Features | Escalation system | 15 | 08,11 | Correct next approver notified once per qualifying transition | Planned | — |
| F-086 | F | W7/Features | Automated reminders | 15 | 08,11 | Retry/restart does not duplicate reminder side effects | Planned | — |
| F-087 | F | W7/Features | SLA tracking | 15 | 08,11 | Business/elapsed clocks obey published workflow calendar | Planned | — |
| F-088 | F | W7/Features | Milestone notifications | 15 | 08,11 | Due/late milestone events create scoped in-app notifications | Planned | — |
| F-089 | F | W8/Graph Relationships | Project to Team graph | 18 | 04,09,11 | Projection reflects authorized project/team relationships | Planned | — |
| F-090 | F | W8/Graph Relationships | Project to Risk graph | 18 | 04,09,11 | Risk edges track updates and deletions without duplicates | Planned | — |
| F-091 | F | W8/Graph Relationships | Team to Skill graph | 18 | 05,09,11 | Skills traverse only within scope and bounded depth | Planned | — |
| F-092 | F | W8/Graph Relationships | Risk to Dependency graph | 18 | 04,09,11 | Evidence distinguishes inferred versus approved dependency edges | Planned | — |
| F-093 | F | W8/Graph Relationships | Portfolio to Business Goal graph | 18 | 04,09,11 | Goal links retain canonical IDs and provenance | Planned | — |
| F-094 | F | W8/AI Benefits | Impact and root cause tracing | 18 | 04,09,11 | Bounded paths cite evidence, show lag and avoid causality claims | Planned | — |
| F-095 | F | W8/AI Benefits | Organizational mapping | 18 | 04,09,11 | Graph and accessible table agree with authoritative records | Planned | — |
| F-096 | F | WA3 | Meeting recording/transcript intake | 20 | 09,10,15 | Audio/transcript formats validated and access/retention applied | Planned | — |
| F-097 | F | WA3 | Meeting minutes generation | 20 | 09,10,15 | Editable minutes reference timestamps/spans | Planned | — |
| F-098 | F | WA3 | Meeting actions and blockers | 20 | 09,10,15 | Unknown owners/dates remain unresolved; approved conversion idempotent | Planned | — |
| F-099 | F | WA4 | Budget-cut simulation | 17 | 05,07,13,15 | 25% reduction scenario preserves live plan and states assumptions | Planned | — |
| F-100 | F | S4.3 | Resource-transfer Time Machine | 17 | 05,07,13,15 | Two-person transfer changes both projects and conserves capacity | Planned | — |
| F-101 | F | WA5 | Department benchmarking | 19 | 06,07,13 | Compatible cohorts show counts and framework version | Planned | — |
| F-102 | F | WA5 | Team benchmarking | 19 | 06,07,13 | No raw cross-team point comparison or small-group sentiment exposure | Planned | — |
| F-103 | F | WA5 | Portfolio benchmarking | 19 | 06,07,13 | Currency/period/size filters yield reproducible comparable aggregates | Planned | — |
| F-104 | F | WA5 | Delivery maturity comparison | 19 | 06,07,13 | Incompatible rubric versions are not silently combined | Planned | — |
| F-105 | F | S4.4 | Weekly executive summaries | 21 | 08,11,13,15 | Scheduled summary matches versioned period snapshot | Planned | — |
| F-106 | F | S4.4 | Email risk alerts | 21 | 08,11,13,15 | Authorized recipients receive threshold-crossing template with deduplication | Planned | — |
| F-107 | F | S4.4 | Slack risk alerts | 21 | 08,11,13,15 | Authorized channel delivery respects cooldown and retries | Planned | — |
| F-108 | F | S4.4 | Daily executive TTS briefing | 21 | 08,11,13,15 | Approximate 2-minute audio agrees with transcript and protected download | Planned | — |
| F-109 | F | S4.4 | HTML email and PDF reports | 21 | 08,11,13,15 | Rendered layouts readable; facts/citations match shared snapshot | Planned | — |

## Controls performance and proposed enhancements

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N-001 | N | S4.1 | bcrypt password hashing | 02 | 01 | Maintained implementation, byte-limit validation, no plaintext storage | Accepted | [Sprint 02 checks](../verification/SPRINT-02-CHECKS.md), bcrypt 5.0.0 cost 12 and UTF-8 byte-limit tests |
| N-002 | N | S4.1 | Sub-second login target | 23 | 22 | p95 under 1 s on documented profile including password verification | Planned | — |
| N-003 | N | S4.1 | Scalable tenant data separation | 23 | 22 | Indexed tenant queries tested at stated load with no isolation failure | Planned | — |
| N-004 | N | S4.2 | Responsive enterprise UI | 03 | 02 | 360/768/1440 layouts usable and keyboard navigable | Accepted for Sprint 03 shell | [Sprint 03 checks](../verification/SPRINT-03-CHECKS.md); [frontend contract](../contracts/frontend.md) |
| N-005 | N | S4.2 | Dark mode and glass effects | 03 | 02 | Tokens/themes retain readable contrast and reduced-motion support | Accepted for Sprint 03 shell | [Sprint 03 checks](../verification/SPRINT-03-CHECKS.md); [frontend contract](../contracts/frontend.md) |
| N-006 | N | S4.2 | FCP under 2 seconds | 23 | 22 | Representative authenticated dashboard meets documented browser profile | Planned | — |
| N-007 | N | S4.2 | 60fps chart rendering target | 23 | 22 | Frame-time distribution reported for documented dataset/device/actions | Planned | — |
| N-008 | N | S4.3 | Nonblocking asynchronous processing | 08 | 07 | Heavy jobs separate from API and restart safely under load | Planned | — |
| N-009 | N | S4.3 | Typed AI output validation | 10 | 08,09 | Invalid provider output never accepted as valid result | Planned | — |
| N-010 | N | S4.3 | Timeout fallback | 10 | 08,09 | Bounded retries and truthful degraded/failure states tested | Planned | — |
| N-011 | N | S4.4 | 99.9% alert worker availability target | 23 | 21,22 | SLI monitoring/runbook created; observed window reported separately | Planned | — |
| N-012 | N | Master prompt | Versioned migrations and contracts | 01 | 00 | Clean/prior-state migration and API client drift checks exist | Foundation accepted; ongoing | [Sprint 01 checks](../verification/SPRINT-01-CHECKS.md); initial base/head lifecycle and contract drift pass; later revisions need new checks |
| N-013 | N | Master prompt | Accessibility target | 03 | 02 | Core keyboard/screen-reader/contrast checks, then release regression | Core checks accepted; release-wide verification ongoing | [Sprint 03 checks](../verification/SPRINT-03-CHECKS.md); full assistive-technology certification not claimed |
| N-014 | N | Master prompt | AI and retrieval access isolation | 10 | 09 | Adversarial source text and changed-access fixtures do not leak data | Planned | — |
| N-015 | N | Master prompt | Model validity and lineage | 12 | 08,11 | Temporal/entity split, model card, baseline and license evidence recorded | Planned | — |
| N-016 | N | Master prompt | Audit retention and revocation | 22 | 02,21 | Revocation covers download/stream/cache/jobs; retention configured | Planned | — |
| N-017 | N | Master prompt | Backup restore and deployment recovery | 23 | 22 | Restore/rollback exercise records measured results and remaining risks | Planned | — |
| N-018 | N | User request | Sprint report and follow-up document | 01 | 00 | Every sprint/sub-sprint updates report, handoff, coverage and evidence | Met through Sprint 02; ongoing | [Report](../sprints/SPRINT-02-REPORT.md), [handoff](../handoffs/SPRINT-02-HANDOFF.md) |
| E-001 | E | Prompt pack enhancement | Evidence drawer | 07 | 04,05,06 | KPI drill-down shows authorized sources and gaps | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| E-002 | E | Prompt pack enhancement | Freshness and data coverage | 07 | 04,05,06 | Stale/missing sources visible without fabricated zeros | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| E-003 | E | Prompt pack enhancement | Saved dashboard views | 07 | 03,04 | Personal scoped filters persist without leaking access | Implemented locally | [Sprint 07 checks](../verification/SPRINT-07-CHECKS.md); [command center](../contracts/command-center.md) |
| E-004 | E | Prompt pack enhancement | Command palette | 03 | 02 | Keyboard navigation exposes only available permitted destinations | Accepted for Sprint 03 shell | [Sprint 03 checks](../verification/SPRINT-03-CHECKS.md); [frontend contract](../contracts/frontend.md) |
| E-005 | E | Prompt pack enhancement | Decision log | 16 | 14,15 | Approved alternatives/rationale and outcome review retained | Planned | — |
| E-006 | E | Prompt pack enhancement | Scenario comparison | 17 | 13,15 | Baseline and scenario differences include assumptions | Planned | — |
| E-007 | E | Prompt pack enhancement | Data-quality console | 08 | 07 | Import errors and rejected rows can be inspected/retried | Planned | — |
| E-008 | E | Prompt pack enhancement | AI usage console | 10 | 08,09 | Tenant usage/errors/budgets visible only to Admin | Planned | — |
| E-009 | E | Ingestion support | CSV Jira GitHub connectors | 08 | 04,07 | Preview/incremental sync/replay limits tested; live credentials explicit | Planned | — |

## Technology and source passages without product acceptance claims

| ID | Type | Source | Choice or passage | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | T | WT; ST | Next.js TypeScript Tailwind shadcn Motion Zustand Recharts; Chart.js alternative | 01 | 00 | Compatible versions pinned; Gantt not misrepresented as built-in chart capability | Partial: foundation and enterprise shell | ADR 007; [checks](../verification/SPRINT-01-CHECKS.md); [ADR 009](../architecture/adr/009-enterprise-shell.md): native shared components implemented; shadcn/Motion/state/chart runtime deferred |
| T-002 | T | WT; ST | FastAPI Python Uvicorn Pydantic; NestJS alternative | 01 | 00 | Async API and schema foundation reproducible | Foundation accepted | ADR 007; [checks](../verification/SPRINT-01-CHECKS.md) |
| T-003 | T | WT; ST | PostgreSQL JSONB SQLAlchemy Alembic Redis | 01 | 00 | Runtime and initial migrations verified | Foundation accepted; domain schema planned | ADR 007; [checks](../verification/SPRINT-01-CHECKS.md); no domain JSONB schema claimed |
| T-004 | T | WT | Pinecone/Weaviate versus pgvector | 09 | 08 | Chosen retrieval adapter records explicit substitution | Planned | ADR 003 |
| T-005 | T | W8; WT | Neo4j | 18 | 04,09,11 | Derived graph rebuild and scope tests pass | Planned | ADR 003 |
| T-006 | T | WT; ST | LangChain; LlamaIndex alternative | 10 | 08,09 | One orchestration/tool contract, no duplicated framework stacks | Planned | ADR 005 |
| T-007 | T | WT; ST | OpenAI Gemini Ollama HuggingFace options | 10 | 08,09 | One configured adapter with supported model and explicit disabled mode | Planned | ADR 005 |
| T-008 | T | W4; WT; S5M | scikit-learn pandas XGBoost Random Forest MLflow | 12 | 08,11 | Reproducible baseline training/evaluation and lineage | Planned | ADR 005 |
| T-009 | T | W4; WT; S5M | LightGBM LSTM time-series PyTorch DistilBERT candidates | 12 | 08,11 | Suitability assessed; experimental candidates not promised production | Planned | ADR 005 |
| T-010 | T | WT; ST | Docker AWS ECS/RDS/S3 Terraform GitHub Actions | 23 | 01,22 | Reusable images/IaC/CI with explicit deployment evidence | Partial: local Compose and CI definition | ADR 007; [checks](../verification/SPRINT-01-CHECKS.md); hosted CI/cloud/IaC not executed |
| T-011 | T | WT | Kubernetes deployment profile | 23 | 22 | Same application images/config; validation status explicit | Planned | ADR 006 |
| T-012 | T | WT; ST | Google Cloud/GCS EC2 Kafka alternatives | 00 | None | Alternatives explicitly deferred with rationale, not unimplemented hidden requirements | Resolved in plan | ADRs 004,006 |
| T-013 | T | WD | Named core schema entities | 00 | None | Each named entity belongs to a domain and ER relationship | Resolved in plan | data-model.md |
| T-014 | T | WP | Four execution phases | 00 | None | All capabilities preserved in dependency-ordered roadmap | Resolved in plan | roadmap.md |
| T-015 | T | WX | Names recruitment and resume claims | 00 | None | Working name only; promotional statements not treated as implemented evidence | Resolved in plan | product-scope.md |

## Coverage maintenance

Before adding code, link relevant IDs in the sprint report. Replace `—` with actual evidence paths when checks run. A contract document is not implementation proof. If one row contains several input categories (for example SRS/BRD/PRD), each named category must be a separate fixture in its acceptance checklist. Split rows when implementations diverge. Required capability rows cannot be silently relabeled optional.

## Sprint 04 control extension

F-002/F-003 now also cover delivery/project grants, RLS, scoped counts/totals, cross-tenant references and live revocation; see Sprint 04 checks. F-008 remains planned for Sprint 05: login-backed teams and dated memberships are implemented, but independent resources, capacity and staffing are not.

## Sprint 05 control extension

The Sprint 04 note above is historical. F-008/013/014 now have local implementation
and acceptance evidence. F-002/003 extend to resource/effort grants, PM project scope,
sensitive audit revocation and SQL archive restrictions. F-036 and F-055/056 remain
planned for their dashboard/predictive extensions; Sprint 05 supplies deterministic
workload/overtime foundations without model/velocity or medical claims. N-018 reports
and handoffs are maintained through Sprint 05; see its report, checks and handoff.
