"""Private operator helper for the isolated browser suite; never a public HTTP mailbox."""

import json
import sys

from ppm_api.config import load_settings

settings = load_settings()
if settings.app_env != "test":
    raise SystemExit("Only available in isolated test environment")
items = []
for path in (settings.storage_root / "__identity_mailbox__").glob("*.json"):
    message = json.loads(path.read_text())
    if message["to"] == sys.argv[1]:
        items.append(message)
print(json.dumps(items))
