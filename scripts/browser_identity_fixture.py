"""Generate private, disposable browser credentials in ppm_test only."""

import asyncio
import json
import os
import secrets
from uuid import uuid4

from ppm_api.config import load_settings
from ppm_api.identity import now, password_hash
from ppm_api.identity_tables import memberships, organizations, users
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


async def run() -> None:
    config = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if config.app_env != "test" or make_url(url).database != "ppm_test":
        raise SystemExit("Browser fixtures are restricted to ppm_test")
    password = secrets.token_urlsafe(24)
    email = f"browser-{uuid4()}@example.com"
    ids = [uuid4() for _ in range(6)]
    a, b, uid, other, capacity_org, capacity_user = ids
    capacity_email = f"capacity-{capacity_user}@example.com"
    assessment_org, assessment_user, assessment_reviewer = uuid4(), uuid4(), uuid4()
    assessment_email = f"assessment-{assessment_user}@example.com"
    reviewer_email = f"reviewer-{assessment_reviewer}@example.com"
    integration_org, integration_user = uuid4(), uuid4()
    integration_email = f"integration-{integration_user}@example.com"
    command_org, command_user = uuid4(), uuid4()
    command_email = f"command-{command_user}@example.com"
    document_org, document_user = uuid4(), uuid4()
    ai_org, ai_user = uuid4(), uuid4()
    ai_email = f"ai-{ai_user}@example.com"
    document_email = f"documents-{document_user}@example.com"
    hashed = await password_hash(password)
    no_org_user = uuid4()
    no_org_email = f"account-only-{no_org_user}@example.com"
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            for oid in (
                a,
                b,
                capacity_org,
                assessment_org,
                command_org,
                integration_org,
                document_org,
                ai_org,
            ):
                await conn.execute(
                    organizations.insert().values(
                        id=oid, name="Acceptance organization", created_at=now()
                    )
                )
            for user, address in [
                (no_org_user, no_org_email),
                (integration_user, integration_email),
                (command_user, command_email),
                (document_user, document_email),
                (ai_user, ai_email),
                (uid, email),
                (other, f"{other}@example.com"),
                (capacity_user, capacity_email),
                (assessment_user, assessment_email),
                (assessment_reviewer, reviewer_email),
            ]:
                await conn.execute(
                    users.insert().values(
                        id=user,
                        email=address,
                        name="Acceptance administrator",
                        verified=True,
                        password_hash=hashed,
                        created_at=now(),
                    )
                )
            for oid, user, role in [
                (integration_org, integration_user, "Admin"),
                (b, integration_user, "Viewer"),
                (command_org, command_user, "Admin"),
                (document_org, document_user, "Admin"),
                (ai_org, ai_user, "Admin"),
                (b, ai_user, "Viewer"),
                (b, document_user, "Viewer"),
                (b, command_user, "Viewer"),
                (a, uid, "Admin"),
                (b, uid, "Viewer"),
                (b, other, "Admin"),
                (capacity_org, capacity_user, "Admin"),
                (b, capacity_user, "Viewer"),
                (assessment_org, assessment_user, "Admin"),
                (assessment_org, assessment_reviewer, "Project Manager"),
            ]:
                await conn.execute(
                    memberships.insert().values(
                        organization_id=oid, user_id=user, role=role, active=True, revision=1
                    )
                )
        from browser_pilot_fixture import run as pilot_fixture

        pilot = await pilot_fixture(password)
        print(
            json.dumps(
                {
                    **pilot,
                    "ai_org": str(ai_org),
                    "ai_email": ai_email,
                    "document_org": str(document_org),
                    "document_user": str(document_user),
                    "document_email": document_email,
                    "integration_org": str(integration_org),
                    "integration_email": integration_email,
                    "command_org": str(command_org),
                    "command_user": str(command_user),
                    "command_email": command_email,
                    "email": email,
                    "no_org_email": no_org_email,
                    "password": password,
                    "admin_org": str(a),
                    "viewer_org": str(b),
                    "capacity_org": str(capacity_org),
                    "capacity_email": capacity_email,
                    "assessment_org": str(assessment_org),
                    "assessment_user": str(assessment_user),
                    "assessment_reviewer": str(assessment_reviewer),
                    "assessment_email": assessment_email,
                    "reviewer_email": reviewer_email,
                }
            )
        )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
