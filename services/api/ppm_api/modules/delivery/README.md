# Delivery

Portfolio/project records, scoped changes, audit and optimistic concurrency.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [metrics.py](metrics.py) | Pure budget-use and strategic-alignment arithmetic |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Delivery inputs and the composed typed-record union/views used by the generic record API |
| [service.py](service.py) | Record reads/writes, scope, reference validation, locking, revisions, audit/idempotency and summaries |
| [tables.py](tables.py) | Delivery records plus shared record audit/idempotency storage |

The generic record API composes inputs from delivery, capacity and command; it delegates workforce rules to capacity. Shared record construction lives in ppm_api/shared. Audit/idempotency transactions retain their existing ordering.

See the [contract](../../../../../docs/contracts/delivery.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
