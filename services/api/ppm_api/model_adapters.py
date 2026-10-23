"""Bounded async transports. No internal retries, redirects, tools or thought publication."""

import asyncio
import json
import os
from collections.abc import Callable
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from time import perf_counter
from typing import Literal
from urllib.parse import quote, urlparse

import httpx

from ppm_api import ai_provider
from ppm_api.config import Settings
from ppm_api.model_contracts import ErrorCode, ModelFailure, ModelRequest, ModelResult, ModelUsage
from ppm_api.model_registry import ModelProfile, load_policy
from ppm_api.model_router import RouteRequirements, candidates

CLOUD_CHAT_ORIGINS = {
    "groq": "https://api.groq.com/openai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "mistral": "https://api.mistral.ai/v1",
}


def strict_schema(schema: dict) -> dict:
    """Require existing properties for strict providers; local validation stays authoritative."""
    result = json.loads(json.dumps(schema))

    def visit(value: object) -> None:
        """Require all object properties and reject additional fields recursively."""
        if isinstance(value, dict):
            value.pop("default", None)
            if (
                value.get("type") == "array"
                and value.get("maxItems") == 0
                and value.get("items") == {}
            ):
                # The only permitted value is still []; strict providers require
                # even an unreachable array item schema to declare a type.
                value["items"] = {"type": "string"}
            if "properties" in value:
                value["required"] = list(value["properties"])
                value["additionalProperties"] = False
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(result)
    return result


