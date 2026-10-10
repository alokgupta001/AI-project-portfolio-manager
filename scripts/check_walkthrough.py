"""Read-only integrity and content fingerprint for the reserved walkthrough organization."""

import asyncio
import hashlib
import json
import os
from uuid import UUID

import sqlalchemy as sa
from ppm_api.assessment_tables import assessments, framework_versions, frameworks
from ppm_api.config import load_settings
from ppm_api.identity_tables import memberships, users
from ppm_api.ppm_tables import TABLES
from seed_walkthrough import ident
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


async def run():
    config = load_settings()
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    expected = {"local": "ppm_local", "test": "ppm_test", "demo": "ppm_demo"}
    if make_url(url).database != expected.get(config.app_env):
        raise SystemExit("Restricted to matching development/test/demo database")
    manifest = json.loads((config.storage_root / "__walkthrough__" / "manifest.json").read_text())
    oid = ident("organization")
    engine = create_async_engine(url)
    try:
        async with engine.connect() as conn:
            roles = {}
            for key, role in [
                ("asha", "Admin"),
                ("priya", "Project Manager"),
                ("ravi", "Project Manager"),
                ("vera", "Viewer"),
            ]:
                row = (
                    await conn.execute(
                        sa.select(
                            memberships.c.role,
                            memberships.c.active,
                            users.c.verified,
                            users.c.active.label("account_active"),
                        )
                        .join(users, users.c.id == memberships.c.user_id)
                        .where(memberships.c.organization_id == oid, users.c.id == ident(key))
                    )
                ).one()
                assert row.role == role and row.active and row.verified and row.account_active, key
                roles[key] = role
            records = {}
            for key, value in manifest.items():
                table = (
                    {
                        "framework": frameworks,
                        "version": framework_versions,
                        "assessment": assessments,
                    }[key]
                    if ":" not in key
                    else TABLES[key.split(":")[0]]
                )
                row = (
                    (await conn.execute(sa.select(table).where(table.c.id == UUID(value))))
                    .mappings()
                    .one()
                )
                assert row["organization_id"] == oid, key
                records[key] = dict(row)
            project = records["projects:Customer Onboarding Portal"]
            assert project["portfolio_id"] == UUID(
                manifest["portfolios:Customer Experience Portfolio"]
            )
            assert project["team_id"] == UUID(manifest["teams:Portal Delivery Team"])
            assessment = records["assessment"]
            assert assessment["assigned_to"] == ident("priya")
            assert assessment["reviewer_id"] == ident("ravi")
            assert assessment["framework_version_id"] == UUID(manifest["version"])
            for key, row in records.items():
                if "project_id" in row and row["project_id"] is not None:
                    assert row["project_id"] == project["id"], key
            counts = {}
            for kind, table in TABLES.items():
                count = await conn.scalar(
                    sa.select(sa.func.count())
                    .select_from(table)
                    .where(table.c.organization_id == oid)
                )
                if count:
                    counts[kind] = count
            checksum = hashlib.sha256(
                json.dumps(records, sort_keys=True, default=str).encode()
            ).hexdigest()
            print(
                json.dumps(
                    {
                        "status": "PASS",
                        "manifest_records": len(records),
                        "roles": roles,
                        "domain_counts": counts,
                        "content_sha256": checksum,
                        "sprint_status": records["sprints:Portal Sprint 1"]["status"],
                        "assessment_status": assessment["status"],
                    },
                    indent=2,
                )
            )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
