"""Create an additive, labeled local demo tenant. Read its password privately from stdin."""

import asyncio
import json
import os
import sys
from datetime import timedelta
from uuid import NAMESPACE_URL, uuid5

import sqlalchemy as sa
from ppm_api.command_tables import risks
from ppm_api.config import load_settings
from ppm_api.identity import now, password_hash
from ppm_api.identity_tables import memberships, organizations, users
from ppm_api.ppm_schemas import Input
from ppm_api.ppm_tables import TABLES
from pydantic import TypeAdapter
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


def ident(name: str):
    """Use a dedicated namespace so repeated setup preserves this demo and other tenants."""
    return uuid5(NAMESPACE_URL, "enterprise-ppm/guided-demo-v1/" + name)


async def run() -> None:
    """Insert only new synthetic records, refusing changes to existing accounts or projects."""
    settings = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if settings.app_env != "local" or make_url(url).database != "ppm_local":
        raise SystemExit("This explicit local demo setup requires local/ppm_local")
    credentials = json.load(sys.stdin)
    if credentials["email"] != "guided-demo@example.com" or len(credentials["password"]) < 20:
        raise SystemExit("Expected dedicated demo login and generated private password")
    stamp = now()
    uid, oid = ident("admin"), ident("organization")
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            await conn.execute(sa.text("SELECT pg_advisory_xact_lock(11111112)"))
            if await conn.scalar(sa.select(organizations.c.id).where(organizations.c.id == oid)):
                print(
                    json.dumps(
                        dict(
                            organization_id=str(oid),
                            project_id=str(ident("project")),
                            status="existing_demo_preserved",
                        )
                    )
                )
                return
            if await conn.scalar(
                sa.select(users.c.id).where(users.c.email == credentials["email"])
            ):
                raise ValueError("Demo email already belongs to another account")
            await conn.execute(
                organizations.insert().values(
                    id=oid,
                    name="Guided Review Demo · synthetic",
                    created_at=stamp,
                    description="Synthetic local demonstration; not production evaluation evidence",
                )
            )
            await conn.execute(
                users.insert().values(
                    id=uid,
                    email=credentials["email"],
                    name="Guided demo administrator",
                    password_hash=await password_hash(credentials["password"]),
                    verified=True,
                    active=True,
                    created_at=stamp,
                )
            )
            await conn.execute(
                memberships.insert().values(
                    organization_id=oid, user_id=uid, role="Admin", active=True, revision=1
                )
            )

            async def add(kind: str, key: str, **extra) -> None:
                """Validate demo writes with normal input schemas before the owner insert."""
                data = (
                    TypeAdapter(Input)
                    .validate_python(
                        dict(
                            kind=kind,
                            name="Demo " + key,
                            description="Synthetic guided review example",
                            **extra,
                        )
                    )
                    .model_dump(exclude={"kind"})
                )
                data.update(
                    id=ident(key),
                    organization_id=oid,
                    revision=1,
                    created_at=stamp,
                    updated_at=stamp,
                )
                if kind == "projects":
                    data["created_by"] = uid
                target = risks if kind == "risks" else TABLES[kind]
                await conn.execute(target.insert().values(**data))

            today = stamp.date()
            await add("settings", "settings", timezone="Asia/Kolkata", currency="INR")
            await add("portfolios", "portfolio")
            await add("teams", "team")
            await add(
                "projects",
                "project",
                portfolio_id=ident("portfolio"),
                team_id=ident("team"),
                currency="INR",
                ledger_complete=True,
                status="active",
                reported_health="Green",
                start_date=today - timedelta(days=7),
                target_end_date=today + timedelta(days=14),
                forecast_end_date=today + timedelta(days=21),
            )
            await add(
                "budget_lines",
                "budget",
                project_id=ident("project"),
                amount="100000",
                currency="INR",
                approved=True,
            )
            await add(
                "expenditures",
                "spend",
                project_id=ident("project"),
                amount="112500",
                currency="INR",
                spent_on=today,
            )
            await add(
                "milestones",
                "overdue milestone",
                project_id=ident("project"),
                critical=True,
                due_date=today - timedelta(days=2),
            )
            await add(
                "risks",
                "supplier risk",
                project_id=ident("project"),
                severity=4,
                likelihood=3,
                review_on=today,
            )
            await add(
                "sprints",
                "sprint",
                project_id=ident("project"),
                team_id=ident("team"),
                start_date=today - timedelta(days=7),
                end_date=today + timedelta(days=7),
                status="active",
            )
        print(
            json.dumps(
                dict(
                    organization_id=str(oid),
                    project_id=str(ident("project")),
                    status="created_synthetic_demo",
                )
            )
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