class NativeAdapter:
    def __init__(
        self,
        settings: Settings,
        profile: ModelProfile,
        transport: httpx.AsyncBaseTransport | None = None,
        checkpoint_response: Callable[[dict], None] | None = None,
    ) -> None:
        """Bind native transport to one validated model profile and settings snapshot."""
        self.settings, self.profile, self.transport = settings, profile, transport
        self.checkpoint_response = checkpoint_response

    def permit(self, request: ModelRequest) -> None:
        """Reject expired permits or provider and model identity mismatches."""
        p = request.permit
        if (
            p.expires_at.tzinfo is None
            or p.expires_at <= datetime.now(UTC)
            or p.provider_id != self.profile.provider
            or p.model_id != self.profile.model
            or not self.profile.enabled
            or not 0 < request.timeout <= 22
            or not 0 < request.max_output_tokens <= 512
            or len(request.payload.encode()) > 100000
        ):
            raise ModelFailure("CONFIGURATION")
        policy = load_policy(self.settings)
        eligible, _ = candidates(
            policy,
            RouteRequirements(
                request.tenant,
                request.project,
                request.task_class,
                len(request.system.encode())
                + len(request.payload.encode())
                + len(json.dumps(request.schema).encode()),
                request.max_output_tokens,
                request.categories,
                request.additional_task_classes,
            ),
            self.settings,
        )
        if p.policy_hash != policy.policy_hash or not any(
            row.id == self.profile.id and row == self.profile for row in eligible
        ):
            raise ModelFailure("SPENDING_NOT_AUTHORIZED")

    def origin(self) -> str:
        """Choose a fixed cloud origin or Ollama on loopback, ollama or host.docker.internal."""
        if self.profile.provider == "ollama":
            parsed = urlparse(self.settings.ai_ollama_base_url)
            if (
                parsed.scheme != "http"
                or parsed.hostname
                not in {"localhost", "127.0.0.1", "ollama", "host.docker.internal"}
                or parsed.username
                or parsed.password
                or parsed.path not in ("", "/")
                or parsed.query
                or parsed.fragment
            ):
                raise ModelFailure("CONFIGURATION")
            return self.settings.ai_ollama_base_url.rstrip("/")
        if self.profile.provider == "gemini":
            return "https://generativelanguage.googleapis.com/v1beta"
        if self.profile.provider == "puter":
            return "https://api.puter.com"
        if self.profile.provider in CLOUD_CHAT_ORIGINS:
            return CLOUD_CHAT_ORIGINS[self.profile.provider]
        raise ModelFailure("SPENDING_NOT_AUTHORIZED")

    async def execute(self, request: ModelRequest) -> ModelResult:
        """Recheck eligibility and admission before one bounded native provider request."""
        self.permit(request)
        started = perf_counter()
        origin = self.origin()
        async with httpx.AsyncClient(
            transport=self.transport,
            timeout=request.timeout,
            follow_redirects=False,
            trust_env=False,
            limits=httpx.Limits(max_connections=1),
        ) as client:
            try:
                async with asyncio.timeout(request.timeout):
                    if self.profile.provider == "ollama":
                        if not self.settings.ai_ollama_enabled:
                            raise ModelFailure("SPENDING_NOT_AUTHORIZED")
                        tags = await self.read(client, "GET", origin + "/api/tags")
                        if not any(
                            t.get("name") == self.profile.model
                            and t.get("digest") == self.profile.installed_digest
                            for t in tags.get("models", [])
                            if isinstance(t, dict)
                        ):
                            raise ModelFailure("MODEL_NOT_INSTALLED")
                        body = dict(
                            model=self.profile.model,
                            stream=False,
                            think=False,
                            format=request.schema,
                            keep_alive=self.settings.ai_ollama_keep_alive,
                            messages=[
                                dict(role="system", content=request.system),
                                dict(role="user", content=request.payload),
                            ],
                            options=dict(
                                num_ctx=request.num_ctx,
                                num_predict=request.max_output_tokens,
                                temperature=0,
                            ),
                        )
                        data = await self.read(client, "POST", origin + "/api/chat", body)
                        return self.ollama_result(
                            request, data, int((perf_counter() - started) * 1000)
                        )
                    if self.profile.provider in CLOUD_CHAT_ORIGINS:
                        return await self.cloud_chat(client, request, origin, started)
                    if self.profile.provider == "puter":
                        return await self.puter_chat(client, request, started)
                    if (
                        not self.settings.ai_runtime_v2_enabled
                        or not self.settings.ai_cloud_enabled
                        or self.settings.ai_execution_mode != "hybrid"
                        or ai_provider.gemini_block_reason(self.settings)
                        or self.profile.model != ai_provider.GEMINI_COMPLETION_MODEL
                        or self.profile.billing_class != "verified_free"
                        or not self.profile.free_tier_confirmed
                        or not self.profile.data_policy_confirmed
                    ):
                        raise ModelFailure("SPENDING_NOT_AUTHORIZED")
                    key = os.environ.get(self.profile.credential_ref or "", "")
                    if not key or key != self.settings.ai_api_key.get_secret_value():
                        raise ModelFailure("AUTHENTICATION")
                    return await self.gemini_chat(client, request, started)
            except (httpx.ConnectError, httpx.ConnectTimeout):
                raise ModelFailure("UNAVAILABLE", "not_sent") from None
            except (httpx.TimeoutException, TimeoutError, httpx.ReadError):
                raise ModelFailure("TIMEOUT", "unknown") from None
            except (AttributeError, KeyError, TypeError, ValueError, IndexError):
                raise ModelFailure("INVALID_OUTPUT", "completed") from None

    async def gemini_chat(
        self, client: httpx.AsyncClient, request: ModelRequest, started: float
    ) -> ModelResult:
        """Send Gemini structured completion with pinned identity and bounded output."""
        key = os.environ.get(self.profile.credential_ref or "", "")
        if not key:
            raise ModelFailure("AUTHENTICATION")
        body = dict(
            systemInstruction={"parts": [{"text": request.system}]},
            contents=[{"role": "user", "parts": [{"text": request.payload}]}],
            generationConfig=dict(
                candidateCount=1,
                maxOutputTokens=request.max_output_tokens,
                thinkingConfig={"thinkingLevel": "minimal", "includeThoughts": False},
                responseMimeType="application/json",
                responseJsonSchema=strict_schema(request.schema),
            ),
        )
        data = await self.read(
            client,
            "POST",
            self.origin() + f"/models/{self.profile.model}:generateContent",
            body,
            {"x-goog-api-key": key},
        )
        return self.gemini_result(request, data, int((perf_counter() - started) * 1000))

    async def puter_chat(
        self, client: httpx.AsyncClient, request: ModelRequest, started: float
    ) -> ModelResult:
        """Call Puter's native free-allowance driver using the bound model and schema."""
        if (
            self.profile.model != "gpt-4.1-mini-2025-04-14"
            or self.profile.upstream_provider != "openai-completion"
        ):
            raise ModelFailure("CONFIGURATION")
        key = os.environ.get(self.profile.credential_ref or "", "")
        if not key:
            raise ModelFailure("AUTHENTICATION")
        # Native /drivers/call uses the account allowance. Never use the paid
        # /puterai/openai compatibility gateway or expose this token to a browser.
        body = dict(
            interface="puter-chat-completion",
            driver="ai-chat",
            method="complete",
            args=dict(
                model=self.profile.model,
                provider=self.profile.upstream_provider,
                stream=False,
                normalize=True,
                max_tokens=request.max_output_tokens,
                temperature=0,
                messages=[
                    dict(role="system", content=request.system),
                    dict(role="user", content=request.payload),
                ],
                outputFormat=dict(
                    type="json_schema",
                    name="ppm_section",
                    strict=True,
                    schema=strict_schema(request.schema),
                ),
            ),
        )
        data = await self.read(
            client,
            "POST",
            self.origin() + "/drivers/call",
            body,
            {"Authorization": "Bearer " + key},
        )
        if data.get("success") is False or data.get("error"):
            error = data.get("error", {})
            code = error.get("code") if isinstance(error, dict) else None
            raise ModelFailure(
                "QUOTA_EXHAUSTED"
                if code in ("insufficient_funds", "too_many_requests", "usage_limit_exceeded")
                else "UNAVAILABLE",
                "completed",
            )
        return self.puter_result(request, data, int((perf_counter() - started) * 1000))

    def puter_result(self, request: ModelRequest, data: dict, latency: int) -> ModelResult:
        """Normalize Puter's completion state, text and reported usage without inventing totals."""
        result = data.get("result", data)
        if not isinstance(result, dict):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        metadata = data.get("metadata") or {}
        reported = result.get("model")
        if reported is None:
            # Puter's native envelope identifies the canonical catalogue ID here,
            # rather than echoing the requested dated alias in ChatResponse.
            # Both the service and canonical ID must match the reviewed route.
            if (
                not isinstance(metadata, dict)
                or metadata.get("service_used") != "openai-completion"
                or metadata.get("providerUsed") != "gpt-4.1-mini"
            ):
                raise ModelFailure("INVALID_OUTPUT", "completed")
            reported = metadata["providerUsed"]
        elif reported != self.profile.model:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        normalized = self.chat_result(
            request,
            dict(
                model=self.profile.model,
                choices=[
                    dict(message=result.get("message"), finish_reason=result.get("finish_reason"))
                ],
                usage=result.get("usage"),
            ),
            latency,
        )
        return normalized.model_copy(update={"reported_model_id": reported})

    async def read(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        body: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        """Read bounded provider JSON and classify HTTP failures without exposing raw bodies."""
        if body is not None and len(json.dumps(body).encode()) > 110000:
            raise ModelFailure("CONTEXT_LIMIT")
        async with client.stream(method, url, json=body, headers=headers) as response:
            if response.status_code != 200:
                error_value = {}
                if response.status_code == 400 or self.checkpoint_response is not None:
                    # Operator diagnostics stay in the private calibration folder.
                    # Error bodies may contain generated text; never publish them.
                    raw_error = bytearray()
                    async for chunk in response.aiter_bytes():
                        raw_error.extend(chunk)
                        if len(raw_error) > 1000000:
                            break
                    if len(raw_error) <= 1000000:
                        try:
                            parsed_error = json.loads(raw_error)
                            if isinstance(parsed_error, dict):
                                error_value = parsed_error
                            if error_value and self.checkpoint_response is not None:
                                self.checkpoint_response(error_value)
                        except ValueError:
                            pass
                errors: dict[int, ErrorCode] = {
                    400: "CONFIGURATION",
                    401: "AUTHENTICATION",
                    402: "SPENDING_NOT_AUTHORIZED",
                    403: "AUTHENTICATION",
                    404: "MODEL_NOT_INSTALLED",
                    429: "QUOTA_EXHAUSTED",
                }
                code = errors.get(response.status_code, "UNAVAILABLE")
                detail = error_value.get("error", {})
                if (
                    response.status_code == 400
                    and self.profile.provider == "groq"
                    and isinstance(detail, dict)
                    and detail.get("code") == "json_validate_failed"
                ):
                    code = (
                        "TRUNCATED"
                        if "max completion tokens" in str(detail.get("message", "")).lower()
                        else "INVALID_OUTPUT"
                    )
                if 300 <= response.status_code < 400:
                    code = "CONFIGURATION"
                retry_after = None
                if response.status_code == 429:
                    from email.utils import parsedate_to_datetime

                    header = response.headers.get("retry-after", "60")
                    try:
                        retry_after = int(header)
                    except ValueError:
                        try:
                            retry_after = int(
                                (parsedate_to_datetime(header) - datetime.now(UTC)).total_seconds()
                            )
                        except (ValueError, TypeError, OverflowError):
                            retry_after = 60
                    retry_after = max(1, min(retry_after, 86400))
                raise ModelFailure(
                    code, "unknown" if response.status_code >= 500 else "completed", retry_after
                )
            raw = bytearray()
            async for chunk in response.aiter_bytes():
                raw.extend(chunk)
                if len(raw) > 1000000:
                    raise ModelFailure("INVALID_OUTPUT", "completed")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise ValueError
            if self.checkpoint_response is not None:
                self.checkpoint_response(value)
            return value

    async def cloud_chat(
        self, client: httpx.AsyncClient, request: ModelRequest, origin: str, started: float
    ) -> ModelResult:
        # execute()/permit() recheck qualification, key hash, free-account
        # confirmation and exact tenant/project/category egress before this point.
        """Send a pinned compatible completion using the authorized provider credential."""
        key = os.environ.get(self.profile.credential_ref or "", "")
        if not key:
            raise ModelFailure("AUTHENTICATION")
        body = dict(
            model=self.profile.model,
            stream=False,
            temperature=0,
            messages=[
                dict(role="system", content=request.system),
                dict(role="user", content=request.payload),
            ],
            response_format=dict(
                type="json_schema",
                json_schema=dict(
                    name="ppm_section", strict=True, schema=strict_schema(request.schema)
                ),
            ),
        )
        if self.profile.provider == "groq":
            body["max_completion_tokens"] = request.max_output_tokens
            body["include_reasoning"] = False
            if self.profile.model.startswith("openai/gpt-oss-"):
                body["reasoning_effort"] = "low"
            elif self.profile.model.startswith("qwen/"):
                body["reasoning_effort"] = "none"
        else:
            body["max_tokens"] = request.max_output_tokens
        if self.profile.provider == "openrouter":
            # Pin a free model and one reviewed upstream. Disable OpenRouter's
            # own retries/fallback routing and paid/data-collecting endpoints.
            await self.check_openrouter_price(client, origin)
            body["provider"] = dict(
                only=[self.profile.upstream_provider],
                allow_fallbacks=False,
                require_parameters=True,
                data_collection="deny",
                zdr=True,
                max_price=dict(prompt=0, completion=0, request=0, image=0),
            )
            body["reasoning"] = dict(enabled=False, exclude=True)
        data = await self.read(
            client, "POST", origin + "/chat/completions", body, {"Authorization": "Bearer " + key}
        )
        return self.chat_result(request, data, int((perf_counter() - started) * 1000))

    async def check_openrouter_price(self, client: httpx.AsyncClient, origin: str) -> None:
        """Require the pinned free upstream and zero prices before OpenRouter generation."""
        model = self.profile.model
        if not model.endswith(":free") or not self.profile.upstream_provider:
            raise ModelFailure("SPENDING_NOT_AUTHORIZED")
        data = await self.read(
            client, "GET", origin + "/models/" + quote(model, safe="/:") + "/endpoints"
        )
        metadata = data.get("data")
        endpoints = metadata.get("endpoints", []) if isinstance(metadata, dict) else []
        if not isinstance(endpoints, list) or not endpoints:
            raise ModelFailure("UNSUPPORTED_CAPABILITY")
        # A price-changing/unknown catalog is a denial, never a paid fallback.
        for endpoint in endpoints:
            prices = endpoint.get("pricing", {}) if isinstance(endpoint, dict) else {}
            if not isinstance(prices, dict) or not {"prompt", "completion"} <= prices.keys():
                raise ModelFailure("SPENDING_NOT_AUTHORIZED")
            try:
                if any(
                    not Decimal(str(v)).is_finite() or Decimal(str(v)) != 0 for v in prices.values()
                ):
                    raise ModelFailure("SPENDING_NOT_AUTHORIZED")
            except (InvalidOperation, TypeError, ValueError):
                raise ModelFailure("SPENDING_NOT_AUTHORIZED") from None

    def chat_result(self, request: ModelRequest, data: dict, latency: int) -> ModelResult:
        """Normalize compatible chat output and usage into the shared model result."""
        rows = data.get("choices", [])
        if (
            not isinstance(rows, list)
            or len(rows) != 1
            or not isinstance(rows[0], dict)
            or data.get("error")
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        row = rows[0]
        message = row.get("message", {})
        if not isinstance(message, dict):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if any(
            message.get(key)
            for key in (
                "tool_calls",
                "function_call",
                "reasoning",
                "reasoning_content",
                "reasoning_details",
            )
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        reason = row.get("finish_reason")
        refused = bool(message.get("refusal")) or reason == "content_filter"
        content = message.get("content")
        if not refused and not isinstance(content, str):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        reported_model = data.get("model")
        permitted_models = {self.profile.model}
        if self.profile.provider == "openrouter":
            permitted_models.add(self.profile.model.removesuffix(":free"))
        if reported_model not in permitted_models:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        usage = data.get("usage") or {}
        if not isinstance(usage, dict) or not isinstance(
            usage.get("completion_tokens_details", {}), dict
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if self.profile.provider == "openrouter":
            try:
                if "cost" not in usage or Decimal(str(usage["cost"])) != 0:
                    raise ModelFailure("SPENDING_NOT_AUTHORIZED", "completed")
            except (InvalidOperation, TypeError, ValueError):
                raise ModelFailure("INVALID_OUTPUT", "completed") from None
        completion: Literal["complete", "incomplete", "refused", "unknown"] = (
            "refused"
            if refused
            else "complete"
            if reason == "stop"
            else "incomplete"
            if reason == "length"
            else "unknown"
        )
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id=self.profile.provider,
            model_id=self.profile.model,
            completion=completion,
            text="" if refused else str(content),
            native_finish_reason=reason if reason in ("stop", "length", "content_filter") else None,
            usage=ModelUsage(
                input_tokens=usage.get("prompt_tokens"),
                output_tokens=usage.get("completion_tokens"),
                reasoning_tokens=(usage.get("completion_tokens_details") or {}).get(
                    "reasoning_tokens"
                ),
                source="reported" if usage else "unknown",
            ),
            latency_ms=latency,
        )

    def ollama_result(self, request: ModelRequest, data: dict, latency: int) -> ModelResult:
        """Normalize local completion, timing and usage with explicit truncation status."""
        message = data.get("message", {})
        if message.get("tool_calls") or message.get("thinking"):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        reason = data.get("done_reason")
        completion: Literal["complete", "incomplete", "refused", "unknown"] = (
            "complete" if data.get("done") is True and reason == "stop" else "incomplete"
        )
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="ollama",
            model_id=self.profile.model,
            completion=completion,
            text=message.get("content", ""),
            native_finish_reason=reason if reason in ("stop", "length") else None,
            usage=ModelUsage(
                input_tokens=data.get("prompt_eval_count"),
                output_tokens=data.get("eval_count"),
                source="reported",
            ),
            latency_ms=latency,
            load_ms=data["load_duration"] // 1000000
            if type(data.get("load_duration")) is int
            else None,
        )

    def gemini_result(self, request: ModelRequest, data: dict, latency: int) -> ModelResult:
        """Normalize Gemini candidates and finish reasons without accepting truncated output."""
        rows = data.get("candidates", [])
        if len(rows) != 1:
            raise ModelFailure("REFUSED", "completed")
        row, usage = rows[0], data.get("usageMetadata", {})
        parts = row.get("content", {}).get("parts", [])
        if any(
            not isinstance(p.get("text"), str)
            or p.get("thought", False)
            or set(p) - {"text", "thought", "thoughtSignature"}
            for p in parts
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        reason = row.get("finishReason")
        completion: Literal["complete", "incomplete", "refused", "unknown"] = (
            "complete"
            if reason == "STOP"
            else "incomplete"
            if reason == "MAX_TOKENS"
            else "refused"
        )
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="gemini",
            model_id=self.profile.model,
            completion=completion,
            text="".join(p["text"] for p in parts),
            native_finish_reason=reason if reason in ("STOP", "MAX_TOKENS", "SAFETY") else None,
            usage=ModelUsage(
                input_tokens=usage.get("promptTokenCount"),
                output_tokens=usage.get("candidatesTokenCount"),
                reasoning_tokens=usage.get("thoughtsTokenCount"),
                source="reported",
            ),
            latency_ms=latency,
        )
