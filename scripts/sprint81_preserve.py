"""Capture hashes/counts of established normal tables; never log rows or credentials."""

import json
import subprocess
import sys
from pathlib import Path

folder = Path("artifacts/local")
folder.mkdir(parents=True, exist_ok=True)
phase = sys.argv[1]
if phase not in {"before", "after"}:
    raise SystemExit("Expected before/after")


def sql(query: str) -> str:
    return subprocess.check_output(
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
            query,
        ],
        text=True,
    ).strip()


prior = folder / "sprint81-normal-before.json"
if phase == "before":
    if prior.exists():
        raise SystemExit("Preservation baseline already exists; refusing overwrite")
    with (folder / "sprint81-normal-before.dump").open("xb") as output:
        subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "postgres",
                "pg_dump",
                "-U",
                "postgres",
                "-Fc",
                "ppm_local",
            ],
            stdout=output,
            check=True,
        )
    names = sql(
        "SELECT tablename FROM pg_tables WHERE schemaname='public' "
        "AND tablename<>'alembic_version' ORDER BY tablename"
    ).splitlines()
else:
    names = list(json.loads(prior.read_text())["tables"])
result = {"revision": sql("SELECT version_num FROM alembic_version"), "tables": {}}
for name in names:
    # Names come from the trusted database catalog; quote identifiers without shell interpolation.
    quoted = '"' + name.replace('"', '""') + '"'
    additions = (
        {
            "organizations": ["revision"],
            "identity_challenges": ["invitation_id", "organization_name"],
            "ppm_projects": ["priority", "industry", "category", "methodology", "size_band"],
            "ppm_work_items": ["priority", "work_type"],
        }.get(name, [])
        if phase == "after"
        else []
    )
    projection = "to_jsonb(t)" + "".join(" - '" + key + "'" for key in additions)
    result["tables"][name] = json.loads(
        sql(
            "SELECT json_build_object('count',count(*),'hash',"
            "md5(coalesce(string_agg(r::text,E'\\n' ORDER BY r::text),''))) "
            f"FROM (SELECT {projection} r FROM {quoted} t) x"
        )
    )
(folder / f"sprint81-normal-{phase}.json").write_text(json.dumps(result, indent=2))
if phase == "after":
    before = json.loads(prior.read_text())
    if before["tables"] != result["tables"]:
        raise SystemExit("Established table preservation differs; inspect private baseline files")
print(
    f"PASS {phase}: revision={result['revision']}; "
    f"{len(names)} established table hashes/counts captured"
    + (" and unchanged" if phase == "after" else "; private backup saved")
)
