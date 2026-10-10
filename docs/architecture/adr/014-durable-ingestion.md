# ADR 014 Durable ingestion and observable progress

Status: accepted for the user-authorized local Sprint 08 slice, 2026-10-09.
Extends ADR 004; sources WT, S4.2/S4.3 and Sprint 08 ordered prompt.

PostgreSQL job/outbox/progress/provenance rows are the authority; Celery/Redis only
dispatch identifiers. Organization locks, live initiating authority, per-effect
transactions, fencing tokens and retained source identities make retries safe.
Narrow owner functions expose control-plane identifiers or cancel objectively
unauthorized work, never bypass domain effect RLS. Real application-role tests and
actual process-crash recovery are required before acceptance.

Connection definitions are explicit and immutable, with revision-checked enable/
disable and delegated session renewal. Secrets are environment references tied to
tenant/provider prefixes. Native GitHub hooks use exact-body signatures and retained
delivery IDs; Jira initially polls. Unsupported host/redirect targets fail closed.
CSV and provider fixtures are labelled and separate from live authentication.

Source time remains distinct from observation and computation. In particular,
Jira sprint modification time is unknown; imported historical sprint closures have
unknown point coverage. Import does not overwrite local edits or weaken delivery
lifecycle, assessment immutability, resource grants or team suppression. Incidental
provider notes are not persisted. SSE contains sanitized observable stages only.

Consequences: bounded at-least-once recovery; no exactly-once external guarantee.
Missing credentials do not block contract acceptance but keep live authentication/
sync unverified. Local retention remains explicit without silently deleting data.
Shared later processing handlers must preserve the same authority and checkpoint
rules; Sprint 09 is not activated by providing this infrastructure.

Implementation, workload bounds, native versus gateway webhook distinction,
cursor semantics and recovery procedures are defined by
[jobs-v1](../../contracts/jobs-integrations.md).
