"""Verify the captured local baseline after additive 0017, without printing private data."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "artifacts/local/sprint12"


def verify() -> None:
    """Compare all original rows, excluding only the newly added nullable columns."""
    frozen = json.loads((FOLDER / "files-before.json").read_text(encoding="utf-8"))
    assert all(
        hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest
        for p, digest in frozen.items()
    ), "A frozen input changed"
    baseline = json.loads((FOLDER / "database-before.json").read_text(encoding="utf-8"))
    assert baseline["revision"] == "0016_guided_project_access"
    queries = []
    for name in baseline["tables"]:
        assert name.replace("_", "").isalnum()
        projection = "to_jsonb(t)"
        if name == "durable_jobs":
            projection += " - 'ai_run_id' - 'ml_run_id' - 'connector_generation'"
        if name == "ingestion_sources":
            projection += " - 'logical_key'"
        queries.append(
            f"SELECT '{name}' name, json_build_object('count',count(*),'hash',"
            "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) data "
            f'FROM (SELECT {projection} r FROM "{name}" t) x'
        )
    sql = (
        "SELECT json_build_object('revision',(SELECT version_num FROM alembic_version),"
        "'tables',json_object_agg(name,data)) FROM (" + " UNION ALL ".join(queries) + ") x"
    )
    result = json.loads(
        subprocess.check_output(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "postgres",
                "psql",
                "-U",
                "postgres",
                "-d",
                "ppm_local",
                "-At",
                "-v",
                "ON_ERROR_STOP=1",
                "-c",
                sql,
            ],
            cwd=ROOT,
            text=True,
        )
    )
    (FOLDER / "database-after.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    assert result["revision"] == "0017_local_ml_foundations", "Unexpected normal schema"
    changed = [name for name, data in baseline["tables"].items() if result["tables"][name] != data]
    assert not changed, f"Established rows changed in: {changed}"
    print(
        f"PASS {len(frozen)} frozen input hashes; all {len(queries)} established table "
        "counts/hashes unchanged; normal 0016 -> 0017"
    )


if __name__ == "__main__":
    verify()
