# Background worker

[ppm_worker/app.py](ppm_worker/app.py) configures Celery and the established
foundation.database_checkpoint, pipeline.dispatch and pipeline.run tasks.
Dispatch delivers due account mail and schedules authorized connectors. run calls
integrations/jobs.run_job; that domain lifecycle routes document, assistance,
specialist and ML processing to their existing feature operations.

Workers call domain services directly. HTTP adapters own endpoint metadata only.
PostgreSQL owns durable jobs/outbox/leases and Redis carries identifier-only task
messages. Live authority, generation fencing and retry behavior are unchanged.

See [features](../api/ppm_api/modules/README.md) and the
[project map](../../docs/01-architecture/PROJECT_MAP.md).
