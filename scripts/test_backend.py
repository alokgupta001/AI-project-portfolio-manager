"""Run migration lifecycle only against the dedicated, disposable test database."""

import os
import subprocess
import sys

from sqlalchemy.engine import make_url

url = os.environ.get("PPM_MIGRATION_DATABASE_URL", "")
if os.environ.get("PPM_APP_ENV") != "test" or make_url(url).database != "ppm_test":
    raise SystemExit("Refusing migration lifecycle check outside ppm_test/test environment")

env = os.environ.copy()
env["PYTHONPATH"] = os.pathsep.join(["services/api", "services/worker", "."])

commands = [
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    [sys.executable, "-m", "alembic", "downgrade", "0006_command_center"],
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    [sys.executable, "-m", "alembic", "downgrade", "base"],
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    [sys.executable, "-m", "alembic", "check"],
    [sys.executable, "-m", "pytest", "-q"],
]
for command in commands:
    print("Running:", " ".join(command), flush=True)
    subprocess.run(command, check=True, env=env)
