# ADR 017: Bounded specialists and independent review

Date: 16 October 2026. Scope: explicitly authorized Sprint 11 only.

Nine specialist interpretations and semantic maturity suggestions need durable,
tenant-scoped evidence and human review. Existing request/spend ceilings cannot
fund nine independent requests. We therefore batch typed specialist outputs in
one completion with the existing two-attempt bound and 512-token ceiling. Omitted
or failed specialists remain explicit; no unverified provider quality is claimed.

Reuse `ai_runs`, budgets/calls, durable jobs, leases, SSE/stages, authorization,
source citations and `command.snapshot`. Persist only an additive immutable
analysis snapshot/result plus append-only review decisions in 0013. Use exact
spans, fixed finding templates and deterministic deduplication/conflict handling.
Compute suggestions through the existing assessment scoring service. Neither
review acceptance nor an agent can mutate plans or original assessment results.

Sentiment receives only a server-created group blocker summary after existing
team privacy checks. Raw workforce notes and individual labels remain excluded.
This narrower delivery-support signal is not emotional sentiment or a trained
NLP model. Such quality claims remain future evaluation work.

Consequences: conservative revocation can withhold an entire analysis evidence
set when capture fails; source changes require a new run. Small output ceilings
may produce partial results for larger assessments. No scale, calibration,
regulatory certification or real-model semantic acceptance follows from mock
success. Provider/model settings, costs, confirmation and controls are unchanged.
Normal data remains at verified 0012 during this task; 0013 is tested only in
guarded disposable databases. No deployment is performed.

[Contract](../../contracts/agents.md) · [Report](../../03-sprints/completed/sprint-11/SPRINT_REPORT.md)
