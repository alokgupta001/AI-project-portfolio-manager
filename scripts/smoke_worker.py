"""Run a real broker/worker/database task without touching domain data."""

from ppm_worker.app import database_checkpoint

result = database_checkpoint.delay().get(timeout=30)
if result.get("status") != "completed" or not result.get("instance_id"):
    raise SystemExit("Worker checkpoint failed")
print("PASS: real Redis -> Linux Celery worker -> PostgreSQL checkpoint", result["instance_id"])
