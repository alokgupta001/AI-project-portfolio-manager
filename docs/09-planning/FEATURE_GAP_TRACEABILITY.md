# Feature gap traceability

Sprint 09 current execution (15 October 2026): [report](../03-sprints/completed/sprint-09/SPRINT_REPORT.md) and [checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md) establish local source/keyword/policy/retention acceptance. Semantic/approval/release dependencies remain open. Earlier dated baselines below are historical.

**8.1 follow-up:** PPM-81-001 and 003–009 complete locally; development Gmail delivery/acceptance/recovery verified 10 October, while 010 remains PARTIAL for hosted CI/archived Word visual QA. [Sprint 8.1 report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md) is the evidence authority. The baseline below remains historical.

**Historical planning baseline (before Sprint 8.1 execution):** 9 October 2026. Documentation only; no feature work is authorized by this pack.** Sprint 08 is complete locally; Sprint 8.1 is proposed, not started. Numbers describe execution order, not dates or delivery promises. The frozen source specifications and original prompt pack remain intact. For future work, this pack supersedes the earlier gap review and the future sections of the original ordered prompts; those prompts remain historical scope evidence. Completed reports retain their original meaning.

Read the [audit](SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](SPRINT_8_1_PLAN.md), [future roadmap](FUTURE_SPRINT_ROADMAP.md), [traceability](FEATURE_GAP_TRACEABILITY.md), and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) together. A later implementation session must read the latest handoff and current working tree before using these plans.

## Findings to execution

32 confirmed gaps and 4 blocked/unverified items, each with a primary owning task. Some tasks close several related gaps; follow-on stage dependencies are retained in the roadmap. Current execution evidence is in the [Sprint 8.1 report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md). External delivery/CI and Word visual acceptance remain open.

