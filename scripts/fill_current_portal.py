"""Fill the specifically authorized local portal with clearly fictional demo records.

Reuses a live Admin session and the restricted application's validated, audited commands.
No credentials, memberships, project ownership or unrelated records are replaced.
The complete operation is atomic; reruns preserve existing records and edits.
"""

import asyncio
import json
import os
from uuid import UUID, uuid4

import ppm_api.command_tables  # noqa: F401 — register risk/benefit/metric tables
import sqlalchemy as sa
from fastapi import Request
from ppm_api import delivery
from ppm_api.config import load_settings
from ppm_api.identity import Principal, context, now
from ppm_api.identity_tables import memberships, sessions, users
from ppm_api.ppm_tables import TABLES
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

PROJECT = UUID("1c152bcb-ff85-4f5b-9c18-2678ba4af628")
ORG = UUID("179d3d14-5d1a-45b7-b3e9-a4d4f31d4265")
ADMIN = UUID("082042d4-09c6-4a33-b814-7e8ded465d28")
MANAGER = UUID("e33aceb1-937e-4af4-bf66-fc44a584ee73")
COORDINATOR = UUID("ff0d4cfb-99cf-4029-9c49-cdebd1242b09")
VIEWER = UUID("e5b3b755-714a-4491-ac41-6e702c2a4be9")
KINDS = (
    "work_items",
    "milestones",
    "sprints",
    "blockers",
    "risks",
    "benefits",
    "metric_plans",
    "dependencies",
    "budget_lines",
    "expenditures",
    "status_updates",
    "baselines",
    "alignments",
    "grants",
)


