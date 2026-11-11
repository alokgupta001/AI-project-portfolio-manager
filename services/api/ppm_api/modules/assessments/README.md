# Assessments

Maturity frameworks, assignments, private evidence, independent reviews and scoring.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description; no eager initialization or hidden imports |
| [access.py](access.py) | Tenant-scoped lookups, framework grants, respondent/reviewer and private-evidence checks, live write authorization |
| [evidence.py](evidence.py) | Private attachment listing/intake, storage and integrity checks, preview/download, draft removal and independent reviewer release |
| [examples.json](examples.json) | The four example frameworks loaded by `frameworks.py` |
| [frameworks.py](frameworks.py) | Framework listing/authoring, immutable published versions, example loading/seeding and framework response data |
| [mutations.py](mutations.py) | Write locking/authorization order, idempotency and replay, revision preconditions, error translation and request audit recording |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Pydantic request validation and response definitions |
| [scoring.py](scoring.py) | Deterministic weighted scores, answer/evidence coverage and reviewer adjustments |
| [service.py](service.py) | Assessment lifecycle operations, grant management, event-history reads, and shared assessment data/score/view/lifecycle helpers |
| [tables.py](tables.py) | SQLAlchemy table definitions registered in shared database metadata |
| [validation.py](validation.py) | Framework validation, question lookup and answer validity rules |

All 21 handlers remain thin. Access/mutation and domain modules reuse the existing Principal/transaction. Framework examples remain adjacent to their loader; private evidence and scoring rules are unchanged.

See the [contract](../../../../../docs/contracts/assessment.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
