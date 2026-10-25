# Requirement coverage matrix

**Sprint 12 current implementation:** [local report](../03-sprints/completed/sprint-12/SPRINT_REPORT.md) and [actual checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) supersede earlier unstarted statements below. Local sample acceptance is complete at schema 0017 with healthy local services. Live source/model quality and AT17 remain blocked; stop before 13.

**Earlier checkpoint before Sprint 12 (25 October 2026; superseded):** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

24 October 2026 additive evidence: [limited guided mode report](../limitations/IMPLEMENTATION_REPORT.md)
and [current limitations](../limitations/LIMITS_AND_FUTURE_SOLUTIONS.md). Normal
0015 rollout and a usable rules-only demo are verified. Closed-choice assistance
is implemented separately from broad interpretation; explicitly approved synthetic-demo
cloud activation passed one request each to Gemini/Puter/Groq. No accuracy criterion,
original requirement or production gate is closed
by this narrower mode. Older normal-rollout statements below are historical.

Sprint 11.1 implementation supplements the existing Sprint 11 scope: [active report](../03-sprints/active/sprint-11.1/README.md), [local acceptance receipts](../verification/sprint11_1/IMPLEMENTATION.md) and [R01–R16 / AT01–AT20 traceability](../09-planning/sprint-11.1/SPRINT_11_1_TRACEABILITY.md). Nine hybrid role paths, checkpointed execution and separate baseline/semantic coverage are implemented behind a default-off flag. Broad semantic accuracy, model/hardware qualification, optional second provider/embedding work and normal rollout remain open; original scoring/privacy/review requirements are unchanged.

Sprint 11 current evidence: [report](../03-sprints/completed/sprint-11/SPRINT_REPORT.md) and [tests](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md). All three packages cover local controls; real-provider interpretation quality remains UNVERIFIED/BLOCKED. Dated notes below retain their historical scope.

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
| F-001 | F | S4.1 | JWT login and session lifecycle | 02 | 01 | Valid login succeeds; expired, revoked and replayed credentials rejected | Accepted for local identity | [Sprint 02 checks](../04-testing/sprint-based/sprint-02/TESTING_REPORT.md); activation/invite/reset and refresh concurrency included; external email unverified |
| F-002 | F | S4.1 | Admin PM Viewer RBAC | 02 | 01 | Permission matrix passes positive/negative API checks | Accepted for identity/member scope | [Sprint 02 checks](../04-testing/sprint-based/sprint-02/TESTING_REPORT.md); future domain actions remain their owning sprint's responsibility |
| F-003 | F | S4.1 | Organization isolation | 02 | 01 | Two-tenant read/write and pooled-connection tests prevent leakage | Accepted for implemented identity surfaces | [Sprint 02 checks](../04-testing/sprint-based/sprint-02/TESTING_REPORT.md); RLS/composite references/live membership/selector tests; future surfaces still planned |
| F-004 | F | S4.1 | Passkey enrollment and login | 22 | 02 | Origin/challenge validation and revoked-credential tests pass | Planned | — |
| F-005 | F | WD; WP | Portfolios | 04 | 02,03 | Create/edit/archive portfolio with scoped projects and history | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-006 | F | WD | Programs | 04 | 02,03 | Program and project portfolio membership remain consistent | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-007 | F | WD; WP | Project tracking | 04 | 02,03 | Persist owner, work, status and baseline with concurrency checks | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-008 | F | WD; W3 | Teams and resources | 05 | 04 | Resource may exist without login; team membership/history persisted | Implemented locally | [Sprint 05 checks](../04-testing/sprint-based/sprint-05/TESTING_REPORT.md); [capacity contract](../contracts/capacity.md) |
| F-009 | F | W3; W8 | Goals and strategic alignment | 04 | 02,03 | Goal links have explicit weights and drill-down evidence | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-010 | F | W3; S4.2 | Budgets and expenditure | 04 | 02,03 | Decimal/currency totals reconcile without mixed-currency sums | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-011 | F | W4; W7 | Sprints and milestones | 04 | 02,03 | Baseline/forecast/actual dates retained with validated transitions | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-012 | F | W3; W8 | Blockers and dependencies | 04 | 02,03 | Track blockers and reject prohibited schedule dependency cycles | Implemented locally | [Sprint 04 checks](../04-testing/sprint-based/sprint-04/TESTING_REPORT.md); [delivery contract](../contracts/delivery.md) |
| F-013 | F | W3 | Resource allocation | 05 | 04 | Date-ranged allocations conserve resource capacity across projects | Implemented locally | [Sprint 05 checks](../04-testing/sprint-based/sprint-05/TESTING_REPORT.md); additive allocation hours, shared capacity and explicit excess |
| F-014 | F | W3; S4.2 | Utilization efficiency | 05 | 04 | Capacity/effort formula handles part-time, leave and zero capacity | Implemented locally | [Sprint 05 checks](../04-testing/sprint-based/sprint-05/TESTING_REPORT.md); [capacity contract](../contracts/capacity.md) |
| F-015 | F | WD; W3 | Risk register | 07 | 04 | Track owner, severity, likelihood, mitigation and lifecycle | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |

## Assessment and dashboards

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-016 | F | W1/Features | Custom maturity framework builder | 06 | 04 | Publish immutable weighted rubric version with valid question types | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-017 | F | W1/Features | Dynamic assessments | 06 | 04 | Assign, autosave, submit, return and review assessment | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-018 | F | W1/Features | Department scoring | 06 | 04 | Compatible department scores reproduce fixture arithmetic | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-019 | F | W1/Features | PMO capability analysis | 06 | 04 | PMO dimension results link to answers and rubric | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-020 | F | W1/Features | Agile maturity analysis | 06 | 04 | Agile dimension results retain framework version and evidence | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-021 | F | W1/Features | Governance evaluation | 06 | 04 | Governance dimension scores and gaps are reviewable | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-022 | F | W1/Features | Delivery capability scoring | 06 | 04 | Delivery dimension score handles incomplete answers explicitly | Accepted locally | [Sprint 06 checks](../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) |
| F-023 | F | W1/AI Features | Semantic answer evaluation | 11 | 06,10 | AI interpretation cites answer/rubric and remains separate from approved score | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-024 | F | W1/AI Features | Pattern and maturity gap detection | 11 | 06,10 | Fixture inconsistency produces supported gap without fabricated evidence | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-025 | F | W1/AI Features | Improvement suggestions | 11 | 06,10 | Suggestions map to identified dimensions and human review | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-026 | F | W3/Executive Dashboard | Portfolio health | 07 | 04,05,06 | Weighted health reconciles to covered projects with unknowns displayed | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-027 | F | W3/Executive Dashboard | Business value | 07 | 04,05,06 | Target/realized benefits show explicit units and source records | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-028 | F | W3/Executive Dashboard | Budget usage | 07 | 04,05,06 | Dashboard spend/budget agrees with ledger by currency | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-029 | F | W3/Executive Dashboard | Alignment dashboard | 07 | 04,05,06 | Goal-weight metric and per-project contribution visible | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-030 | F | W3/Delivery Dashboard | Sprint velocity | 07 | 04,05,06 | Count completed points using team-specific definitions and periods | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-031 | F | W3/Delivery Dashboard; S4.2 | Delay and timeline variance | 07 | 04,05,06 | Baseline/actual/forecast variance units and dates are consistent | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-032 | F | W3/Delivery Dashboard | Blocker and dependency visualization | 07 | 04,05,06 | Accessible graph/table drill-down respects project scope | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-033 | F | W3/Risk Dashboard | Project risk score | 07 | 04,05,06 | Versioned deterministic score matches fixtures, no probability claim | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-034 | F | W3/Risk Dashboard | Escalation matrix | 15 | 07,08,11 | Risk severity/role policy routes to correct authorized approver | Planned | — |
| F-035 | F | W3/Risk Dashboard | Predictive failure indicators | 13 | 12 | Eligible model output shows horizon, uncertainty and evidence | Planned | — |
| F-036 | F | W3/Resource Dashboard | Allocation workload dashboard | 07 | 05,06 | Capacity and team workload values reconcile with source allocations | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-037 | F | S1 | Reported versus evidence health | 07 | 04,05,06 | Reported-green troubled fixture displays evidence discrepancy | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| F-038 | F | S4.2 | Live project visibility | 08 | 07 | Authorized event updates dashboard; reconnect resumes or requests snapshot | Accepted locally: authorized sync-stage dashboard refresh/resume; other mutation broadcasts outside slice | [Sprint 08 checks](../04-testing/sprint-based/sprint-08/TESTING_REPORT.md); [jobs-v1](../contracts/jobs-integrations.md) |
| F-039 | F | S4.2 | AI progress streaming | 10 | 08,09 | SSE exposes observable stages, not hidden reasoning or secret inputs | Accepted locally: deterministic/runtime/browser gates; real model acceptance not claimed | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |

