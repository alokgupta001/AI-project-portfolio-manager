"""Record exact local acceptance return codes; fail without masking an earlier gate."""

import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
evidence = root / "docs/verification"
python = str(root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
npm = "npm.cmd" if os.name == "nt" else "npm"
commands = {
    "ruff": [python, "-m", "ruff", "check", "services", "scripts", "tests"],
    "python-format": [python, "-m", "ruff", "format", "--check", "services", "scripts", "tests"],
    "mypy": [python, "-m", "mypy", "services/api/ppm_api", "services/worker/ppm_worker"],
    "contracts": [npm, "run", "contracts:check"],
    "types": [npm, "run", "typecheck"],
    "lint": [npm, "run", "lint"],
    "format": [npm, "run", "format:check"],
    "sources": [python, "scripts/check_sources.py"],
}
results = {}
for name, command in commands.items():
    with (evidence / f"sprint81-{name}.txt").open("w", encoding="utf-8") as log:
        log.write("Command: " + " ".join(command) + "\n")
        log.flush()
        result = subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT)
        log.write(f"\nExit: {result.returncode}\n")
    results[name] = dict(command=command, exit_code=result.returncode)
    print(f"{name}: exit {result.returncode}", flush=True)
    (evidence / "sprint81-static-results.json").write_text(json.dumps(results, indent=2))
    if result.returncode:
        sys.exit(result.returncode)
