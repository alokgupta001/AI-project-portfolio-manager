"""Validate configuration without exposing credential values in failures."""

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Literal

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
    TypeAdapter,
    ValidationError,
    field_validator,
    model_validator,
)
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
    mail_mode: Literal["local", "smtp"] = "local"
    smtp_host: str = ""
    smtp_port: int = Field(default=587, ge=1, le=65535)
    smtp_user: str = ""
    smtp_password: SecretStr = SecretStr("")
    mail_sender: str = ""
    document_scanner_host: str = ""
    document_scanner_port: int = Field(default=3310, ge=1, le=65535)
    ai_provider: Literal["disabled", "openai", "gemini"] = "disabled"
    ai_real_calls_authorized: bool = False
    ai_api_key: SecretStr = SecretStr("")
    ai_completion_model: str = Field(default="", max_length=160)
    ai_embedding_model: str = Field(default="", max_length=160)
    ai_spend_limit_usd: Decimal = Field(default=Decimal("0"), ge=0, le=10000)
    ai_input_usd_per_million: Decimal = Field(default=Decimal("0"), ge=0, le=1000)
    ai_output_usd_per_million: Decimal = Field(default=Decimal("0"), ge=0, le=1000)
    ai_embedding_usd_per_million: Decimal = Field(default=Decimal("0"), ge=0, le=1000)
    # Gemini API has no request-level "free only" switch. This records the operator's
    # confirmation that this key's project has NO linked Cloud Billing account.
    ai_gemini_free_tier_project: str = Field(default="", max_length=100)
    ai_gemini_free_tier_confirmed_at: datetime | None = None
    ai_gemini_free_tier_key_sha256: str = Field(default="", max_length=64)
    ai_gemini_daily_call_limit: int = Field(default=20, ge=1, le=100)

    @model_validator(mode="after")
    def validate_mail(self) -> "Settings":
        if self.mail_mode != "smtp":
            return self
        from email.utils import parseaddr

        if not self.smtp_host.strip() or any(c.isspace() for c in self.smtp_host):
            raise ValueError("SMTP requires PPM_SMTP_HOST")
        if self.smtp_port == 465:
            raise ValueError("Use a STARTTLS SMTP port (usually 587), not implicit TLS port 465")
        if "\r" in self.mail_sender or "\n" in self.mail_sender:
            raise ValueError("PPM_MAIL_SENDER must be a valid sender address")
        try:
            TypeAdapter(EmailStr).validate_python(parseaddr(self.mail_sender)[1])
        except ValidationError:
            raise ValueError("PPM_MAIL_SENDER must be a valid sender address") from None
        if bool(self.smtp_user) != bool(self.smtp_password.get_secret_value()):
            raise ValueError(
                "Configure both PPM_SMTP_USER and PPM_SMTP_PASSWORD, or neither for a relay"
            )
        return self

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
        fields = sorted(
            {
                "PPM_" + str(e["loc"][0]).upper() if e["loc"] else "PPM_MAIL_CONFIGURATION"
                for e in exc.errors()
            }
        )
        raise RuntimeError("Missing or invalid configuration: " + ", ".join(fields)) from None