## Agents and predictive analytics

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-040 | F | W2/Agents | PMO agent | 11 | 06,07,10 | Portfolio synthesis links to scoped metrics and findings | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-041 | F | W2/Agents | Risk agent | 11 | 06,07,10 | Structured risks/mitigations validate and missing evidence stays unknown | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-042 | F | W2/Agents | Governance agent | 11 | 06,07,10 | Gaps reference policy versions; no unsupported compliance certification | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-043 | F | W2/Agents | Agile coach agent | 11 | 06,07,10 | Practice suggestions connect to maturity/delivery evidence | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-044 | F | W2/Agents | Executive agent | 11 | 06,07,10 | Concise summary preserves source values and limitations | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-045 | F | W2/Agents | Resource agent | 11 | 06,07,10 | Staffing proposals honor capacity and remain unexecuted drafts | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-046 | F | S4.3 | Financial agent | 11 | 06,07,10 | Costs match metric service and currency grouping | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-047 | F | S4.3 | Schedule agent | 11 | 06,07,10 | Schedule findings reference baseline/dependency versions | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-048 | F | S4.3 | Sentiment agent | 11 | 06,07,10 | Team-level blockers include source support and uncertainty | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-049 | F | W2; S4.3 | Multi-agent aggregation | 11 | 10 | Partial failure, disagreement and duplicates handled deterministically | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
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
| F-061 | F | S5D/PROMISE | PROMISE dataset suitability | 12 | 08,11 | License/labels/schema assessed; reject unsuitable task mapping | PARTIALLY IMPLEMENTED: unreviewed external real data rejected; PROMISE-specific license/target review unavailable | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |
| F-062 | F | S5D/JIRA | Jira dataset suitability | 12 | 08,11 | Lineage/permission and temporal splits recorded | PARTIALLY IMPLEMENTED: provenance/temporal contract; live Jira dataset/labels unavailable | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |
| F-063 | F | S5D/Git Commit Logs | Authorized public repository data | 12 | 08,11 | Source/license/rate limits and as-of feature mapping recorded | Planned | — |
| F-064 | F | S5D/Synthetic Project Data | Synthetic dataset generator | 12 | 08,11 | Seeded schema-valid fixtures isolated from real accuracy claims | IMPLEMENTED AND VERIFIED LOCALLY: isolated seed-12 numeric fixture; no real accuracy claim | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |

## Documents copilot and transformation

