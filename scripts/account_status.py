"""Explicit development operator account status; organization Admin is not global authority.

Requires the migration-owner connection. Does not remove memberships or ownership.
Disabling revokes sessions; enabling requires a fresh login and restores no grants.
"""

import argparse
import asyncio
import os
from uuid import UUID

import sqlalchemy as sa
from ppm_api.config import load_settings
from ppm_api.identity_tables import memberships, sessions, users
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


async def set_status(conn, user_id: UUID, active: bool) -> bool:
    await conn.execute(sa.text("SELECT pg_advisory_xact_lock(10102027)"))
    user = (
        (await conn.execute(sa.select(users).where(users.c.id == user_id).with_for_update()))
        .mappings()
        .one()
    )
    if user["active"] == active:
        return False
    if not active:
        orgs = list(
            await conn.scalars(
                sa.select(memberships.c.organization_id)
                .where(
                    memberships.c.user_id == user_id,
                    memberships.c.active,
                    memberships.c.role == "Admin",
                )
                .order_by(memberships.c.organization_id)
            )
        )
        for oid in orgs:
            await conn.execute(
                sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"),
                {"org": str(oid)},
            )
            count = await conn.scalar(
                sa.select(sa.func.count())
                .select_from(memberships.join(users, users.c.id == memberships.c.user_id))
                .where(
                    memberships.c.organization_id == oid,
                    memberships.c.active,
                    memberships.c.role == "Admin",
                    users.c.active,
                    users.c.verified,
                    users.c.id != user_id,
                )
            )
            if not count:
                raise ValueError("Assign another active Admin before disabling this account")
        await conn.execute(
            sessions.update().where(sessions.c.user_id == user_id).values(revoked=True)
        )
    await conn.execute(users.update().where(users.c.id == user_id).values(active=active))
    return True


async def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user_id", type=UUID)
    parser.add_argument("status", choices=["enable", "disable"])
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    if not args.reason.strip():
        parser.error("A nonempty operator reason is required")
    config = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    expected = {"local": "ppm_local", "test": "ppm_test", "demo": "ppm_demo"}
    if make_url(url).database != expected.get(config.app_env):
        raise SystemExit("Restricted to matching development/test/demo database")
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            changed = await set_status(conn, args.user_id, args.status == "enable")
        print(f"Account {args.user_id}: {args.status}; changed={changed}. Memberships preserved.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
