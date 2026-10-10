"""Private backup and original-column hashes before/after the additive repair migration."""

import json
import subprocess
import sys
from pathlib import Path

folder = Path("artifacts/local/repair-20261010")
folder.mkdir(parents=True, exist_ok=True)
phase = sys.argv[1]
if phase not in {"before", "after"}:
    raise SystemExit("Expected before or after")
baseline_file = folder / "database-before.json"
base = ["docker", "compose", "exec", "-T", "postgres"]


def sql(query):
    return subprocess.check_output(
        base
        + [
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
        text=True,
    ).strip()


if phase == "before":
    if baseline_file.exists():
        raise SystemExit("Refusing to overwrite the preservation baseline")
    with (folder / "database-before.dump").open("xb") as output:
        subprocess.run(
            base + ["pg_dump", "-U", "postgres", "-Fc", "ppm_local"], stdout=output, check=True
        )
    tables = sql(
        "SELECT tablename FROM pg_tables WHERE schemaname='public' "
        "AND tablename<>'alembic_version' ORDER BY tablename"
    ).splitlines()
else:
    tables = list(json.loads(baseline_file.read_text())["tables"])
result = {"revision": sql("SELECT version_num FROM alembic_version"), "tables": {}}
for name in tables:
    quoted = '"' + name.replace('"', '""') + '"'
    exclude = (
        {"identity_users": ["active"], "organizations": ["description", "industry", "website"]}.get(
            name, []
        )
        if phase == "after"
        else []
    )
    projection = "to_jsonb(t)" + "".join(" - '" + field + "'" for field in exclude)
    result["tables"][name] = json.loads(
        sql(
            "SELECT json_build_object('count',count(*),'hash',"
            "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) "
            f"FROM (SELECT {projection} r FROM {quoted} t) x"
        )
    )
(folder / f"database-{phase}.json").write_text(json.dumps(result, indent=2))
if phase == "after" and json.loads(baseline_file.read_text())["tables"] != result["tables"]:
    raise SystemExit("Established records differ; inspect private hashes before proceeding")
print(
    f"PASS {phase}: {len(tables)} established table counts/hashes "
    + ("unchanged" if phase == "after" else "captured; private backup saved")
)
