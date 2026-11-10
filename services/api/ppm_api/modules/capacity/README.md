# Capacity

Workforce records, staffing eligibility, calendars, effort privacy and capacity.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Validated feature inputs and public response models |
| [service.py](service.py) | Workforce scope/eligibility, source loading, daily/weekly arithmetic and snapshots |
| [tables.py](tables.py) | Resources, calendars, availability, teams/skills, time off, allocations, resource access, effort and snapshots |

Workforce inputs and tables both belong here. Delivery delegates capacity kinds to this service; command consumes its authorized summaries. Typed records register through the explicit shared registry.

See the [contract](../../../../../docs/contracts/capacity.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
