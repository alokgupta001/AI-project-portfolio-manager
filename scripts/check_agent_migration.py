"""Guard Sprint 11 destructive lifecycle to disposable ppm_test, never the normal database."""

import os
import subprocess
import sys

from sqlalchemy.engine import make_url

if (
    os.environ.get("PPM_APP_ENV") != "test"
    or make_url(os.environ.get("PPM_MIGRATION_DATABASE_URL", "")).database != "ppm_test"
):
    raise SystemExit("Refusing specialist lifecycle outside test/ppm_test")
for args in [
    ("downgrade", "0013_specialist_reviews"),
    ("upgrade", "head"),
    ("downgrade", "0012_ai_runtime"),
    ("upgrade", "head"),
    ("check",),
]:
    subprocess.run([sys.executable, "-m", "alembic", *args], check=True)
print("PASS disposable 0012/0013 -> 0014 lifecycle and metadata drift")
