"""Validate configuration without exposing credential values in failures."""

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PPM_", extra="ignore", hide_input_in_errors=True)

    app_env: Literal["local", "test", "demo"]
    database_url: SecretStr
    redis_url: SecretStr
    storage_root: Path
    jwt_secret: SecretStr
    web_origin: str = "http://localhost:3000"
    cookie_secure: bool = True

    @field_validator("jwt_secret")
    @classmethod
    def validate_key(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value().encode()) < 32:
            raise ValueError("must contain at least 32 bytes")
        return value

    @field_validator("web_origin")
    @classmethod
    def validate_origin(cls, value: str) -> str:
        from urllib.parse import urlparse

        url = urlparse(value)
        if url.scheme not in {"http", "https"} or not url.netloc or url.path:
            raise ValueError("must be an origin without a path")
        if url.scheme == "http" and url.hostname not in {"localhost", "127.0.0.1"}:
            raise ValueError("HTTP is allowed only on loopback")
        return value

    dependency_timeout_seconds: float = Field(default=3.0, gt=0, le=10)

    @field_validator("database_url")
    @classmethod
    def validate_database(cls, value: SecretStr) -> SecretStr:
        try:
            url = make_url(value.get_secret_value())
            if url.drivername != "postgresql+asyncpg" or not url.database or not url.host:
                raise ValueError
        except Exception as exc:
            raise ValueError("must be a postgresql+asyncpg URL with host and database") from exc
        return value

    @field_validator("redis_url")
    @classmethod
    def validate_redis(cls, value: SecretStr) -> SecretStr:
        from urllib.parse import urlparse

        url = urlparse(value.get_secret_value())
        if url.scheme not in {"redis", "rediss"} or not url.hostname:
            raise ValueError("must be a redis or rediss URL with a host")
        return value


def load_settings() -> Settings:
    try:
        return Settings()  # type: ignore[call-arg]
    except ValidationError as exc:
        fields = sorted({"PPM_" + str(e["loc"][0]).upper() for e in exc.errors()})
        raise RuntimeError("Missing or invalid configuration: " + ", ".join(fields)) from None
