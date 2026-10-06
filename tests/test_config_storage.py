from pathlib import Path

import pytest
from ppm_api.config import Settings, load_settings
from ppm_api.storage import LocalObjectStore
from pydantic import ValidationError


def test_missing_configuration_reports_names_without_secrets(monkeypatch):
    for key in ("PPM_APP_ENV", "PPM_DATABASE_URL", "PPM_REDIS_URL", "PPM_STORAGE_ROOT"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(RuntimeError, match="PPM_DATABASE_URL"):
        load_settings()


def test_production_disabled_until_security_modules(tmp_path):
    with pytest.raises(ValidationError):
        Settings(
            app_env="production",
            database_url="postgresql+asyncpg://u:p@localhost/db",
            redis_url="redis://localhost/0",
            storage_root=tmp_path,
        )


def test_storage_roundtrip_persists_between_adapter_instances(tmp_path: Path):
    store = LocalObjectStore(tmp_path)
    store.put("fixture/example.txt", b"initial")
    store.put("fixture/example.txt", b"replacement")
    assert LocalObjectStore(tmp_path).get("fixture/example.txt") == b"replacement"
    store.delete("fixture/example.txt")
    with pytest.raises(FileNotFoundError):
        store.get("fixture/example.txt")


@pytest.mark.parametrize("key", ["../secret", "/absolute", "C:/secret", "a\\b", "a/../../x", ""])
def test_storage_rejects_escaping_keys(tmp_path, key):
    with pytest.raises(ValueError):
        LocalObjectStore(tmp_path).put(key, b"forbidden")
