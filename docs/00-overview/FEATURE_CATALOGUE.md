# Feature catalogue

**Sprint 12 current implementation:** [local report](../03-sprints/completed/sprint-12/SPRINT_REPORT.md) and [actual checks](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) supersede earlier unstarted statements below. Local sample acceptance is complete at schema 0017 with healthy local services. Live source/model quality and AT17 remain blocked; stop before 13.

Sprint 11 current disposition: [nine specialists, semantic suggestions and independent review](../03-sprints/completed/sprint-11/README.md) are locally verified with deterministic responses. Real-model quality UNVERIFIED/BLOCKED. [Actual tests](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md); earlier dated notes retain their historical scope.

Code and retained local evidence establish current capability; original acceptance obligations are unchanged. Read [current scope and evidence limits](CURRENT_STATUS.md). Current status labels below translate the existing traceability vocabulary; a multi-stage parent remains partial until all stages pass. Future sprints describe intended user outcomes, not available buttons.

## Gap-level user outcomes

10 October account-email follow-up improves templates, configuration validation, truthful delivery statuses, reset-page wording and expired-invitation resend. Development Gmail signup and recovery journeys are confirmed; the test Admin signup arrived in Inbox and personal signup in Spam. A Viewer invitation was created through the website and accepted by Gmail; existing-account acceptance and active Viewer membership are verified. G-002 is verified for these development email journeys, with production readiness unchanged. See [account email checks](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md).

