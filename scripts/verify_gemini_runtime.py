"""Read-only local runtime probe; no credentials, sessions or provider requests emitted."""

import json
import subprocess
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as response:
        assert response.status == 200
        return json.loads(response.read())


def main() -> None:
    config_script = (
        "import json; from datetime import UTC, datetime, timedelta; "
        "from ppm_api.config import load_settings; from ppm_api.ai_provider import enabled; "
        "from ppm_api.ai import provider_status; s=load_settings(); "
        "old=s.model_copy(update={'ai_gemini_free_tier_confirmed_at':"
        "datetime.now(UTC)-timedelta(days=3650)}); "
        "print(json.dumps(dict(status=provider_status(s),"
        "spend_limit_usd=str(s.ai_spend_limit_usd),"
        "daily_call_limit=s.ai_gemini_daily_call_limit,"
        "confirmation_expires_hours=None,old_confirmation_enabled=enabled(old))))"
    )
    configs = {}
    for service in ("api", "worker", "dispatcher"):
        configs[service] = json.loads(
            subprocess.check_output(
                ["docker", "compose", "exec", "-T", service, "python", "-c", config_script],
                cwd=ROOT,
                text=True,
            )
        )
        assert configs[service]["status"]["provider"] == "gemini"
        assert configs[service]["status"]["enabled"]
        assert configs[service]["spend_limit_usd"] == "0"
        assert configs[service]["old_confirmation_enabled"]
    assert configs["api"] == configs["worker"] == configs["dispatcher"]
    ready = get("http://127.0.0.1:8000/api/v1/health/ready")
    assert ready["status"] == "ready"
    foundation = get("http://127.0.0.1:8000/api/v1/foundation")
    assert foundation["schema_revision"] == "0012_ai_runtime"
    with urllib.request.urlopen("http://localhost:3000/ai", timeout=10) as response:
        web_status = response.status
    assert web_status == 200
    result = dict(
        checked_at=datetime.now(UTC).isoformat(),
        services=configs,
        readiness=ready,
        schema_revision=foundation["schema_revision"],
        web_ai_http=web_status,
        provider_requests=0,
    )
    (ROOT / "docs/verification/gemini-runtime.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS: Gemini $0 and old confirmations enabled on API/worker/dispatcher; API/web ready.")


if __name__ == "__main__":
    main()
