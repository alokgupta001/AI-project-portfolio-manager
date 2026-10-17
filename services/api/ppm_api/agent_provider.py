"""Domain schema over the existing fixed-origin transports and unchanged model allowlist."""

import asyncio

from ppm_api import ai_provider as P
from ppm_api.agent_engine import SYSTEM_PROMPT
from ppm_api.agent_schemas import AgentBatch
from ppm_api.config import Settings


class AgentProvider:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.name: str = settings.ai_provider if P.enabled(settings) else "disabled"

    async def embed(self, texts: list[str]) -> P.ProviderResult:
        raise P.ProviderError("EMBEDDINGS_DISABLED")

    async def complete(self, query: str, evidence: list[dict]) -> P.ProviderResult:
        if not P.enabled(self.settings):
            raise P.ProviderError("PROVIDER_DISABLED")
        if self.settings.ai_provider == "gemini":
            data = await asyncio.to_thread(
                P.GeminiProvider(self.settings).post,
                f"models/{P.GEMINI_COMPLETION_MODEL}:generateContent",
                {
                    "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                    "contents": [{"role": "user", "parts": [{"text": query}]}],
                    "generationConfig": {
                        "candidateCount": 1,
                        "maxOutputTokens": 512,
                        "thinkingConfig": {"thinkingLevel": "minimal", "includeThoughts": False},
                        "responseMimeType": "application/json",
                        "responseJsonSchema": AgentBatch.model_json_schema(),
                    },
                },
            )
            try:
                candidates = data["candidates"]
                if len(candidates) != 1 or candidates[0].get("finishReason") != "STOP":
                    raise ValueError
                parts = candidates[0]["content"]["parts"]
                if not parts or any(
                    not isinstance(p.get("text"), str)
                    or p.get("thought", False)
                    or set(p) - {"text", "thoughtSignature", "thought"}
                    for p in parts
                ):
                    raise ValueError
                value = AgentBatch.model_validate_json("".join(p["text"] for p in parts))
                usage = data.get("usageMetadata", {})
                output = usage.get("candidatesTokenCount")
                thoughts = usage.get("thoughtsTokenCount", 0)
                if type(thoughts) is not int or thoughts < 0:
                    raise ValueError
                return P.ProviderResult(
                    value,
                    usage.get("promptTokenCount"),
                    output + thoughts if output is not None else None,
                )
            except Exception:
                raise P.ProviderError("PROVIDER_MALFORMED") from None
        data = await asyncio.to_thread(
            P.OpenAIProvider(self.settings).post,
            "chat/completions",
            {
                "model": self.settings.ai_completion_model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query},
                ],
                "max_completion_tokens": 512,
                "response_format": {"type": "json_object"},
                "store": False,
            },
        )
        try:
            value = AgentBatch.model_validate_json(data["choices"][0]["message"]["content"])
            usage = data.get("usage", {})
            return P.ProviderResult(
                value, usage.get("prompt_tokens"), usage.get("completion_tokens")
            )
        except Exception:
            raise P.ProviderError("PROVIDER_MALFORMED") from None
