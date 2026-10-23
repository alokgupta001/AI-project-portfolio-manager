"""Inspect privately entered keys; optional authenticated GETs never request inference."""

import argparse
import asyncio
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import httpx

PROVIDERS = {
    "groq": ("PPM_AI_GROQ_API_KEY", "https://api.groq.com/openai/v1/models"),
    "openrouter": ("PPM_AI_OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/key"),
    "mistral": ("PPM_AI_MISTRAL_API_KEY", "https://api.mistral.ai/v1/models"),
    "puter": ("PPM_AI_PUTER_API_KEY", "https://api.puter.com/whoami"),
    "deepinfra": ("PPM_AI_DEEPINFRA_API_KEY", "https://api.deepinfra.com/payment/checklist"),
}
PRIVATE = Path(__file__).resolve().parents[1] / "artifacts/local"


def read_keys(path: Path) -> dict[str, str]:
    """Read known private credential fields, rejecting duplicates and malformed values."""
    if not path.resolve().is_relative_to(PRIVATE.resolve()):
        raise ValueError("Private path required")
    if path.stat().st_size > 64000:
        raise ValueError("Private file too large")
    keys: dict[str, str] = {}
    expected = {row[0] for row in PROVIDERS.values()}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        name, separator, value = line.partition("=")
        if not separator or name.strip() not in expected:
            continue  # The same env file may contain other v2 settings.
        name, value = name.strip(), value.strip()
        if name in keys:
            raise ValueError("Duplicate private key field")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if value and (len(value) > 1024 or any(c.isspace() for c in value)):
            raise ValueError("Invalid private key value")
        keys[name] = value
    return keys


async def inspect(
    keys: dict[str, str],
    confirmed: set[str],
    verify: bool,
    transport: httpx.AsyncBaseTransport | None = None,
) -> tuple[dict, dict]:
    """Inspect fixed provider metadata endpoints; return sanitized status and bindings."""
    public: dict = {"schema_version": "provider-setup-v1", "inference_requests": 0, "providers": {}}
    bindings: dict = {"confirmed_at": datetime.now(UTC).isoformat(), "providers": {}}
    async with httpx.AsyncClient(
        transport=transport, timeout=10, follow_redirects=False, trust_env=False
    ) as client:
        for provider, (variable, url) in PROVIDERS.items():
            key = keys.get(variable, "")
            row = dict(
                key_present=bool(key),
                free_tier_confirmed=provider in confirmed,
                authentication="not_checked",
            )
            if provider == "puter":
                row["blocked_reason"] = "FREE_API_CAPABILITY_UNVERIFIED"
            if provider == "deepinfra":
                row["free_tier_confirmed"] = False
                row["blocked_reason"] = "BILLING_UNVERIFIED"
            public["providers"][provider] = row
            if key and (provider in confirmed or provider == "deepinfra"):
                bindings["providers"][provider] = dict(
                    credential_ref=variable,
                    credential_sha256=hashlib.sha256(key.encode()).hexdigest(),
                    free_tier_confirmed=row["free_tier_confirmed"],
                )
            if not key or not verify or (provider not in confirmed and provider != "deepinfra"):
                continue
            try:
                # Fixed origin, GET only, no retries/redirects, response body never logged.
                async with client.stream(
                    "GET", url, headers={"Authorization": "Bearer " + key}
                ) as response:
                    if response.status_code != 200:
                        row["authentication"] = (
                            "rejected" if response.status_code in (401, 403) else "unavailable"
                        )
                        continue
                    raw = bytearray()
                    async for chunk in response.aiter_bytes():
                        raw.extend(chunk)
                        if len(raw) > 1000000:
                            raise ValueError
                    data = json.loads(raw)
                    if provider == "deepinfra":
                        if (
                            not isinstance(data, dict)
                            or not {"stripe_balance", "suspended", "payment_method", "topup"}
                            <= data.keys()
                        ):
                            raise ValueError
                        row["authentication"] = "read_only_verified"
                        for source, target in (
                            ("payment_method", "payment_method_present"),
                            ("topup", "automatic_topup_enabled"),
                            ("suspended", "inference_suspended"),
                        ):
                            row[target] = data[source] if type(data[source]) is bool else None
                        reasons = {
                            "balance",
                            "payment-method",
                            "overdue-invoices",
                            "limit-reached",
                            "admin",
                            "bad-cc",
                            "missing-address",
                            None,
                        }
                        row["suspend_reason"] = (
                            data.get("suspend_reason")
                            if data.get("suspend_reason") in reasons
                            else "unknown"
                        )
                        scoped = data.get("scoped_credits", [])
                        row["scoped_credit_available"] = (
                            any(
                                isinstance(c, dict)
                                and c.get("expired") is False
                                and type(c.get("remaining_cents")) in (int, float)
                                and c["remaining_cents"] > 0
                                for c in scoped
                            )
                            if isinstance(scoped, list)
                            else None
                        )
                        row["blocked_reason"] = "NO_VERIFIED_FREE_INFERENCE"
                        # Financial/identity/card details never enter public diagnostics.
                        continue
                    if provider == "puter":
                        if not isinstance(data, dict) or not isinstance(data.get("uuid"), str):
                            raise ValueError
                        row["authentication"] = "read_only_verified"
                        continue  # Never print account identity or use the paid-compatible API.
                    expected_type = dict if provider == "openrouter" else list
                    if not isinstance(data, dict) or not isinstance(
                        data.get("data"), expected_type
                    ):
                        raise ValueError
                    row["authentication"] = "read_only_verified"
                    if provider == "openrouter":
                        # Do not print key label, account usage, balance or raw metadata.
                        if data["data"].get("is_free_tier") is not True:
                            row["authentication"] = "account_review_required"
                    else:
                        models = sorted(
                            m["id"]
                            for m in data["data"]
                            if isinstance(m, dict)
                            and isinstance(m.get("id"), str)
                            and len(m["id"]) < 160
                            and "latest" not in m["id"].lower()
                        )
                        row["dated_or_pinned_model_count"] = len(models)
                        bindings["providers"][provider]["available_models"] = models
            except (httpx.HTTPError, ValueError, TypeError, KeyError, AttributeError):
                row["authentication"] = "unavailable"
    return public, bindings


def main() -> None:
    """Check private setup and optionally record bindings, without inference requests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=PRIVATE / "ai-v2.env")
    parser.add_argument("--verify", action="store_true", help="Authenticated metadata GETs only")
    parser.add_argument("--confirmed-free-tier", nargs="*", choices=list(PROVIDERS), default=[])
    parser.add_argument(
        "--record-bindings",
        action="store_true",
        help="Save key hashes/confirmation privately; never enable profiles",
    )
    args = parser.parse_args()
    try:
        keys = read_keys(args.env_file)
        public, bindings = asyncio.run(inspect(keys, set(args.confirmed_free_tier), args.verify))
        if args.record_bindings:
            target = PRIVATE / "ai-v2/provider-bindings.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            # Rebinding is explicit. Neither credentials nor existing Gemini settings change.
            target.write_text(json.dumps(bindings, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(public, indent=2))
    except Exception:
        raise SystemExit(
            "BLOCKED private provider setup could not be checked; no values disclosed"
        ) from None


if __name__ == "__main__":
    main()
