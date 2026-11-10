# Ml

Versioned history/datasets, reproducible baselines and authorized ML artifacts.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [pipeline.py](pipeline.py) | Deterministic dataset building, leakage checks, CPU baselines and reproducible cards |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Dataset/history, split, baseline and result validation |
| [service.py](service.py) | History/dataset/run operations, worker processing, withdrawal and artifact access |
| [tables.py](tables.py) | ML history, dataset and run lineage only |

Connector authority/conflict tables moved to integrations. This feature owns ML history/datasets/runs, as-of split/reproduction and artifact authority. Source fingerprinting and stored lineage retain their existing behavior.

See the [contract](../../../../../docs/contracts/ml.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
