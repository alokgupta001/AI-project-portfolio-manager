"""Restore synthetic document DB and objects to new scratch targets, then check signed access."""

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

root = Path("artifacts/local/sprint09").resolve()
database = "ppm_sprint09_documents_restore"
pg = ["docker", "compose", "exec", "-T", "postgres"]
compose = [
    "docker",
    "compose",
    "-f",
    "compose.yaml",
    "-f",
    "compose.documents.yaml",
    "--profile",
    "test",
    "run",
    "--rm",
    "--no-deps",
]


def sql(db: str, query: str) -> str:
    return subprocess.check_output(
        [*pg, "psql", "-U", "postgres", "-d", db, "-At", "-v", "ON_ERROR_STOP=1", "-c", query],
        text=True,
    ).strip()


def hashes(db: str) -> dict:
    result = {}
    tables = sql(db, "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
    for table in tables.splitlines():
        quoted = '"' + table.replace('"', '""') + '"'
        result[table] = json.loads(
            sql(
                db,
                "SELECT json_build_object('count',count(*),'hash',"
                "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) "
                f"FROM (SELECT to_jsonb(t) r FROM {quoted} t) x",
            )
        )
    return result


if sql("postgres", f"SELECT 1 FROM pg_database WHERE datname='{database}'"):
    raise SystemExit("Refusing to overwrite existing scratch database")
if (root / "document-fixture.json").exists():
    raise SystemExit("Refusing to overwrite existing synthetic recovery fixture")

mounts = [
    "-v",
    f"{root.as_posix()}:/recovery",
    "-v",
    f"{Path('services').resolve().as_posix()}:/app/services:ro",
    "-v",
    f"{Path('scripts').resolve().as_posix()}:/app/scripts:ro",
]
for phase in ["seed"]:
    subprocess.run(
        [
            *compose,
            *mounts,
            "-e",
            f"PPM_RECOVERY_PHASE={phase}",
            "test",
            "python",
            "scripts/sprint09_document_restore.py",
        ],
        check=True,
    )
baseline = hashes("ppm_test")
with (root / "document-database.dump").open("xb") as output:
    subprocess.run([*pg, "pg_dump", "-U", "postgres", "-Fc", "ppm_test"], stdout=output, check=True)
sql("postgres", f"CREATE DATABASE {database} OWNER ppm_owner")
with (root / "document-database.dump").open("rb") as source:
    subprocess.run(
        [*pg, "pg_restore", "-U", "postgres", "-d", database, "--exit-on-error"],
        stdin=source,
        check=True,
    )
assert hashes(database) == baseline, "Scratch table hashes/counts differ"
shutil.copytree(root / "source-objects", root / "restored-document-objects")
expected = {
    p.relative_to(root / "source-objects").as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in (root / "source-objects").rglob("*")
    if p.is_file()
}
actual = {
    p.relative_to(root / "restored-document-objects").as_posix(): hashlib.sha256(
        p.read_bytes()
    ).hexdigest()
    for p in (root / "restored-document-objects").rglob("*")
    if p.is_file()
}
assert actual == expected
(root / "document-recovery-manifest.json").write_text(
    json.dumps(dict(tables=baseline, objects=actual), indent=2)
)
subprocess.run(
    [
        *compose,
        *mounts,
        "-e",
        "PPM_RECOVERY_PHASE=verify",
        "test",
        "python",
        "scripts/sprint09_document_restore.py",
    ],
    check=True,
)
print(
    f"PASS document scratch restore: {len(baseline)} table hashes/counts, "
    f"{len(actual)} object hashes, authenticated signed download and keyword citation"
)
