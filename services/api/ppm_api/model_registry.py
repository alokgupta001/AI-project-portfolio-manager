"""Operator-owned, versioned model policy. Missing configuration never enables inference."""

import hashlib
import json
from pathlib import Path
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from ppm_api.config import Settings
from ppm_api.document_schemas import Strict
from ppm_api.model_contracts import ModelFailure, TaskClass


def canonical(value: object) -> str:
    """Serialize deterministic UTF-8 JSON content for policy and request fingerprints."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def digest(value: object) -> str:
    """Fingerprint the canonical JSON representation with SHA-256."""
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class ModelProfile(Strict):
    id: str = Field(pattern=r"^[a-z0-9_-]{1,64}$")
    provider: Literal["ollama", "gemini", "groq", "puter", "openrouter", "mistral", "openai"]
    model: str = Field(min_length=1, max_length=160)
    enabled: bool = False
    billing_class: Literal["local", "verified_free", "paid", "unknown"] = "unknown"
    quota_scope: str = Field(min_length=1, max_length=160)
    allowed_tenants: list[UUID] = Field(default_factory=list, max_length=1000)
    allowed_projects: list[UUID] = Field(default_factory=list, max_length=1000)
    qualified_task_classes: list[TaskClass] = Field(default_factory=list, max_length=10)
    # Assignment restricts routing; it never grants semantic qualification.
    assigned_task_classes: list[TaskClass] = Field(default_factory=list, max_length=10)
    benchmark_only: bool = True
    # Independent permission for closed-choice assistance; never qualifies interpretation.
    guided_selection_enabled: bool = False
    structured_mode: Literal["json_schema", "json_object", "none"] = "json_schema"
    context_tokens: int = Field(default=4096, ge=512, le=32768)
    max_output_tokens: int = Field(default=512, ge=64, le=512)
    priority: int = Field(default=10, ge=0, le=1000)
    quality_tier: int = Field(default=0, ge=0, le=10)
    latency_bucket: Literal["fast", "normal", "unknown"] = "unknown"
    concurrency: int = Field(default=1, ge=1, le=4)
    requests_per_minute: int = Field(ge=1, le=1000)
    requests_per_day: int = Field(ge=1, le=100000)
    tenant_requests_per_day: int = Field(default=20, ge=1, le=10000)
    tokens_per_minute: int = Field(ge=512, le=10000000)
    installed_digest: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    credential_ref: str | None = Field(default=None, pattern=r"^PPM_[A-Z0-9_]{1,100}$")
    credential_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    free_tier_confirmed: bool = False
    data_policy_confirmed: bool = False
    # OpenRouter's exact upstream is part of the reviewed model/data-policy binding.
    upstream_provider: str | None = Field(default=None, pattern=r"^[a-z0-9_/-]{1,100}$")
    memory_reservation_mb: int = Field(default=4096, ge=1024, le=12000)

    @model_validator(mode="after")
    def bounded_local(self) -> "ModelProfile":
        """Validate profile identity, credentials, limits and provider-specific local bounds."""
        if self.provider == "ollama" and (
            self.concurrency != 1
            or self.context_tokens not in (2048, 4096)
            or self.billing_class != "local"
            or ":cloud" in self.model
        ):
            raise ValueError("Local profile must use a bounded private local model")
        return self


class ModelPolicy(Strict):
    schema_version: Literal["model-policy-v1"] = "model-policy-v1"
    profiles: list[ModelProfile] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def distinct(self) -> "ModelPolicy":
        """Reject duplicate profiles and inconsistent settings within a shared account scope."""
        if len({p.id for p in self.profiles}) != len(self.profiles):
            raise ValueError("Duplicate model profile")
        if len({p.quota_scope for p in self.profiles if p.provider == "ollama"}) > 1:
            raise ValueError("Local profiles must share one host quota scope")
        for credential in {p.credential_sha256 for p in self.profiles if p.credential_sha256}:
            if len({p.quota_scope for p in self.profiles if p.credential_sha256 == credential}) > 1:
                raise ValueError("A shared credential must share one quota scope")
        # A provider account/host cannot acquire extra quota through a profile alias.
        for scope in {p.quota_scope for p in self.profiles}:
            rows = [p for p in self.profiles if p.quota_scope == scope]
            fingerprints = {
                (
                    p.provider,
                    p.billing_class,
                    p.credential_sha256,
                    p.concurrency,
                    p.requests_per_minute,
                    p.requests_per_day,
                    p.tenant_requests_per_day,
                    p.tokens_per_minute,
                )
                for p in rows
            }
            if len(fingerprints) != 1:
                raise ValueError("Shared quota scope has conflicting limits")
        return self

    @property
    def policy_hash(self) -> str:
        """Fingerprint the validated policy used to fence admission and replay."""
        return digest(self.model_dump(mode="json"))


def trusted_json(path: Path, settings: Settings) -> dict:
    """Read a bounded operator JSON object, rejecting paths inside tenant storage_root."""
    resolved = path.resolve()
    if resolved.is_relative_to(settings.storage_root.resolve()):
        raise ModelFailure("CONFIGURATION")
    try:
        raw = resolved.read_bytes()
        if len(raw) > 64000:
            raise ValueError
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError
        return data
    except (OSError, ValueError):
        raise ModelFailure("CONFIGURATION") from None


def load_policy(settings: Settings) -> ModelPolicy:
    """Load the validated private model policy, defaulting to no enabled profiles."""
    if settings.ai_model_registry_path is None:
        return ModelPolicy()
    try:
        return ModelPolicy.model_validate(trusted_json(settings.ai_model_registry_path, settings))
    except ValueError:
        raise ModelFailure("CONFIGURATION") from None
