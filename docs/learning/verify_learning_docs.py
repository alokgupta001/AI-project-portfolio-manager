"""Verify the simple AI-PPM guide without starting services or changing application files."""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CHAPTERS = [
    "00-start-here.md", "01-project-overview.md", "02-how-the-application-works.md",
    "03-frontend-explained.md", "04-backend-explained.md", "05-database-explained.md",
    "06-login-and-permissions.md", "07-main-features-explained.md",
    "08-assessments-and-dashboards.md", "09-ai-features-explained.md",
    "10-sprint-history.md", "11-how-to-read-and-change-the-code.md",
    "12-interview-preparation.md", "13-current-status-and-limitations.md",
]
files = [DOCS / name for name in CHAPTERS]
files += list(DOCS.glob("[0-3][0-9]-*.md"))
files += [DOCS / name for name in ["AI-PPM-MASTER-LEARNING-GUIDE.md", "DATABASE-DICTIONARY.md",
    "CODE-AND-TEST-INDEX.md", "18-api-contracts.md", "LEARNING-DOCUMENTATION-VERIFICATION.md"]]
files += [ROOT / "README.md"]
files = sorted(set(files))
errors = []
links = 0
for path in files:
    if not path.is_file():
        errors.append(f"Missing document: {path.name}")
        continue
    content = path.read_text(encoding="utf-8-sig")
    if len(re.findall(r"^```", content, re.M)) % 2:
        errors.append(f"Unbalanced code fence: {path.name}")
    for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", content):
        if re.match(r"^[a-zA-Z]+://", target) or target.startswith("#"):
            continue
        target = unquote(target.split("#")[0]).strip("<>")
        if target and not (path.parent / target).exists():
            errors.append(f"Broken local link: {path.name} -> {target}")
        links += 1
    if path.name in CHAPTERS:
        for target in re.findall(r"`((?:apps|services|packages|scripts|tests|infra|docs)/[^`]+)`", content):
            target = target.split(":", 1)[0]
            if "*" in target or "..." in target or target.endswith("/"):
                continue
            if not (ROOT / target).exists():
                errors.append(f"Missing referenced source path: {path.name} -> {target}")
        if "ef196c9" in content and path.name != "10-sprint-history.md":
            errors.append(f"Stale primary snapshot: {path.name}")

expected = {
    "delivery.py": ["create", "write", "get", "view", "lock", "authorize", "refs", "cycle_check", "audit_change", "can_edit"],
    "identity.py": ["principal", "login", "refresh", "context", "limited"],
    "assessment.py": ["compute_scores", "save_answers", "submit", "review", "publish_framework", "release_evidence"],
    "capacity.py": ["calculate", "summary", "sources_for", "resource_summary", "team_summary"],
    "command.py": ["snapshot", "combined", "workdays"],
    "ppm_schemas.py": ["ProjectInput", "RecordView"],
}
for filename, names in expected.items():
    tree = ast.parse((ROOT / "services/api/ppm_api" / filename).read_text(encoding="utf-8-sig"))
    symbols = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    errors += [f"Missing source symbol: {filename}:{name}" for name in names if name not in symbols]
identity = (ROOT / "services/api/ppm_api/identity.py").read_text(encoding="utf-8")
if 'Depends(principal, scope="function")' not in identity:
    errors.append("Transaction-boundary explanation differs from Auth definition")
frontend = (ROOT / "apps/web/components/delivery.tsx").read_text(encoding="utf-8")
for symbol in ["RecordEditor", "async function save", "onSaved();", "onClose();"]:
    if symbol not in frontend:
        errors.append(f"Missing frontend flow symbol: {symbol}")
interview = (DOCS / "12-interview-preparation.md").read_text(encoding="utf-8")
questions = len(re.findall(r"^\d+\. \*\*", interview, re.M))
if not 25 <= questions <= 40:
    errors.append(f"Expected 25-40 interview questions, found {questions}")

sys.path.insert(0, str(ROOT / "services/api"))
from ppm_api.main import create_app
from ppm_api.database import Base
spec = create_app().openapi()  # App lifespan is not entered; no DB/Redis connection.
committed = json.loads((ROOT / "packages/contracts/openapi.json").read_text(encoding="utf-8"))
if spec != committed:
    errors.append("Current OpenAPI differs from committed contract")
for endpoint in ["/api/v1/delivery/{kind}", "/api/v1/auth/login",
    "/api/v1/assessment/assessments/{assessment_id}/answers", "/api/v1/command/snapshot",
    "/api/v1/capacity/resources/{rid}"]:
    if endpoint not in spec["paths"]:
        errors.append(f"Missing documented route: {endpoint}")
dictionary = (DOCS / "DATABASE-DICTIONARY.md").read_text(encoding="utf-8")
for table in Base.metadata.tables:
    if f"## {table}\n" not in dictionary:
        errors.append(f"Table missing from dictionary: {table}")
migrations = list((ROOT / "services/api/migrations/versions").glob("*.py"))
if len(migrations) != 6 or not any(p.stem == "0006_command_center" for p in migrations):
    errors.append("Migration chain differs from documented six-file chain")
git = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]
changed = subprocess.check_output(git + ["diff", "--name-only", "HEAD"], cwd=ROOT, text=True).splitlines()
for name in changed:
    if name != "README.md" and not name.startswith("docs/"):
        errors.append(f"Tracked non-documentation change: {name}")
preserved = subprocess.run([sys.executable, "-B", "scripts/check_sources.py"], cwd=ROOT,
                           text=True, capture_output=True)
if preserved.returncode:
    errors.append("Preserved source/prompt hashes failed")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
operations = sum(method in {"get", "post", "put", "patch", "delete"}
                 for routes in spec["paths"].values() for method in routes)
print(f"PASS: 14 primary chapters, {questions} interview questions; {links} local links across {len(files)} documents.")
print(f"PASS: fences, source paths, key backend/frontend symbols, function-scope transaction boundary.")
print(f"PASS: current OpenAPI matches committed contract ({operations} operations); dictionary covers {len(Base.metadata.tables)} tables; six migrations.")
print("PASS: tracked changes are documentation only; " + preserved.stdout.strip())
print("No application lifespan, runtime tests, service restart or database mutation performed.")
