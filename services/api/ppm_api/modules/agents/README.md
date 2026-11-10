# Agents

Read-only specialists, bounded task graphs and independent analysis review.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [batch.py](batch.py) | Compact multi-role request packing and independent result validation |
| [context.py](context.py) | Role-scoped evidence packing and restricted section schemas |
| [critique.py](critique.py) | Independent critique packing and validation |
| [engine.py](engine.py) | Deterministic specialist baselines and immutable analysis findings |
| [examples.py](examples.py) | Authored positive training-format examples |
| [guided_review.py](guided_review.py) | Limited model selection of existing review observations and explicit guided project grants |
| [planner.py](planner.py) | Validated bounded graph planning and dependency rules |
| [prompts.py](prompts.py) | Versioned role guidance and cloud prompt construction |
| [provider.py](provider.py) | Existing specialist adapter interface and fixture envelopes |
| [recovery.py](recovery.py) | Bounded recovery/fallback classification |
| [registry.py](registry.py) | The nine specialist roles, modes and evidence capabilities |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [runtime.py](runtime.py) | Bounded permission-rechecked graph execution, replay and section settlement |
| [schemas.py](schemas.py) | Specialist, analysis and independent-review public validation models |
| [service.py](service.py) | Specialist capabilities, evidence/fact capture, analysis lifecycle, independent review and publish/execute orchestration |
| [tables.py](tables.py) | Persisted analysis/review data |
| [task_tables.py](task_tables.py) | Persisted task graphs, usage, sections and execution lineage |
| [validation.py](validation.py) | Grounding, predicate, section and reconciliation validation |

registry.py defines specialist roles; ai/registry.py defines model policy. service.py orchestrates facts/evidence and independent review, while runtime.py executes bounded persisted task graphs through AI adapters.

See the [contract](../../../../../docs/contracts/agents.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
