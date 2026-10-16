"""Focused prior-head/upgrade/drift check against the disposable test DB only."""

import os
import subprocess
import sys

from sqlalchemy.engine import make_url

if (
    os.environ.get("PPM_APP_ENV") != "test"
    or make_url(os.environ.get("PPM_MIGRATION_DATABASE_URL", "")).database != "ppm_test"
):
    raise SystemExit("Refusing migration checks outside test/ppm_test")
for args in [("downgrade", "0010_account_authority"), ("upgrade", "head"), ("check",)]:
    subprocess.run([sys.executable, "-m", "alembic", *args], check=True)
print("PASS final 0010 -> 0011 upgrade and schema drift check")
