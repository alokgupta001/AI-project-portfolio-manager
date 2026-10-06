"""Run migration lifecycle only against the dedicated, disposable test database."""

import os
import subprocess
import sys

from sqlalchemy.engine import make_url

url = os.environ.get("PPM_MIGRATION_DATABASE_URL", "")
if os.environ.get("PPM_APP_ENV") != "test" or make_url(url).database != "ppm_test":
    raise SystemExit("Refusing migration lifecycle check outside ppm_test/test environment")
commands = [
    ["alembic", "upgrade", "head"],
    ["alembic", "downgrade", "base"],
    ["alembic", "upgrade", "head"],
    ["alembic", "upgrade", "head"],
    ["alembic", "check"],
    [sys.executable, "-m", "pytest", "-q"],
]
for command in commands:
    print("Running:", " ".join(command), flush=True)
    subprocess.run(command, check=True)
