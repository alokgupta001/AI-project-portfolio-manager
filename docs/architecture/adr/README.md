# Architecture decision records

Records 001–006 are the Sprint 00 **proposed baseline**. Record 007 describes the local foundation implemented under the user's Sprint 01 instruction. Each record states its own verification limits; production deployment choices are not automatically approved. Changing a decision requires a dated superseding record and consumer impact review.

| Record | Decision |
| --- | --- |
| [001](001-runtime-and-boundaries.md) | Modular monolith and frontend/backend ownership |
| [002](002-identity-and-tenancy.md) | JWT sessions, authorization and tenant isolation |
| [003](003-authority-and-projections.md) | PostgreSQL authority, object storage, vectors and graph |
| [004](004-jobs-and-events.md) | Durable asynchronous jobs and delivery semantics |
| [005](005-ai-and-model-governance.md) | AI tool boundaries, evidence and model eligibility |
| [006](006-deployment.md) | Local runtime and cloud deployment alternatives |
| [007](007-sprint-01-runtime.md) | Implemented Sprint 01 local runtime and dependency choices |
| [008](008-identity-implementation.md) | Implemented identity, cookie/CSRF/refresh policy, local mailbox and tenant RLS |
| [009](009-enterprise-shell.md) | Enterprise shell, native accessible primitives, semantic themes and deferred UI dependencies |
| [010](010-delivery-system-of-record.md) | Scoped delivery records, immutable plans/ledger, typed consumers and isolated demo |
| [011](011-resource-capacity.md) | Independent resources, local-date capacity, workforce grants and immutable allocation snapshots |

- [012 — Versioned assessments and quarantined evidence](012-assessment-engine.md): implemented Sprint 06 boundaries.

- [ADR 013 — Shared deterministic command-center snapshots](013-command-center.md)