| ID | Type | Source | Requirement | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-065 | F | W5/Supported Documents | SRS BRD PRD classification | 09 | 08 | Each document category retains type, version and source locations | Accepted locally: categories, immutable versions, source locations | [Sprint 09 checks](../verification/PPM-09-001.md) |
| F-066 | F | W5/Supported Documents | MOM and sprint report ingestion | 09,11 | 08 | Both categories yield attributable text/findings | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-067 | F | W5/Supported Documents | Risk log ingestion | 09,11 | 08 | Tabular/text risk candidates enter review without duplicate live risks | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-068 | F | W5/Supported Documents | Project charter ingestion | 09 | 08 | Charter evidence links to project and source version | Accepted locally: scoped charter version/source evidence | [Sprint 09 checks](../verification/PPM-09-001.md) |
| F-069 | F | W5/Supported Documents | Governance policy ingestion | 09 | 08 | Restricted policy version used only by authorized consumers | Accepted locally: scoped policy registry and source versions | [Sprint 09 checks](../verification/PPM-09-003.md) |
| F-070 | F | W5/AI Processing | Extract risks and blockers | 11 | 08,09,10 | Sprint 09 candidate interfaces integrate with shared AI gateway; schema and evidence validate | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-071 | F | W5/AI Processing | Extract dependencies | 11 | 08,09,10 | Semantic extraction integrates with gateway; proposed edges require review | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-072 | F | W5/AI Processing | Compliance gaps and maturity indicators | 11 | 08,09,10 | Semantic findings cite sources and remain provisional until reviewed | Implemented local controls; real semantic quality UNVERIFIED/BLOCKED | [Sprint 11 evidence](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md) |
| F-073 | F | W5/Add OCR + RAG | OCR | 09 | 08 | Scanned fixture extracts text with page references/confidence | Accepted locally: real English scanned PDF/PNG/JPEG OCR | [Sprint 09 checks](../verification/PPM-09-001.md) |
| F-074 | F | W5/Add OCR + RAG | Scoped RAG | 09,10 | 08 | Retrieval prevents access leakage and invalid/deleted citations | Partial: budgeted hybrid/fallback implemented; Gemini embedding smoke passed; retrieval quality/scale unverified | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
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
| N-001 | N | S4.1 | bcrypt password hashing | 02 | 01 | Maintained implementation, byte-limit validation, no plaintext storage | Accepted | [Sprint 02 checks](../04-testing/sprint-based/sprint-02/TESTING_REPORT.md), bcrypt 5.0.0 cost 12 and UTF-8 byte-limit tests |
| N-002 | N | S4.1 | Sub-second login target | 23 | 22 | p95 under 1 s on documented profile including password verification | Planned | — |
| N-003 | N | S4.1 | Scalable tenant data separation | 23 | 22 | Indexed tenant queries tested at stated load with no isolation failure | Planned | — |
| N-004 | N | S4.2 | Responsive enterprise UI | 03 | 02 | 360/768/1440 layouts usable and keyboard navigable | Accepted for Sprint 03 shell | [Sprint 03 checks](../04-testing/sprint-based/sprint-03/TESTING_REPORT.md); [frontend contract](../contracts/frontend.md) |
| N-005 | N | S4.2 | Dark mode and glass effects | 03 | 02 | Tokens/themes retain readable contrast and reduced-motion support | Accepted for Sprint 03 shell | [Sprint 03 checks](../04-testing/sprint-based/sprint-03/TESTING_REPORT.md); [frontend contract](../contracts/frontend.md) |
| N-006 | N | S4.2 | FCP under 2 seconds | 23 | 22 | Representative authenticated dashboard meets documented browser profile | Planned | — |
| N-007 | N | S4.2 | 60fps chart rendering target | 23 | 22 | Frame-time distribution reported for documented dataset/device/actions | Planned | — |
| N-008 | N | S4.3 | Nonblocking asynchronous processing | 08 | 07 | Heavy jobs separate from API and restart safely under load | Accepted locally: leased worker/crash recovery with bounded inputs; production load unverified | [Sprint 08 checks](../04-testing/sprint-based/sprint-08/TESTING_REPORT.md); [jobs-v1](../contracts/jobs-integrations.md) |
| N-009 | N | S4.3 | Typed AI output validation | 10 | 08,09 | Invalid provider output never accepted as valid result | Accepted locally: deterministic/runtime/browser gates; real model acceptance not claimed | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| N-010 | N | S4.3 | Timeout fallback | 10 | 08,09 | Bounded retries and truthful degraded/failure states tested | Accepted locally: deterministic/runtime/browser gates; real model acceptance not claimed | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| N-011 | N | S4.4 | 99.9% alert worker availability target | 23 | 21,22 | SLI monitoring/runbook created; observed window reported separately | Planned | — |
| N-012 | N | Master prompt | Versioned migrations and contracts | 01 | 00 | Clean/prior-state migration and API client drift checks exist | Foundation accepted; ongoing | [Sprint 01 checks](../04-testing/sprint-based/sprint-01/TESTING_REPORT.md); initial base/head lifecycle and contract drift pass; later revisions need new checks |
| N-013 | N | Master prompt | Accessibility target | 03 | 02 | Core keyboard/screen-reader/contrast checks, then release regression | Core checks accepted; release-wide verification ongoing | [Sprint 03 checks](../04-testing/sprint-based/sprint-03/TESTING_REPORT.md); full assistive-technology certification not claimed |
| N-014 | N | Master prompt | AI and retrieval access isolation | 09,10 | 09 | Adversarial source text and changed-access fixtures do not leak data | Accepted locally: deterministic/runtime/browser gates; real model acceptance not claimed | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| N-015 | N | Master prompt | Model validity and lineage | 12 | 08,11 | Temporal/entity split, model card, baseline and license evidence recorded | PARTIALLY IMPLEMENTED: local manifests/splits/model cards; genuine outcome quality unverified | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |
| N-016 | N | Master prompt | Audit retention and revocation | 22 | 02,21 | Revocation covers download/stream/cache/jobs; retention configured | Planned | — |
| N-017 | N | Master prompt | Backup restore and deployment recovery | 09,23 | 22 | Restore/rollback exercise records measured results and remaining risks | Partial: pilot scratch restore verified; production/all-surface recovery pending 23 | [Recovery checks](../verification/PPM-09-003.md) |
| N-018 | N | User request | Sprint report and follow-up document | 01 | 00 | Every sprint/sub-sprint updates report, handoff, coverage and evidence | Met through Sprint 02; ongoing | [Report](../03-sprints/completed/sprint-02/SPRINT_REPORT.md), [handoff](../03-sprints/completed/sprint-02/HANDOFF.md) |
| E-001 | E | Prompt pack enhancement | Evidence drawer | 07 | 04,05,06 | KPI drill-down shows authorized sources and gaps | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| E-002 | E | Prompt pack enhancement | Freshness and data coverage | 07 | 04,05,06 | Stale/missing sources visible without fabricated zeros | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| E-003 | E | Prompt pack enhancement | Saved dashboard views | 07 | 03,04 | Personal scoped filters persist without leaking access | Implemented locally | [Sprint 07 checks](../04-testing/sprint-based/sprint-07/TESTING_REPORT.md); [command center](../contracts/command-center.md) |
| E-004 | E | Prompt pack enhancement | Command palette | 03 | 02 | Keyboard navigation exposes only available permitted destinations | Accepted for Sprint 03 shell | [Sprint 03 checks](../04-testing/sprint-based/sprint-03/TESTING_REPORT.md); [frontend contract](../contracts/frontend.md) |
| E-005 | E | Prompt pack enhancement | Decision log | 16 | 14,15 | Approved alternatives/rationale and outcome review retained | Planned | — |
| E-006 | E | Prompt pack enhancement | Scenario comparison | 17 | 13,15 | Baseline and scenario differences include assumptions | Planned | — |
| E-007 | E | Prompt pack enhancement | Data-quality console | 08 | 07 | Import errors and rejected rows can be inspected/retried | Accepted locally: row errors, partial recovery and new corrected sync | [Sprint 08 checks](../04-testing/sprint-based/sprint-08/TESTING_REPORT.md); [jobs-v1](../contracts/jobs-integrations.md) |
| E-008 | E | Prompt pack enhancement | AI usage console | 10 | 08,09 | Tenant usage/errors/budgets visible only to Admin | Accepted locally: deterministic/runtime/browser gates; real model acceptance not claimed | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| E-009 | E | Ingestion support | CSV Jira GitHub connectors | 08 | 04,07 | Preview/incremental sync/replay limits tested; live credentials explicit | PARTIALLY IMPLEMENTED: local authority/dedup/conflict/recovery controls; live source equality BLOCKED | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |

## Technology and source passages without product acceptance claims

| ID | Type | Source | Choice or passage | Owner | Depends | Acceptance criterion | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | T | WT; ST | Next.js TypeScript Tailwind shadcn Motion Zustand Recharts; Chart.js alternative | 01 | 00 | Compatible versions pinned; Gantt not misrepresented as built-in chart capability | Partial: foundation and enterprise shell | ADR 007; [checks](../04-testing/sprint-based/sprint-01/TESTING_REPORT.md); [ADR 009](../architecture/adr/009-enterprise-shell.md): native shared components implemented; shadcn/Motion/state/chart runtime deferred |
| T-002 | T | WT; ST | FastAPI Python Uvicorn Pydantic; NestJS alternative | 01 | 00 | Async API and schema foundation reproducible | Foundation accepted | ADR 007; [checks](../04-testing/sprint-based/sprint-01/TESTING_REPORT.md) |
| T-003 | T | WT; ST | PostgreSQL JSONB SQLAlchemy Alembic Redis | 01 | 00 | Runtime and initial migrations verified | Foundation accepted; domain schema planned | ADR 007; [checks](../04-testing/sprint-based/sprint-01/TESTING_REPORT.md); no domain JSONB schema claimed |
| T-004 | T | WT | Pinecone/Weaviate versus pgvector | 09,10 | 08 | Chosen retrieval adapter records explicit substitution | Partial: bounded JSONB projection; pgvector/ANN unverified (ADR 016) | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| T-005 | T | W8; WT | Neo4j | 18 | 04,09,11 | Derived graph rebuild and scope tests pass | Planned | ADR 003 |
| T-006 | T | WT; ST | LangChain; LlamaIndex alternative | 10 | 08,09 | One orchestration/tool contract, no duplicated framework stacks | Accepted local typed-native alternative; ADR 016 (no duplicate frameworks) | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| T-007 | T | WT; ST | OpenAI Gemini Ollama HuggingFace options | 10 | 08,09 | One configured adapter with supported model and explicit disabled mode | Adapter/disabled path implemented; real configured provider BLOCKED | [Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); [ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) |
| T-008 | T | W4; WT; S5M | scikit-learn pandas XGBoost Random Forest MLflow | 12 | 08,11 | Reproducible baseline training/evaluation and lineage | PARTIALLY IMPLEMENTED: pandas/scikit-learn constant/linear/RF; local JSON tracking; native MLflow/XGBoost deferred | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |
| T-009 | T | W4; WT; S5M | LightGBM LSTM time-series PyTorch DistilBERT candidates | 12 | 08,11 | Suitability assessed; experimental candidates not promised production | DEFERRED: no suitable genuine labels/resources for larger/text candidates | [Sprint 12 checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) |
| T-010 | T | WT; ST | Docker AWS ECS/RDS/S3 Terraform GitHub Actions | 23 | 01,22 | Reusable images/IaC/CI with explicit deployment evidence | Partial: local Compose and CI definition | ADR 007; [checks](../04-testing/sprint-based/sprint-01/TESTING_REPORT.md); hosted CI/cloud/IaC not executed |
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

