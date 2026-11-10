# Integrations

Durable ingestion jobs, bounded adapters, connector authority and source conflicts.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [connector_router.py](connector_router.py) | Thin HTTP adapters for connector authority and conflict review |
| [connectors.py](connectors.py) | Connector principals, approvals, generation fencing, source conflict review and scheduling |
| [ingestion.py](ingestion.py) | Bounded adapters, connector configuration, input validation, normalization and fingerprints |
| [jobs.py](jobs.py) | Durable job operations, outbox/events, live worker authority, leases, ingestion effects and dispatch |
| [limits.py](limits.py) | Existing ASGI intake body-size guard used by main.py |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Integration, job, stage, source, authority and conflict request/response DTOs |
| [tables.py](tables.py) | Integration/job/outbox/event/provenance and connector principal/conflict tables |

Celery pipeline.run calls jobs.run_job. That lifecycle dispatches document, AI, agent and ML processing. HTTP routes live only in router/connector_router; job and connector services do not register endpoints. Table constructors live in shared/table_base.

See the [contract](../../../../../docs/contracts/jobs-integrations.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
