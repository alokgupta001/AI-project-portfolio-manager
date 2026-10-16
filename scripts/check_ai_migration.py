"""Prior-head lifecycle/drift guard; refuses every database except disposable ppm_test."""

import os
import subprocess
import sys

from sqlalchemy.engine import make_url

if (
    os.environ.get("PPM_APP_ENV") != "test"
    or make_url(os.environ.get("PPM_MIGRATION_DATABASE_URL", "")).database != "ppm_test"
):
    raise SystemExit("Refusing AI migration lifecycle outside test/ppm_test")
for args in [("downgrade", "0011_document_sources"), ("upgrade", "head"), ("check",)]:
    subprocess.run([sys.executable, "-m", "alembic", *args], check=True)
print("PASS disposable prior-head 0011 -> 0012 and no schema drift")
