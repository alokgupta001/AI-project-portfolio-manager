"""Record installed Python dependency versions and declared licenses without credentials."""

import importlib.metadata
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
records = []
for package in importlib.metadata.distributions():
    meta = package.metadata
    license_value = meta.get("License-Expression") or meta.get("License") or "Not declared"
    records.append(
        {
            "name": meta["Name"],
            "version": package.version,
            "declared_license": license_value,
            "license_classifiers": [
                c for c in meta.get_all("Classifier", []) if c.startswith("License")
            ],
        }
    )
target = root / "docs/verification/python-dependencies.json"
target.write_text(
    json.dumps(sorted(records, key=lambda p: p["name"].lower()), indent=2) + "\n", encoding="utf-8"
)
print(f"Recorded {len(records)} installed Python packages and their declared license metadata")
