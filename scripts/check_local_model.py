"""Record current Windows host and Ollama readiness without requesting inference."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services/api"))

from ppm_api.local_model_readiness import readiness  # noqa: E402


def main() -> None:
    """Report read-only host and Ollama readiness without loading a model."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--reservation-mb", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = readiness(args.model, args.base_url, args.reservation_mb)
        encoded = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(encoded)
        print(encoded, end="")
    except Exception:
        raise SystemExit("BLOCKED local readiness could not be measured") from None
    if result["blocked"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
