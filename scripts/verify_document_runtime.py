"""Fail image builds if apt has silently changed the verified parser/OCR packages."""

import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = (root / "infra/document-packages.lock").read_text().splitlines()
actual = subprocess.check_output(
    ["dpkg-query", "-W", "-f=${Package}=${Version}\n", *[line.split("=")[0] for line in expected]],
    text=True,
).splitlines()
if sorted(actual) != sorted(expected):
    raise SystemExit("Parser runtime differs from document-packages.lock; review and reverify")
print("PASS exact parser/OCR package versions match document-packages.lock")
