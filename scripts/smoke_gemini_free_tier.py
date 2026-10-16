"""Explicit, bounded real Gemini smoke using synthetic bytes only; never print secrets."""

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from dotenv import dotenv_values
from ppm_api.ai_provider import GeminiProvider, ProviderError, enabled
from ppm_api.config import Settings

ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", required=True)
    parser.parse_args()
    values = dotenv_values(ROOT / "artifacts/local/ai-provider.env", interpolate=False)
    fields = {k[4:].lower(): v for k, v in values.items() if k.startswith("PPM_AI_")}
    settings = Settings(
        app_env="local",
        jwt_secret="synthetic-smoke-only-at-least-32-characters",
        database_url="postgresql+asyncpg://unused:unused@localhost/unused",
        redis_url="redis://localhost/0",
        storage_root=ROOT / "artifacts/local",
        **fields,
    )
    if settings.ai_provider != "gemini" or not enabled(settings):
        raise SystemExit("Gemini free-tier policy is not configured; no request made.")
    adapter = GeminiProvider(settings)
    evidence = [
        {
            "chunk_id": "00000000-0000-4000-8000-000000000001",
            "text": "Supplier risk is 15 days.",
        }
    ]
    report: dict = dict(
        checked_at=datetime.now(UTC).isoformat(),
        provider="gemini",
        project=settings.ai_gemini_free_tier_project,
        completion_model=settings.ai_completion_model,
        embedding_model=settings.ai_embedding_model,
        billing_verification="operator-confirmed Free Tier; no linked billing account",
        usd_authorized="0",
        input="synthetic-only",
        requests=0,
        acceptance="BLOCKED",
        checks={},
    )
    for operation in ("completion", "embedding"):
        report["requests"] += 1
        try:
            result = await asyncio.wait_for(
                adapter.complete("What is the supplier risk?", evidence)
                if operation == "completion"
                else adapter.embed([evidence[0]["text"]]),
                timeout=22 if operation == "completion" else 12,
            )
            if operation == "completion":
                output = result.value
                if (
                    output.status != "supported"
                    or len(output.excerpts) != 1
                    or str(output.excerpts[0].chunk_id) != str(UUID(evidence[0]["chunk_id"]))
                    or output.excerpts[0].quote != evidence[0]["text"]
                ):
                    raise ProviderError("OUTPUT_UNSUPPORTED")
            report["checks"][operation] = dict(
                status="PASS",
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                **({"dimensions": len(result.value[0])} if operation == "embedding" else {}),
            )
        except (ProviderError, TimeoutError) as exc:
            code = exc.code if isinstance(exc, ProviderError) else "PROVIDER_TIMEOUT"
            report["checks"][operation] = dict(
                status="BLOCKED",
                code=code,
                http_status=exc.http_status if isinstance(exc, ProviderError) else None,
            )
            break  # No retries, alternate models, paid providers, or quota upgrades.
    if len(report["checks"]) == 2 and all(v["status"] == "PASS" for v in report["checks"].values()):
        report["acceptance"] = "BOUNDED_SMOKE_PASS"
    target = ROOT / "docs/verification/gemini-free-tier-smoke.json"
    if target.exists():
        prior = json.loads(target.read_text(encoding="utf-8"))
        prior_target = target.with_name(
            "gemini-smoke-" + prior["checked_at"].replace(":", "-").replace("+", "_") + ".json"
        )
        if not prior_target.exists():
            prior_target.write_bytes(target.read_bytes())
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["acceptance"] != "BOUNDED_SMOKE_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
