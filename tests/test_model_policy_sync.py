"""Schema admission for the explicit owner-only policy tool; no database/model calls."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from ppm_api.modules.ai.registry import ModelPolicy

from scripts import sync_model_policy


@pytest.mark.parametrize("revision", ["0019_selection_pilot", "0020_guided_cloud_timeout"])
async def test_sync_accepts_current_schema_revisions(monkeypatch, revision):
    conn = AsyncMock()
    conn.scalar.return_value = revision
    engine = MagicMock()
    engine.begin.return_value.__aenter__.return_value = conn
    engine.dispose = AsyncMock()
    monkeypatch.setenv("PPM_MIGRATION_DATABASE_URL", "postgresql+asyncpg://test/ppm_test")
    monkeypatch.setattr(sync_model_policy, "create_async_engine", lambda _: engine)

    await sync_model_policy.sync(ModelPolicy(profiles=[]))

    conn.scalar.assert_awaited_once()
    engine.dispose.assert_awaited_once()


async def test_sync_rejects_unknown_schema_before_writing(monkeypatch):
    conn = AsyncMock()
    conn.scalar.return_value = "9999_unreviewed_schema"
    engine = MagicMock()
    engine.begin.return_value.__aenter__.return_value = conn
    engine.dispose = AsyncMock()
    monkeypatch.setenv("PPM_MIGRATION_DATABASE_URL", "postgresql+asyncpg://test/ppm_test")
    monkeypatch.setattr(sync_model_policy, "create_async_engine", lambda _: engine)

    with pytest.raises(ValueError):
        await sync_model_policy.sync(ModelPolicy(profiles=[]))

    conn.execute.assert_not_awaited()
    engine.dispose.assert_awaited_once()
