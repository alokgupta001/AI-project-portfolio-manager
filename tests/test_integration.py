import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from ppm_api.config import load_settings
from ppm_api.main import create_app
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Use isolated Compose test service"
    ),
]


def test_real_readiness_and_persisted_checkpoint():
    with TestClient(create_app(load_settings())) as client:
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200, response.text
        first = client.get("/api/v1/foundation").json()
    with TestClient(create_app(load_settings())) as restarted_client:
        second = restarted_client.get("/api/v1/foundation").json()
    assert first["instance_id"] == second["instance_id"]
    assert first["environment"] == "test"
    assert first["schema_revision"] == "0014_specialist_reviewer"


async def test_real_database_write_commit_read_roundtrip():
    engine = create_async_engine(os.environ["PPM_MIGRATION_DATABASE_URL"])
    value = str(uuid4())
    try:
        async with engine.connect() as conn:
            assert await conn.scalar(text("SELECT current_database()")) == "ppm_test"
            await conn.execute(
                text("CREATE TEMP TABLE roundtrip (value text) ON COMMIT PRESERVE ROWS")
            )
            await conn.execute(text("INSERT INTO roundtrip VALUES (:value)"), {"value": value})
            await conn.commit()
            assert await conn.scalar(text("SELECT value FROM roundtrip")) == value
    finally:
        await engine.dispose()


async def test_app_role_cannot_bypass_security_or_mutate_checkpoint():
    engine = create_async_engine(load_settings().database_url.get_secret_value())
    try:
        async with engine.connect() as conn:
            flags = (
                await conn.execute(
                    text("SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user")
                )
            ).one()
            assert flags == (False, False)
            assert await conn.scalar(text("SELECT current_user")) == "ppm_app"
            with pytest.raises(DBAPIError):
                await conn.execute(text("UPDATE foundation_state SET id = 1"))
    finally:
        await engine.dispose()
