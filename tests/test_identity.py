"""Real database/Redis identity boundaries. All mutations use isolated ppm_test."""

import asyncio
import json
import os
import secrets
import subprocess
import sys
from datetime import timedelta
from uuid import uuid4

import httpx
import jwt
import pytest
import sqlalchemy as sa
from ppm_api.config import load_settings
from ppm_api.identity import context, digest, now, password_hash
from ppm_api.identity_tables import (
    audit,
    challenges,
    memberships,
    organizations,
    sessions,
    users,
)
from ppm_api.main import create_app
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated Compose test DB"
    ),
]
PASSWORD = "Only-for-fixtures-27!"


@pytest.fixture
async def identity():
    config = load_settings()
    owner = create_async_engine(os.environ["PPM_MIGRATION_DATABASE_URL"])
    ids = {key: uuid4() for key in ["a", "b", "admin", "pm", "viewer", "other", "pending"]}
    emails = {key: f"{value}@example.com" for key, value in ids.items() if key not in {"a", "b"}}
    hashed = await password_hash(PASSWORD)
    async with owner.begin() as conn:
        assert await conn.scalar(sa.text("SELECT current_database()")) == "ppm_test"
        for key in ["a", "b"]:
            await conn.execute(
                organizations.insert().values(id=ids[key], name="Shared name", created_at=now())
            )
        for key, email in emails.items():
            await conn.execute(
                users.insert().values(
                    id=ids[key],
                    email=email,
                    name="Same member name",
                    password_hash=hashed,
                    verified=key != "pending",
                    created_at=now(),
                )
            )
        for org, user, role in [
            ("a", "admin", "Admin"),
            ("a", "pm", "Project Manager"),
            ("a", "viewer", "Viewer"),
            ("a", "pending", "Viewer"),
            ("b", "other", "Admin"),
            ("b", "admin", "Viewer"),
        ]:
            await conn.execute(
                memberships.insert().values(
                    organization_id=ids[org], user_id=ids[user], role=role, active=True, revision=1
                )
            )
    app = create_app(config)
    async with app.router.lifespan_context(app):
        # Rate limiter reset only in the isolated test broker DB, never local/demo.
        assert config.redis_url.get_secret_value().endswith("/1")
        await app.state.redis.flushdb()
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="https://testserver"
        ) as client:
            yield client, app, owner, ids, emails
    await owner.dispose()


async def send(client, method, path, **kwargs):
    if not client.cookies.get("ppm_csrf"):
        assert (await client.get("/api/v1/auth/csrf")).status_code == 200
    headers = {"origin": "http://localhost:3000", "x-csrf-token": client.cookies.get("ppm_csrf")}
    headers.update(kwargs.pop("headers", {}))
    result = await client.request(method, "/api/v1" + path, headers=headers, **kwargs)
    if path in {"/auth/login", "/auth/switch"} and result.status_code == 200:
        client.headers["x-organization-id"] = result.json()["organization_id"]
    return result


async def login(client, emails, key="admin", org=None):
    result = await send(
        client, "POST", "/auth/login", json={"email": emails[key], "password": PASSWORD}
    )
    assert result.status_code == 200, result.text
    if org:
        result = await send(client, "POST", "/auth/switch", json={"organization_id": str(org)})
        assert result.status_code == 200, result.text
    return result


async def challenge(owner, email, kind, **extra):
    token = secrets.token_urlsafe(32)
    async with owner.begin() as conn:
        await conn.execute(
            challenges.insert().values(
                token_hash=digest(token),
                email=email,
                kind=kind,
                expires_at=now() + timedelta(minutes=10),
                used=False,
                **extra,
            )
        )
    return token


