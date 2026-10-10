"""Restore the private backup into a new scratch database and object folder."""

import hashlib
import json
import subprocess
import tarfile
from pathlib import Path

root = Path("artifacts/local/sprint81")
root.mkdir(parents=True, exist_ok=True)
scratch = "ppm_sprint81_restore"
compose = ["docker", "compose", "exec", "-T", "postgres"]


def sql(database: str, query: str) -> str:
    return subprocess.check_output(
        [
            *compose,
            "psql",
            "-U",
            "postgres",
            "-d",
            database,
            "-At",
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            query,
        ],
        text=True,
    ).strip()


if sql("postgres", f"SELECT 1 FROM pg_database WHERE datname='{scratch}'"):
    raise SystemExit("Scratch database already exists; refusing to overwrite it")
sql("postgres", f"CREATE DATABASE {scratch}")
with Path("artifacts/local/sprint81-normal-before.dump").open("rb") as backup:
    subprocess.run(
        [*compose, "pg_restore", "-U", "postgres", "-d", scratch, "--exit-on-error"],
        stdin=backup,
        check=True,
    )
baseline = json.loads(Path("artifacts/local/sprint81-normal-before.json").read_text())
restored = {}
for name in baseline["tables"]:
    quoted = '"' + name.replace('"', '""') + '"'
    restored[name] = json.loads(
        sql(
            scratch,
            "SELECT json_build_object('count',count(*),'hash',"
            "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) "
            f"FROM (SELECT to_jsonb(t) r FROM {quoted} t) x",
        )
    )
assert baseline["tables"] == restored, "Scratch database hashes differ"
assert sql(scratch, "SELECT version_num FROM alembic_version") == baseline["revision"]

volume = "enterprise-ppm_objects"
subprocess.run(["docker", "volume", "inspect", volume], check=True, stdout=subprocess.DEVNULL)
archive = root / "objects-before.tar"
if archive.exists():
    raise SystemExit("Private object archive already exists; refusing to overwrite it")
with archive.open("xb") as output:
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--mount",
            f"type=volume,src={volume},dst=/objects,readonly",
            "enterprise-ppm-test",
            "python",
            "-c",
            "import sys,tarfile; t=tarfile.open(fileobj=sys.stdout.buffer,mode='w|'); "
            "t.add('/objects',arcname='objects'); t.close()",
        ],
        stdout=output,
        check=True,
    )
target = (root / "object-restore").resolve()
expected = {}
with tarfile.open(archive) as bundle:
    for member in bundle.getmembers():
        if member.isfile():
            stream = bundle.extractfile(member)
            assert stream is not None
            expected[member.name] = hashlib.sha256(stream.read()).hexdigest()
    bundle.extractall(target, filter="data")
actual = {
    p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in target.rglob("*")
    if p.is_file()
}
assert expected == actual, "Restored object hashes differ"
(root / "object-manifest.json").write_text(json.dumps(expected, indent=2))
(root / "restore-result.json").write_text(
    json.dumps(
        {
            "database": scratch,
            "revision": baseline["revision"],
            "tables": len(restored),
            "objects": len(actual),
            "result": "PASS",
        },
        indent=2,
    )
)
print(
    f"PASS scratch restore: {len(restored)} table hashes/counts and "
    f"{len(actual)} object hashes match; normal DB unchanged"
)
