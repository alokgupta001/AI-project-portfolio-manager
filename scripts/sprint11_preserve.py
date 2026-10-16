"""Private, append-only Sprint 11 preservation checkpoints; no secret output."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "artifacts/local/sprint11"
FOLDER.mkdir(parents=True, exist_ok=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files() -> None:
    target = FOLDER / "files-before.json"
    if target.exists():
        raise SystemExit("Refusing to replace the preservation baseline")
    paths = [ROOT / ".env"]
    paths += list((ROOT / "services/api/migrations/versions").glob("*.py"))
    paths += [p for p in (ROOT / "docs/source").rglob("*") if p.is_file()]
    paths += [
        ROOT / "docs/prompts" / name
        for name in (
            "01-MASTER-PROMPT.md",
            "02-ORDERED-SPRINT-PROMPTS.md",
            "03-SPRINT-REPORT-TEMPLATE.md",
            "04-FOLLOW-UP-HANDOFF-TEMPLATE.md",
            "05-REQUIREMENTS-COVERAGE-TEMPLATE.md",
        )
    ]
    target.write_text(
        json.dumps(
            {p.relative_to(ROOT).as_posix(): sha(p) for p in paths if p.is_file()}, indent=2
        ),
        encoding="utf-8",
    )
    git = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]
    (FOLDER / "git-before.txt").write_bytes(
        subprocess.check_output([*git, "status", "--short"], cwd=ROOT)
    )
    with (FOLDER / "working-tree-before.patch").open("xb") as stream:
        subprocess.run([*git, "diff", "--binary"], cwd=ROOT, stdout=stream, check=True)
    # Preserve every pre-existing non-ignored untracked file without copying private runtime data.
    untracked = (
        subprocess.check_output([*git, "ls-files", "--others", "--exclude-standard"], cwd=ROOT)
        .decode()
        .splitlines()
    )
    import zipfile

    with zipfile.ZipFile(FOLDER / "untracked-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        for relative in untracked:
            archive.write(ROOT / relative, relative)
    print("PASS private frozen-file hashes, working-tree patch and untracked archive captured")


def check() -> None:
    baseline = json.loads((FOLDER / "files-before.json").read_text(encoding="utf-8"))
    assert all(
        (ROOT / path).is_file() and sha(ROOT / path) == digest for path, digest in baseline.items()
    ), "Frozen input or applied migration changed"
    print(f"PASS {len(baseline)} preserved .env/source/prompt/migration hashes")


def database() -> None:
    phase = sys.argv[2]
    if phase not in {"before", "after"}:
        raise SystemExit("Expected before/after")
    target = FOLDER / f"database-{phase}.json"
    if target.exists():
        raise SystemExit("Refusing to overwrite a checkpoint")
    base = ["docker", "compose", "exec", "-T", "postgres"]

    def sql(query):
        return subprocess.check_output(
            [
                *base,
                "psql",
                "-U",
                "postgres",
                "-d",
                "ppm_local",
                "-At",
                "-v",
                "ON_ERROR_STOP=1",
                "-c",
                query,
            ],
            cwd=ROOT,
            text=True,
        ).strip()

    if phase == "before":
        tables = sql(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' "
            "AND tablename<>'alembic_version' ORDER BY tablename"
        ).splitlines()
    else:
        tables = list(json.loads((FOLDER / "database-before.json").read_text())["tables"])
    result = {"revision": sql("SELECT version_num FROM alembic_version"), "tables": {}}
    for name in tables:
        quoted = '"' + name.replace('"', '""') + '"'
        projection = "to_jsonb(t) - 'ai_run_id'" if name == "durable_jobs" else "to_jsonb(t)"
        result["tables"][name] = json.loads(
            sql(
                "SELECT json_build_object('count',count(*),'hash',md5(coalesce("
                "string_agg(r::text,E'\\n' ORDER BY r::text),''))) FROM "
                f"(SELECT {projection} r FROM {quoted} t) x"
            )
        )
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if phase == "before":
        # Finish SQL/hash validation and write the checkpoint before creating
        # permanent backups. A failed query/JSON write leaves the capture retryable.
        with (FOLDER / "database-before.dump").open("xb") as stream:
            subprocess.run(
                [*base, "pg_dump", "-U", "postgres", "-Fc", "ppm_local"],
                cwd=ROOT,
                stdout=stream,
                check=True,
            )
        # Read the original volume through the existing API image, without its entrypoint.
        with (FOLDER / "objects-before.tar").open("xb") as stream:
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "run",
                    "--rm",
                    "--no-deps",
                    "api",
                    "tar",
                    "-cf",
                    "-",
                    "-C",
                    "/var/ppm/objects",
                    ".",
                ],
                cwd=ROOT,
                stdout=stream,
                check=True,
            )
    if phase == "after":
        assert (
            result["tables"] == json.loads((FOLDER / "database-before.json").read_text())["tables"]
        )
    print(
        f"PASS {phase}: {result['revision']}; {len(tables)} established table counts/hashes "
        + ("unchanged" if phase == "after" else "captured; private DB/object backups saved")
    )


def objects() -> None:
    import tarfile

    target = FOLDER / "objects-after.tar"
    if target.exists():
        raise SystemExit("Refusing to overwrite object verification evidence")
    with target.open("xb") as stream:
        subprocess.run(
            [
                "docker",
                "compose",
                "run",
                "--rm",
                "--no-deps",
                "api",
                "tar",
                "-cf",
                "-",
                "-C",
                "/var/ppm/objects",
                ".",
            ],
            cwd=ROOT,
            stdout=stream,
            check=True,
        )

    def hashes(path):
        with tarfile.open(path) as archive:
            return {
                member.name: hashlib.sha256(archive.extractfile(member).read()).hexdigest()
                for member in archive
                if member.isfile()
            }

    before = hashes(FOLDER / "objects-before.tar")
    assert before == hashes(target), "Original object set/bytes changed"
    print(f"PASS {len(before)} original object keys/byte hashes unchanged")


if __name__ == "__main__":
    {"files": files, "check": check, "database": database, "objects": objects}[sys.argv[1]]()
