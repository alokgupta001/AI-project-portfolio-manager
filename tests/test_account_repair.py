"""Account independence, live tenant revocation and the reported Hement grant scenario."""

import os
from uuid import uuid4

import pytest
import sqlalchemy as sa
from ppm_api.identity_tables import memberships, organizations, users
from test_delivery import create, setup
from test_identity import PASSWORD, challenge, login, send
from test_identity import identity as identity

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


async def test_no_membership_login_refresh_personal_profile_and_logout(identity):
    c, app, owner, ids, emails = identity
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update().where(memberships.c.user_id == ids["pm"]).values(active=False)
        )
    result = await login(c, emails, "pm")
    assert result.json()["organization_id"] is None
    assert result.json()["role"] is None and result.json()["organizations"] == []
    assert (await c.get("/api/v1/auth/me")).status_code == 200
    assert (await c.get("/api/v1/delivery/projects")).status_code == 403
    assert (await send(c, "POST", "/auth/refresh")).status_code == 200
    assert (
        await send(c, "PATCH", "/auth/profile", json={"name": "Still an account"})
    ).status_code == 200
    assert (await c.get("/api/v1/auth/sessions")).json()["items"]
    assert (await send(c, "POST", "/auth/logout")).status_code == 200
    assert (await c.get("/api/v1/auth/me")).status_code == 401
    async with owner.connect() as conn:
        assert await conn.scalar(sa.select(users.c.active).where(users.c.id == ids["pm"]))


async def test_explicit_operator_status_preserves_memberships_and_last_admin(identity):
    from ppm_api.identity_tables import sessions

    from scripts.account_status import set_status

    c, app, owner, ids, emails = identity
    await login(c, emails, "pm")
    async with owner.begin() as conn:
        assert await set_status(conn, ids["pm"], False)
        assert not await set_status(conn, ids["pm"], False)
        assert await conn.scalar(
            sa.select(memberships.c.active).where(
                memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["pm"]
            )
        )
        assert await conn.scalar(
            sa.select(sessions.c.revoked).where(sessions.c.user_id == ids["pm"])
        )
    assert (await c.get("/api/v1/auth/me")).status_code == 401
    async with owner.begin() as conn:
        assert await set_status(conn, ids["pm"], True)
    assert (await c.get("/api/v1/auth/me")).status_code == 401
    assert (await login(c, emails, "pm")).status_code == 200
    with pytest.raises(ValueError, match="another active Admin"):
        async with owner.begin() as conn:
            await set_status(conn, ids["other"], False)


async def test_duplicate_grant_preserves_business_reason_and_record_count(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    await create(c, "grants", user_id=str(ids["pm"]), project_id=project["id"], access="edit")
    result = await send(
        c,
        "POST",
        "/delivery/grants",
        headers={"idempotency-key": str(uuid4())},
        json={
            "kind": "grants",
            "name": "Duplicate grant",
            "user_id": str(ids["pm"]),
            "project_id": project["id"],
            "access": "edit",
        },
    )
    assert result.status_code == 409
    assert "already has a grant" in result.json()["error"]["message"]
    assert result.json()["error"]["request_id"]
    async with owner.connect() as conn:
        from ppm_api.ppm_tables import TABLES

        g = TABLES["grants"]
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(g)
                .where(
                    g.c.organization_id == ids["a"],
                    g.c.user_id == ids["pm"],
                    g.c.project_id == project["id"],
                )
            )
            == 1
        )


async def test_admin_revocation_preserves_global_session_and_other_organization(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, "other", org=ids["b"])
    assert (
        await send(
            c,
            "PATCH",
            f"/organization/members/{ids['admin']}",
            json={"role": "Viewer", "active": False},
            headers={"if-match": "1"},
        )
    ).status_code == 200
    c.cookies.clear()
    await login(c, emails, org=ids["a"])
    assert (await c.get("/api/v1/organization/members")).status_code == 200
    assert (
        await send(c, "POST", "/auth/switch", json={"organization_id": str(ids["b"])})
    ).status_code == 404
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update()
            .where(memberships.c.user_id == ids["admin"], memberships.c.organization_id == ids["a"])
            .values(active=False)
        )
    assert (await c.get("/api/v1/auth/me")).status_code == 200
    assert (await c.get("/api/v1/organization/profile")).status_code == 403
    assert (await send(c, "POST", "/auth/refresh")).status_code == 200
    assert (await c.get("/api/v1/auth/me")).json()["organization_id"] is None


