"""Prepare disabled, key-bound cloud candidates. No inference, rollout or qualification."""

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.ai_provider import gemini_block_reason  # noqa: E402
from ppm_api.config import Settings  # noqa: E402
from ppm_api.model_registry import ModelPolicy  # noqa: E402

from scripts.benchmark_agent_runtime import CORPUS, write_new  # noqa: E402
from scripts.check_provider_setup import PRIVATE, read_keys  # noqa: E402


def gemini_settings() -> Settings:
    """Load the private Gemini configuration needed to bind synthetic calibration."""
    return Settings(
        _env_file=PRIVATE / "ai-provider.env",
        app_env="test",
        storage_root=PRIVATE / "ai-v2/synthetic-only",
        database_url="postgresql+asyncpg://unused:unused@127.0.0.1:9/ppm_test",
        redis_url="redis://127.0.0.1:9/1",
        jwt_secret="synthetic-cloud-benchmark-no-authority",
    )


def prepare() -> dict:
    """Prepare disabled assigned profiles and bounded synthetic calibration authorizations."""
    keys = read_keys(PRIVATE / "ai-v2.env")
    settings = gemini_settings()
    if gemini_block_reason(settings):
        raise ValueError("Existing Gemini authorization is not usable")
    keys["PPM_AI_API_KEY"] = settings.ai_api_key.get_secret_value()
    folder = PRIVATE / "ai-v2"
    bindings = json.loads((folder / "provider-bindings.json").read_bytes())["providers"]
    candidates = ModelPolicy.model_validate_json(
        (ROOT / "config/model-policy.cloud.example.json").read_bytes()
    )
    old_path = folder / "policy.json"
    old = ModelPolicy.model_validate_json(old_path.read_bytes())
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    corpus_hash = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    for profile in candidates.profiles:
        key_hash = hashlib.sha256(keys[profile.credential_ref].encode()).hexdigest()
        if profile.provider != "gemini" and (
            bindings[profile.provider].get("credential_sha256") != key_hash
            or not bindings[profile.provider].get("free_tier_confirmed")
        ):
            raise ValueError("Preserved free-account binding changed")
        profile.credential_sha256 = key_hash
        profile.free_tier_confirmed = True
        # Only synthetic benchmark egress is authorized here. No tenant scope granted.
        profile.data_policy_confirmed = False
        existing = next((p for p in old.profiles if p.id == profile.id), None)
        if existing:
            if existing.enabled or existing.qualified_task_classes:
                raise ValueError("Refusing to replace an active/qualified profile")
            profile.quota_scope = existing.quota_scope
        auth_path = folder / (profile.provider + "-specialist-authorization.json")
        record = dict(
            schema_version="cloud-calibration-authorization-v1",
            provider=profile.provider,
            model=profile.model,
            account_scope=profile.quota_scope,
            key_sha256=key_hash,
            corpus_sha256=corpus_hash,
            synthetic_only=True,
            calibration_only=True,
            free_tier_confirmed=True,
            max_spend_usd="0",
            max_calls=9,
            authorized_at=datetime.now(UTC).isoformat(),
            basis="User requested the three cloud providers across nine roles; no paid training.",
        )
        if auth_path.exists():
            prior = json.loads(auth_path.read_bytes())
            # Do not silently renew or reset a previous bounded authorization.
            if any(prior.get(k) != record[k] for k in record if k not in ("authorized_at",)):
                raise ValueError("Existing benchmark authorization differs")
        else:
            write_new(auth_path, record)
    merged = ModelPolicy(
        profiles=[p for p in old.profiles if p.id not in {c.id for c in candidates.profiles}]
        + candidates.profiles
    )
    write_new(
        folder / ("policy-before-cloud-" + timestamp + ".json"), json.loads(old_path.read_bytes())
    )
    old_path.write_text(merged.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return dict(
        profiles=len(merged.profiles),
        cloud_candidates=len(candidates.profiles),
        roles=9,
        all_candidates_disabled=all(not p.enabled for p in merged.profiles),
        tenant_scopes_granted=0,
        model_requests=0,
    )


if __name__ == "__main__":
    try:
        print(json.dumps(prepare()))
    except Exception:
        raise SystemExit("BLOCKED cloud preparation; private details withheld") from None