| Finding | Current status | Impact | Primary task / sprint | Intended result | Previous review |
| --- | --- | --- | --- | --- | --- |
| G-001 Public sign-up | IMPLEMENTED AND VERIFIED | P1 | PPM-81-001 / 8.1 | Add verified registration with organization creation separated from login and invitation acceptance. | A01 |
| G-002 Usable invitation and recovery delivery | IMPLEMENTED AND VERIFIED IN DEVELOPMENT | P1 | PPM-81-002 / 8.1 | Gmail signup, existing-account Viewer invitation and recovery completed; isolated tests cover lifecycle variants. Production acceptance remains separate. | A02 |
| G-003 First-time setup and organization profile | IMPLEMENTED AND VERIFIED | P1 | PPM-81-003 / 8.1 | Add setup checklist and minimal profile editing with clear account versus resource explanations. | A01,A03 |
| G-004 Browser access management | IMPLEMENTED AND VERIFIED | P1 | PPM-81-004 / 8.1 | Expose existing project/resource/assessment grants and understandable effective-access explanations. | A04 |
| G-005 Search actual records | IMPLEMENTED AND VERIFIED | P1 | PPM-81-005 / 8.1 | Add permission-filtered record search; document content search remains Sprint 09. | A05 |
| G-006 Complete lists and selectors | IMPLEMENTED AND VERIFIED | P1 | PPM-81-006 / 8.1 | Add pagination and server search; make departmental comparison period and full cohort explicit. | A05 |
| G-007 My work and basic notifications | IMPLEMENTED AND VERIFIED | P1 | PPM-81-007 / 8.1 | Provide assigned work/assessment views and a small in-app feed; timed reminders and external channels stay in 15/21. | A06 |
| G-008 Metadata needed by later analytics | IMPLEMENTED AND VERIFIED | P1 | PPM-81-008 / 8.1 | Add optional controlled metadata with unknown values; never backfill invented categories. | A07,A08 |
| G-009 Live refresh of manual changes | IMPLEMENTED AND VERIFIED | P2 | PPM-81-009 / 8.1 | Publish bounded authorized change notices and show freshness; do not broadcast record content. | A15 |
| G-010 Guide and readiness wording | PARTIALLY IMPLEMENTED | P1 | PPM-81-010 / 8.1 | Correct the guide steps and readiness descriptions; verify each documented route on the browser. | A16,A18 |
| G-011 Document library and assessment evidence bridge | IMPLEMENTED AND VERIFIED LOCALLY | P1 | PPM-09-001 / 09 | Build shared versioned documents; preserve existing assessment scores and attachment authority. | A09 |
| G-012 Governance policy lifecycle | REGISTRY VERIFIED; APPROVALS PENDING 15 | P1 | PPM-09-003 / 09 | Create policy registry in 09 and approval integration in 15. | A11 |
| G-013 Retention and pilot restore evidence | LOCAL RETENTION/RESTORE VERIFIED; RELEASE RECOVERY 22/23 OPEN | P1 | PPM-09-003 / 09 | Establish scoped purge/hold rules and a non-destructive scratch restore before real documents; finish all surfaces in 22/23. | A17 |
| G-014 Document and AI dependency conflict | PARTIALLY IMPLEMENTED | P1 | PPM-10-001 / 10 | Stage keyword retrieval/contracts in 09, budgeted embedding adapter in 10, reviewed extraction in 11. | A12 |
| G-015 AI gateway and operations | PARTIALLY IMPLEMENTED | P1 | PPM-10-001 / 10 | Shared runtime/UI and local guards verified; Gemini free-tier completion/embedding smoke passed; broader model/retrieval quality and scale remain unverified. | — |
| G-016 Nine agents and semantic maturity scoring | PLANNED | P1 | PPM-11-001 / 11 | Build all nine agents with evidence and distinct suggested/reviewer scores. | — |
| G-017 Recommendation review versus application | PLANNED | P1 | PPM-11-003 / 11 | Separate accepted recommendation from applied change; no generic mutation before 15. | A13 |
| G-018 Repeat assessments, due dates and trend/export | PARTIALLY IMPLEMENTED | P2 | PPM-15-002 / 15 | Extend the existing assessment lifecycle and connect workflow reminders, keeping published score history immutable. | A10 |
| G-019 Unattended connector identity and conflict resolution | PARTIALLY IMPLEMENTED | P1 | PPM-12-001 / 12 | Add narrow renewable connector authority, source identity uniqueness and reviewable conflict resolution. | A14 |
| G-020 Live Jira/GitHub acceptance | BLOCKED | P1 | PPM-12-001 / 12 | Run authorized read-only provider checks and controlled import with scoped credentials in 12; preserve fixtures and mark blocked until supplied. | — |
| G-021 Historical features, labels and models | PLANNED | P1 | PPM-12-002 / 12 | Capture justified historical fields and consented notes, validate labels and evaluate baseline models. | A08 |
| G-022 Production model promotion evidence | BLOCKED | P1 | PPM-13-001 / 13 | Require real temporal evaluation and suitability evidence; demo fixtures cannot satisfy promotion. | — |
| G-023 Forecast serving | PLANNED | P1 | PPM-13-002 / 13 | Serve eligible versions with uncertainty and honest unavailable/fallback states. | — |
| G-024 Copilot, scoped context and natural language analytics | PLANNED | P1 | PPM-14-001 / 14 | Build bounded authorized tools and cited conversation UI after evidence runtime. | — |
| G-025 Approvals, escalation, due-event reminders | PLANNED | P1 | PPM-15-001 / 15 | Implement inbox, calendars, authority checks and repeat-safe approved actions. | A06,A11,A13 |
| G-026 Transformation and decisions | PLANNED | P1 | PPM-16-001 / 16 | Build evidence-linked roadmaps and approval-based project conversion; consume copilot drafts. | — |
| G-027 Resource and budget scenarios | PLANNED | P1 | PPM-17-001 / 17 | Simulate immutable copies with conservation and stale-apply rejection. | — |
| G-028 Knowledge graph and impact paths | PLANNED | P1 | PPM-18-001 / 18 | Build scoped projection and bounded impact paths without changing source authority. | — |
| G-029 Comparable benchmarks | PARTIALLY IMPLEMENTED | P1 | PPM-19-001 / 19 | Compare compatible cohorts with counts, denominators and privacy suppression. | A08 |
| G-030 Meeting intelligence | PLANNED | P1 | PPM-20-001 / 20 | Add authorized uploads, transcription and evidence-linked review. | — |
| G-031 Reports, alerts and daily audio | PARTIALLY IMPLEMENTED | P1 | PPM-21-001 / 21 | Ship exports and authorized subscriptions; account emails remain 8.1. | A16 |
| G-032 Passkeys and account lifecycle settings | PARTIALLY IMPLEMENTED | P1 | PPM-22-001 / 22 | Implement passkeys and settings, preserving last-admin protection and all-surface revocation. | A03,A04 |
| G-033 Release engineering and production configuration | PARTIALLY IMPLEMENTED | P1 | PPM-23-001 / 23 | Integrate all journeys and prepare deployment profiles; live deployment requires credentials and authorization. | A17 |
| G-034 Sprint 08 hosted CI | IMPLEMENTED BUT UNVERIFIED | P1 | PPM-81-010 / 8.1 | Record a reviewed checkpoint and hosted checks during implementation closure without discarding existing changes. | — |
| G-035 Current direct ASGI rerun | IMPLEMENTED AND VERIFIED | P2 | PPM-81-010 / 8.1 | Full isolated suite completed:74 passing, including transaction-boundary tests. See Sprint 8.1 report. | — |
| G-036 Planning consistency and source reconciliation | PARTIALLY IMPLEMENTED | P1 | PPM-81-010 / 8.1 | Make the new future roadmap authoritative, preserve originals and reconcile every requirement at release. | A18 |

