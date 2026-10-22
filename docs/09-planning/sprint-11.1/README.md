# Sprint 11.1 — AI architecture implementation blueprint

Planning checkpoint: 17 October 2026 (Asia/Calcutta). Source baseline: `d0ebe32e691a3d63166ced669450911c63151127`. This package records the selected architecture. The user subsequently authorized implementation; the current [implementation report](../../03-sprints/active/sprint-11.1/README.md), [tracker](SPRINT_11_1_TASK_TRACKER.md) and [receipts](../../verification/sprint11_1/IMPLEMENTATION.md) supersede the original planning-only status. Model qualification and normal rollout remain open.

Selected direction (hybrid-role revision): retain nine business capability IDs, each combining deterministic services with optional qualified AI interpretation. Select model calls by requested analysis, evidence and budget, rather than permanently excluding six roles from AI. Extend the existing PostgreSQL/Celery runtime with bounded task checkpoints and provider-independent execution. Ollama supplies inference only. Existing scoring, privacy, review and zero-spend boundaries remain authoritative.

Python owns calculations, scoring, policy and execution. Models interpret evidence and synthesize findings where those tasks are justified. The existing four-attempt, 512-token and 90-second ceilings remain: they limit work per run, not which roles can ever use AI. Requested interpretations that do not fit remain explicitly deferred. See ADR 11.1-11, the catalog and orchestration for the revised contracts and scheduling policy.

## Reading order and artifacts

1. [Handover and resumption](SPRINT_11_1_HANDOVER.md)
2. [Sprint plan](SPRINT_11_1_PLAN.md)
3. [Repository discovery](SPRINT_11_1_DISCOVERY.md)
4. [Target architecture](SPRINT_11_1_ARCHITECTURE.md)
5. [Decision records and alternative assessment](SPRINT_11_1_DECISION_LOG.md)
6. [Nine capability contracts](SPRINT_11_1_AGENT_CATALOG.md)
7. [Provider and routing contract](SPRINT_11_1_PROVIDER_ROUTING.md)
8. [Orchestration and state](SPRINT_11_1_ORCHESTRATION.md)
9. [Validation and recovery](SPRINT_11_1_VALIDATION_RECOVERY.md)
10. [API, schema and persistence](SPRINT_11_1_TECHNICAL_CONTRACTS.md)
11. [Ordered implementation guide](SPRINT_11_1_IMPLEMENTATION_GUIDE.md)
12. [Testing and benchmarks](SPRINT_11_1_TEST_PLAN.md)
13. [Setup](SPRINT_11_1_SETUP.md)
14. [Risks and explicit unknowns](SPRINT_11_1_RISKS.md)
15. [Implementation tracker](SPRINT_11_1_TASK_TRACKER.md)
16. [Requirement traceability](SPRINT_11_1_TRACEABILITY.md)
17. [External source verification](SPRINT_11_1_SOURCES.md)

The technical contracts own schema names; orchestration owns state transitions and execution bounds; routing owns authorization/eligibility; validation owns acceptance. Other documents refer to those definitions rather than overriding them. An implementation conflict must be recorded and corrected across affected documents before the affected change proceeds.

Fresh evidence is kept in [Sprint 11.1 verification](../../verification/sprint11_1/README.md). Historical Sprint 11 evidence remains in [the existing review record](../../04-testing/sprint-based/sprint-11/REVIEW_FIXES.md).
