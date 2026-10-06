# ADR 010 — Transactional delivery foundation

Accepted for local Sprint 04, 2026-10-06.

Use normalized PostgreSQL tables and typed REST DTOs within the existing modular monolith. Extend migration history with 0003; preserve 0001/0002. Composite references, application authorization and RLS jointly bind records to organization/project scope. Shared organization locking serializes grant, membership, concurrency and dependency validation. This favors correctness over maximum write throughput; no load claim is made.

Use explicit project/portfolio grants, never infer access from ownership. Restrict cross-project dependency writes to Admin because a scoped graph could omit a cycle. Store immutable baseline snapshots, status updates and expenditure, with auditable reversals and optimistic revisions for mutable entities. Retain exact decimal strings in snapshots/API. Incomplete ledgers or alignment weights yield unknown metrics.

Reuse native Sprint 03 components with server-paged tables, forms, timeline and work board; no new runtime dependency or old-repository code import. Advanced schedule interactions remain future UX work. Portfolio summary currently queries each visible project; batching and load measurements remain needed before scale claims.

Run deterministic fixtures only in a separate demo project/database/volumes, guarded by both configuration and actual database name. Do not overwrite the user's local Demo organization or invent shared passwords. The full contract is [delivery.md](../../contracts/delivery.md).