| Feature / gap | Current status | User benefit / intended result | Task / sprint |
| --- | --- | --- | --- |
| G-001 Public sign-up | IMPLEMENTED AND VERIFIED | Add verified registration with organization creation separated from login and invitation acceptance. | PPM-81-001 / 8.1 |
| G-002 Usable invitation and recovery delivery | IMPLEMENTED AND VERIFIED IN DEVELOPMENT | Gmail signup, existing-account Viewer invitation acceptance and recovery confirmed; lifecycle variants covered in isolated tests. Production acceptance remains open. | PPM-81-002 / 8.1 |
| G-003 First-time setup and organization profile | IMPLEMENTED AND VERIFIED | Add setup checklist and minimal profile editing with clear account versus resource explanations. | PPM-81-003 / 8.1 |
| G-004 Browser access management | IMPLEMENTED AND VERIFIED | Expose existing project/resource/assessment grants and understandable effective-access explanations. | PPM-81-004 / 8.1 |
| G-005 Search actual records | IMPLEMENTED AND VERIFIED | Add permission-filtered record search; document content keyword search is separately verified in Sprint 09. | PPM-81-005 / 8.1 |
| G-006 Complete lists and selectors | IMPLEMENTED AND VERIFIED | Add pagination and server search; make departmental comparison period and full cohort explicit. | PPM-81-006 / 8.1 |
| G-007 My work and basic notifications | IMPLEMENTED AND VERIFIED | Provide assigned work/assessment views and a small in-app feed; timed reminders and external channels stay in 15/21. | PPM-81-007 / 8.1 |
| G-008 Metadata needed by later analytics | IMPLEMENTED AND VERIFIED | Add optional controlled metadata with unknown values; never backfill invented categories. | PPM-81-008 / 8.1 |
| G-009 Live refresh of manual changes | IMPLEMENTED AND VERIFIED | Publish bounded authorized change notices and show freshness; do not broadcast record content. | PPM-81-009 / 8.1 |
| G-010 Guide and readiness wording | IMPLEMENTED AND VERIFIED IN DEVELOPMENT | Current pilot guide corrected, rendered and visually verified; prior browser journeys and hosted CI at 631c149 pass. Production release remains separate. | PPM-81-010 / 8.1 |
| G-011 Document library and assessment evidence bridge | IMPLEMENTED AND VERIFIED LOCALLY | Versioned sources/OCR and same-byte released-attachment bridge; original assessment authority/scores preserved. | PPM-09-001 / 09 |
| G-012 Governance policy lifecycle | PARTIALLY IMPLEMENTED | Registry/owner/applicability/source/dates/state verified locally in 09; approval integration remains 15. | PPM-09-003 / 09 |
| G-013 Retention and pilot restore evidence | PARTIALLY IMPLEMENTED | Scoped purge/holds and non-destructive scratch restore verified locally in 09; production backup erasure and all-surface release recovery remain 22/23. | PPM-09-003 / 09 |
| G-014 Document and AI dependency conflict | PARTIALLY IMPLEMENTED | Stage keyword retrieval/contracts in 09, budgeted embedding adapter in 10, reviewed extraction in 11. | PPM-10-001 / 10 |
| G-015 AI gateway and operations | PARTIALLY IMPLEMENTED | Shared runtime/UI and local guards verified; Gemini free-tier completion/embedding smoke passed; broader model/retrieval quality and scale remain unverified. | PPM-10-001 / 10 |
| G-016 Nine agents and semantic maturity scoring | IMPLEMENTED LOCALLY; real-model quality blocked | Build all nine agents with evidence and distinct suggested/reviewer scores. | PPM-11-001 / 11 |
| G-017 Recommendation review versus application | IMPLEMENTED LOCALLY; real-model quality blocked | Separate accepted recommendation from applied change; no generic mutation before 15. | PPM-11-003 / 11 |
| G-018 Repeat assessments, due dates and trend/export | PARTIALLY IMPLEMENTED | Extend the existing assessment lifecycle and connect workflow reminders, keeping published score history immutable. | PPM-15-002 / 15 |
| G-019 Unattended connector identity and conflict resolution | PARTIALLY IMPLEMENTED | Add narrow renewable connector authority, source identity uniqueness and reviewable conflict resolution. | PPM-12-001 / 12 |
| G-020 Live Jira/GitHub acceptance | BLOCKED | Run authorized read-only provider checks and controlled import with scoped credentials in 12; preserve fixtures and mark blocked until supplied. | PPM-12-001 / 12 |
| G-021 Historical features, labels and models | PLANNED | Capture justified historical fields and consented notes, validate labels and evaluate baseline models. | PPM-12-002 / 12 |
| G-022 Production model promotion evidence | BLOCKED | Require real temporal evaluation and suitability evidence; demo fixtures cannot satisfy promotion. | PPM-13-001 / 13 |
| G-023 Forecast serving | PLANNED | Serve eligible versions with uncertainty and honest unavailable/fallback states. | PPM-13-002 / 13 |
| G-024 Copilot, scoped context and natural language analytics | PLANNED | Build bounded authorized tools and cited conversation UI after evidence runtime. | PPM-14-001 / 14 |
| G-025 Approvals, escalation, due-event reminders | PLANNED | Implement inbox, calendars, authority checks and repeat-safe approved actions. | PPM-15-001 / 15 |
| G-026 Transformation and decisions | PLANNED | Build evidence-linked roadmaps and approval-based project conversion; consume copilot drafts. | PPM-16-001 / 16 |
| G-027 Resource and budget scenarios | PLANNED | Simulate immutable copies with conservation and stale-apply rejection. | PPM-17-001 / 17 |
| G-028 Knowledge graph and impact paths | PLANNED | Build scoped projection and bounded impact paths without changing source authority. | PPM-18-001 / 18 |
| G-029 Comparable benchmarks | PARTIALLY IMPLEMENTED | Compare compatible cohorts with counts, denominators and privacy suppression. | PPM-19-001 / 19 |
| G-030 Meeting intelligence | PLANNED | Add authorized uploads, transcription and evidence-linked review. | PPM-20-001 / 20 |
| G-031 Reports, alerts and daily audio | PARTIALLY IMPLEMENTED | Ship exports and authorized subscriptions; account emails remain 8.1. | PPM-21-001 / 21 |
| G-032 Passkeys and account lifecycle settings | PARTIALLY IMPLEMENTED | Implement passkeys and settings, preserving last-admin protection and all-surface revocation. | PPM-22-001 / 22 |
| G-033 Release engineering and production configuration | PARTIALLY IMPLEMENTED | Integrate all journeys and prepare deployment profiles; live deployment requires credentials and authorization. | PPM-23-001 / 23 |
| G-034 Sprint 08 hosted CI | IMPLEMENTED AND VERIFIED IN DEVELOPMENT | Reviewed application checkpoint 631c149 passed hosted CI run 38885041673; earlier source/data evidence is preserved. | PPM-81-010 / 8.1 |
| G-035 Current direct ASGI rerun | IMPLEMENTED AND VERIFIED | Full isolated suite completed:74 passing, including transaction-boundary tests. See Sprint 8.1 report. | PPM-81-010 / 8.1 |
| G-036 Planning consistency and source reconciliation | PARTIALLY IMPLEMENTED | Make the new future roadmap authoritative, preserve originals and reconcile every requirement at release. | PPM-81-010 / 8.1 |

