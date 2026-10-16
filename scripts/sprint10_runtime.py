"""Read-only normal-stack probe with public-safe results; no sessions or provider calls."""

import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.status, json.loads(response.read())


_, foundation = get("http://127.0.0.1:8000/api/v1/foundation")
ready, health = get("http://127.0.0.1:8000/api/v1/health/ready")
with urllib.request.urlopen("http://localhost:3000/ai", timeout=10) as response:
    web = response.status
config = json.loads(
    subprocess.check_output(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "api",
            "python",
            "-c",
            "import json; from ppm_api.config import load_settings; "
            "from ppm_api.ai_provider import enabled; s=load_settings(); "
            "print(json.dumps(dict(provider=s.ai_provider,enabled=enabled(s),"
            "real_calls_authorized=s.ai_real_calls_authorized,spend_limit_usd=str(s.ai_spend_limit_usd))))",
        ],
        cwd=ROOT,
        text=True,
    )
)
assert foundation["schema_revision"] == "0012_ai_runtime"
assert ready == web == 200 and health["status"] == "ready"
assert not config["enabled"] and not config["real_calls_authorized"]
record = dict(
    schema_revision=foundation["schema_revision"],
    api_ready=ready,
    web_ai=web,
    dependencies=health["dependencies"],
    ai=config,
    real_provider_acceptance="BLOCKED",
    hosted_ci="unverified",
    scope="Sprint 10 only; stop before 11",
)
(ROOT / "docs/verification/sprint10-runtime-probe.json").write_text(
    json.dumps(record, indent=2) + "\n", encoding="utf-8"
)
print("PASS normal 0012 API readiness/web AI route; real provider disabled with zero ceiling")
