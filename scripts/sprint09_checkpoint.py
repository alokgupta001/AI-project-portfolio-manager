"""Record a reviewable local file checkpoint, never a hosted CI/commit claim."""

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

root = Path(__file__).resolve().parents[1]
git = ["git", "-c", f"safe.directory={root.as_posix()}"]


def output(*args: str) -> bytes:
    return subprocess.check_output([*git, *args], cwd=root, stderr=subprocess.DEVNULL)


# Next's generated declaration was changed by our build only; preserve its original bytes.
generated = root / "apps/web/next-env.d.ts"
original = output("show", "HEAD:apps/web/next-env.d.ts")
if (
    generated.read_bytes().replace(b"\r\n", b"\n").strip()
    == original.replace(b"\r\n", b"\n").strip()
):
    generated.write_bytes(original)

paths = set(output("diff", "--name-only").decode().splitlines())
paths.update(output("ls-files", "--others", "--exclude-standard").decode().splitlines())
target = "docs/verification/sprint09-checkpoint.json"
records = {}
for relative in sorted(paths - {target, "docs/verification/sprint09-checkpoint.txt"}):
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or relative.startswith("artifacts/") or relative == ".env":
        raise SystemExit("Unexpected private/external checkpoint path")
    if path.is_file():
        records[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
frozen = json.loads((root / "artifacts/local/sprint09/migrations-before.json").read_text())
assert all(hashlib.sha256((root / p).read_bytes()).hexdigest() == h for p, h in frozen.items())
runtime = json.loads((root / "docs/verification/sprint09-runtime-probe.json").read_text())
assert runtime["schema_revision"] == "0011_document_sources"
record = dict(
    date=datetime.now(UTC).isoformat(),
    branch=output("branch", "--show-current").decode().strip(),
    base_commit=output("rev-parse", "HEAD").decode().strip(),
    committed=False,
    hosted_ci="unverified",
    scope="Sprint 09 only; stop before 10",
    runtime=runtime,
    frozen_prior_migrations=len(frozen),
    migration_sha256=hashlib.sha256(
        (root / "services/api/migrations/versions/0011_document_sources.py").read_bytes()
    ).hexdigest(),
    files=records,
)
(root / target).write_text(json.dumps(record, indent=2) + "\n")
print(
    f"PASS {len(records)} changed source/evidence hashes; "
    f"{len(frozen)} prior migrations unchanged; local uncommitted checkpoint"
)
