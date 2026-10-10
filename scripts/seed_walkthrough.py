"""Provision reserved fictional walkthrough data; never reset an existing database.

Run through the Compose migration service, which supplies the owner connection.
Credentials stay in private storage, are generated once, and are never printed.
"""

import argparse
import asyncio
import json
import os
import secrets
from uuid import NAMESPACE_URL, uuid5

import httpx
import sqlalchemy as sa
from ppm_api.config import load_settings
from ppm_api.identity import now, password_hash
from ppm_api.identity_tables import memberships, organizations, users
from ppm_api.main import create_app
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


def ident(key):
    return uuid5(NAMESPACE_URL, "enterprise-ppm/website-training-v1/" + key)


async def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--empty", action="store_true", help="Provision identities only")
    args = parser.parse_args()
    config = load_settings()
    owner_url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    database = make_url(owner_url).database
    expected = {"local": "ppm_local", "test": "ppm_test", "demo": "ppm_demo"}
    if database != expected.get(config.app_env):
        raise SystemExit("Refusing seed outside the matching development/test/demo database")
    if make_url(config.database_url.get_secret_value()).database != database:
        raise SystemExit("Application and migration databases must match")
    folder = config.storage_root / "__walkthrough__"
    folder.mkdir(parents=True, exist_ok=True)
    private = folder / "credentials.json"
    manifest_file = folder / "manifest.json"
    oid = ident("organization")
    people = [
        ("asha", "Asha Admin", "Admin"),
        ("priya", "Priya Manager", "Project Manager"),
        ("ravi", "Ravi Reviewer", "Project Manager"),
        ("vera", "Vera Viewer", "Viewer"),
    ]
    if private.exists():
        credentials = json.loads(private.read_text())
    else:
        credentials = {
            "organization_id": str(oid),
            "people": {
                key: {
                    "id": str(ident(key)),
                    "email": f"walkthrough-{key}@example.com",
                    "password": secrets.token_urlsafe(24),
                    "name": name,
                    "role": role,
                }
                for key, name, role in people
            },
        }
        private.write_text(json.dumps(credentials, indent=2))
        private.chmod(0o600)
    manifest = json.loads(manifest_file.read_text()) if manifest_file.exists() else {}
    owner = create_async_engine(owner_url)
    try:
        async with owner.begin() as conn:
            if await conn.scalar(sa.text("SELECT current_database()")) != database:
                raise RuntimeError("Unexpected target database")
            await conn.execute(sa.text("SELECT pg_advisory_xact_lock(10102026)"))
            existing = (
                (await conn.execute(sa.select(organizations).where(organizations.c.id == oid)))
                .mappings()
                .first()
            )
            if not existing:
                await conn.execute(
                    organizations.insert().values(
                        id=oid,
                        name="Northstar Website Training",
                        created_at=now(),
                        description="Fictional website walkthrough; not real delivery evidence.",
                        industry="Technology",
                    )
                )
                for key, name, role in people:
                    p = credentials["people"][key]
                    if await conn.scalar(sa.select(users.c.id).where(users.c.email == p["email"])):
                        raise RuntimeError(
                            "Reserved demo email already exists; refusing to adopt it"
                        )
                    await conn.execute(
                        users.insert().values(
                            id=ident(key),
                            email=p["email"],
                            name=name,
                            verified=True,
                            active=True,
                            password_hash=await password_hash(p["password"]),
                            created_at=now(),
                        )
                    )
                    await conn.execute(
                        memberships.insert().values(
                            organization_id=oid,
                            user_id=ident(key),
                            role=role,
                            active=True,
                            revision=1,
                        )
                    )
            else:
                for key, _name, _role in people:
                    p = credentials["people"][key]
                    user = (
                        (await conn.execute(sa.select(users).where(users.c.id == ident(key))))
                        .mappings()
                        .first()
                    )
                    if not user or user["email"] != p["email"]:
                        raise RuntimeError(
                            "Reserved identity mismatch; refusing to alter existing data"
                        )
        app = create_app(config)
        async with app.router.lifespan_context(app):
            clients = {}
            try:
                for key, _, _ in people:
                    client = httpx.AsyncClient(
                        transport=httpx.ASGITransport(app=app), base_url="https://seed.local"
                    )
                    clients[key] = client
                    await client.get("/api/v1/auth/csrf")
                    client.headers.update(
                        {
                            "origin": config.web_origin,
                            "x-csrf-token": client.cookies.get("ppm_csrf"),
                            "x-organization-id": str(oid),
                        }
                    )
                    p = credentials["people"][key]
                    login = await client.post(
                        "/api/v1/auth/login", json={"email": p["email"], "password": p["password"]}
                    )
                    if login.status_code != 200:
                        raise RuntimeError(
                            "Reserved account cannot authenticate; "
                            "preserve it and inspect its status"
                        )

                async def command(actor, method, path, body=None, revision=None, key=None):
                    headers = {"idempotency-key": str(ident(key or path))}
                    if revision is not None:
                        headers["if-match"] = str(revision)
                    response = await clients[actor].request(
                        method, "/api/v1" + path, json=body, headers=headers
                    )
                    if response.status_code not in (200, 201):
                        error = response.json().get("error", {})
                        raise RuntimeError(
                            f"Seed operation {method} {path}: {response.status_code} "
                            f"{error.get('message', 'failed')}"
                        )
                    return response.json()

                async def add(actor, kind, name, **values):
                    key = kind + ":" + name
                    if key in manifest:
                        record = await command(actor, "GET", f"/delivery/{kind}/{manifest[key]}")
                    else:
                        record = await command(
                            actor,
                            "POST",
                            "/delivery/" + kind,
                            {"kind": kind, "name": name, **values},
                            key=key,
                        )
                        manifest[key] = record["id"]
                        manifest_file.write_text(json.dumps(manifest, indent=2))
                    return record["id"]

                if not args.empty:
                    await add(
                        "asha",
                        "settings",
                        "Northstar operating settings",
                        timezone="Asia/Kolkata",
                        currency="INR",
                    )
                    dep = await add(
                        "asha", "departments", "Digital Delivery", owner_id=str(ident("asha"))
                    )
                    team = await add(
                        "asha",
                        "teams",
                        "Portal Delivery Team",
                        department_id=dep,
                        owner_id=str(ident("priya")),
                    )
                    for key in ("priya", "ravi"):
                        await add(
                            "asha",
                            "team_members",
                            f"{key.title()} — Portal Delivery Team",
                            team_id=team,
                            user_id=str(ident(key)),
                            start_date="2026-10-12",
                        )
                    goal = await add(
                        "asha",
                        "goals",
                        "Reduce customer onboarding effort",
                        owner_id=str(ident("asha")),
                    )
                    portfolio = await add(
                        "asha",
                        "portfolios",
                        "Customer Experience Portfolio",
                        owner_id=str(ident("asha")),
                    )
                    program = await add(
                        "asha",
                        "programs",
                        "Customer Self-Service Program",
                        portfolio_id=portfolio,
                        owner_id=str(ident("priya")),
                    )
                    await add(
                        "asha",
                        "grants",
                        "Priya — customer portfolio manage",
                        user_id=str(ident("priya")),
                        portfolio_id=portfolio,
                        access="manage",
                    )
                    await add(
                        "asha",
                        "grants",
                        "Vera — customer portfolio read",
                        user_id=str(ident("vera")),
                        portfolio_id=portfolio,
                        access="read",
                    )
                    await add(
                        "asha",
                        "metric_policies",
                        "Northstar training metric policy",
                        amber="30",
                        red="60",
                        stale_days=7,
                    )
                    calendar = await add(
                        "asha",
                        "calendars",
                        "India weekday calendar — v1",
                        timezone="Asia/Kolkata",
                        **{
                            d: "8" for d in ["monday", "tuesday", "wednesday", "thursday", "friday"]
                        },
                        saturday="0",
                        sunday="0",
                        holidays="",
                    )
                    resource = await add(
                        "asha", "resources", "Priya delivery capacity", user_id=str(ident("priya"))
                    )
                    await add(
                        "asha",
                        "resource_access",
                        "Priya — own training resource management",
                        resource_id=resource,
                        user_id=str(ident("priya")),
                        manage=True,
                        effort=True,
                    )
                    await add(
                        "asha",
                        "resource_access",
                        "Asha — training effort oversight",
                        resource_id=resource,
                        user_id=str(ident("asha")),
                        effort=True,
                    )
                    dates = {"start_date": "2026-10-12", "end_date": "2026-11-07"}
                    await add(
                        "asha",
                        "availability",
                        "Priya — October availability",
                        resource_id=resource,
                        calendar_id=calendar,
                        **dates,
                    )
                    await add(
                        "asha",
                        "resource_teams",
                        "Priya — portal staffing",
                        resource_id=resource,
                        team_id=team,
                        **dates,
                    )
                    await add(
                        "asha",
                        "resource_skills",
                        "Priya — delivery planning",
                        resource_id=resource,
                        skill="Project delivery planning",
                    )
                    project = await add(
                        "priya",
                        "projects",
                        "Customer Onboarding Portal",
                        portfolio_id=portfolio,
                        program_id=program,
                        department_id=dep,
                        team_id=team,
                        owner_id=str(ident("priya")),
                        priority="high",
                        industry="technology",
                        category="delivery",
                        methodology="agile",
                        size_band="small",
                        status="active",
                        reported_health="Green",
                        currency="INR",
                        start_date="2026-10-12",
                        target_end_date="2026-11-06",
                        forecast_end_date="2026-11-06",
                    )
                    await add(
                        "asha",
                        "grants",
                        "Ravi — portal project read",
                        user_id=str(ident("ravi")),
                        project_id=project,
                        access="read",
                    )
                    sprint = await add(
                        "priya",
                        "sprints",
                        "Portal Sprint 1",
                        project_id=project,
                        team_id=team,
                        start_date="2026-10-12",
                        end_date="2026-10-23",
                        status="planned",
                    )
                    work = []
                    for name, kind, points, start, due in [
                        (
                            "Confirm onboarding requirements",
                            "story",
                            "3",
                            "2026-10-12",
                            "2026-10-14",
                        ),
                        ("Build onboarding form", "feature", "5", "2026-10-15", "2026-10-21"),
                        ("Run acceptance checks", "task", "2", "2026-10-21", "2026-10-23"),
                    ]:
                        work.append(
                            await add(
                                "priya",
                                "work_items",
                                name,
                                project_id=project,
                                sprint_id=sprint,
                                owner_id=str(ident("priya")),
                                work_type=kind,
                                points=points,
                                start_date=start,
                                due_date=due,
                            )
                        )
                    for name, due in [
                        ("Requirements agreed", "2026-10-14"),
                        ("Portal release", "2026-11-06"),
                    ]:
                        await add(
                            "priya",
                            "milestones",
                            name,
                            project_id=project,
                            due_date=due,
                            critical=True,
                        )
                    await add(
                        "priya",
                        "budget_lines",
                        "Portal delivery budget",
                        project_id=project,
                        amount="200000",
                        currency="INR",
                        approved=True,
                    )
                    await add(
                        "priya",
                        "expenditures",
                        "Portal design workshop",
                        project_id=project,
                        amount="20000",
                        currency="INR",
                        spent_on="2026-10-12",
                    )
                    await add(
                        "priya",
                        "risks",
                        "Customer validation rules may arrive late",
                        project_id=project,
                        owner_id=str(ident("priya")),
                        severity=3,
                        likelihood=3,
                        mitigation="Review validation rules before form development.",
                        review_on="2026-10-16",
                    )
                    await add(
                        "priya",
                        "blockers",
                        "Awaiting validation examples",
                        project_id=project,
                        work_item_id=work[1],
                        owner_id=str(ident("priya")),
                    )
                    await add(
                        "priya",
                        "alignments",
                        "Portal contribution to onboarding goal",
                        project_id=project,
                        goal_id=goal,
                        weight="1",
                        contribution="0.8",
                    )
                    await add(
                        "priya",
                        "benefits",
                        "Onboarding administration hours saved",
                        project_id=project,
                        unit="hours saved",
                        target="100",
                        realized="20",
                        period_start="2026-10-12",
                        period_end="2026-11-07",
                    )
                    baseline = await add(
                        "priya",
                        "baselines",
                        "Portal approved plan — v1",
                        project_id=project,
                        description="Initial training schedule and budget before changes.",
                    )
                    await add(
                        "priya",
                        "metric_plans",
                        "Portal measurement plan — v1",
                        project_id=project,
                        baseline_id=baseline,
                        calendar_id=calendar,
                        forecast_cost="210000",
                    )
                    await add(
                        "priya",
                        "status_updates",
                        "Portal weekly update — 12 October",
                        project_id=project,
                        reported_health="Amber",
                        description="Fictional requirements review; examples outstanding.",
                    )
                    await add(
                        "priya",
                        "allocations",
                        "Priya — portal allocation",
                        resource_id=resource,
                        project_id=project,
                        hours_per_day="4",
                        **dates,
                    )
                    await add(
                        "priya",
                        "time_off",
                        "Priya — training half day",
                        resource_id=resource,
                        start_date="2026-10-16",
                        end_date="2026-10-17",
                        hours_per_day="4",
                    )
                    await add(
                        "priya",
                        "effort",
                        "Priya — portal work — 12 October",
                        resource_id=resource,
                        project_id=project,
                        worked_on="2026-10-12",
                        hours="4",
                        overtime_hours="0",
                    )
                    # Leave delivery and assessment workflows mutable for the user to perform.
                    framework_key = "framework"
                    if framework_key not in manifest:
                        definitions = [
                            (
                                "Governance",
                                "0.30",
                                [
                                    ("Named accountable owner", "boolean"),
                                    ("Governance practice", "rubric"),
                                ],
                            ),
                            (
                                "Delivery planning",
                                "0.40",
                                [
                                    ("Baseline and milestones", "boolean"),
                                    ("Risk management practice", "rubric"),
                                ],
                            ),
                            (
                                "Evidence discipline",
                                "0.30",
                                [
                                    ("Traceable supporting evidence", "boolean"),
                                    ("Evidence summary", "text"),
                                ],
                            ),
                        ]
                        body = {
                            "name": "Northstar Delivery Readiness",
                            "category": "delivery",
                            "description": "Fictional manual assessment; no AI evaluation.",
                            "dimensions": [
                                {
                                    "id": str(ident(name)),
                                    "name": name,
                                    "weight": weight,
                                    "questions": [
                                        {
                                            "id": str(ident(q)),
                                            "name": q,
                                            "text": q + " — use the supplied walkthrough evidence.",
                                            "answer_type": typ,
                                            "weight": "1",
                                            "required": True,
                                            "rubric_levels": [
                                                {"level": i, "label": label}
                                                for i, label in enumerate(
                                                    [
                                                        "Not demonstrated",
                                                        "Partially established",
                                                        "Established and repeatable",
                                                    ]
                                                )
                                            ]
                                            if typ == "rubric"
                                            else [],
                                        }
                                        for q, typ in questions
                                    ],
                                }
                                for name, weight, questions in definitions
                            ],
                        }
                        framework = await command(
                            "asha", "POST", "/assessment/frameworks", body, key="framework"
                        )
                        manifest[framework_key] = framework["id"]
                        manifest_file.write_text(json.dumps(manifest, indent=2))
                    if "version" not in manifest:
                        frameworks = await command("asha", "GET", "/assessment/frameworks")
                        fw = next(f for f in frameworks if f["id"] == manifest["framework"])
                        version = await command(
                            "asha",
                            "POST",
                            f"/assessment/frameworks/{fw['id']}/publish",
                            {},
                            fw["revision"],
                            key="publish",
                        )
                        manifest["version"] = version["id"]
                        manifest_file.write_text(json.dumps(manifest, indent=2))
                    if "assessment" not in manifest:
                        assessment = await command(
                            "asha",
                            "POST",
                            "/assessment/assessments",
                            {
                                "name": "Digital Delivery — Portal Readiness — October 2026",
                                "framework_version_id": manifest["version"],
                                "department_id": dep,
                                "team_id": team,
                                "assigned_to": str(ident("priya")),
                                "reviewer_id": str(ident("ravi")),
                            },
                            key="assessment",
                        )
                        manifest["assessment"] = assessment["id"]
                        manifest_file.write_text(json.dumps(manifest, indent=2))
                print(
                    f"Verified {len(people)} reserved accounts and {len(manifest)} "
                    f"walkthrough records in {database}. Existing edits preserved."
                )
                print("Private credentials: " + str(private))
            finally:
                for client in clients.values():
                    if client.cookies.get("ppm_access"):
                        await client.post("/api/v1/auth/logout", json={})
                    await client.aclose()
    finally:
        await owner.dispose()


if __name__ == "__main__":
    asyncio.run(run())