async def test_roles_tenant_selectors_hidden_ids_and_audit(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    result = await client.get(
        "/api/v1/organization/members", headers={"X-Organization-ID": str(ids["b"])}
    )
    assert result.status_code == 200
    assert emails["other"] not in result.text
    assert emails["pm"] in result.text
    stale = await send(
        client,
        "POST",
        "/organization/invitations",
        json={"email": "stale@example.com", "role": "Viewer"},
        headers={"x-organization-id": str(ids["b"])},
    )
    assert stale.status_code == 409
    hidden = await send(
        client,
        "PATCH",
        f"/organization/members/{ids['other']}",
        json={"role": "Viewer", "active": False},
        headers={"if-match": "1"},
    )
    assert hidden.status_code == 404
    assert (
        await send(client, "POST", "/auth/switch", json={"organization_id": str(uuid4())})
    ).status_code == 404
    switched = await send(client, "POST", "/auth/switch", json={"organization_id": str(ids["b"])})
    assert switched.json()["role"] == "Viewer"
    assert (await client.get("/api/v1/organization/members")).status_code == 403
    for key in ["pm", "viewer"]:
        client.cookies.clear()
        await login(client, emails, key)
        assert (await client.get("/api/v1/auth/me")).status_code == 200
        assert (
            await send(
                client,
                "POST",
                "/organization/invitations",
                json={"email": "new@example.com", "role": "Admin"},
            )
        ).status_code == 403
        assert (await client.get("/api/v1/organization/audit")).status_code == 403
        assert (
            await send(
                client,
                "PATCH",
                f"/organization/members/{ids[key]}",
                json={"role": "Admin", "active": True},
                headers={"if-match": "1"},
            )
        ).status_code == 403


async def test_csrf_secure_cookies_expired_forged_and_logout(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    cookies = await send(
        client, "POST", "/auth/login", json={"email": emails["admin"], "password": PASSWORD}
    )
    for value in cookies.headers.get_list("set-cookie"):
        assert "Secure" in value and "HttpOnly" in value and "SameSite=strict" in value
    rejected = await client.post("/api/v1/auth/logout")
    assert rejected.status_code == 403
    assert rejected.headers["x-request-id"] == rejected.json()["error"]["request_id"]
    assert (
        await send(client, "POST", "/auth/logout", headers={"origin": "https://evil.example"})
    ).status_code == 403
    assert (
        await send(client, "POST", "/auth/logout", headers={"x-csrf-token": "wrong"})
    ).status_code == 403
    access = client.cookies.get("ppm_access")
    claims = jwt.decode(access, options={"verify_signature": False})
    for changes in [{"exp": 0}, {"org": str(uuid4())}, {"sid": str(uuid4())}, {"aud": "other"}]:
        forged = jwt.encode(
            {**claims, **changes},
            app.state.settings.jwt_secret.get_secret_value(),
            algorithm="HS256",
        )
        result = await client.get("/api/v1/auth/me", headers={"cookie": f"ppm_access={forged}"})
        assert result.status_code == 401
    assert (await send(client, "POST", "/auth/logout")).status_code == 200
    assert (
        await client.get("/api/v1/auth/me", headers={"cookie": f"ppm_access={access}"})
    ).status_code == 401


async def test_refresh_rotation_replay_and_concurrent_replay(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    old = client.cookies.get("ppm_refresh")
    assert (await send(client, "POST", "/auth/refresh")).status_code == 200
    assert client.cookies.get("ppm_refresh") != old
    csrf = client.cookies.get("ppm_csrf")
    replay = await send(
        client, "POST", "/auth/refresh", headers={"cookie": f"ppm_refresh={old}; ppm_csrf={csrf}"}
    )
    assert replay.status_code == 401
    assert (await client.get("/api/v1/auth/me")).status_code == 401
    client.cookies.clear()
    await login(client, emails, org=ids["a"])
    raw = (
        f"ppm_refresh={client.cookies.get('ppm_refresh')}; "
        f"ppm_csrf={client.cookies.get('ppm_csrf')}"
    )
    headers = {
        "cookie": raw,
        "origin": "http://localhost:3000",
        "x-csrf-token": client.cookies.get("ppm_csrf"),
    }
    results = await asyncio.gather(
        *[client.post("/api/v1/auth/refresh", headers=headers) for _ in range(2)]
    )
    assert sorted(r.status_code for r in results) == [200, 401]
    assert (await client.get("/api/v1/auth/me")).status_code == 401


async def test_final_admin_stale_revision_live_role_and_removal(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    path = f"/organization/members/{ids['admin']}"
    assert (
        await send(client, "PATCH", path, json={"role": "Viewer", "active": True})
    ).status_code == 428
    assert (
        await send(
            client,
            "PATCH",
            path,
            json={"role": "Viewer", "active": True},
            headers={"if-match": "2"},
        )
    ).status_code == 412
    assert (
        await send(
            client,
            "PATCH",
            path,
            json={"role": "Viewer", "active": True},
            headers={"if-match": "1"},
        )
    ).status_code == 409
    assert (
        await send(
            client,
            "PATCH",
            path,
            json={"role": "Admin", "active": False},
            headers={"if-match": "1"},
        )
    ).status_code == 409
    assert (
        await send(
            client,
            "PATCH",
            f"/organization/members/{ids['pm']}",
            json={"role": "Admin", "active": True},
            headers={"if-match": "1"},
        )
    ).status_code == 200
    assert (
        await send(
            client,
            "PATCH",
            path,
            json={"role": "Viewer", "active": True},
            headers={"if-match": "1"},
        )
    ).status_code == 200
    assert (await client.get("/api/v1/organization/members")).status_code == 403
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update()
            .where(memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["admin"])
            .values(active=False)
        )
    assert (await client.get("/api/v1/auth/me")).status_code == 401


async def test_activation_invitation_scope_and_single_use(identity):
    client, app, owner, ids, emails = identity
    assert (
        await send(
            client, "POST", "/auth/login", json={"email": emails["pending"], "password": PASSWORD}
        )
    ).status_code == 401
    token = await challenge(owner, emails["pending"], "activate", organization_id=ids["a"])
    body = {"token": token, "password": PASSWORD, "name": "Activated"}
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 200
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 400
    await login(client, emails, org=ids["a"])
    recipient = f"{uuid4()}@example.com"
    assert (
        await send(
            client,
            "POST",
            "/organization/invitations",
            json={"email": recipient, "role": "Viewer", "organization_id": str(ids["b"])},
        )
    ).status_code == 422
    result = await send(
        client, "POST", "/organization/invitations", json={"email": recipient, "role": "Viewer"}
    )
    assert result.status_code == 201
    files = list((app.state.settings.storage_root / "__identity_mailbox__").glob("*.json"))
    mail = next(
        json.loads(p.read_text()) for p in files if json.loads(p.read_text())["to"] == recipient
    )
    assert mail["organization_id"] == str(ids["a"])
    token = mail["link"].split("#token=")[1]
    body = {"token": token, "password": PASSWORD, "name": "Invited"}
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 200
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 400
    client.cookies.clear()
    result = await login(client, {"admin": recipient})
    assert [o["id"] for o in result.json()["organizations"]] == [str(ids["a"])]


async def test_reset_expiry_non_enumeration_bcrypt_bytes_and_session_revoke(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    old = client.cookies.get("ppm_access")
    a = await send(client, "POST", "/auth/reset-request", json={"email": emails["admin"]})
    b = await send(client, "POST", "/auth/reset-request", json={"email": "absent@example.com"})
    assert a.json() == b.json() and a.status_code == 200
    token = await challenge(owner, emails["admin"], "reset")
    body = {"token": token, "password": "界" * 25, "name": "Admin"}
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 422
    body["password"] = PASSWORD + "new"
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 200
    assert (
        await client.get("/api/v1/auth/me", headers={"cookie": f"ppm_access={old}"})
    ).status_code == 401
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 400
    token = await challenge(owner, emails["admin"], "reset")
    async with owner.begin() as conn:
        await conn.execute(
            challenges.update()
            .where(challenges.c.token_hash == digest(token))
            .values(expires_at=now() - timedelta(seconds=1))
        )
        user = (
            (await conn.execute(sa.select(users).where(users.c.id == ids["admin"])))
            .mappings()
            .one()
        )
        assert user["password_hash"].startswith("$2b$12$") and PASSWORD not in user["password_hash"]
    body["token"] = token
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 400


async def test_rls_pool_reuse_foreign_writes_and_composite_fk(identity):
    client, app, owner, ids, emails = identity
    engine = create_async_engine(
        app.state.settings.database_url.get_secret_value(), pool_size=1, max_overflow=0
    )
    try:
        async with engine.begin() as conn:
            flags = (
                await conn.execute(
                    sa.text("SELECT rolsuper,rolbypassrls FROM pg_roles WHERE rolname=current_user")
                )
            ).one()
            assert flags == (False, False)
            assert not (await conn.execute(sa.select(memberships))).all()
            await context(conn, ids["admin"], ids["a"], "Admin")
            assert not (
                await conn.execute(
                    sa.select(memberships).where(memberships.c.user_id == ids["other"])
                )
            ).all()
            await conn.execute(
                memberships.update()
                .where(memberships.c.user_id == ids["other"])
                .values(role="Viewer")
            )
        async with engine.begin() as conn:
            assert not (await conn.execute(sa.select(memberships))).all()
            assert not (await conn.execute(sa.select(organizations))).all()
            await context(conn, ids["other"], ids["b"], "Admin")
            assert not (
                await conn.execute(
                    sa.select(memberships).where(memberships.c.organization_id == ids["a"])
                )
            ).all()
        with pytest.raises(DBAPIError):
            async with engine.begin() as conn:
                await context(conn, ids["admin"], ids["a"], "Admin")
                await conn.execute(
                    memberships.insert().values(
                        organization_id=ids["b"],
                        user_id=ids["viewer"],
                        role="Admin",
                        active=True,
                        revision=1,
                    )
                )
        with pytest.raises(DBAPIError):
            async with engine.begin() as conn:
                await context(conn, ids["admin"], ids["a"], "Admin")
                await conn.execute(
                    audit.insert().values(
                        id=uuid4(),
                        organization_id=ids["a"],
                        actor_id=ids["other"],
                        action="forged",
                        request_id=uuid4(),
                        created_at=now(),
                    )
                )
        with pytest.raises(DBAPIError):
            async with owner.begin() as conn:
                await conn.execute(
                    challenges.insert().values(
                        token_hash=digest(secrets.token_urlsafe()),
                        kind="invite",
                        email="x@example.com",
                        organization_id=ids["a"],
                        inviter_id=ids["other"],
                        role="Viewer",
                        expires_at=now(),
                        used=False,
                    )
                )
    finally:
        await engine.dispose()


async def test_rate_limit_and_session_id_guessing(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    assert (await send(client, "DELETE", f"/auth/sessions/{uuid4()}")).status_code == 404
    for _ in range(10):
        assert (
            await send(
                client,
                "POST",
                "/auth/login",
                json={"email": "unknown@example.com", "password": PASSWORD},
            )
        ).status_code == 401
    result = await send(
        client, "POST", "/auth/login", json={"email": "unknown@example.com", "password": PASSWORD}
    )
    assert result.status_code == 429 and result.headers["retry-after"] == "600"


async def test_existing_account_invites_and_revoked_inviter(identity):
    client, app, owner, ids, emails = identity
    token = await challenge(
        owner,
        emails["other"],
        "invite",
        organization_id=ids["a"],
        inviter_id=ids["admin"],
        role="Project Manager",
    )
    body = {"token": token, "password": "incorrect-password", "name": "Should not replace"}
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 400
    body["password"] = PASSWORD
    assert (await send(client, "POST", "/auth/complete", json=body)).status_code == 200
    async with owner.begin() as conn:
        assert (
            await conn.scalar(sa.select(users.c.name).where(users.c.id == ids["other"]))
            == "Same member name"
        )
    token = await challenge(
        owner,
        f"{uuid4()}@example.com",
        "invite",
        organization_id=ids["a"],
        inviter_id=ids["admin"],
        role="Viewer",
    )
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update()
            .where(memberships.c.user_id == ids["admin"], memberships.c.organization_id == ids["a"])
            .values(active=False)
        )
    assert (
        await send(client, "POST", "/auth/complete", json={**body, "token": token})
    ).status_code == 400


async def test_concurrent_last_admin_demotion_keeps_one_admin(identity):
    client, app, owner, ids, emails = identity
    async with owner.begin() as conn:
        await conn.execute(
            memberships.update()
            .where(memberships.c.user_id == ids["pm"], memberships.c.organization_id == ids["a"])
            .values(role="Admin")
        )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://testserver"
    ) as second:
        await login(client, emails, org=ids["a"])
        await login(second, emails, "pm")
        result = await asyncio.gather(
            *[
                send(
                    c,
                    "PATCH",
                    f"/organization/members/{ids[key]}",
                    json={"role": "Viewer", "active": True},
                    headers={"if-match": "1"},
                )
                for c, key in [(client, "admin"), (second, "pm")]
            ]
        )
        assert sorted(r.status_code for r in result) == [200, 409]
    async with owner.begin() as conn:
        count = await conn.scalar(
            sa.select(sa.func.count())
            .select_from(memberships)
            .where(
                memberships.c.organization_id == ids["a"],
                memberships.c.role == "Admin",
                memberships.c.active,
            )
        )
        assert count == 1


async def test_session_expiry_foreign_session_and_revocation(identity):
    client, app, owner, ids, emails = identity
    await login(client, emails, org=ids["a"])
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://testserver"
    ) as second:
        await login(second, emails, "other")
        foreign = (await second.get("/api/v1/auth/sessions")).json()["items"][0]["id"]
        assert (await send(client, "DELETE", f"/auth/sessions/{foreign}")).status_code == 404
        second.cookies.clear()
        await login(second, emails, org=ids["a"])
        sid = next(
            s["id"]
            for s in (await second.get("/api/v1/auth/sessions")).json()["items"]
            if s["current"]
        )
        assert (await send(client, "DELETE", f"/auth/sessions/{sid}")).status_code == 200
        assert (await second.get("/api/v1/auth/me")).status_code == 401
    async with owner.begin() as conn:
        await conn.execute(
            sessions.update()
            .where(sessions.c.user_id == ids["admin"])
            .values(expires_at=now() - timedelta(seconds=1))
        )
    assert (await client.get("/api/v1/auth/me")).status_code == 401
    assert (await send(client, "POST", "/auth/refresh")).status_code == 401


async def test_controlled_operator_bootstrap_activation(identity):
    client, app, owner, ids, emails = identity
    email = f"operator-{uuid4()}@example.com"
    args = [
        sys.executable,
        "scripts/bootstrap_identity.py",
        "--email",
        email,
        "--organization",
        "Operator-created organization",
    ]
    refused = await asyncio.to_thread(subprocess.run, args, capture_output=True, text=True)
    assert refused.returncode != 0 and "Already initialized" in refused.stderr
    created = await asyncio.to_thread(
        subprocess.run, [*args, "--additional-organization"], capture_output=True, text=True
    )
    assert created.returncode == 0, created.stderr
    mail = next(
        json.loads(p.read_text())
        for p in (app.state.settings.storage_root / "__identity_mailbox__").glob("*.json")
        if json.loads(p.read_text())["to"] == email
    )
    assert mail["kind"] == "activate"
    result = await send(
        client,
        "POST",
        "/auth/complete",
        json={
            "token": mail["link"].split("#token=")[1],
            "password": PASSWORD,
            "name": "First Admin",
        },
    )
    assert result.status_code == 200
    result = await login(client, {"admin": email})
    assert result.json()["role"] == "Admin"
