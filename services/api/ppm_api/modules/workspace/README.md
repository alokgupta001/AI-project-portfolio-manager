# Workspace

Search, personal work, onboarding, cohort comparison and notification receipts.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Validated feature inputs and public response models |
| [service.py](service.py) | Scoped discovery/My Work, cohort views, notifications/preferences and authorized freshness streams |
| [tables.py](tables.py) | Personal notification receipts and preferences only |

This was formerly named pilot.py. It is the personal workspace API. Account mail tables/delivery belong to identity; financial-selection research belongs to selection.

See the [contract](../../../../../docs/contracts/pilot.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
