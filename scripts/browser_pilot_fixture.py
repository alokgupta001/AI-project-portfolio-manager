"""125-record browser cohort, confined to the browser runner's ppm_test database."""

import os
from uuid import uuid4

from ppm_api import assessment_tables as A
from ppm_api.assessment_schemas import FrameworkInput
from ppm_api.identity import now, password_hash
from ppm_api.identity_tables import memberships, organizations, users
from ppm_api.main import create_app  # noqa: F401 — register current table metadata
from ppm_api.ppm_schemas import PortfolioInput, ProjectInput, SettingsInput, WorkInput
from ppm_api.ppm_tables import TABLES
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


async def run(password: str) -> dict:
    url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if os.environ.get("PPM_APP_ENV") != "test" or make_url(url).database != "ppm_test":
        raise SystemExit("Refusing pilot fixture outside ppm_test")
    org, admin, pm, viewer, portfolio, department, framework, version = [uuid4() for _ in range(8)]
    engine = create_async_engine(url)
    hashed = await password_hash(password)
    emails = {
        "admin": f"pilot-{admin}@example.com",
        "pm": f"pilot-{pm}@example.com",
        "viewer": f"pilot-{viewer}@example.com",
    }
    try:
        async with engine.begin() as conn:
            await conn.execute(
                organizations.insert().values(id=org, name="Pilot fixture", created_at=now())
            )
            for user, role, key in [
                (admin, "Admin", "admin"),
                (pm, "Project Manager", "pm"),
                (viewer, "Viewer", "viewer"),
            ]:
                await conn.execute(
                    users.insert().values(
                        id=user,
                        email=emails[key],
                        name="Pilot " + key,
                        password_hash=hashed,
                        verified=True,
                        created_at=now(),
                    )
                )
                await conn.execute(
                    memberships.insert().values(
                        organization_id=org, user_id=user, role=role, active=True, revision=1
                    )
                )
            for i in range(125):
                user = uuid4()
                await conn.execute(
                    users.insert().values(
                        id=user,
                        email=f"pilot-{user}@example.com",
                        name=f"Pilot member {i:03}",
                        password_hash=None,
                        verified=False,
                        created_at=now(),
                    )
                )
                await conn.execute(
                    memberships.insert().values(
                        organization_id=org, user_id=user, role="Viewer", active=True, revision=1
                    )
                )

            async def delivery(kind, id_, data, **extra):
                await conn.execute(
                    TABLES[kind]
                    .insert()
                    .values(
                        id=id_,
                        organization_id=org,
                        revision=1,
                        created_at=stamp,
                        updated_at=stamp,
                        **data,
                        **extra,
                    )
                )

            stamp = now()
            await delivery(
                "settings",
                uuid4(),
                SettingsInput(
                    name="Pilot settings", timezone="Asia/Kolkata", currency="INR"
                ).model_dump(exclude={"kind"}),
            )
            await delivery(
                "portfolios",
                portfolio,
                PortfolioInput(name="Pilot portfolio").model_dump(exclude={"kind"}),
            )
            await delivery(
                "departments",
                department,
                {
                    "name": "Pilot department",
                    "description": "Fixture",
                    "archived": False,
                    "owner_id": None,
                },
            )
            definition = FrameworkInput.model_validate(
                {
                    "name": "Pilot framework",
                    "dimensions": [
                        {
                            "name": "Governance",
                            "weight": "1",
                            "questions": [
                                {
                                    "name": "Practice",
                                    "text": "Practice defined?",
                                    "answer_type": "boolean",
                                    "weight": "1",
                                }
                            ],
                        }
                    ],
                }
            ).model_dump(mode="json")
            await conn.execute(
                A.frameworks.insert().values(
                    id=framework,
                    organization_id=org,
                    created_at=stamp,
                    revision=1,
                    definition=definition,
                )
            )
            await conn.execute(
                A.framework_versions.insert().values(
                    id=version,
                    organization_id=org,
                    created_at=stamp,
                    framework_id=framework,
                    version=1,
                    snapshot=definition,
                    published_by=admin,
                )
            )
            projects = []
            assessments = []
            for i in range(125):
                project = uuid4()
                projects.append(project)
                await delivery(
                    "projects",
                    project,
                    ProjectInput(
                        name=f"Pilot project {i:03}",
                        portfolio_id=portfolio,
                        currency="INR",
                        industry="fintech" if i == 124 else None,
                    ).model_dump(exclude={"kind"}),
                    created_by=admin,
                )
                await delivery(
                    "resources",
                    uuid4(),
                    {
                        "name": f"Pilot resource {i:03}",
                        "description": "Fixture",
                        "archived": False,
                        "user_id": None,
                    },
                )
                aid = uuid4()
                assessments.append(aid)
                await conn.execute(
                    A.assessments.insert().values(
                        id=aid,
                        organization_id=org,
                        created_at=stamp,
                        framework_version_id=version,
                        name=f"Pilot assessment {i:03}",
                        department_id=department,
                        assigned_to=admin,
                        reviewer_id=pm,
                        status="completed",
                        revision=1,
                        results={"overall_score": "75", "dimension_scores": [], "notes": []},
                    )
                )
            project = projects[-1]
            grant = uuid4()
            await delivery(
                "grants",
                grant,
                {
                    "name": "Pilot PM edit",
                    "description": "Fixture",
                    "archived": False,
                    "user_id": pm,
                    "project_id": project,
                    "portfolio_id": None,
                    "access": "edit",
                },
            )
            work = uuid4()
            await delivery(
                "work_items",
                work,
                WorkInput(
                    name="Pilot assigned work",
                    project_id=project,
                    owner_id=pm,
                    due_date="2026-11-01",
                ).model_dump(exclude={"kind"}),
            )
        return {
            "pilot_org": str(org),
            "pilot_email": emails["admin"],
            "pilot_pm_email": emails["pm"],
            "pilot_viewer_email": emails["viewer"],
            "pilot_pm": str(pm),
            "pilot_viewer": str(viewer),
            "pilot_project": str(project),
            "pilot_work": str(work),
            "pilot_grant": str(grant),
            "pilot_assessment": str(assessments[-1]),
            "pilot_version": str(version),
        }
    finally:
        await engine.dispose()
