"""Sprint 8.1 acceptance in the established isolated database and app-role environment."""

import asyncio
import json
import os
from datetime import timedelta
from uuid import uuid4

import pytest
import sqlalchemy as sa
from ppm_api.identity import context, digest, now
from ppm_api.identity_tables import challenges, memberships, organizations, users
from ppm_api.pilot import notify
from ppm_api.pilot_tables import notifications
from test_delivery import create
from test_identity import PASSWORD, login, send
from test_identity import identity as identity

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


def mailbox(app, email):
    return [
        json.loads(p.read_text())
        for p in (app.state.settings.storage_root / "__identity_mailbox__").glob("*.json")
        if json.loads(p.read_text())["to"] == email
    ]


async def test_registration_replacement_replay_and_organization(identity):
    c, app, owner, ids, emails = identity
    email = f"signup-{uuid4()}@example.com"
    body = {"email": email, "organization_name": "Pilot organization"}
    responses = await asyncio.gather(
        *[send(c, "POST", "/auth/register", json=body) for _ in range(2)]
    )
    assert [r.status_code for r in responses] == [200, 200]
    async with owner.connect() as conn:
        assert not await conn.scalar(sa.select(users.c.id).where(users.c.email == email))
        current = await conn.scalar(
            sa.select(challenges.c.token_hash).where(
                challenges.c.email == email, ~challenges.c.used
            )
        )
    mail = next(m for m in mailbox(app, email) if digest(m["link"].split("#token=")[1]) == current)
    token = mail["link"].split("#token=")[1]
    completion = {"token": token, "password": PASSWORD, "name": "New Admin"}
    assert (await send(c, "POST", "/auth/complete", json=completion)).status_code == 200
    assert (await send(c, "POST", "/auth/complete", json=completion)).status_code == 400
    await login(c, {"admin": email})
    me = (await c.get("/api/v1/auth/me")).json()
    assert me["role"] == "Admin" and len(me["organizations"]) == 1
    assert (await c.get("/api/v1/workspace/setup")).status_code == 200
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count()).select_from(users).where(users.c.email == email)
            )
            == 1
        )


async def test_invitation_resend_cancel_profile_roles_and_foreign_ids(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, org=ids["a"])
    email = f"invite-{uuid4()}@example.com"
    assert (
        await send(c, "POST", "/organization/invitations", json={"email": email, "role": "Viewer"})
    ).status_code == 201
    old = mailbox(app, email)[0]["link"].split("#token=")[1]
    # Simulate an invitation issued before migration0008; no old token/data rewrite.
    async with owner.begin() as conn:
        await conn.execute(
            challenges.update()
            .where(challenges.c.token_hash == digest(old))
            .values(invitation_id=None)
        )
    invitation = (await c.get("/api/v1/organization/invitations")).json()[0]
    path = "/organization/invitations/" + invitation["invitation_id"]
    assert old not in json.dumps(invitation) and "token_hash" not in invitation
    assert (await send(c, "POST", path + "/resend")).status_code == 200
    assert (
        await send(
            c,
            "POST",
            "/auth/complete",
            json={"token": old, "password": PASSWORD, "name": "Invited"},
        )
    ).status_code == 400
    invitation = (await c.get("/api/v1/organization/invitations")).json()[0]
    assert (
        await send(
            c, "POST", "/organization/invitations/" + invitation["invitation_id"] + "/cancel"
        )
    ).status_code == 200
    assert (await c.get("/api/v1/organization/invitations")).json() == []
    p = (await c.get("/api/v1/organization/profile")).json()
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json={"name": "Renamed pilot"},
            headers={"if-match": str(p["revision"])},
        )
    ).status_code == 200
    assert (
        await send(
            c,
            "PATCH",
            "/organization/profile",
            json={"name": "Stale"},
            headers={"if-match": str(p["revision"])},
        )
    ).status_code == 412
    for role in ["pm", "viewer", "other"]:
        c.cookies.clear()
        await login(c, emails, role)
        assert (await send(c, "POST", path + "/cancel")).status_code in [403, 404]
        if role != "other":
            assert (
                await send(
                    c,
                    "PATCH",
                    "/organization/profile",
                    json={"name": "Forbidden"},
                    headers={"if-match": "1"},
                )
            ).status_code == 403


