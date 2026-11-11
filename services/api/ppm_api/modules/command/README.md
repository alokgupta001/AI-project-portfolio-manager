# Command

Evidence-backed current portfolio metrics and dashboard snapshots.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [record_schemas.py](record_schemas.py) | Risk, benefit, metric-plan/policy and saved-view record inputs |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Snapshot, metric, evidence and resource/team response DTOs |
| [service.py](service.py) | Source fact assembly, freshness/coverage, risk rules and current snapshot orchestration |
| [tables.py](tables.py) | Command metric/risk/benefit plans, policies and saved views |

record_schemas separates writable metric/risk inputs from snapshot response DTOs, allowing the generic record API to compose types without circular imports. Snapshot calculations still call scoped capacity and delivery operations.

See the [contract](../../../../../docs/contracts/command-center.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
