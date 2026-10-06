"""Local operator creates an organization and delivers activation to the private spool."""

import argparse
import asyncio
import os
from uuid import uuid4

import sqlalchemy as sa
from email_validator import validate_email
from ppm_api.config import load_settings
from ppm_api.identity import issue_challenge, now
from ppm_api.identity_tables import memberships, organizations, users
from sqlalchemy.ext.asyncio import create_async_engine


async def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--organization", required=True)
    parser.add_argument("--additional-organization", action="store_true")
    args = parser.parse_args()
    settings = load_settings()
    email = validate_email(args.email, check_deliverability=False).normalized.lower()
    name = args.organization.strip()
    if not 1 <= len(name) <= 120:
        raise SystemExit("Organization name must contain 1–120 characters")
    url = os.environ.get("PPM_MIGRATION_DATABASE_URL")
    if not url:
        raise SystemExit("Run through the migrate service with local operator credentials")
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            await conn.execute(sa.text("SELECT pg_advisory_xact_lock(200200)"))
            if await conn.scalar(sa.select(sa.func.count()).select_from(organizations)):
                if not args.additional_organization:
                    raise SystemExit(
                        "Already initialized. Explicit --additional-organization required."
                    )
            user = (
                (await conn.execute(sa.select(users).where(users.c.email == email)))
                .mappings()
                .first()
            )
            uid = user["id"] if user else uuid4()
            oid = uuid4()
            if not user:
                await conn.execute(
                    users.insert().values(
                        id=uid,
                        email=email,
                        name="Administrator",
                        password_hash=None,
                        verified=False,
                        created_at=now(),
                    )
                )
            await conn.execute(organizations.insert().values(id=oid, name=name, created_at=now()))
            await conn.execute(
                memberships.insert().values(
                    organization_id=oid, user_id=uid, role="Admin", active=True, revision=1
                )
            )
            if not user or not user["verified"]:
                await issue_challenge(conn, settings, email, "activate", oid)
        print("Organization created. Activation is in the local mailbox if needed; no email sent.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