async def test_notification_insert_app_role_and_dedup(identity):
    c, app, owner, ids, emails = identity
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        for _ in range(2):
            await notify(conn, ids["a"], ids["pm"], "work_items", uuid4(), "test-dedup")
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(notifications)
                .where(
                    notifications.c.event_key == "test-dedup",
                    notifications.c.organization_id == ids["a"],
                )
            )
            == 1
        )


async def test_search_125_records_roles_metadata_notifications_revocation(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, org=ids["a"])
    await create(c, "settings", timezone="Asia/Kolkata", currency="INR")
    portfolio = await create(c, "portfolios")
    projects = []
    for i in range(125):
        projects.append(
            await create(
                c,
                "projects",
                name=f"Pilot project {i:03}",
                portfolio_id=portfolio["id"],
                currency="INR",
                industry="fintech" if i == 124 else None,
            )
        )
    query = "/api/v1/workspace/search?kind=projects&q=Pilot&limit=100"
    first = (await c.get(query)).json()
    second = (await c.get(query + "&offset=100")).json()
    assert first["total"] == 125 and len(second["items"]) == 25
    assert len({r["id"] for r in first["items"] + second["items"]}) == 125
    assert (await c.get("/api/v1/workspace/search?q=%25")).json()["total"] == 0
    assert (await c.get("/api/v1/workspace/search?limit=101")).status_code == 422
    industry = (await c.get("/api/v1/delivery/projects?industry=fintech")).json()
    assert industry["total"] == 1 and industry["items"][0]["id"] == projects[-1]["id"]
    assert (await c.get("/api/v1/delivery/projects?industry=unknown")).json()["total"] == 124
    invalid = await send(
        c,
        "POST",
        "/delivery/projects",
        json={
            "kind": "projects",
            "name": "Invalid metadata",
            "portfolio_id": portfolio["id"],
            "currency": "INR",
            "priority": "invented",
            "industry": "invented",
        },
    )
    assert invalid.status_code == 422
    assert (await c.get("/api/v1/workspace/search?q=Invalid%20metadata")).json()["total"] == 0
    pid = projects[-1]["id"]
    await create(c, "grants", user_id=str(ids["pm"]), project_id=pid, access="edit")
    work = await create(
        c,
        "work_items",
        project_id=pid,
        owner_id=str(ids["pm"]),
        name="Assigned work",
        priority="high",
        work_type="bug",
    )
    assert (await create(c, "projects", portfolio_id=portfolio["id"], currency="INR"))["data"][
        "industry"
    ] is None
    c.cookies.clear()
    await login(c, emails, "pm")
    assert (await c.get("/api/v1/workspace/search?kind=projects&q=Pilot")).json()["total"] == 1
    assert (await c.get("/api/v1/workspace/my-work")).json()["items"][0]["id"] == work["id"]
    feed = (await c.get("/api/v1/workspace/notifications")).json()
    assert feed["total"] == 1
    nid = feed["items"][0]["id"]
    assert (
        await send(c, "PUT", "/workspace/notification-preference", json={"enabled": False})
    ).status_code == 200
    disabled = (await c.get("/api/v1/workspace/notifications")).json()
    assert disabled["enabled"] is False and disabled["total"] == 0
    assert (
        await send(c, "PUT", "/workspace/notification-preference", json={"enabled": True})
    ).status_code == 200
    assert (await c.get("/api/v1/workspace/notifications")).json()["total"] == 1
    assert (await send(c, "POST", f"/workspace/notifications/{nid}/read")).status_code == 200
    assert (await c.get("/api/v1/workspace/notifications")).json()["items"][0]["read"]
    async with owner.begin() as conn:
        await conn.execute(
            sa.text("UPDATE ppm_grants SET archived=true WHERE user_id=:u"), {"u": ids["pm"]}
        )
    assert (await c.get("/api/v1/workspace/my-work")).json()["total"] == 0
    assert (await c.get("/api/v1/workspace/notifications")).json()["total"] == 0
    c.cookies.clear()
    await login(c, emails, "other")
    assert (await c.get("/api/v1/workspace/search?q=Pilot")).json()["total"] == 0
    assert (await send(c, "POST", f"/workspace/notifications/{nid}/read")).status_code == 404