## Recommendation decisions

Previously proposed A01–A18 are adopted into this planning pack with the narrower boundaries below. "Adopted" means recommended scope in this requested plan, not deployed or separately approved implementation. Already-built candidates are retained without duplicate tasks.

| Prior recommendation | Owner task(s) | Users / business benefit | Complexity | Release level / dependency |
| --- | --- | --- | --- | --- |
| A01 signup/onboarding | 81-001,81-003 | New users/Admin; self-service entry and useful next steps | High | Operational pilot; identity/mail |
| A02 email/invites | 81-002 | Admin/all users; usable invitation/recovery without operator | High | Operational pilot; challenge/outbox |
| A03 org/account lifecycle | 81-003,22-002 | Admin/member; profile clarity and safe account changes | Medium | Basic pilot; full lifecycle 22 |
| A04 effective permissions | 81-004,22-003 | Admin/PM; grant browser access without API tooling | Medium | Pilot UI; full-surface release regression |
| A05 record discovery | 81-005,81-006 | All users; find/select older permitted records | Medium | Pilot; bounded scoped queries |
| A06 My Work/notifications | 81-007,15-003,21-002 | PM/assessor/executive; see owned work and follow-up | Medium | Basic pilot; scheduled/external full release |
| A07 work enhancements | 81-008,OPT-001 | PM; distinguish urgent work and later discuss it | Medium | Priority/type pilot; comments optional |
| A08 source metadata | 81-008,12-002,19-001 | PM/executive; valid analytic questions and comparisons | Medium–High | Required downstream inputs |
| A09 evidence bridge | 09-001,11-002 | Assessor/PM; reuse source evidence safely | High | Full product; storage/access before AI |
| A10 assessment follow-through | 15-002,21-001 | Assessor/PM; due/repeat/trend/export | Medium | Recommended full product; current history retained |
| A11 policy lifecycle | 09-003,15-003 | Admin/PMO; know current applicable approved policy | Medium | Full product; governed source lifecycle |
| A12 document/AI sequence | 09-002,10-001,11-003 | All evidence users; honest staged retrieval | High | Required interface sequencing |
| A13 accept versus apply | 11-003,15-001 | PM/approver; reviewed suggestions cannot silently act | High | Required action safety |
| A14 connector operations | 12-001 | Admin/PM; scheduled sync survives logouts, conflicts reviewed | High | Full product; narrow authority and live credentials |
| A15 manual freshness | 81-009 | Dashboard users; ordinary edits become visible | Medium | Pilot stabilization; SSE revocation |
| A16 exports/guides | 81-010,21-001 | Tester/executive; accurate instructions and portable results | Medium | Guide pilot; PDF/HTML/report full product |
| A17 retention/recovery | 81-010,09-003,22-003,23-002 | Admin/operator; protect real data and recover | High | Pilot proof first; all-surface release proof |
| A18 planning coherence | 81-010,23-003 | Product owner/developer; know current status and next work | Low | This pack establishes plan; evidence reconciled at release |

All abbreviated task IDs above have `PPM-` prefix. Optional rows have explicit scope decisions in the future roadmap. Existing project workspace, explainable health, risk register, milestones, capacity conflict signals, source drill-down, audit history and fixture imports are retained with tests, not classified absent.

## Original requirement-by-requirement crosswalk

Each original coverage row appears once below, including controls, technologies and planning deliverables. The original criterion is preserved verbatim as an acceptance obligation. The future task owns closure or continuing regression; existing covered core flows are not rebuilt. **VERIFIED COMPLETE here is limited to accepted current local behavior and retained checks, not full production certification.** For multi-stage requirements, the primary owner is accountable for checking every prerequisite stage. Original framework/library alternatives are design choices, not separate user features.

