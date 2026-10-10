"""Operator-only mailbox reader. Output contains single-use account credentials."""

import argparse
import json

from ppm_api.config import load_settings

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--email", required=True)
parser.add_argument("--kind", choices=["register", "activate", "invite", "reset"])
args = parser.parse_args()
folder = load_settings().storage_root / "__identity_mailbox__"
for path in sorted(folder.glob("*.json"), key=lambda p: p.stat().st_mtime):
    message = json.loads(path.read_text(encoding="utf-8"))
    if message["to"] == args.email.lower() and (not args.kind or message["kind"] == args.kind):
        print(json.dumps(message, indent=2))
