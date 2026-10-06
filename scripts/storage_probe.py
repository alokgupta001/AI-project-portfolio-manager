"""Reserved local acceptance fixture; not an enterprise upload interface."""

import argparse

from ppm_api.config import load_settings
from ppm_api.storage import LocalObjectStore

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["write", "verify"])
args = parser.parse_args()
settings = load_settings()
if settings.app_env != "local":
    raise SystemExit("Storage acceptance fixture is restricted to local mode")
store = LocalObjectStore(settings.storage_root)
key = "__foundation_acceptance__/restart.txt"
content = b"Sprint 01 storage persistence fixture"
if args.mode == "write":
    store.put(key, content)
else:
    if store.get(key) != content:
        raise SystemExit("Object did not survive restart")
    store.delete(key)
print("PASS: storage persistence", args.mode)
