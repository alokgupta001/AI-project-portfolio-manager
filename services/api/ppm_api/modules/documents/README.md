# Documents

Versioned sources, extraction/OCR, scoped retrieval and controlled retention.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description, with no eager exports |
| [access.py](access.py) | Tenant/project-scoped document/version lookup, deleted-source handling and write eligibility |
| [files.py](files.py) | Bounded upload, private download tickets/downloads and reprocessing |
| [lifecycle.py](lifecycle.py) | Cancellation, governance, deletion/purge, evidence links and controlled orphan retention |
| [mutations.py](mutations.py) | Revision preconditions, UUID request keys and shared path/body fingerprints |
| [parser.py](parser.py) | Intake validation, scanner transport, bounded subprocess extraction, OCR and source chunk locations |
| [queries.py](queries.py) | Library/search/detail, chunk previews/citations, job progress and authorized evidence-reference reads |
| [retrieval.py](retrieval.py) | Embedding-provider protocol and typed source/candidate-finding inputs |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Pydantic request/response contracts |
| [service.py](service.py) | Shared source responses, authorized replay and processing job/outbox enqueueing |
| [tables.py](tables.py) | SQLAlchemy source tables and the existing shared table-definition helper |
| [worker.py](worker.py) | Existing durable-job processor: persisted/live authority, fenced leases, scanner/parser, integrity and atomic publication |

All 18 handlers remain thin. Operations separate access, reads, file handling and lifecycle; worker.py retains scan/parse/publication, source integrity, leases and live authority. API/agent consumers call operations directly.

See the [contract](../../../../../docs/contracts/documents.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
