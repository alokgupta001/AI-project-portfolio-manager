import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "docs/source/source-manifest.json").read_text(encoding="utf-8-sig"))
for entry in manifest["files"]:
    digest = hashlib.sha256((root / entry["copy"]).read_bytes()).hexdigest()
    if digest.upper() != entry["sha256"].upper():
        raise SystemExit(f"Source changed: {entry['copy']}")
print(f"PASS: {len(manifest['files'])} preserved sources/prompts match SHA256 manifest")