## Requirement-level catalogue

These are the complete 156 approved crosswalk rows, including scope exclusions and technical controls. Acceptance wording is retained in the canonical traceability matrix.

| ID | Feature | Current scope status | Owning task / scope decision |
| --- | --- | --- | --- |
| P-001 | Preserve originals and prompts | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| P-002 | Trace scope and source conflicts | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| P-003 | Architecture and domain model | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| P-004 | Permissions and shared contracts | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| P-005 | Explain work and provide continuity | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-001 | JWT login and session lifecycle | PARTIALLY IMPLEMENTED | PPM-81-010 |
| F-002 | Admin PM Viewer RBAC | PARTIALLY IMPLEMENTED | PPM-81-010 |
| F-003 | Organization isolation | PARTIALLY IMPLEMENTED | PPM-81-010 |
| F-004 | Passkey enrollment and login | PLANNED | PPM-22-001 |
| F-005 | Portfolios | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-006 | Programs | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-007 | Project tracking | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-008 | Teams and resources | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-009 | Goals and strategic alignment | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-010 | Budgets and expenditure | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-011 | Sprints and milestones | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-012 | Blockers and dependencies | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-013 | Resource allocation | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-014 | Utilization efficiency | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-015 | Risk register | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-016 | Custom maturity framework builder | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-017 | Dynamic assessments | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-018 | Department scoring | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-019 | PMO capability analysis | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-020 | Agile maturity analysis | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-021 | Governance evaluation | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-022 | Delivery capability scoring | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-023 | Semantic answer evaluation | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-002 |
| F-024 | Pattern and maturity gap detection | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-003 |
| F-025 | Improvement suggestions | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-003 |
| F-026 | Portfolio health | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-027 | Business value | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-028 | Budget usage | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-029 | Alignment dashboard | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-030 | Sprint velocity | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-031 | Delay and timeline variance | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-032 | Blocker and dependency visualization | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-033 | Project risk score | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-034 | Escalation matrix | PLANNED | PPM-15-001 |
| F-035 | Predictive failure indicators | PLANNED | PPM-13-001 |
| F-036 | Allocation workload dashboard | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-037 | Reported versus evidence health | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| F-038 | Live project visibility | PARTIALLY IMPLEMENTED | PPM-81-009 |
| F-039 | AI progress streaming | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 |
| F-040 | PMO agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-041 | Risk agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-042 | Governance agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-043 | Agile coach agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-044 | Executive agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-045 | Resource agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-046 | Financial agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-047 | Schedule agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-048 | Sentiment agent | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-049 | Multi-agent aggregation | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-001 |
| F-050 | Sprint delay model | PLANNED | PPM-13-001 |
| F-051 | Project delay regression | PLANNED | PPM-13-001 |
| F-052 | Missed milestone model | PLANNED | PPM-13-001 |
| F-053 | Budget overrun forecast | PLANNED | PPM-13-002 |
| F-054 | Risk trends | PLANNED | PPM-13-003 |
| F-055 | Resource inefficiency indicators | PLANNED | PPM-13-003 |
| F-056 | Team overload signals | PLANNED | PPM-13-003 |
| F-057 | Project failure probability | PLANNED | PPM-13-001 |
| F-058 | Delivery confidence | PLANNED | PPM-13-003 |
| F-059 | High Medium Low risk classifier | PLANNED | PPM-13-001 |
| F-060 | NLP sentiment pipeline | PLANNED | PPM-12-003 |
| F-061 | PROMISE dataset suitability | PARTIALLY IMPLEMENTED: unreviewed external real data rejected; PROMISE-specific license/target review unavailable | PPM-12-002 |
| F-062 | Jira dataset suitability | PARTIALLY IMPLEMENTED: provenance/temporal contract; live Jira dataset/labels unavailable | PPM-12-002 |
| F-063 | Authorized public repository data | PLANNED | PPM-12-002 |
| F-064 | Synthetic dataset generator | IMPLEMENTED AND VERIFIED LOCALLY: isolated seed-12 numeric fixture; no real accuracy claim | PPM-12-002 |
| F-065 | SRS BRD PRD classification | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 |
| F-066 | MOM and sprint report ingestion | PARTIALLY IMPLEMENTED; local review controls verified, real semantic quality blocked | PPM-11-003 |
| F-067 | Risk log ingestion | PARTIALLY IMPLEMENTED; local review controls verified, real semantic quality blocked | PPM-11-003 |
| F-068 | Project charter ingestion | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 |
| F-069 | Governance policy ingestion | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-003 |
| F-070 | Extract risks and blockers | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-003 |
| F-071 | Extract dependencies | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-003 |
| F-072 | Compliance gaps and maturity indicators | IMPLEMENTED AND VERIFIED LOCALLY; model quality UNVERIFIED/BLOCKED | PPM-11-003 |
| F-073 | OCR | IMPLEMENTED AND VERIFIED LOCALLY | PPM-09-001 |
| F-074 | Scoped RAG | PARTIALLY IMPLEMENTED | PPM-10-001 |
| F-075 | Conversational copilot | PLANNED | PPM-14-001 |
| F-076 | Root causes and predicted impact | PLANNED | PPM-14-001 |
| F-077 | Natural language analytics | PLANNED | PPM-14-001 |
| F-078 | PMO transformation roadmap | PLANNED | PPM-16-001 |
| F-079 | Process improvement plans | PLANNED | PPM-16-001 |
| F-080 | Governance structures | PLANNED | PPM-16-001 |
| F-081 | KPI frameworks | PLANNED | PPM-16-001 |
| F-082 | Delivery optimization strategy | PLANNED | PPM-16-001 |
| F-083 | Agile transformation roadmap | PLANNED | PPM-16-001 |
| F-084 | Approval flows | PLANNED | PPM-15-001 |
| F-085 | Escalation system | PLANNED | PPM-15-003 |
| F-086 | Automated reminders | PLANNED | PPM-15-003 |
| F-087 | SLA tracking | PLANNED | PPM-15-003 |
| F-088 | Milestone notifications | PLANNED | PPM-15-003 |
| F-089 | Project to Team graph | PLANNED | PPM-18-001 |
| F-090 | Project to Risk graph | PLANNED | PPM-18-001 |
| F-091 | Team to Skill graph | PLANNED | PPM-18-001 |
| F-092 | Risk to Dependency graph | PLANNED | PPM-18-001 |
| F-093 | Portfolio to Business Goal graph | PLANNED | PPM-18-001 |
| F-094 | Impact and root cause tracing | PLANNED | PPM-18-003 |
| F-095 | Organizational mapping | PLANNED | PPM-18-003 |
| F-096 | Meeting recording/transcript intake | PLANNED | PPM-20-001 |
| F-097 | Meeting minutes generation | PLANNED | PPM-20-002 |
| F-098 | Meeting actions and blockers | PLANNED | PPM-20-003 |
| F-099 | Budget-cut simulation | PLANNED | PPM-17-001 |
| F-100 | Resource-transfer Time Machine | PLANNED | PPM-17-001 |
| F-101 | Department benchmarking | PLANNED | PPM-19-003 |
| F-102 | Team benchmarking | PLANNED | PPM-19-003 |
| F-103 | Portfolio benchmarking | PLANNED | PPM-19-003 |
| F-104 | Delivery maturity comparison | PLANNED | PPM-19-001 |
| F-105 | Weekly executive summaries | PLANNED | PPM-21-001 |
| F-106 | Email risk alerts | PLANNED | PPM-21-002 |
| F-107 | Slack risk alerts | PLANNED | PPM-21-002 |
| F-108 | Daily executive TTS briefing | PLANNED | PPM-21-001 |
| F-109 | HTML email and PDF reports | PLANNED | PPM-21-003 |
| N-001 | bcrypt password hashing | PARTIALLY IMPLEMENTED | PPM-22-003 |
| N-002 | Sub-second login target | PLANNED | PPM-22-003 |
| N-003 | Scalable tenant data separation | PLANNED | PPM-22-001 |
| N-004 | Responsive enterprise UI | PARTIALLY IMPLEMENTED | PPM-81-010 |
| N-005 | Dark mode and glass effects | PARTIALLY IMPLEMENTED | PPM-23-001 |
| N-006 | FCP under 2 seconds | PLANNED | PPM-23-001 |
| N-007 | 60fps chart rendering target | PLANNED | PPM-23-001 |
| N-008 | Nonblocking asynchronous processing | PARTIALLY IMPLEMENTED | PPM-23-001 |
| N-009 | Typed AI output validation | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 |
| N-010 | Timeout fallback | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 |
| N-011 | 99.9% alert worker availability target | PLANNED | PPM-21-003 |
| N-012 | Versioned migrations and contracts | PARTIALLY IMPLEMENTED | PPM-81-010 |
| N-013 | Accessibility target | PARTIALLY IMPLEMENTED | PPM-23-001 |
| N-014 | AI and retrieval access isolation | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 |
| N-015 | Model validity and lineage | PARTIALLY IMPLEMENTED: local manifests/splits/model cards; genuine outcome quality unverified | PPM-12-003 |
| N-016 | Audit retention and revocation | PLANNED | PPM-22-003 |
| N-017 | Backup restore and deployment recovery | PARTIALLY IMPLEMENTED | PPM-23-002 |
| N-018 | Sprint report and follow-up document | PARTIALLY IMPLEMENTED | PPM-81-010 |
| E-001 | Evidence drawer | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| E-002 | Freshness and data coverage | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| E-003 | Saved dashboard views | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| E-004 | Command palette | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| E-005 | Decision log | PLANNED | PPM-16-003 |
| E-006 | Scenario comparison | PLANNED | PPM-17-002 |
| E-007 | Data-quality console | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| E-008 | AI usage console | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-003 |
| E-009 | CSV Jira GitHub connectors | PARTIALLY IMPLEMENTED: local authority/dedup/conflict/recovery controls; live source equality BLOCKED | PPM-12-001 |
| T-001 | Next.js TypeScript Tailwind shadcn Motion Zustand Recharts; Chart.js alternative | PARTIALLY IMPLEMENTED | PPM-23-001 |
| T-002 | FastAPI Python Uvicorn Pydantic; NestJS alternative | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| T-003 | PostgreSQL JSONB SQLAlchemy Alembic Redis | IMPLEMENTED AND VERIFIED | PPM-81-010 |
| T-004 | Pinecone/Weaviate versus pgvector | PARTIALLY IMPLEMENTED | PPM-10-001 / ADR 016 |
| T-005 | Neo4j | PLANNED | PPM-18-001 |
| T-006 | LangChain; LlamaIndex alternative | IMPLEMENTED AND VERIFIED LOCALLY | PPM-10-002 |
| T-007 | OpenAI Gemini Ollama HuggingFace options | PARTIALLY IMPLEMENTED | PPM-10-001 |
| T-008 | scikit-learn pandas XGBoost Random Forest MLflow | PARTIALLY IMPLEMENTED: pandas/scikit-learn constant/linear/RF; local JSON tracking; native MLflow/XGBoost deferred | PPM-12-003 |
| T-009 | LightGBM LSTM time-series PyTorch DistilBERT candidates | DEFERRED: no suitable genuine labels/resources for larger/text candidates | PPM-12-003 |
| T-010 | Docker AWS ECS/RDS/S3 Terraform GitHub Actions | PARTIALLY IMPLEMENTED | PPM-23-002 |
| T-011 | Kubernetes deployment profile | PLANNED | PPM-23-002 |
| T-012 | Google Cloud/GCS EC2 Kafka alternatives | NOT IN SCOPE | Scope decision: ADRs 004/006 |
| T-013 | Named core schema entities | PARTIALLY IMPLEMENTED | PPM-09-003 |
| T-014 | Four execution phases | IMPLEMENTED AND VERIFIED | PPM-23-003 |
| T-015 | Names recruitment and resume claims | NOT IN SCOPE | Scope decision: working name only |

User steps: [current guide](../06-user-guides/USER_GUIDE.md); future outcomes/acceptance: [roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md); obligations: [traceability](../09-planning/FEATURE_GAP_TRACEABILITY.md).

## Sprint 09 requirement boundaries

[Task evidence](../04-testing/sprint-based/sprint-09/README.md): F-065/068/069/073
accepted locally. F-066/067 cover attributable MOM/sprint/risk-log text now; findings/review
remain Sprint 11. F-074 covers scoped keyword/citation interfaces now; embeddings/hybrid
are implemented with bounded Gemini completion/embedding smoke verified; broad quality remains unverified. F-070–072 remain planned for 11. T-004 vector-provider choice is not
activated by PostgreSQL keyword search. [Coverage](../requirements/coverage.md) retains
the combined acceptance obligations; approvals and production recovery are not closed.
