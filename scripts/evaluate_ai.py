"""Run offline evidence-gate fixtures; no database, credentials or provider access."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services/api"))
from ppm_api.ai_evaluation import run_evaluation  # noqa: E402

result = run_evaluation()
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["eligible"] else 1)
