# What AI actually does in this checkpoint

[Learning roadmap](../00-getting-started/README.md) Â· Next: [sprint history](../01-project-foundations/SPRINT_HISTORY.md)

No complete AI request path was found in the current application source. The product name and requirements describe a broader destination than the Sprint 8.1 implementation.

| Category | Current finding | Evidence |
| --- | --- | --- |
| Implemented and traceable AI | None found | Current API modules, worker tasks, frontend calls and runtime dependencies contain no connected model inference path. |
| Partially implemented AI feature | None found | There is no partly connected provider/retrieval feature to trace as a user workflow. |
| Existing infrastructure that could support AI later | PostgreSQL, private files, Redis, Celery, typed APIs, assessments and snapshots | These are working general components; they are not an AI pipeline. |
| Documentation/plans | Document retrieval, model gateway, semantic assessments, agents, training/serving and copilot | `docs/requirements/roadmap.md`, ADR `005-ai-and-model-governance.md` and planned contracts |

Assessment input is a published rubric, saved answers and human adjustments. `assessment.compute_scores` returns numeric scores/coverage/notes, stored by submission/review and displayed in assessment bars/tables. Invalid answers or missing required data are rejected by normal code. There is no model or model-request failure in that path.

Dashboard input is authorized schedule, finance and staffing data. `command.snapshot` calculates fixed risk/health values and returns them to `CommandCenter`. A missing component produces Unknown. Resource warnings similarly use hours and thresholds. Calling these AI would misdescribe the implementation.

## Redis and Celery: existing supporting technology

**What?** Redis stores shared small values and queued messages. Celery sends registered tasks to a worker process that executes them separately from the API.

**Why here?** Redis provides login attempt counts shared across API processes. Redis/Celery transport durable ingestion jobs and also demonstrate a real worker-to-database checkpoint round trip. **Where?** `identity.limited`, `main.ready`, [`services/worker/ppm_worker/app.py`](../../../services/worker/ppm_worker/app.py) and `scripts/smoke_worker.py`.

Real worker excerpt:

```python
@celery_app.task(name="foundation.database_checkpoint")
def database_checkpoint() -> dict[str, str]:
```

The decorator registers a task name that the smoke script can send. The function is the worker's task entry point. Inside it, `asyncio.run` runs a coroutine that creates its own engine, selects `FoundationState.instance_id`, returns the ID/status, and disposes the engine. That fresh engine belongs to the task's event loop.

**Internally:** the smoke script sends a JSON task through Redis â†’ Linux Celery worker reads it â†’ worker queries PostgreSQL â†’ result goes to Redis. Configuration uses the `foundation` queue, JSON serializers, time limits and result expiry of 300 seconds. The result is temporary task output, not a permanent business audit.

**If something goes wrong:** unavailable Redis makes rate-limited identity actions fail with 503 and readiness report unavailable. A dead worker cannot complete the checkpoint normally. The checkpoint task has no application-level retry/recovery workflow. Durable imports use the separate PostgreSQL outbox/job protocol, which does implement bounded retries and recovery; broker reconnect alone is insufficient.

Remember:

- Project, assessment and dashboard requests currently execute synchronously in the API.
- A working Celery checkpoint proves connectivity, not scheduled reports or AI agents.
- Redis is not a project-record cache in these flows.
- General durable jobs, retry history and recovery were implemented in Sprint 08; see the current jobs contract and tests.

## How to understand the planned terms

RAG means retrieving relevant stored material and giving it to a language model to help answer a question. This app has CSV/fixture record ingestion, but no connected document embedding, vector search or model-answer path, so there is no actual RAG input/output to document yet.

An agent is a model-driven process that can choose from permitted tools. No running agent or callable agent-tool set was found. Current backend functions should not be relabeled as agent tools without an integration.

An AI extension would need a defined input, permission check, provider/model call, validated output, storage/display path and failure behavior. For example, a future project-summary assistant could read only permitted project facts and return a clearly labeled suggestion. This is a proposal; it is not a current route or implemented function.

Chapter [11](../07-testing-and-debugging/DEVELOPER_GUIDE.md) gives the change sequence. Before claiming any future feature is complete, trace it from the UI to the model and back, test failure and unauthorized-input cases, and distinguish generated advice from deterministic stored facts.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Current durable imports live in `jobs.py` and `ingestion.py`; job state/outbox is PostgreSQL authority and Redis/Celery transports work. `account_mail.deliver_due` handles account deliveries separately. Provider failure/retry/cancellation diagnostics are not model inference. See `tests/test_jobs.py` and the jobs contract for recovery. A checkpoint-only task’s limitations must not be generalized to the implemented durable import pipeline.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Account mail now has verified development Gmail outcomes. Its durable delivery queue still has different semantics from an import job or an AI workflow: provider acceptance does not prove receipt, retries are bounded, and a cancelled/replaced challenge cannot authorize completion. Follow [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md) and the live evidence report before claiming a provider-backed result.
