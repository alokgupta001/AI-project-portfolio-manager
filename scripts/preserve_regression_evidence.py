"""Keep fresh Sprint 09 regression renders without overwriting earlier committed evidence."""

import re
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
git = ["git", "-c", f"safe.directory={root.as_posix()}"]
changed = subprocess.check_output(
    [*git, "diff", "--name-only", "--", "docs/verification"], cwd=root, text=True
).splitlines()
count = 0
for relative in changed:
    name = Path(relative).name
    if not re.fullmatch(r"(?:sprint-0[678]-.+\.(?:png|json)|sprint81-.+\.png)", name):
        continue
    source = (root / relative).resolve()
    if not source.is_relative_to(root / "docs/verification"):
        raise SystemExit("Unexpected evidence path")
    target = source.with_name("sprint09-regression-" + name)
    if target.exists():
        raise SystemExit("Refusing to overwrite saved regression evidence")
    shutil.copy2(source, target)
    source.write_bytes(subprocess.check_output([*git, "show", f"HEAD:{relative}"], cwd=root))
    count += 1
print(
    f"PASS {count} fresh regression artifacts saved with Sprint 09 prefix; prior evidence restored"
)
