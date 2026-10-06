# ADR 004 Durable jobs and at least once events

Status: proposed baseline. Sources: WT, S4.3, S4.4. Decision date: 2026-10-05.

Use PostgreSQL outbox and job rows, Redis as Celery broker, and explicit idempotent consumers. Domain writes and their outbox events commit together. Dispatcher leases/retries events; worker inbox/dedup records protect logical effects. Recovery reconciles queued/running jobs against leases so broker loss does not erase authoritative job state.

CPU-heavy parsing/training/inference runs outside the API loop. Workers open their own transaction/tenant context and recheck current action authority. Cancellation is cooperative with clear outcomes for already-started external effects. SSE exposes persisted observable stages and retained event IDs; it is not the authoritative queue.

At-least-once delivery does not mean exactly-once effects at arbitrary external providers. Store attempt IDs, use provider idempotency if supported and represent unknown delivery status after ambiguous timeouts. Retries are bounded with backoff/jitter and dead-letter/operator recovery.

Alternatives: FastAPI in-process background tasks are suitable for small noncritical work but not the durability required here; Kafka is deferred until streaming scale or replay requirements justify its operations. Reference: [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), consulted 2026-10-05.

Consequence: Sprint 08 must demonstrate crash/replay recovery before later AI/reporting modules depend on it. Initial broker choice does not establish any availability claim.
