"""One scoped development data correction for the confirmed Hement portal relationship."""

import asyncio
import os
from uuid import UUID, uuid5

import sqlalchemy as sa
from ppm_api.config import load_settings
from ppm_api.identity import now
from ppm_api.identity_tables import memberships, users
from ppm_api.ppm_schemas import GrantInput
from ppm_api.ppm_tables import TABLES
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

USER = UUID("e33aceb1-937e-4af4-bf66-fc44a584ee73")
PROJECT = UUID("1c152bcb-ff85-4f5b-9c18-2678ba4af628")


async def run():
    config = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if config.app_env != "local" or make_url(url).database != "ppm_local":
        raise SystemExit("This correction is restricted to the diagnosed local database")
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            user = (await conn.execute(sa.select(users).where(users.c.id == USER))).mappings().one()
            project = (
                (
                    await conn.execute(
                        sa.select(TABLES["projects"]).where(TABLES["projects"].c.id == PROJECT)
                    )
                )
                .mappings()
                .one()
            )
            oid = project["organization_id"]
            await conn.execute(
                sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"), {"org": str(oid)}
            )
            role = await conn.scalar(
                sa.select(memberships.c.role).where(
                    memberships.c.organization_id == oid,
                    memberships.c.user_id == USER,
                    memberships.c.active,
                )
            )
            grants = TABLES["grants"]
            portfolio_manage = await conn.scalar(
                sa.select(grants.c.id).where(
                    grants.c.organization_id == oid,
                    grants.c.user_id == USER,
                    grants.c.portfolio_id == project["portfolio_id"],
                    grants.c.access == "manage",
                    ~grants.c.archived,
                )
            )
            if (
                user["name"] != "Hement"
                or not user["active"]
                or role != "Project Manager"
                or project["name"] != "Customer Onboarding Portal"
                or project["archived"]
                or not portfolio_manage
            ):
                raise RuntimeError(
                    "Diagnosed relationship changed; refusing an inferred permission grant"
                )
            existing = await conn.scalar(
                sa.select(grants.c.id).where(
                    grants.c.organization_id == oid,
                    grants.c.user_id == USER,
                    grants.c.project_id == PROJECT,
                    grants.c.access.in_(["edit", "manage"]),
                    ~grants.c.archived,
                )
            )
            if existing:
                print("Hement already has the required scoped project grant; no change.")
                return
            data = GrantInput(
                name="Hement — portal project edit",
                description=(
                    "Authorized development repair: existing portfolio manager needs "
                    "explicit edit access to this administrator-created project."
                ),
                user_id=USER,
                project_id=PROJECT,
                access="edit",
            ).model_dump(exclude={"kind"})
            await conn.execute(
                grants.insert().values(
                    **data,
                    id=uuid5(USER, "portal-project-edit-repair"),
                    organization_id=oid,
                    revision=1,
                    created_at=now(),
                    updated_at=now(),
                )
            )
            print(
                "Created Hement's explicit portal project edit grant. "
                "Organization role and other grants preserved."
            )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