async def test_full_cohort_paging_result_grants_and_equal_timestamps(identity):
    from ppm_api import assessment_tables as A
    from test_assessment import fixture, ok

    c, app, owner, ids, emails, fw, v, a = await fixture(identity)
    department = a["department_id"]
    stamp = now()
    records = []
    async with owner.begin() as conn:
        for i in range(125):
            records.append(
                dict(
                    id=uuid4(),
                    organization_id=ids["a"],
                    created_at=stamp,
                    framework_version_id=v["id"],
                    name=f"Cohort {i:03}",
                    department_id=department,
                    assigned_to=ids["admin"],
                    reviewer_id=ids["pm"],
                    status="completed",
                    revision=1,
                    results={"overall_score": str(i % 101), "dimension_scores": [], "notes": []},
                )
            )
        await conn.execute(A.assessments.insert(), records)
    query = "/api/v1/assessment/assessments?q=Cohort&limit=100"
    first = (await c.get(query)).json()
    second = (await c.get(query + "&offset=100")).json()
    assert len(first) == 100 and len(second) == 25
    assert len({r["id"] for r in first + second}) == 125
    period = f"start={stamp.date()}&end={stamp.date()}&framework_version_id={v['id']}"
    cohort = (await c.get("/api/v1/workspace/comparison?" + period)).json()
    assert cohort["count"] == 125
    incompatible = period.replace(v["id"], str(uuid4()))
    assert (await c.get("/api/v1/workspace/comparison?" + incompatible)).json()["count"] == 0
    assert (await c.get(query + "&offset=125")).json() == []
    assert float(cohort["items"][0]["score"]) == pytest.approx(
        sum(i % 101 for i in range(125)) / 125
    )
    assert (
        await c.get(
            "/api/v1/workspace/comparison?start=2026-10-10&end=2026-10-09&framework_version_id="
            + v["id"]
        )
    ).status_code == 422
    target = str(records[124]["id"])
    for active in [True, False]:
        await ok(
            c,
            "POST",
            "/access",
            {"user_id": str(ids["viewer"]), "assessment_id": target, "active": active},
        )
        c.cookies.clear()
        await login(c, emails, "viewer")
        found = (await c.get("/api/v1/workspace/search?kind=assessments&q=Cohort")).json()
        assert found["total"] == int(active)
        result = await c.get(f"/api/v1/assessment/assessments/{target}")
        assert result.status_code == (200 if active else 404)
        if active:
            assert result.json()["answers"] == []
        c.cookies.clear()
        await login(c, emails, org=ids["a"])


