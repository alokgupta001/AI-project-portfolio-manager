from pathlib import Path

import pytest
from ppm_api.config import Settings


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        app_env="test",
        jwt_secret="unit-test-only-signing-key-at-least-32-bytes",
        database_url="postgresql+asyncpg://unused:unused@127.0.0.1:9/ppm_test",
        redis_url="redis://127.0.0.1:9/1",
        storage_root=tmp_path,
        dependency_timeout_seconds=0.2,
    )