## Active future planning reconciliation — 2026-10-09

Historical acceptance rows above remain unchanged. The current requirement-by-requirement planning dispositions and all gap owners are in [FEATURE_GAP_TRACEABILITY.md](../09-planning/FEATURE_GAP_TRACEABILITY.md). Use [Sprint 8.1](../09-planning/SPRINT_8_1_PLAN.md) and the [future roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md) for proposed execution. Do not interpret stale historic wording as current absence or claim future work completed. Full release retains the original required advanced scope and [release gates](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md).

## Sprint 8.1 pilot execution

The revised gap mapping adds PPM-81-001–010 without replacing source requirements. Identity F-001–003, delivery F-005–007, compatible comparison F-018 and enhancement A01–A08/A15–A18 now have pilot implementation evidence in the [report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md) and per-task checks. Local implementation does not establish real account delivery, hosted CI, Word layout or production acceptance. PPM-81-002 is BLOCKED external mail and010 PARTIAL; parent acceptance remains OPEN. Future original-spec capabilities keep their existing owning sprint and status.

| Task | Pilot acceptance | Evidence |
| --- | --- | --- |
| PPM-81-001 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-001.md) |
| PPM-81-002 | BLOCKED real SMTP inbox checks | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-002.md) |
| PPM-81-003 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-003.md) |
| PPM-81-004 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-004.md) |
| PPM-81-005 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-005.md) |
| PPM-81-006 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-006.md) |
| PPM-81-007 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-007.md) |
| PPM-81-008 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-008.md) |
| PPM-81-009 | COMPLETE locally | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-009.md) |
| PPM-81-010 | PARTIAL hosted CI and DOCX visual QA | [Task checks](../04-testing/sprint-based/sprint-8.1/PPM-81-010.md) |