async def test_inactive_global_account_blocks_existing_session_login_reset_and_invitation(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, "pm")
    async with owner.begin() as conn:
        await conn.execute(users.update().where(users.c.id == ids["pm"]).values(active=False))
    assert (await c.get("/api/v1/auth/me")).status_code == 401
    assert (await send(c, "POST", "/auth/refresh")).status_code == 401
    assert (
        await send(c, "POST", "/auth/login", json={"email": emails["pm"], "password": PASSWORD})
    ).status_code == 401
    token = await challenge(owner, emails["pm"], "reset")
    assert (
        await send(
            c,
            "POST",
            "/auth/complete",
            json={"token": token, "password": PASSWORD, "name": "Disabled"},
        )
    ).status_code == 400
    token = await challenge(
        owner,
        emails["pm"],
        "invite",
        organization_id=ids["b"],
        inviter_id=ids["other"],
        role="Admin",
    )
    assert (
        await send(
            c,
            "POST",
            "/auth/complete",
            json={"token": token, "password": PASSWORD, "name": "Disabled"},
        )
    ).status_code == 400


async def test_profile_persistence_admin_relationship_validation_and_noop(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, org=ids["a"])
    profile = (await c.get("/api/v1/organization/profile")).json()
    assert profile["administrators"] == [{"id": str(ids["admin"]), "name": "Same member name"}]
    body = {
        "description": "Fictional training profile",
        "industry": "Technology",
        "website": "https://example.com/",
    }
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json=body,
            headers={"if-match": str(profile["revision"])},
        )
    ).status_code == 200
    saved = (await c.get("/api/v1/organization/profile")).json()
    assert all(saved[k] == v for k, v in body.items())
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json=body,
            headers={"if-match": str(saved["revision"])},
        )
    ).status_code == 200
    assert (await c.get("/api/v1/organization/profile")).json()["revision"] == saved["revision"]
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json={"website": "javascript:alert(1)"},
            headers={"if-match": str(saved["revision"])},
        )
    ).status_code == 422
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json={"name": " "},
            headers={"if-match": str(saved["revision"])},
        )
    ).status_code == 422
    c.cookies.clear()
    await login(c, emails, "viewer")
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json=body,
            headers={"if-match": str(saved["revision"])},
        )
    ).status_code == 403
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(organizations.c.description).where(organizations.c.id == ids["a"])
            )
            == body["description"]
        )


async def test_hement_sprint_requires_project_grant_and_planned_initial_state(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    team = await create(c, "teams", department_id=(await create(c, "departments"))["id"])
    await create(c, "grants", user_id=str(ids["pm"]), portfolio_id=portfolio["id"], access="manage")
    c.cookies.clear()
    await login(c, emails, "pm")
    body = {
        "kind": "sprints",
        "name": "Portal Sprint 1",
        "project_id": project["id"],
        "team_id": team["id"],
        "start_date": "2026-10-12",
        "end_date": "2026-10-23",
        "status": "planned",
    }
    denied = await send(
        c, "POST", "/delivery/sprints", json=body, headers={"idempotency-key": str(uuid4())}
    )
    assert (
        denied.status_code == 403
        and "Project edit grant required" in denied.json()["error"]["message"]
    )
    c.cookies.clear()
    await login(c, emails, org=ids["a"])
    await create(c, "grants", user_id=str(ids["pm"]), project_id=project["id"], access="edit")
    c.cookies.clear()
    await login(c, emails, "pm")
    invalid = await send(
        c,
        "POST",
        "/delivery/sprints",
        json=body | {"status": "active"},
        headers={"idempotency-key": str(uuid4())},
    )
    assert invalid.status_code == 422 and "planned sprint" in invalid.json()["error"]["message"]
    saved = await send(
        c, "POST", "/delivery/sprints", json=body, headers={"idempotency-key": str(uuid4())}
    )
    assert saved.status_code == 201 and saved.json()["organization_id"] == str(ids["a"])
    c.cookies.clear()
    await login(c, emails, "viewer")
    assert (
        await send(
            c, "POST", "/delivery/sprints", json=body, headers={"idempotency-key": str(uuid4())}
        )
    ).status_code in {403, 404}
