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
    task_time_limit=30,
    task_soft_time_limit=20,
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
