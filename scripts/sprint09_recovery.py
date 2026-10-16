"""Non-destructive pilot backup/restore; refuses existing scratch targets and archives."""

import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

root = Path("artifacts/local/sprint09")
root.mkdir(parents=True, exist_ok=True)
compose = ["docker", "compose", "exec", "-T", "postgres"]
phase = sys.argv[1]


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


def manifest(folder: Path) -> dict:
    return {
        p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in folder.rglob("*")
        if p.is_file()
    }


if phase == "capture":
    archive = root / "objects-before.tar"
    if archive.exists():
        raise SystemExit("Refusing to overwrite the private object archive")
    with archive.open("xb") as output:
        subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "api",
                "tar",
                "-cf",
                "-",
                "-C",
                "/var/ppm/objects",
                ".",
            ],
            stdout=output,
            check=True,
        )
    frozen = {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in Path("services/api/migrations/versions").glob("*.py")
        if p.name < "0011"
    }
    (root / "migrations-before.json").write_text(json.dumps(frozen, indent=2))
    print(f"PASS private object archive and {len(frozen)} frozen migration hashes captured")
elif phase == "restore":
    scratch = "ppm_sprint09_restore"
    if sql("postgres", f"SELECT 1 FROM pg_database WHERE datname='{scratch}'"):
        raise SystemExit("Scratch database exists; refusing to overwrite")
    sql("postgres", f"CREATE DATABASE {scratch} OWNER ppm_owner")
    with (root / "database-before.dump").open("rb") as source:
        subprocess.run(
            [*compose, "pg_restore", "-U", "postgres", "-d", scratch, "--exit-on-error"],
            stdin=source,
            check=True,
        )
    baseline = json.loads((root / "database-before.json").read_text())
    actual = {}
    for name in baseline["tables"]:
        quoted = '"' + name.replace('"', '""') + '"'
        actual[name] = json.loads(
            sql(
                scratch,
                "SELECT json_build_object('count',count(*),'hash',"
                "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) "
                f"FROM (SELECT to_jsonb(t) r FROM {quoted} t) x",
            )
        )
    assert actual == baseline["tables"], "Restored database differs"
    assert sql(scratch, "SELECT version_num FROM alembic_version") == baseline["revision"]
    target = (root / "restored-normal-objects").resolve()
    if target.exists():
        raise SystemExit("Refusing to overwrite scratch objects")
    with tarfile.open(root / "objects-before.tar") as archive:
        expected = {
            str(Path(m.name).as_posix()).removeprefix("./"): hashlib.sha256(
                archive.extractfile(m).read()
            ).hexdigest()
            for m in archive.getmembers()
            if m.isfile()
        }
        archive.extractall(target, filter="data")
    assert manifest(target) == expected, "Restored object hashes differ"
    print(
        f"PASS isolated normal backup restore: {len(actual)} table hashes/counts, "
        f"{len(expected)} object hashes; original head {baseline['revision']}; "
        "normal data untouched"
    )
elif phase == "verify":
    baseline = json.loads((root / "objects-before.json").read_text(encoding="utf-8-sig"))
    actual = json.loads(
        subprocess.check_output(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "api",
                "python",
                "-c",
                "import pathlib,hashlib,json; p=pathlib.Path('/var/ppm/objects'); "
                "print(json.dumps({str(f.relative_to(p)):"
                "hashlib.sha256(f.read_bytes()).hexdigest() "
                "for f in p.rglob('*') if f.is_file()}))",
            ],
            text=True,
        )
    )
    assert all(actual.get(k) == v for k, v in baseline.items()), "Established object changed"
    frozen = json.loads((root / "migrations-before.json").read_text())
    assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest() == v for k, v in frozen.items())
    print(
        f"PASS {len(baseline)} established object hashes and "
        f"{len(frozen)} applied migration files unchanged"
    )
else:
    raise SystemExit("Expected capture, restore or verify")