async def test_mail_adapter_templates_retry_expiry_and_redaction(identity, monkeypatch):
    from ppm_api.account_mail import deliver_due
    from ppm_api.identity import issue_challenge
    from ppm_api.pilot_tables import mail

    c, app, owner, ids, emails = identity
    settings = app.state.settings.model_copy(update={"mail_mode": "smtp"})
    sent = []

    def adapter(config, payload, delivery_id):
        sent.append(payload["kind"])

    monkeypatch.setattr("ppm_api.account_mail.smtp_delivery", adapter)
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        for kind in ["register", "activate", "reset", "invite"]:
            await issue_challenge(
                conn,
                settings,
                emails["pending"],
                kind,
                ids["a"] if kind == "invite" else None,
                ids["admin"] if kind == "invite" else None,
                "Viewer" if kind == "invite" else None,
                "Fixture" if kind == "register" else None,
            )
    assert await deliver_due(app.state.engine, settings) == 4
    assert sorted(sent) == ["activate", "invite", "register", "reset"]
    async with owner.connect() as conn:
        accepted = (
            (
                await conn.execute(
                    sa.select(mail).where(
                        mail.c.status == "provider_accepted",
                        mail.c.token_hash.in_(
                            sa.select(challenges.c.token_hash).where(
                                challenges.c.email == emails["pending"]
                            )
                        ),
                    )
                )
            )
            .mappings()
            .all()
        )
        assert len(accepted) == 4
        assert all(r["payload"] == {} and r["error_code"] is None for r in accepted)

    def timeout(*args):
        raise TimeoutError("SECRET-TOKEN-MUST-NOT-APPEAR")

    monkeypatch.setattr("ppm_api.account_mail.smtp_delivery", timeout)
    async with app.state.engine.begin() as conn:
        await issue_challenge(conn, settings, emails["pending"], "reset")
    assert await deliver_due(app.state.engine, settings) == 0
    async with owner.begin() as conn:
        pending = (
            (await conn.execute(sa.select(mail).where(mail.c.status == "queued"))).mappings().all()
        )
        assert pending and all(r["error_code"] == "DELIVERY_UNCONFIRMED" for r in pending)
        for r in pending:
            assert "SECRET-TOKEN-MUST-NOT-APPEAR" not in str(r)
            await conn.execute(
                challenges.update()
                .where(challenges.c.token_hash == r["token_hash"])
                .values(expires_at=now() - timedelta(seconds=1))
            )
            await conn.execute(mail.update().where(mail.c.id == r["id"]).values(available_at=now()))
    assert await deliver_due(app.state.engine, settings) == 0
    async with owner.connect() as conn:
        for r in pending:
            stopped = (
                (await conn.execute(sa.select(mail).where(mail.c.id == r["id"]))).mappings().one()
            )
            assert stopped["status"] == "cancelled" and stopped["payload"] == {}

    # Exhaustion clears secrets, and revoked inviter authority stops queued mail.
    async with app.state.engine.begin() as conn:
        await issue_challenge(conn, settings, emails["pending"], "reset")
    for _attempt in range(5):
        async with owner.begin() as conn:
            await conn.execute(
                mail.update().where(mail.c.status == "queued").values(available_at=now())
            )
        assert await deliver_due(app.state.engine, settings) == 0
    async with owner.connect() as conn:
        failed = (
            (await conn.execute(sa.select(mail).where(mail.c.status == "failed"))).mappings().all()
        )
        assert failed and all(r["attempts"] == 5 and r["payload"] == {} for r in failed)
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        await issue_challenge(
            conn, settings, emails["pending"], "invite", ids["a"], ids["admin"], "Viewer"
        )
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update().where(memberships.c.user_id == ids["admin"]).values(active=False)
        )
    monkeypatch.setattr("ppm_api.account_mail.smtp_delivery", adapter)
    assert await deliver_due(app.state.engine, settings) == 0


async def test_expired_invitation_visible_resend_and_historical_status(identity):
    from ppm_api.pilot_tables import mail

    c, app, owner, ids, emails = identity
    await login(c, emails, org=ids["a"])
    email = f"expired-invite-{uuid4()}@example.com"
    response = await send(
        c, "POST", "/organization/invitations", json={"email": email, "role": "Project Manager"}
    )
    assert response.status_code == 201 and "no inbox email" in response.json()["message"]
    invitation = (await c.get("/api/v1/organization/invitations")).json()[0]
    assert invitation["delivery_status"] == "local_preview"
    old = mailbox(app, email)[0]["link"].split("#token=")[1]
    async with owner.begin() as conn:
        await conn.execute(
            challenges.update()
            .where(challenges.c.token_hash == digest(old))
            .values(expires_at=now() - timedelta(seconds=1))
        )
        await conn.execute(
            mail.update().where(mail.c.token_hash == digest(old)).values(status="delivered")
        )
    expired = (await c.get("/api/v1/organization/invitations")).json()[0]
    assert expired["delivery_status"] == "acceptance_unverified"
    assert expired["invitation_id"] == invitation["invitation_id"]
    path = "/organization/invitations/" + invitation["invitation_id"]
    assert (await send(c, "POST", path + "/resend")).status_code == 200
    assert (
        await send(
            c, "POST", "/auth/complete", json={"token": old, "password": PASSWORD, "name": "PM"}
        )
    ).status_code == 400
    replacement = (await c.get("/api/v1/organization/invitations")).json()[0]
    assert replacement["invitation_id"] != invitation["invitation_id"]
    assert replacement["role"] == "Project Manager"
    async with owner.connect() as conn:
        name = await conn.scalar(
            sa.select(organizations.c.name).where(organizations.c.id == ids["a"])
        )
        token_hash = await conn.scalar(
            sa.select(challenges.c.token_hash).where(
                challenges.c.invitation_id == replacement["invitation_id"]
            )
        )
    new_mail = next(
        m for m in mailbox(app, email) if digest(m["link"].split("#token=")[1]) == token_hash
    )
    assert new_mail["organization_name"] == name and new_mail["role"] == "Project Manager"


