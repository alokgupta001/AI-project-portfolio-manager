"""Save fresh regression renders and restore earlier evidence from its exact baseline."""

import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
git = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]
folder = ROOT / "artifacts/local/sprint10"
initial = (folder / "git-before.txt").read_text(encoding="utf-8").splitlines()
modified = {line[3:] for line in initial if not line.startswith("??")}
changed = subprocess.check_output(
    [*git, "diff", "--name-only", "--", "docs/verification"], cwd=ROOT, text=True
).splitlines()
baselines = {}
pattern = re.compile(
    r"(?:sprint-0[678]-.+\.(?:png|json)|sprint81-.+\.png|sprint09-documents-.+\.png)"
)
for relative in changed:
    if pattern.fullmatch(Path(relative).name):
        if relative in modified:
            raise SystemExit("Prior tracked evidence had local changes; do not restore from HEAD")
        baselines[relative] = subprocess.check_output([*git, "show", f"HEAD:{relative}"], cwd=ROOT)
with zipfile.ZipFile(folder / "untracked-before.zip") as archive:
    for relative in archive.namelist():
        if relative.startswith("docs/verification/") and pattern.fullmatch(Path(relative).name):
            baselines[relative] = archive.read(relative)
count = 0
for relative, original in baselines.items():
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT / "docs/verification"):
        raise SystemExit("Unexpected external evidence path")
    if path.read_bytes() != original:
        target = path.with_name("sprint10-regression-" + path.name)
        if target.exists():
            raise SystemExit("Refusing to overwrite current regression evidence")
        target.write_bytes(path.read_bytes())
        path.write_bytes(original)
        count += 1
print(f"PASS {count} new regression renders saved; earlier tracked/uncommitted evidence restored")
