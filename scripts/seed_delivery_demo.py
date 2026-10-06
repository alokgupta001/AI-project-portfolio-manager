"""Idempotent, deterministic business fixtures in the isolated ppm_demo database only."""

import argparse
import asyncio
import os
from datetime import UTC, datetime
from uuid import NAMESPACE_URL, uuid5

import sqlalchemy as sa
from ppm_api.config import load_settings
from ppm_api.identity import issue_challenge
from ppm_api.identity_tables import memberships, organizations, users
from ppm_api.ppm_schemas import Input
from ppm_api.ppm_tables import TABLES
from pydantic import TypeAdapter
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

STAMP = datetime(2026, 10, 1, tzinfo=UTC)


def id_for(name: str):
    return uuid5(NAMESPACE_URL, "enterprise-ppm/demo-v1/" + name)


async def run() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", default="demo@example.com")
    args = parser.parse_args()
    from email_validator import validate_email

    email = validate_email(args.email, check_deliverability=False).normalized.lower()
    config = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if config.app_env != "demo" or make_url(url).database != "ppm_demo":
        raise SystemExit("Refusing business fixture writes outside demo/ppm_demo")
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            assert await conn.scalar(sa.text("SELECT current_database()")) == "ppm_demo"
            await conn.execute(sa.text("SELECT pg_advisory_xact_lock(400400)"))
            if await conn.scalar(
                sa.select(TABLES["settings"].c.id).where(
                    TABLES["settings"].c.id == id_for("a/settings")
                )
            ):
                print("Demo v1 already seeded; preserving all records and subsequent edits.")
                return
            uid = await conn.scalar(sa.select(users.c.id).where(users.c.email == email))
            if not uid:
                uid = id_for("admin/" + email)
                await conn.execute(
                    users.insert().values(
                        id=uid,
                        email=email,
                        name="Demo administrator",
                        password_hash=None,
                        verified=False,
                        created_at=STAMP,
                    )
                )
            other = id_for("other-admin")
            if not await conn.scalar(sa.select(users.c.id).where(users.c.id == other)):
                await conn.execute(
                    users.insert().values(
                        id=other,
                        email="other-demo@example.com",
                        name="Other organization Admin",
                        password_hash=None,
                        verified=False,
                        created_at=STAMP,
                    )
                )
            for key in ("a", "b"):
                oid = id_for(key + "/org")
                await conn.execute(
                    organizations.insert().values(
                        id=oid,
                        name="Northstar Demo" if key == "a" else "Separate Demo",
                        created_at=STAMP,
                    )
                )
                await conn.execute(
                    memberships.insert().values(
                        organization_id=oid,
                        user_id=uid if key == "a" else other,
                        role="Admin",
                        active=True,
                        revision=1,
                    )
                )

                async def add(kind: str, name: str, _key=key, _oid=oid, **extra):
                    ident = id_for(_key + "/" + name)
                    data = (
                        TypeAdapter(Input)
                        .validate_python(
                            {"kind": kind, "name": name.replace("_", " ").title(), **extra}
                        )
                        .model_dump(exclude={"kind"})
                    )
                    data.update(
                        id=ident,
                        organization_id=_oid,
                        created_at=STAMP,
                        updated_at=STAMP,
                        revision=1,
                    )
                    if kind == "projects":
                        data["created_by"] = uid if _key == "a" else other
                    await conn.execute(TABLES[kind].insert().values(**data))
                    return ident

                await add(
                    "settings",
                    "settings",
                    description="Isolated synthetic demo v1",
                    timezone="Asia/Kolkata",
                    currency="INR",
                )
                dep = await add("departments", "technology")
                team = await add("teams", "delivery_team", department_id=dep)
                goal = await add("goals", "reliable_delivery")
                portfolio = await add("portfolios", "transformation_portfolio")
                program = await add("programs", "digital_program", portfolio_id=portfolio)
                healthy = await add(
                    "projects",
                    "customer_portal",
                    portfolio_id=portfolio,
                    program_id=program,
                    department_id=dep,
                    team_id=team,
                    currency="INR",
                    status="active",
                    reported_health="Green",
                    start_date="2026-10-01",
                    target_end_date="2026-12-01",
                    forecast_end_date="2026-11-25",
                    ledger_complete=True,
                    description="Synthetic healthy delivery fixture",
                )
                troubled = await add(
                    "projects",
                    "erp_modernization",
                    portfolio_id=portfolio,
                    currency="USD",
                    status="active",
                    reported_health="Red",
                    start_date="2026-10-01",
                    target_end_date="2026-12-01",
                    forecast_end_date="2027-01-15",
                    description="Synthetic delayed project with partial cost coverage",
                )
                for project, label, currency, budget, spend in [
                    (healthy, "portal", "INR", "100000.00", "25000.25"),
                    (troubled, "erp", "USD", "50000.00", "55000.10"),
                ]:
                    await add(
                        "budget_lines",
                        label + "_budget",
                        project_id=project,
                        currency=currency,
                        amount=budget,
                    )
                    await add(
                        "expenditures",
                        label + "_spend",
                        project_id=project,
                        currency=currency,
                        amount=spend,
                        spent_on="2026-10-05",
                    )
                    await add(
                        "alignments",
                        label + "_goal",
                        project_id=project,
                        goal_id=goal,
                        weight="1",
                        contribution=".8",
                    )
                    await add(
                        "milestones",
                        label + "_launch",
                        project_id=project,
                        due_date="2026-12-01",
                        critical=True,
                    )
                work = await add(
                    "work_items",
                    "integration_work",
                    project_id=troubled,
                    status="in_progress",
                    blocked=True,
                    start_date="2026-10-01",
                    due_date="2026-11-20",
                )
                await add(
                    "blockers",
                    "vendor_access",
                    project_id=troubled,
                    work_item_id=work,
                    description="Synthetic vendor dependency",
                )
            verified = await conn.scalar(sa.select(users.c.verified).where(users.c.id == uid))
            if not verified:
                await issue_challenge(conn, config, email, "activate", id_for("a/org"))
        print(
            "Seeded isolated demo v1: two tenants, healthy/troubled projects, INR/USD budgets "
            "and work. Activation is in the private local mailbox; no email sent."
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
