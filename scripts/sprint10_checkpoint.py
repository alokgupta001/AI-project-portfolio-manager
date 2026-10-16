"""Hash the final reviewable uncommitted result, preserving all earlier checkpoints."""

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
git = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]


def output(*args):
    return subprocess.check_output([*git, *args], cwd=ROOT, stderr=subprocess.DEVNULL)


frozen = json.loads((ROOT / "artifacts/local/sprint10/files-before.json").read_text())
assert all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in frozen.items())
targets = {
    "docs/verification/sprint10-checkpoint.json",
    "docs/verification/sprint10-checkpoint.txt",
}
paths = set(output("diff", "--name-only").decode().splitlines())
paths.update(output("ls-files", "--others", "--exclude-standard").decode().splitlines())
records = {}
for relative in sorted(paths - targets):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or relative.startswith("artifacts/") or relative == ".env":
        raise SystemExit("Unexpected private/external checkpoint path")
    if path.is_file():
        records[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
runtime = json.loads((ROOT / "docs/verification/sprint10-runtime-probe.json").read_text())
assert runtime["schema_revision"] == "0012_ai_runtime" and not runtime["ai"]["enabled"]
record = dict(
    date=datetime.now(UTC).isoformat(),
    branch=output("branch", "--show-current").decode().strip(),
    base_commit=output("rev-parse", "HEAD").decode().strip(),
    committed=False,
    scope="Sprint 10 only; stop before 11",
    real_provider_acceptance="BLOCKED",
    runtime=runtime,
    preserved_frozen_files=len(frozen),
    migration_sha256=hashlib.sha256(
        (ROOT / "services/api/migrations/versions/0012_ai_runtime.py").read_bytes()
    ).hexdigest(),
    files=records,
)
(ROOT / "docs/verification/sprint10-checkpoint.json").write_text(
    json.dumps(record, indent=2) + "\n", encoding="utf-8"
)
print(
    f"PASS {len(records)} reviewable source/evidence hashes; "
    f"{len(frozen)} frozen inputs unchanged; uncommitted"
)