| Requirement | Capability | Planning status | Closure / regression owner | Original acceptance obligation |
| --- | --- | --- | --- | --- |
| P-001 | Preserve originals and prompts | VERIFIED COMPLETE | PPM-81-010 | Both source and all five prompt copies hash-match originals |
| P-002 | Trace scope and source conflicts | VERIFIED COMPLETE | PPM-81-010 | Each source capability mapped with acceptance and owner |
| P-003 | Architecture and domain model | VERIFIED COMPLETE | PPM-81-010 | Boundaries, flows, entity relationships and choices documented |
| P-004 | Permissions and shared contracts | VERIFIED COMPLETE | PPM-81-010 | Roles, project scope, API/events/metrics/versioning specified |
| P-005 | Explain work and provide continuity | VERIFIED COMPLETE | PPM-81-010 | Separate report and latest handoff identify next step |
| F-001 | JWT login and session lifecycle | PARTIAL | PPM-81-010 | Valid login succeeds; expired, revoked and replayed credentials rejected |
| F-002 | Admin PM Viewer RBAC | PARTIAL | PPM-81-010 | Permission matrix passes positive/negative API checks |
| F-003 | Organization isolation | PARTIAL | PPM-81-010 | Two-tenant read/write and pooled-connection tests prevent leakage |
| F-004 | Passkey enrollment and login | NOT IMPLEMENTED | PPM-22-001 | Origin/challenge validation and revoked-credential tests pass |
| F-005 | Portfolios | VERIFIED COMPLETE | PPM-81-010 | Create/edit/archive portfolio with scoped projects and history |
| F-006 | Programs | VERIFIED COMPLETE | PPM-81-010 | Program and project portfolio membership remain consistent |
| F-007 | Project tracking | VERIFIED COMPLETE | PPM-81-010 | Persist owner, work, status and baseline with concurrency checks |
| F-008 | Teams and resources | VERIFIED COMPLETE | PPM-81-010 | Resource may exist without login; team membership/history persisted |
| F-009 | Goals and strategic alignment | VERIFIED COMPLETE | PPM-81-010 | Goal links have explicit weights and drill-down evidence |
| F-010 | Budgets and expenditure | VERIFIED COMPLETE | PPM-81-010 | Decimal/currency totals reconcile without mixed-currency sums |
| F-011 | Sprints and milestones | VERIFIED COMPLETE | PPM-81-010 | Baseline/forecast/actual dates retained with validated transitions |
| F-012 | Blockers and dependencies | VERIFIED COMPLETE | PPM-81-010 | Track blockers and reject prohibited schedule dependency cycles |
| F-013 | Resource allocation | VERIFIED COMPLETE | PPM-81-010 | Date-ranged allocations conserve resource capacity across projects |
| F-014 | Utilization efficiency | VERIFIED COMPLETE | PPM-81-010 | Capacity/effort formula handles part-time, leave and zero capacity |
| F-015 | Risk register | VERIFIED COMPLETE | PPM-81-010 | Track owner, severity, likelihood, mitigation and lifecycle |
| F-016 | Custom maturity framework builder | VERIFIED COMPLETE | PPM-81-010 | Publish immutable weighted rubric version with valid question types |
| F-017 | Dynamic assessments | VERIFIED COMPLETE | PPM-81-010 | Assign, autosave, submit, return and review assessment |
| F-018 | Department scoring | VERIFIED COMPLETE | PPM-81-010 | Compatible department scores reproduce fixture arithmetic |
| F-019 | PMO capability analysis | VERIFIED COMPLETE | PPM-81-010 | PMO dimension results link to answers and rubric |
| F-020 | Agile maturity analysis | VERIFIED COMPLETE | PPM-81-010 | Agile dimension results retain framework version and evidence |
| F-021 | Governance evaluation | VERIFIED COMPLETE | PPM-81-010 | Governance dimension scores and gaps are reviewable |
| F-022 | Delivery capability scoring | VERIFIED COMPLETE | PPM-81-010 | Delivery dimension score handles incomplete answers explicitly |
| F-023 | Semantic answer evaluation | NOT IMPLEMENTED | PPM-11-002 | AI interpretation cites answer/rubric and remains separate from approved score |
| F-024 | Pattern and maturity gap detection | NOT IMPLEMENTED | PPM-11-003 | Fixture inconsistency produces supported gap without fabricated evidence |
| F-025 | Improvement suggestions | NOT IMPLEMENTED | PPM-11-003 | Suggestions map to identified dimensions and human review |
| F-026 | Portfolio health | VERIFIED COMPLETE | PPM-81-010 | Weighted health reconciles to covered projects with unknowns displayed |
| F-027 | Business value | VERIFIED COMPLETE | PPM-81-010 | Target/realized benefits show explicit units and source records |
| F-028 | Budget usage | VERIFIED COMPLETE | PPM-81-010 | Dashboard spend/budget agrees with ledger by currency |
| F-029 | Alignment dashboard | VERIFIED COMPLETE | PPM-81-010 | Goal-weight metric and per-project contribution visible |
| F-030 | Sprint velocity | VERIFIED COMPLETE | PPM-81-010 | Count completed points using team-specific definitions and periods |
| F-031 | Delay and timeline variance | VERIFIED COMPLETE | PPM-81-010 | Baseline/actual/forecast variance units and dates are consistent |
| F-032 | Blocker and dependency visualization | VERIFIED COMPLETE | PPM-81-010 | Accessible graph/table drill-down respects project scope |
| F-033 | Project risk score | VERIFIED COMPLETE | PPM-81-010 | Versioned deterministic score matches fixtures, no probability claim |
| F-034 | Escalation matrix | NOT IMPLEMENTED | PPM-15-001 | Risk severity/role policy routes to correct authorized approver |
| F-035 | Predictive failure indicators | NOT IMPLEMENTED | PPM-13-001 | Eligible model output shows horizon, uncertainty and evidence |
| F-036 | Allocation workload dashboard | VERIFIED COMPLETE | PPM-81-010 | Capacity and team workload values reconcile with source allocations |
| F-037 | Reported versus evidence health | VERIFIED COMPLETE | PPM-81-010 | Reported-green troubled fixture displays evidence discrepancy |
| F-038 | Live project visibility | PARTIAL | PPM-81-009 | Authorized event updates dashboard; reconnect resumes or requests snapshot |
| F-039 | AI progress streaming | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 | SSE exposes observable stages, not hidden reasoning or secret inputs |
| F-040 | PMO agent | NOT IMPLEMENTED | PPM-11-001 | Portfolio synthesis links to scoped metrics and findings |
| F-041 | Risk agent | NOT IMPLEMENTED | PPM-11-001 | Structured risks/mitigations validate and missing evidence stays unknown |
| F-042 | Governance agent | NOT IMPLEMENTED | PPM-11-001 | Gaps reference policy versions; no unsupported compliance certification |
| F-043 | Agile coach agent | NOT IMPLEMENTED | PPM-11-001 | Practice suggestions connect to maturity/delivery evidence |
| F-044 | Executive agent | NOT IMPLEMENTED | PPM-11-001 | Concise summary preserves source values and limitations |
| F-045 | Resource agent | NOT IMPLEMENTED | PPM-11-001 | Staffing proposals honor capacity and remain unexecuted drafts |
| F-046 | Financial agent | NOT IMPLEMENTED | PPM-11-001 | Costs match metric service and currency grouping |
| F-047 | Schedule agent | NOT IMPLEMENTED | PPM-11-001 | Schedule findings reference baseline/dependency versions |
| F-048 | Sentiment agent | NOT IMPLEMENTED | PPM-11-001 | Team-level blockers include source support and uncertainty |
| F-049 | Multi-agent aggregation | NOT IMPLEMENTED | PPM-11-001 | Partial failure, disagreement and duplicates handled deterministically |
| F-050 | Sprint delay model | NOT IMPLEMENTED | PPM-13-001 | As-of sprint labels and out-of-time evaluation precede model promotion |
| F-051 | Project delay regression | NOT IMPLEMENTED | PPM-13-001 | Delay-day MAE versus baseline and horizon documented |
| F-052 | Missed milestone model | NOT IMPLEMENTED | PPM-13-001 | Eligible milestone forecast has explicit baseline date and horizon |
| F-053 | Budget overrun forecast | NOT IMPLEMENTED | PPM-13-002 | Forecast spend/overrun values specify currency, horizon and model eligibility |
| F-054 | Risk trends | NOT IMPLEMENTED | PPM-13-003 | Compare versioned time snapshots, flag model/rule changes |
| F-055 | Resource inefficiency indicators | NOT IMPLEMENTED | PPM-13-003 | Indicators derive from explicit capacity/effort assumptions |
| F-056 | Team overload signals | NOT IMPLEMENTED | PPM-13-003 | Workload, overtime and velocity-drop signals suppress small groups and avoid diagnosis |
| F-057 | Project failure probability | NOT IMPLEMENTED | PPM-13-001 | Defined outcome labels and calibration required before probability display |
| F-058 | Delivery confidence | NOT IMPLEMENTED | PPM-13-003 | Meaning/horizon distinct from risk score and source uncertainty shown |
| F-059 | High Medium Low risk classifier | NOT IMPLEMENTED | PPM-13-001 | Held-out classification results and threshold policy recorded |
| F-060 | NLP sentiment pipeline | NOT IMPLEMENTED | PPM-12-003 | Candidate evaluated on labeled text, not treated as workforce truth |
| F-061 | PROMISE dataset suitability | NOT IMPLEMENTED | PPM-12-002 | License/labels/schema assessed; reject unsuitable task mapping |
| F-062 | Jira dataset suitability | NOT IMPLEMENTED | PPM-12-002 | Lineage/permission and temporal splits recorded |
| F-063 | Authorized public repository data | NOT IMPLEMENTED | PPM-12-002 | Source/license/rate limits and as-of feature mapping recorded |
| F-064 | Synthetic dataset generator | NOT IMPLEMENTED | PPM-12-002 | Seeded schema-valid fixtures isolated from real accuracy claims |
| F-065 | SRS BRD PRD classification | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 | Each document category retains type, version and source locations |
| F-066 | MOM and sprint report ingestion | PARTIALLY IMPLEMENTED | PPM-11-003 | Both categories yield attributable text/findings |
| F-067 | Risk log ingestion | PARTIALLY IMPLEMENTED | PPM-11-003 | Tabular/text risk candidates enter review without duplicate live risks |
| F-068 | Project charter ingestion | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 | Charter evidence links to project and source version |
| F-069 | Governance policy ingestion | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-003 | Restricted policy version used only by authorized consumers |
| F-070 | Extract risks and blockers | NOT IMPLEMENTED | PPM-11-003 | Sprint 09 candidate interfaces integrate with shared AI gateway; schema and evidence validate |
| F-071 | Extract dependencies | NOT IMPLEMENTED | PPM-11-003 | Semantic extraction integrates with gateway; proposed edges require review |
| F-072 | Compliance gaps and maturity indicators | NOT IMPLEMENTED | PPM-11-003 | Semantic findings cite sources and remain provisional until reviewed |
| F-073 | OCR | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 | Scanned fixture extracts text with page references/confidence |
| F-074 | Scoped RAG | PARTIALLY IMPLEMENTED | PPM-10-001 | Retrieval prevents access leakage and invalid/deleted citations |
| F-075 | Conversational copilot | NOT IMPLEMENTED | PPM-14-001 | Scoped multi-turn answers contain valid evidence or abstain |
| F-076 | Root causes and predicted impact | NOT IMPLEMENTED | PPM-14-001 | Distinguish supported associations, hypotheses and measured predictions |
| F-077 | Natural language analytics | NOT IMPLEMENTED | PPM-14-001 | Allowlisted query plan matches deterministic expected answer |
| F-078 | PMO transformation roadmap | NOT IMPLEMENTED | PPM-16-001 | Initiatives trace to gaps/goals with owner and quarterly milestones |
| F-079 | Process improvement plans | NOT IMPLEMENTED | PPM-16-001 | Steps, assumptions and measurable outcomes documented |
| F-080 | Governance structures | NOT IMPLEMENTED | PPM-16-001 | Proposed decision/reporting hierarchy reviewed before adoption |
| F-081 | KPI frameworks | NOT IMPLEMENTED | PPM-16-001 | Each KPI has baseline, target, unit, owner and cadence |
| F-082 | Delivery optimization strategy | NOT IMPLEMENTED | PPM-16-001 | Resource/tooling recommendations state evidence and constraints |
| F-083 | Agile transformation roadmap | NOT IMPLEMENTED | PPM-16-001 | Sprint/process changes map to approved improvement initiatives |
| F-084 | Approval flows | NOT IMPLEMENTED | PPM-15-001 | Versioned state machine rejects unauthorized/stale/self-approved actions |
| F-085 | Escalation system | NOT IMPLEMENTED | PPM-15-003 | Correct next approver notified once per qualifying transition |
| F-086 | Automated reminders | NOT IMPLEMENTED | PPM-15-003 | Retry/restart does not duplicate reminder side effects |
| F-087 | SLA tracking | NOT IMPLEMENTED | PPM-15-003 | Business/elapsed clocks obey published workflow calendar |
| F-088 | Milestone notifications | NOT IMPLEMENTED | PPM-15-003 | Due/late milestone events create scoped in-app notifications |
| F-089 | Project to Team graph | NOT IMPLEMENTED | PPM-18-001 | Projection reflects authorized project/team relationships |
| F-090 | Project to Risk graph | NOT IMPLEMENTED | PPM-18-001 | Risk edges track updates and deletions without duplicates |
| F-091 | Team to Skill graph | NOT IMPLEMENTED | PPM-18-001 | Skills traverse only within scope and bounded depth |
| F-092 | Risk to Dependency graph | NOT IMPLEMENTED | PPM-18-001 | Evidence distinguishes inferred versus approved dependency edges |
| F-093 | Portfolio to Business Goal graph | NOT IMPLEMENTED | PPM-18-001 | Goal links retain canonical IDs and provenance |
| F-094 | Impact and root cause tracing | NOT IMPLEMENTED | PPM-18-003 | Bounded paths cite evidence, show lag and avoid causality claims |
| F-095 | Organizational mapping | NOT IMPLEMENTED | PPM-18-003 | Graph and accessible table agree with authoritative records |
| F-096 | Meeting recording/transcript intake | NOT IMPLEMENTED | PPM-20-001 | Audio/transcript formats validated and access/retention applied |
| F-097 | Meeting minutes generation | NOT IMPLEMENTED | PPM-20-002 | Editable minutes reference timestamps/spans |
| F-098 | Meeting actions and blockers | NOT IMPLEMENTED | PPM-20-003 | Unknown owners/dates remain unresolved; approved conversion idempotent |
| F-099 | Budget-cut simulation | NOT IMPLEMENTED | PPM-17-001 | 25% reduction scenario preserves live plan and states assumptions |
| F-100 | Resource-transfer Time Machine | NOT IMPLEMENTED | PPM-17-001 | Two-person transfer changes both projects and conserves capacity |
| F-101 | Department benchmarking | NOT IMPLEMENTED | PPM-19-003 | Compatible cohorts show counts and framework version |
| F-102 | Team benchmarking | NOT IMPLEMENTED | PPM-19-003 | No raw cross-team point comparison or small-group sentiment exposure |
| F-103 | Portfolio benchmarking | NOT IMPLEMENTED | PPM-19-003 | Currency/period/size filters yield reproducible comparable aggregates |
| F-104 | Delivery maturity comparison | NOT IMPLEMENTED | PPM-19-001 | Incompatible rubric versions are not silently combined |
| F-105 | Weekly executive summaries | NOT IMPLEMENTED | PPM-21-001 | Scheduled summary matches versioned period snapshot |
| F-106 | Email risk alerts | NOT IMPLEMENTED | PPM-21-002 | Authorized recipients receive threshold-crossing template with deduplication |
| F-107 | Slack risk alerts | NOT IMPLEMENTED | PPM-21-002 | Authorized channel delivery respects cooldown and retries |
| F-108 | Daily executive TTS briefing | NOT IMPLEMENTED | PPM-21-001 | Approximate 2-minute audio agrees with transcript and protected download |
| F-109 | HTML email and PDF reports | NOT IMPLEMENTED | PPM-21-003 | Rendered layouts readable; facts/citations match shared snapshot |
| N-001 | bcrypt password hashing | PARTIAL | PPM-22-003 | Maintained implementation, byte-limit validation, no plaintext storage |
| N-002 | Sub-second login target | NOT IMPLEMENTED | PPM-22-003 | p95 under 1 s on documented profile including password verification |
| N-003 | Scalable tenant data separation | NOT IMPLEMENTED | PPM-22-001 | Indexed tenant queries tested at stated load with no isolation failure |
| N-004 | Responsive enterprise UI | PARTIAL | PPM-81-010 | 360/768/1440 layouts usable and keyboard navigable |
| N-005 | Dark mode and glass effects | PARTIAL | PPM-23-001 | Tokens/themes retain readable contrast and reduced-motion support |
| N-006 | FCP under 2 seconds | NOT IMPLEMENTED | PPM-23-001 | Representative authenticated dashboard meets documented browser profile |
| N-007 | 60fps chart rendering target | NOT IMPLEMENTED | PPM-23-001 | Frame-time distribution reported for documented dataset/device/actions |
| N-008 | Nonblocking asynchronous processing | PARTIAL | PPM-23-001 | Heavy jobs separate from API and restart safely under load |
| N-009 | Typed AI output validation | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 | Invalid provider output never accepted as valid result |
| N-010 | Timeout fallback | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 | Bounded retries and truthful degraded/failure states tested |
| N-011 | 99.9% alert worker availability target | NOT IMPLEMENTED | PPM-21-003 | SLI monitoring/runbook created; observed window reported separately |
| N-012 | Versioned migrations and contracts | PARTIAL | PPM-81-010 | Clean/prior-state migration and API client drift checks exist |
| N-013 | Accessibility target | PARTIAL | PPM-23-001 | Core keyboard/screen-reader/contrast checks, then release regression |
| N-014 | AI and retrieval access isolation | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 | Adversarial source text and changed-access fixtures do not leak data |
| N-015 | Model validity and lineage | NOT IMPLEMENTED | PPM-12-003 | Temporal/entity split, model card, baseline and license evidence recorded |
| N-016 | Audit retention and revocation | NOT IMPLEMENTED | PPM-22-003 | Revocation covers download/stream/cache/jobs; retention configured |
| N-017 | Backup restore and deployment recovery | PARTIALLY IMPLEMENTED | PPM-23-002 | Restore/rollback exercise records measured results and remaining risks |
| N-018 | Sprint report and follow-up document | PARTIAL | PPM-81-010 | Every sprint/sub-sprint updates report, handoff, coverage and evidence |
| E-001 | Evidence drawer | VERIFIED COMPLETE | PPM-81-010 | KPI drill-down shows authorized sources and gaps |
| E-002 | Freshness and data coverage | VERIFIED COMPLETE | PPM-81-010 | Stale/missing sources visible without fabricated zeros |
| E-003 | Saved dashboard views | VERIFIED COMPLETE | PPM-81-010 | Personal scoped filters persist without leaking access |
| E-004 | Command palette | VERIFIED COMPLETE | PPM-81-010 | Keyboard navigation exposes only available permitted destinations |
| E-005 | Decision log | NOT IMPLEMENTED | PPM-16-003 | Approved alternatives/rationale and outcome review retained |
| E-006 | Scenario comparison | NOT IMPLEMENTED | PPM-17-002 | Baseline and scenario differences include assumptions |
| E-007 | Data-quality console | VERIFIED COMPLETE | PPM-81-010 | Import errors and rejected rows can be inspected/retried |
| E-008 | AI usage console | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-003 | Tenant usage/errors/budgets visible only to Admin |
| E-009 | CSV Jira GitHub connectors | BLOCKED | PPM-12-001 | Preview/incremental sync/replay limits tested; live credentials explicit |
| T-001 | Next.js TypeScript Tailwind shadcn Motion Zustand Recharts; Chart.js alternative | PARTIAL | PPM-23-001 | Compatible versions pinned; Gantt not misrepresented as built-in chart capability |
| T-002 | FastAPI Python Uvicorn Pydantic; NestJS alternative | VERIFIED COMPLETE | PPM-81-010 | Async API and schema foundation reproducible |
| T-003 | PostgreSQL JSONB SQLAlchemy Alembic Redis | VERIFIED COMPLETE | PPM-81-010 | Runtime and initial migrations verified |
| T-004 | Pinecone/Weaviate versus pgvector | PARTIALLY IMPLEMENTED | PPM-10-001 / ADR 016 | Chosen retrieval adapter records explicit substitution |
| T-005 | Neo4j | NOT IMPLEMENTED | PPM-18-001 | Derived graph rebuild and scope tests pass |
| T-006 | LangChain; LlamaIndex alternative | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 | One orchestration/tool contract, no duplicated framework stacks |
| T-007 | OpenAI Gemini Ollama HuggingFace options | PARTIALLY IMPLEMENTED | PPM-10-001 | One configured adapter with supported model and explicit disabled mode |
| T-008 | scikit-learn pandas XGBoost Random Forest MLflow | NOT IMPLEMENTED | PPM-12-003 | Reproducible baseline training/evaluation and lineage |
| T-009 | LightGBM LSTM time-series PyTorch DistilBERT candidates | NOT IMPLEMENTED | PPM-12-003 | Suitability assessed; experimental candidates not promised production |
| T-010 | Docker AWS ECS/RDS/S3 Terraform GitHub Actions | PARTIAL | PPM-23-002 | Reusable images/IaC/CI with explicit deployment evidence |
| T-011 | Kubernetes deployment profile | NOT IMPLEMENTED | PPM-23-002 | Same application images/config; validation status explicit |
| T-012 | Google Cloud/GCS EC2 Kafka alternatives | NOT REQUIRED | Scope decision: ADRs 004/006 | Alternatives explicitly deferred with rationale, not unimplemented hidden requirements |
| T-013 | Named core schema entities | PARTIAL | PPM-09-003 | Each named entity belongs to a domain and ER relationship |
| T-014 | Four execution phases | VERIFIED COMPLETE | PPM-23-003 | All capabilities preserved in dependency-ordered roadmap |
| T-015 | Names recruitment and resume claims | NOT REQUIRED | Scope decision: working name only | Working name only; promotional statements not treated as implemented evidence |