async def run():
    config = load_settings()
    owner_url = os.environ["PPM_MIGRATION_DATABASE_URL"]
    if config.app_env != "local" or any(
        make_url(url).database != "ppm_local"
        for url in (owner_url, config.database_url.get_secret_value())
    ):
        raise SystemExit("Restricted to the diagnosed local portal/database")
    owner = create_async_engine(owner_url)
    app = create_async_engine(config.database_url.get_secret_value())
    folder = config.storage_root / "__current_portal__"
    folder.mkdir(parents=True, exist_ok=True)
    created, reused = [], []
    try:
        async with owner.begin() as conn:
            project = (
                (
                    await conn.execute(
                        sa.select(TABLES["projects"]).where(TABLES["projects"].c.id == PROJECT)
                    )
                )
                .mappings()
                .one()
            )
            if (
                project["organization_id"] != ORG
                or project["name"] != "Customer Onboarding Portal"
                or project["archived"]
            ):
                raise RuntimeError("Target project changed; refusing inferred changes")
            people = {
                row["id"]: dict(row)
                for row in (
                    await conn.execute(
                        sa.select(
                            users.c.id,
                            users.c.name,
                            users.c.active,
                            users.c.verified,
                            memberships.c.role,
                        )
                        .join(memberships, memberships.c.user_id == users.c.id)
                        .where(memberships.c.organization_id == ORG, memberships.c.active)
                    )
                ).mappings()
            }
            expected = {
                ADMIN: ("Ashu", "Admin"),
                MANAGER: ("Hement", "Project Manager"),
                COORDINATOR: ("Alok Gupta", "Project Manager"),
                VIEWER: ("Blaze", "Viewer"),
            }
            for uid, (name, role) in expected.items():
                person = people.get(uid)
                if (
                    not person
                    or person["name"] != name
                    or person["role"] != role
                    or not person["active"]
                    or not person["verified"]
                ):
                    raise RuntimeError("Expected active member/role changed")
            session = (
                (
                    await conn.execute(
                        sa.select(
                            sessions.c.id,
                            sessions.c.user_id,
                            sessions.c.organization_id,
                            sessions.c.expires_at,
                            sessions.c.revoked,
                        )
                        .where(
                            sessions.c.user_id == ADMIN,
                            sessions.c.organization_id == ORG,
                            ~sessions.c.revoked,
                            sessions.c.expires_at > now(),
                        )
                        .order_by(sessions.c.created_at.desc())
                        .limit(1)
                    )
                )
                .mappings()
                .first()
            )
            if not session:
                raise RuntimeError("Sign in as the current organization Admin before this fill")
            before = {}
            for kind in KINDS:
                table = TABLES[kind]
                before[kind] = delivery.encode(
                    [
                        dict(row)
                        for row in (
                            await conn.execute(
                                sa.select(table).where(
                                    table.c.organization_id == ORG, table.c.project_id == PROJECT
                                )
                            )
                        ).mappings()
                    ]
                )
            backup = folder / "before.json"
            if not backup.exists():
                backup.write_text(json.dumps(before, indent=2))
                backup.chmod(0o600)
        async with app.begin() as conn:
            await context(conn, ADMIN, ORG, "Admin")
            principal = Principal(conn, people[ADMIN], dict(session), "Admin")
            request = Request(
                {"type": "http", "headers": [(b"x-organization-id", str(ORG).encode())]}
            )
            request.state.request_id = str(uuid4())
            await delivery.lock(principal, request)

            async def add(kind, name, **fields):
                table = TABLES[kind]
                conditions = [table.c.organization_id == ORG, table.c.name == name]
                if "project_id" in fields:
                    conditions.append(table.c.project_id == fields["project_id"])
                existing = (
                    (await conn.execute(sa.select(table).where(*conditions))).mappings().all()
                )
                if len(existing) > 1 or existing and existing[0]["archived"]:
                    raise RuntimeError("Ambiguous/archived demo record requires inspection")
                if existing:
                    reused.append(kind + ":" + name)
                    return existing[0]["id"]
                payload = delivery.adapter.validate_python({"kind": kind, "name": name, **fields})
                result = await delivery.write(principal, request, kind, payload, None, None, "")
                created.append(kind + ":" + name)
                return result["id"]

            async def child(kind, name, description, **fields):
                return await add(
                    kind,
                    name,
                    description="Fictional demo: " + description,
                    project_id=PROJECT,
                    **fields,
                )

            for uid, access in ((MANAGER, "edit"), (COORDINATOR, "edit"), (VIEWER, "read")):
                grants = TABLES["grants"]
                existing = (
                    (
                        await conn.execute(
                            sa.select(grants).where(
                                grants.c.organization_id == ORG,
                                grants.c.project_id == PROJECT,
                                grants.c.user_id == uid,
                            )
                        )
                    )
                    .mappings()
                    .first()
                )
                if existing:
                    if existing["archived"] or access == "edit" and existing["access"] == "read":
                        data = delivery.view("grants", existing)["data"].model_dump()
                        data.update(archived=False, access=access)
                        await delivery.write(
                            principal,
                            request,
                            "grants",
                            delivery.adapter.validate_python(data),
                            existing["id"],
                            existing["revision"],
                            "Authorized local demo project access",
                        )
                    reused.append("grants:" + existing["name"])
                else:
                    await child(
                        "grants",
                        f"{people[uid]['name']} — portal project {access}",
                        "Explicit project access for the existing active organization member.",
                        user_id=uid,
                        access=access,
                    )

            calendar = await add(
                "calendars",
                "Portal India weekday calendar — v1",
                description="Fictional demo: immutable eight-hour India weekday planning calendar.",
                timezone="Asia/Kolkata",
                monday="8",
                tuesday="8",
                wednesday="8",
                thursday="8",
                friday="8",
                saturday="0",
                sunday="0",
                holidays="",
            )
            sprint1 = await child(
                "sprints",
                "Portal Sprint 1 — requirements and first slice",
                "Confirm scope, obtain validation examples and build the first onboarding form.",
                team_id=project["team_id"],
                start_date="2026-10-12",
                end_date="2026-10-23",
                status="planned",
            )
            sprint2 = await child(
                "sprints",
                "Portal Sprint 2 — acceptance and release",
                "Integrate validation, perform acceptance checks and prepare release handover.",
                team_id=project["team_id"],
                start_date="2026-10-26",
                end_date="2026-11-06",
                status="planned",
            )
            work = []
            for name, desc, kind, owner_id, sprint, points, start, due, status, blocked in [
                (
                    "Confirm onboarding requirements",
                    "Capture fields, validation rules, decision owners and acceptance criteria.",
                    "story",
                    MANAGER,
                    sprint1,
                    "3",
                    "2026-10-12",
                    "2026-10-14",
                    "ready",
                    False,
                ),
                (
                    "Design onboarding experience",
                    "Define accessible form layout, field hints and failure states.",
                    "task",
                    COORDINATOR,
                    sprint1,
                    "3",
                    "2026-10-14",
                    "2026-10-16",
                    "backlog",
                    False,
                ),
                (
                    "Build onboarding form",
                    "Implement required fields and clear validation errors; awaiting "
                    "representative examples.",
                    "feature",
                    MANAGER,
                    sprint1,
                    "5",
                    "2026-10-15",
                    "2026-10-23",
                    "backlog",
                    True,
                ),
                (
                    "Integrate validation and notifications",
                    "Connect validation rules and confirmation receipts without exposing private "
                    "data.",
                    "feature",
                    COORDINATOR,
                    sprint2,
                    "5",
                    "2026-10-26",
                    "2026-10-30",
                    "backlog",
                    False,
                ),
                (
                    "Run acceptance checks",
                    "Test valid/invalid input, keyboard navigation and agreed error handling.",
                    "task",
                    COORDINATOR,
                    sprint2,
                    "3",
                    "2026-11-02",
                    "2026-11-04",
                    "backlog",
                    False,
                ),
                (
                    "Prepare release and handover",
                    "Record release checklist, rollback procedure and support ownership.",
                    "task",
                    MANAGER,
                    sprint2,
                    "2",
                    "2026-11-05",
                    "2026-11-06",
                    "backlog",
                    False,
                ),
            ]:
                work.append(
                    await child(
                        "work_items",
                        name,
                        desc,
                        work_type=kind,
                        priority="high" if blocked or kind == "story" else "normal",
                        owner_id=owner_id,
                        sprint_id=sprint,
                        points=points,
                        start_date=start,
                        due_date=due,
                        status=status,
                        blocked=blocked,
                    )
                )
            for name, due, desc in [
                (
                    "Requirements agreed",
                    "2026-10-14",
                    "Scope and acceptance criteria reviewed by the named decision owner.",
                ),
                (
                    "Acceptance checks complete",
                    "2026-11-04",
                    "Planned acceptance gate; no completed customer approval is claimed.",
                ),
                (
                    "Portal release and handover",
                    "2026-11-06",
                    "Planned release readiness and support handover before the project target "
                    "date.",
                ),
            ]:
                await child("milestones", name, desc, due_date=due, critical=True)
            await child(
                "blockers",
                "Awaiting validation examples",
                "Valid and invalid customer examples are required before the form rules can be "
                "completed.",
                work_item_id=work[2],
                owner_id=MANAGER,
                status="open",
            )
            for name, desc, owner_id, severity, likelihood, mitigation, review in [
                (
                    "Customer validation rules may arrive late",
                    "Late rules could delay development and acceptance.",
                    MANAGER,
                    3,
                    3,
                    "Review examples with stakeholders before form development; keep the blocker "
                    "and owner visible.",
                    "2026-10-16",
                ),
                (
                    "Acceptance coverage may miss accessibility cases",
                    "Incomplete keyboard/error-state checks could delay the release gate.",
                    COORDINATOR,
                    4,
                    2,
                    "Include keyboard-only, screen-reader labels and invalid-input cases in "
                    "acceptance checks.",
                    "2026-10-30",
                ),
            ]:
                await child(
                    "risks",
                    name,
                    desc,
                    owner_id=owner_id,
                    severity=severity,
                    likelihood=likelihood,
                    mitigation=mitigation,
                    review_on=review,
                    status="open",
                )
            for name, unit, target, desc in [
                (
                    "Onboarding administration hours saved",
                    "hours saved",
                    "100",
                    "Target for reduced manual follow-up; realized outcome remains unknown.",
                ),
                (
                    "Customer onboarding cycle time reduction",
                    "percent reduction",
                    "25",
                    "Target improvement from self-service; not yet measured or independently "
                    "verified.",
                ),
            ]:
                await child(
                    "benefits",
                    name,
                    desc,
                    unit=unit,
                    target=target,
                    realized=None,
                    period_start="2026-10-12",
                    period_end="2026-11-19",
                )
            for name, amount, desc in [
                (
                    "Portal implementation budget",
                    "160000",
                    "Example approved allocation for form, validation and integration work.",
                ),
                (
                    "Portal acceptance and release budget",
                    "40000",
                    "Example approved allocation for acceptance and release preparation.",
                ),
            ]:
                await child(
                    "budget_lines",
                    name,
                    desc,
                    amount=amount,
                    currency=project["currency"],
                    approved=True,
                )
            for name, amount, spent_on, desc in [
                (
                    "Portal discovery workshop",
                    "12000",
                    "2026-10-10",
                    "Example workshop expense; fictional amount, not an actual payment.",
                ),
                (
                    "Portal design preparation",
                    "8000",
                    "2026-10-10",
                    "Example design preparation expense; fictional amount, not an actual payment.",
                ),
            ]:
                await child(
                    "expenditures",
                    name,
                    desc,
                    amount=amount,
                    currency=project["currency"],
                    spent_on=spent_on,
                )
            for index, (source, target) in enumerate(((0, 2), (2, 3), (3, 4)), 1):
                await child(
                    "dependencies",
                    f"Portal delivery dependency {index}",
                    "Predecessor must be ready before successor delivery; acyclic work-item "
                    "planning link.",
                    target_project_id=PROJECT,
                    source_work_item_id=work[source],
                    target_work_item_id=work[target],
                )
            alignment = TABLES["alignments"]
            if not await conn.scalar(
                sa.select(alignment.c.id)
                .where(alignment.c.project_id == PROJECT, ~alignment.c.archived)
                .limit(1)
            ):
                goals = TABLES["goals"]
                goal = await conn.scalar(
                    sa.select(goals.c.id).where(
                        goals.c.name == "Reduce customer onboarding effort", ~goals.c.archived
                    )
                )
                if not goal:
                    goal = await add(
                        "goals",
                        "Reduce customer onboarding effort",
                        description="Fictional demo: strategic target for self-service onboarding.",
                        owner_id=ADMIN,
                    )
                await child(
                    "alignments",
                    "Portal contribution to onboarding goal",
                    "Declared contribution to the existing onboarding goal; not measured realized"
                    " impact.",
                    goal_id=goal,
                    weight="1",
                    contribution="0.8",
                )
            for name, desc, health in [
                (
                    "Portal initial planning update",
                    "Owners, two sprints, budget and delivery gates are planned; no release "
                    "completion claimed.",
                    "Green",
                ),
                (
                    "Portal validation risk update",
                    "Validation examples are outstanding. Hement owns mitigation; review 16 "
                    "October. Alok owns accessibility acceptance coverage.",
                    "Amber",
                ),
            ]:
                await child("status_updates", name, desc, reported_health=health)
            baseline = await child(
                "baselines",
                "Portal initial delivery baseline — v1",
                "Freeze the populated fictional scope, two sprints, six work items, critical "
                "milestones and INR 200000 approved budget before subsequent edits.",
            )
            await child(
                "metric_plans",
                "Portal delivery measurement plan — v1",
                "Use the preserved baseline and India working calendar; INR 210000 is a manual "
                "example forecast, not AI output.",
                baseline_id=baseline,
                calendar_id=calendar,
                forecast_cost="210000",
            )
            counts = {}
            for kind in KINDS:
                table = TABLES[kind]
                counts[kind] = int(
                    await conn.scalar(
                        sa.select(sa.func.count())
                        .select_from(table)
                        .where(
                            table.c.organization_id == ORG,
                            table.c.project_id == PROJECT,
                            ~table.c.archived,
                        )
                    )
                    or 0
                )
                if not counts[kind]:
                    raise RuntimeError(f"Required section still empty: {kind}")
            for uid in (MANAGER, COORDINATOR, VIEWER):
                role = people[uid]["role"]
                await context(conn, uid, ORG, role)
                allowed = await delivery.can_edit(
                    Principal(conn, people[uid], {"organization_id": ORG}, role), PROJECT
                )
                if allowed != (uid != VIEWER):
                    raise RuntimeError("Effective project permission does not match assigned role")
        result = {
            "project_id": str(PROJECT),
            "organization_id": str(ORG),
            "created": created,
            "reused": reused,
            "counts": counts,
            "roles": {person["name"]: person["role"] for person in people.values()},
            "project_access": {
                "Ashu": "Admin",
                "Hement": "edit",
                "Alok Gupta": "edit",
                "Blaze": "read",
            },
        }
        (folder / "result.json").write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
    finally:
        await app.dispose()
        await owner.dispose()


if __name__ == "__main__":
    asyncio.run(run())
