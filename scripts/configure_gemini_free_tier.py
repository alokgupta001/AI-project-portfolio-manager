"""Record an operator's no-billing confirmation without printing or accepting a key in argv."""

import argparse
import hashlib
import re
from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values, set_key

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--confirm-no-billing", action="store_true", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]{4,61}[a-z0-9]|[0-9]{6,30}", args.project):
        raise SystemExit("Provide the key's Google project ID or number, not the API key.")
    target = ROOT / "artifacts/local/ai-provider.env"
    values = dotenv_values(target, interpolate=False)
    key = values.get("PPM_AI_API_KEY", "") or ""
    if len(key) < 20 or key.upper().startswith(("PASTE", "REPLACE", "YOUR_")):
        raise SystemExit("Save a key privately in artifacts/local/ai-provider.env first.")
    now = datetime.now(UTC)
    backup = target.with_name("ai-provider.before-" + now.strftime("%Y%m%dT%H%M%S%fZ") + ".env")
    backup.write_bytes(target.read_bytes())
    for name, value in {
        "PPM_AI_PROVIDER": "gemini",
        "PPM_AI_REAL_CALLS_AUTHORIZED": "true",
        "PPM_AI_SPEND_LIMIT_USD": "0",
        "PPM_AI_INPUT_USD_PER_MILLION": "0",
        "PPM_AI_OUTPUT_USD_PER_MILLION": "0",
        "PPM_AI_EMBEDDING_USD_PER_MILLION": "0",
        "PPM_AI_COMPLETION_MODEL": "gemini-3.5-flash-lite",
        "PPM_AI_EMBEDDING_MODEL": "gemini-embedding-2",
        "PPM_AI_GEMINI_FREE_TIER_PROJECT": args.project,
        "PPM_AI_GEMINI_FREE_TIER_CONFIRMED_AT": now.isoformat(),
        "PPM_AI_GEMINI_FREE_TIER_KEY_SHA256": hashlib.sha256(key.encode()).hexdigest(),
        "PPM_AI_GEMINI_DAILY_CALL_LIMIT": "20",
    }.items():
        set_key(str(target), name, value, quote_mode="always")
    print("Recorded operator-confirmed no-billing project; $0 cap; no daily renewal required.")
    print("No provider request was made. Existing containers require recreation to load settings.")


if __name__ == "__main__":
    main()