**Coverage count:** 156 original rows (109 functional, 18 controls, 9 enhancements, 15 technology choices, 5 planning deliverables). The old table's historical statuses are not overwritten; this is the current planning crosswalk.

F-001–003 closure additionally requires 8.1 entry/email/grant flows and 22/23 all-surface regression. F-065–074 require 09 documents/retrieval, 10 embedding runtime and 11 extraction/evidence review. F-075–077 consume 13 contracts and 14 factual/cited analytics. E-005 requires 14 drafts, 15 approval and 16 final decision log. N-011 availability monitoring is prepared in 21 and observed/reported in 23; a unit test cannot close an uptime target. T-013 named domain entities are validated against the whole final data model, not only the policy registry. T-015 is a working-name/promotion scope exclusion, not an absent product feature.

## Closure rules

No finding closes until its owning task's acceptance, negative cases and user result have evidence. Live credentials, genuine labels and external deployment require their own status and proof. A parent feature spanning stages remains PARTIAL until all required stages pass. Proposed optional items never count as release blockers unless later explicitly adopted. Application-source preservation in this planning session is separate from future implementation migration-preservation tests.


## 10 October 2026 follow-up: account and website workflow repair

The separate [repair and walkthrough execution report](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records migration `0009_account_repair`, account/membership separation, organization profile/name controls, calendar navigation, shared business errors, the verified scoped Hement grant correction, guarded training data and current tests. Earlier sprint evidence remains historical. Global production identity administration, live-provider acceptance, general document intake and AI remain PLANNED or unverified according to their existing gates; this follow-up does not close those gates.

## Sprint 09 crosswalk status reconciliation

F-065/068/069/073 have local source/OCR acceptance. F-066/067 are partial for
attributed intake, with semantic review still 11; F-074 is partial for keyword/citation
retrieval and Sprint 10 budgeted hybrid implementation; real-provider embedding smoke passed; broader retrieval quality remains unverified. N-014 is partial for source isolation and
adversarial input, pending the AI path. N-017 is partial for pilot scratch restores,
pending production/all-surface recovery. T-004 still has no vector implementation;
PostgreSQL keyword search is an explicit staged adapter, not acceptance of a vector
substitution. [Coverage](../requirements/coverage.md) and [checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md)
carry the matching scope and evidence. Required later acceptance is unchanged.
