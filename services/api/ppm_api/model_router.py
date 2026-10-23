"""Eligibility first, stable ranking second. No network or spending decision by a model."""

import hashlib
import hmac
import os
import re
from dataclasses import dataclass
from uuid import UUID

from ppm_api import ai_provider
from ppm_api.config import Settings
from ppm_api.model_contracts import ModelFailure, TaskClass
from ppm_api.model_registry import ModelPolicy, ModelProfile, trusted_json


@dataclass(frozen=True)
class RouteRequirements:
    tenant: UUID
    project: UUID
    task_class: TaskClass
    input_tokens: int
    output_tokens: int = 512
    categories: tuple[str, ...] = ()
    additional_task_classes: tuple[TaskClass, ...] = ()


def eligibility(p: ModelProfile, r: RouteRequirements, s: Settings) -> str | None:
    """Return the first unmet scope, quality, resource, credential or free-egress gate."""
    if not s.ai_runtime_v2_enabled or s.ai_execution_mode == "disabled" or not p.enabled:
        return "PROVIDER_DISABLED"
    if r.tenant not in p.allowed_tenants or (
        p.allowed_projects and r.project not in p.allowed_projects
    ):
        return "SCOPE_NOT_AUTHORIZED"
    classes = {r.task_class, *r.additional_task_classes}
    if p.benchmark_only or not classes <= set(p.qualified_task_classes):
        return "QUALITY_UNVERIFIED"
    if p.assigned_task_classes and not classes <= set(p.assigned_task_classes):
        return "ROLE_NOT_ASSIGNED"
    if p.structured_mode != "json_schema":
        return "UNSUPPORTED_CAPABILITY"
    if (
        r.input_tokens + r.output_tokens + 256 > p.context_tokens
        or r.output_tokens > p.max_output_tokens
    ):
        return "CONTEXT_LIMIT"
    if p.provider == "ollama":
        if not s.ai_ollama_enabled or not p.installed_digest:
            return "MODEL_NOT_INSTALLED"
        available = s.ai_local_available_memory_mb
        if available is None or available < p.memory_reservation_mb + 2048:
            return "LOCAL_RESOURCE"
        return None
    if (
        s.ai_execution_mode != "hybrid"
        or not s.ai_cloud_enabled
        or not s.ai_real_calls_authorized
        or s.ai_spend_limit_usd != 0
        or p.billing_class != "verified_free"
        or not p.free_tier_confirmed
        or not p.data_policy_confirmed
    ):
        return "SPENDING_NOT_AUTHORIZED"
    if s.ai_egress_policy_path is None:
        return "EGRESS_NOT_AUTHORIZED"
    egress = trusted_json(s.ai_egress_policy_path, s)
    tenant = egress.get(str(r.tenant))
    project = tenant.get(str(r.project)) if isinstance(tenant, dict) else None
    rule = project.get(p.provider) if isinstance(project, dict) else None
    if not isinstance(rule, list) or not set(r.categories) <= set(rule):
        return "EGRESS_NOT_AUTHORIZED"
    key = os.environ.get(p.credential_ref or "", "")
    if (
        not key
        or not p.credential_sha256
        or not hmac.compare_digest(hashlib.sha256(key.encode()).hexdigest(), p.credential_sha256)
    ):
        return "AUTHENTICATION"
    if p.provider == "gemini":
        # The legacy query/index/v1-agent ledger is deliberately unchanged. Do
        # not let it bypass the new shared account scope through mixed traffic.
        if s.ai_provider != "disabled" or p.requests_per_day > s.ai_gemini_daily_call_limit:
            return "CONFIGURATION"
        if p.model != ai_provider.GEMINI_COMPLETION_MODEL or key != s.ai_api_key.get_secret_value():
            return "CONFIGURATION"
        return ai_provider.gemini_block_reason(s)
    if p.provider == "puter":
        # The native Free allowance is distinct from Puter's paid compatible gateway.
        if p.upstream_provider != "openai-completion" or p.model != "gpt-4.1-mini-2025-04-14":
            return "CONFIGURATION"
        return None
    if p.provider in ("groq", "openrouter", "mistral"):
        if not re.fullmatch(r"[A-Za-z0-9_.:/-]+", p.model) or any(
            word in p.model.lower() for word in ("latest", "auto", "router")
        ):
            return "CONFIGURATION"
        if p.provider == "openrouter" and (
            not p.model.endswith(":free") or not p.upstream_provider
        ):
            return "SPENDING_NOT_AUTHORIZED"
        # Mistral exposes rolling aliases as well as dated model IDs. Qualify
        # and bind an exact dated version, never upgrade a model implicitly.
        if p.provider == "mistral" and not re.search(r"-\d{4}(?:\d{2})?$", p.model):
            return "CONFIGURATION"
        return None
    return "SPENDING_NOT_AUTHORIZED"


def candidates(
    policy: ModelPolicy, requirements: RouteRequirements, settings: Settings
) -> tuple[list[ModelProfile], dict[str, str]]:
    """Filter profiles through eligibility and rank eligible choices deterministically."""
    eligible, reasons = [], {}
    for profile in policy.profiles:
        try:
            reason = eligibility(profile, requirements, settings)
        except ModelFailure as exc:
            reason = exc.code
        if reason:
            reasons[profile.id] = reason
        else:
            eligible.append(profile)
    latency = {"fast": 0, "normal": 1, "unknown": 2}
    eligible.sort(
        key=lambda p: (p.priority, -p.quality_tier, latency[p.latency_bucket], p.provider, p.model)
    )
    return eligible, reasons