async def test_freshness_rollback_other_tenant_and_membership_revoke(identity):
    from ppm_api.identity import Principal
    from ppm_api.pilot import freshness
    from ppm_api.ppm_tables import TABLES
    from test_delivery import setup

    c, app, owner, ids, emails, portfolio, project = await setup(identity)

    async def signature(org, actor):
        async with app.state.engine.begin() as conn:
            await context(conn, actor, org, "Admin")
            return await freshness(
                Principal(conn, {"id": actor}, {"organization_id": org}, "Admin")
            )

    own = await signature(ids["a"], ids["admin"])
    foreign = await signature(ids["b"], ids["other"])
    await create(c, "milestones", project_id=project["id"], due_date="2026-11-01")
    changed = await signature(ids["a"], ids["admin"])
    assert changed != own and await signature(ids["b"], ids["other"]) == foreign
    assert await signature(ids["a"], ids["admin"]) == changed
    async with owner.connect() as conn:
        transaction = await conn.begin()
        await conn.execute(
            TABLES["projects"]
            .update()
            .where(TABLES["projects"].c.id == project["id"])
            .values(revision=999)
        )
        await transaction.rollback()
    assert await signature(ids["a"], ids["admin"]) == changed
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update()
            .where(memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["admin"])
            .values(active=False)
        )
    for path in ["search", "my-work", "notifications", "events"]:
        assert (await c.get("/api/v1/workspace/" + path)).status_code == 403


async def test_workspace_stream_reconnect_and_live_revocation(identity):
    from fastapi import Request
    from ppm_api.identity import Principal
    from ppm_api.pilot import stream
    from test_delivery import setup

    c, app, owner, ids, emails, portfolio, project = await setup(identity)

    class ConnectedRequest(Request):
        async def is_disconnected(self):
            return False

    async def response(cursor=""):
        headers = [(b"cookie", "; ".join(f"{k}={v}" for k, v in c.cookies.items()).encode())]
        if cursor:
            headers.append((b"last-event-id", cursor.encode()))
        request = ConnectedRequest(
            {
                "type": "http",
                "method": "GET",
                "path": "/api/v1/workspace/events",
                "query_string": b"",
                "headers": headers,
                "app": app,
                "server": ("localhost", 80),
                "scheme": "http",
            }
        )
        async with app.state.engine.begin() as conn:
            await context(conn, ids["admin"], ids["a"], "Admin")
            return await stream(
                request,
                Principal(conn, {"id": ids["admin"]}, {"organization_id": ids["a"]}, "Admin"),
            )

    first = (await response()).body_iterator
    frame = await asyncio.wait_for(anext(first), 3)
    assert "event: changed" in frame and "workspace-v1" in frame
    assert str(project["id"]) not in frame and project["data"]["name"] not in frame
    cursor = frame.split("\n")[0].removeprefix("id: ")
    await first.aclose()
    resumed = (await response(cursor)).body_iterator
    assert await asyncio.wait_for(anext(resumed), 3) == ": heartbeat\n\n"
    await create(c, "milestones", project_id=project["id"], due_date="2026-11-01")
    changed = await asyncio.wait_for(anext(resumed), 3)
    assert "event: changed" in changed and not changed.startswith(f"id: {cursor}\n")
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update().where(memberships.c.user_id == ids["admin"]).values(active=False)
        )
    assert await asyncio.wait_for(anext(resumed), 3) == "event: access_revoked\ndata: {}\n\n"
    with pytest.raises(StopAsyncIteration):
        await anext(resumed)