## Sprint 09 execution — 15 October 2026

PPM-09-001/002/003 accepted locally for the revised source/keyword/policy/retention
slice. [Report](../03-sprints/completed/sprint-09/SPRINT_REPORT.md) and
[checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md) distinguish full,
focused and browser runs. F-066/067/074 remain partial for their combined semantic
scope. F-070–072 stay planned for 11; embeddings/hybrid stay 10. No required scope
was relabeled optional, and parent 8.1 external/visual gates remain open.

## Sprint 10 execution and follow-up — 16 October 2026

PPM-10-001/002/003 have local implementation evidence in [the report](../03-sprints/completed/sprint-10/SPRINT_REPORT.md)
and [checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md). F-039, N-009/010/014,
E-008 and the ADR 016 typed-native T-006 alternative are verified locally. F-074,
T-004 and T-007 remain partial for broad retrieval quality and scale obligations.
Gemini free-tier completion/embedding smoke passed and the final no-expiry AI suite
recorded 63 passes. G-014 keeps semantic review in 11; G-015 remains partial for
broader quality/release acceptance rather than missing provider authorization.
Normal 0012 upgrade preserved 66 established tables, five original objects,
.env, frozen sources/prompts and eleven predecessor migration files. No required
capability was relabeled optional; overall acceptance stays OPEN. Stop before 11.

## Sprint 12 package trace

| Package | Implemented owning slice | Local evidence | Retained external gate |
| --- | --- | --- | --- |
| PPM-12-001 | Existing ingestion/jobs/UI plus connectors authority and conflict review | [Receipt](../verification/PPM-12-001.md) | Approved live Jira/GitHub source comparison |
| PPM-12-002 | Versioned manual/fixture numeric history and as-of manifests | [Receipt](../verification/PPM-12-002.md) | Independently verified genuine labels and external dataset suitability |
| PPM-12-003 | CPU baselines, artifacts, comparison/model cards | [Receipt](../verification/PPM-12-003.md) | Real quality, native MLflow import, justified larger candidates, Sprint 13 promotion |

AT17 remains BLOCKED. Local pipeline acceptance never substitutes for model quality.
