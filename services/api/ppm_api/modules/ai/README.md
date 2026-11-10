# Ai

Evidence-grounded assistance, budgets and policy-controlled model execution.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [adapters.py](adapters.py) | Shared native provider transports, cancellation and bounded protocol parsing |
| [ai_evaluation_v1.json](ai_evaluation_v1.json) | Versioned authored evaluation cases and deterministic acceptance thresholds |
| [contracts.py](contracts.py) | Shared typed model requests/results, agent modes and failure contracts |
| [deadlines.py](deadlines.py) | Task-specific execution deadline rules |
| [evaluation.py](evaluation.py) | Deterministic release-gate evaluation of the adjacent authored corpus |
| [model_router.py](model_router.py) | Policy-constrained candidate selection and fallback order |
| [ollama_provider.py](ollama_provider.py) | Existing compatibility export of the native adapter |
| [provider.py](provider.py) | Assistance adapter interface, fixed origins, provider envelopes and bounded errors |
| [qualification.py](qualification.py) | Versioned eligibility/qualification checks for model profiles |
| [readiness.py](readiness.py) | Local model availability/readiness diagnostics |
| [registry.py](registry.py) | Operator-owned policy/profile parsing, canonical JSON and fingerprints |
| [retrieval.py](retrieval.py) | Evidence selection, exact-quote validation and retrieval evaluation |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Assistance/index/query request and response models |
| [service.py](service.py) | Assistance/budget/run operations, source authorization, immutable snapshots and fenced worker processing |
| [tables.py](tables.py) | AI jobs, usage, source-index and immutable answer tables |
| [timing.py](timing.py) | Transport timing measurements |

The operator model policy/runtime is shared with agents. registry.py is model policy; model_router.py selects allowed transports. The worker entrypoint calls service.ai_worker. Existing prompt/provider/budget controls are unchanged.

See the [contract](../../../../../docs/contracts/ai.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
