import asyncio
import os

from alembic import context
from ppm_api import assessment_tables, command_tables, identity_tables, ppm_tables  # noqa: F401
from ppm_api.database import Base
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

target_metadata = Base.metadata


def run_sync(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async():
    url = os.environ.get("PPM_MIGRATION_DATABASE_URL")
    if not url:
        raise RuntimeError("PPM_MIGRATION_DATABASE_URL is required; use the migration role")
    engine = create_async_engine(url, poolclass=pool.NullPool)
    try:
        async with engine.connect() as connection:
            await connection.run_sync(run_sync)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    context.configure(
        url="postgresql+asyncpg://",
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(run_async())
