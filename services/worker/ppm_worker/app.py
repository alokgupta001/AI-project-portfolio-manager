import asyncio

from celery import Celery
from ppm_api.config import load_settings
from ppm_api.database import FoundationState, make_engine
from sqlalchemy import select

settings = load_settings()
celery_app = Celery(
    "enterprise_ppm",
    broker=settings.redis_url.get_secret_value(),
    backend=settings.redis_url.get_secret_value(),
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_default_queue="foundation",
    task_track_started=True,
    result_expires=300,
    task_time_limit=300,
    task_soft_time_limit=280,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="foundation.database_checkpoint")  # type: ignore[untyped-decorator]
def database_checkpoint() -> dict[str, str]:
    async def run() -> dict[str, str]:
        # Engine belongs to this task/event loop, never inherited from the API or another loop.
        engine = make_engine(settings)
        try:
            async with engine.connect() as connection:
                instance = await connection.scalar(select(FoundationState.instance_id))
                if instance is None:
                    raise RuntimeError("Foundation migration required")
                return {"instance_id": str(instance), "status": "completed"}
        finally:
            await engine.dispose()

    return asyncio.run(run())


@celery_app.task(name="pipeline.dispatch")  # type: ignore[untyped-decorator]
def dispatch() -> int:
    async def run() -> int:
        import sqlalchemy as sa

        engine = make_engine(settings)
        try:
            from ppm_api.account_mail import deliver_due

            await deliver_due(engine, settings)
            async with engine.connect() as conn:
                due = list(
                    (await conn.execute(sa.text("SELECT * FROM public.ppm_due_jobs()"))).mappings()
                )
            for row in due:
                celery_app.send_task(
                    "pipeline.run",
                    args=[str(row["job_id"]), str(row["organization_id"]), str(row["actor_id"])],
                )
            return len(due)
        finally:
            await engine.dispose()

    return asyncio.run(run())


@celery_app.task(name="pipeline.run", acks_late=True, reject_on_worker_lost=True)  # type: ignore[untyped-decorator]
def pipeline_run(job_id: str, organization_id: str, actor_id: str) -> None:
    from uuid import UUID

    from ppm_api.jobs import run_job

    async def run() -> None:
        engine = make_engine(settings)
        try:
            await run_job(engine, UUID(job_id), UUID(organization_id), UUID(actor_id))
        finally:
            await engine.dispose()

    asyncio.run(run())


celery_app.conf.beat_schedule = {
    "reconcile-durable-jobs": {"task": "pipeline.dispatch", "schedule": 10.0}
}
