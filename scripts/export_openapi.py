import argparse
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "services/api"))
from ppm_api.main import create_app  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
target = root / "packages/contracts/openapi.json"
content = json.dumps(create_app().openapi(), sort_keys=True, indent=2) + "\n"
if args.check:
    if not target.exists() or target.read_text(encoding="utf-8") != content:
        raise SystemExit("OpenAPI drift. Run npm run contracts:generate and review the result.")
else:
    target.write_text(content, encoding="utf-8", newline="\n")
