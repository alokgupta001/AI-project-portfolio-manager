"""Local identity, live session authorization and transaction-scoped tenant access."""

import asyncio
import hashlib
import json
import os
import secrets
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, NoReturn
from uuid import UUID, uuid4

import bcrypt
import jwt
import sqlalchemy as sa
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncConnection

from ppm_api.identity_schemas import (
    AccountView,
    AuditsView,
    CompleteChallenge,
    Credentials,
    CsrfResponse,
    EmailInput,
    InviteInput,
    MemberInput,
    MembersView,
    MemberView,
    Message,
    ProfileInput,
    SessionsView,
    SwitchInput,
)
from ppm_api.identity_tables import (
    audit,
    challenges,
    memberships,
    organizations,
    refresh_tokens,
    sessions,
    users,
)

router = APIRouter(prefix="/api/v1", tags=["Identity"])
ACCESS = "ppm_access"
REFRESH = "ppm_refresh"
CSRF = "ppm_csrf"
ACCESS_SECONDS = 600
SESSION_SECONDS = 604800
DUMMY_HASH = bcrypt.hashpw(b"constant-non-account-password", bcrypt.gensalt(rounds=12))


def now() -> datetime:
    return datetime.now(UTC)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def deny(status: int = 401) -> NoReturn:
    raise HTTPException(status_code=status)


async def password_hash(value: str) -> str:
    if not 12 <= len(value) or len(value.encode()) > 72:
        deny(422)
    return (await asyncio.to_thread(bcrypt.hashpw, value.encode(), bcrypt.gensalt(12))).decode()


async def password_matches(value: str, encoded: str | None) -> bool:
    raw = value.encode()
    if len(raw) > 72:
        return False
    return await asyncio.to_thread(bcrypt.checkpw, raw, encoded.encode() if encoded else DUMMY_HASH)


async def context(
    conn: AsyncConnection, user: UUID | None = None, org: UUID | None = None, role: str = ""
) -> None:
    # true makes every setting transaction-local; commit/rollback clears pooled connections.
    await conn.execute(
        sa.text(
            "SELECT set_config('ppm.user_id', :u, true), "
            "set_config('ppm.organization_id', :o, true), "
            "set_config('ppm.role', :r, true)"
        ),
        {"u": str(user or ""), "o": str(org or ""), "r": role},
    )


async def limited(request: Request, bucket: str, subject: str, maximum: int = 10) -> None:
    # Atomic increment + expiry. Fail closed if the shared limiter is unavailable.
    key = "identity:limit:" + digest(bucket + ":" + subject)
    try:
        count = await request.app.state.redis.eval(
            "local n=redis.call('INCR',KEYS[1]); "
            "if n==1 then redis.call('EXPIRE',KEYS[1],600) end; return n",
            1,
            key,
        )
    except Exception:
        deny(503)
        return
    if count > maximum:
        raise HTTPException(429, headers={"Retry-After": "600"})


def cookie(
    response: Response,
    request: Request,
    name: str,
    value: str,
    seconds: int,
    http_only: bool = True,
) -> None:
    response.set_cookie(
        name,
        value,
        max_age=seconds,
        httponly=http_only,
        secure=request.app.state.settings.cookie_secure,
        samesite="strict",
        path="/",
    )


def access_cookie(request: Request, response: Response, session: Any) -> None:
    issued = now()
    token = jwt.encode(
        {
            "sub": str(session["user_id"]),
            "sid": str(session["id"]),
            "org": str(session["organization_id"]),
            "iat": issued,
            "exp": issued + timedelta(seconds=ACCESS_SECONDS),
            "iss": "enterprise-ppm",
            "aud": "ppm-web",
            "jti": str(uuid4()),
        },
        request.app.state.settings.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )
    cookie(response, request, ACCESS, token, ACCESS_SECONDS)


async def record(
    conn: AsyncConnection,
    request: Request,
    user: UUID,
    org: UUID,
    action: str,
    target: UUID | None = None,
) -> None:
    await conn.execute(
        audit.insert().values(
            id=uuid4(),
            organization_id=org,
            actor_id=user,
            action=action,
            target_id=target,
            created_at=now(),
            request_id=UUID(request.state.request_id),
        )
    )


async def issue_challenge(
    conn: AsyncConnection,
    settings: Any,
    email: str,
    kind: str,
    org: UUID | None = None,
    inviter: UUID | None = None,
    role: str | None = None,
) -> None:
    token = secrets.token_urlsafe(32)
    expires = now() + timedelta(minutes=30 if kind == "reset" else 1440)
    await conn.execute(
        challenges.insert().values(
            token_hash=digest(token),
            kind=kind,
            email=email,
            organization_id=org,
            inviter_id=inviter,
            role=role,
            expires_at=expires,
            used=False,
        )
    )
    # Local-only spool, no unauthenticated HTTP mailbox and no external delivery.
    folder = settings.storage_root / "__identity_mailbox__"
    await asyncio.to_thread(folder.mkdir, parents=True, exist_ok=True)
    path = folder / (str(uuid4()) + ".json")
    content = json.dumps(
        {
            "to": email,
            "kind": kind,
            "expires_at": expires.isoformat(),
            "link": settings.web_origin + "/account/complete#token=" + token,
            "organization_id": str(org) if org else None,
        }
    )

    def write_private() -> None:
        folder.chmod(0o700)
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as output:
            output.write(content)

    await asyncio.to_thread(write_private)


@dataclass
class Principal:
    conn: AsyncConnection
    user: Any
    session: Any
    role: str


async def principal(
    request: Request,
    x_organization_id: Annotated[UUID | None, Header()] = None,
) -> AsyncIterator[Principal]:
    try:
        claims = jwt.decode(
            request.cookies.get(ACCESS, ""),
            request.app.state.settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
            issuer="enterprise-ppm",
            audience="ppm-web",
            options={"require": ["exp", "iat", "sub", "sid", "org", "jti"]},
        )
        uid, sid, oid = UUID(claims["sub"]), UUID(claims["sid"]), UUID(claims["org"])
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        deny()
        return
    async with request.app.state.engine.begin() as conn:
        session = (
            (
                await conn.execute(
                    sa.select(sessions).where(sessions.c.id == sid, sessions.c.user_id == uid)
                )
            )
            .mappings()
            .first()
        )
        if (
            not session
            or session["revoked"]
            or session["expires_at"] <= now()
            or session["organization_id"] != oid
        ):
            deny()
        await context(conn, uid)
        member = (
            (
                await conn.execute(
                    sa.select(memberships).where(
                        memberships.c.organization_id == oid,
                        memberships.c.user_id == uid,
                        memberships.c.active,
                    )
                )
            )
            .mappings()
            .first()
        )
        if not member:
            deny()
        user = (await conn.execute(sa.select(users).where(users.c.id == uid))).mappings().one()
        if not user["verified"]:
            deny()
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            if request.url.path.startswith("/api/v1/organization/") and x_organization_id != oid:
                # A precondition only, never tenant authority; rejects stale tabs after a switch.
                deny(409)
            if not secrets.compare_digest(
                session["csrf_hash"], digest(request.headers.get("x-csrf-token", ""))
            ):
                deny(403)
        await context(conn, uid, oid, member["role"])
        yield Principal(conn, user, session, member["role"])


# Commit (or fail) the transaction before the response can trigger a follow-up read.
Auth = Annotated[Principal, Depends(principal, scope="function")]


async def admin(p: Principal) -> None:
    # Serialize all membership changes, preventing concurrent removal of the last admin.
    oid = p.session["organization_id"]
    await p.conn.execute(
        sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org, 2))"), {"org": str(oid)}
    )
    role = await p.conn.scalar(
        sa.select(memberships.c.role).where(
            memberships.c.organization_id == oid,
            memberships.c.user_id == p.user["id"],
            memberships.c.active,
        )
    )
    if role != "Admin":
        deny(403)


async def account(conn: AsyncConnection, user: Any, session: Any) -> dict[str, Any]:
    rows = (
        (
            await conn.execute(
                sa.select(organizations.c.id, organizations.c.name, memberships.c.role)
                .join(memberships)
                .where(memberships.c.user_id == user["id"], memberships.c.active)
                .order_by(organizations.c.name, organizations.c.id)
            )
        )
        .mappings()
        .all()
    )
    role = next(r["role"] for r in rows if r["id"] == session["organization_id"])
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "organization_id": session["organization_id"],
        "role": role,
        "organizations": [dict(r) for r in rows],
    }


@router.get("/auth/csrf", response_model=CsrfResponse)
async def csrf(request: Request, response: Response) -> dict[str, str]:
    value = request.cookies.get(CSRF) or secrets.token_urlsafe(32)
    cookie(response, request, CSRF, value, SESSION_SECONDS, False)
    return {"csrf_token": value}


@router.post("/auth/login", response_model=AccountView)
async def login(body: Credentials, request: Request, response: Response) -> dict[str, Any]:
    email = str(body.email).lower()
    await limited(request, "login-email", email)
    await limited(request, "login-peer", request.client.host if request.client else "unknown", 100)
    async with request.app.state.engine.begin() as conn:
        user = (
            (await conn.execute(sa.select(users).where(users.c.email == email).with_for_update()))
            .mappings()
            .first()
        )
        valid = await password_matches(body.password, user["password_hash"] if user else None)
        if not user or not valid or not user["verified"]:
            deny()
        await context(conn, user["id"])
        org = await conn.scalar(
            sa.select(memberships.c.organization_id)
            .where(memberships.c.user_id == user["id"], memberships.c.active)
            .order_by(memberships.c.organization_id)
            .limit(1)
        )
        if not org:
            deny()
        await context(conn, user["id"], org)
        session = dict(
            id=uuid4(),
            user_id=user["id"],
            organization_id=org,
            csrf_hash=digest(request.headers["x-csrf-token"]),
            created_at=now(),
            expires_at=now() + timedelta(seconds=SESSION_SECONDS),
            revoked=False,
        )
        await conn.execute(sessions.insert().values(**session))
        refresh = secrets.token_urlsafe(48)
        await conn.execute(
            refresh_tokens.insert().values(
                token_hash=digest(refresh), session_id=session["id"], used=False
            )
        )
        await record(conn, request, user["id"], org, "session.login", session["id"])
        result = await account(conn, user, session)
    access_cookie(request, response, session)
    cookie(response, request, REFRESH, refresh, SESSION_SECONDS)
    return result


@router.post("/auth/refresh", response_model=Message)
async def refresh(request: Request, response: Response) -> dict[str, str]:
    token_hash = digest(request.cookies.get(REFRESH, ""))
    replay = False
    async with request.app.state.engine.begin() as conn:
        sid = await conn.scalar(
            sa.select(refresh_tokens.c.session_id).where(refresh_tokens.c.token_hash == token_hash)
        )
        if not sid:
            deny()
        session = (
            (await conn.execute(sa.select(sessions).where(sessions.c.id == sid).with_for_update()))
            .mappings()
            .one()
        )
        if session["revoked"] or session["expires_at"] <= now():
            deny()
        if not secrets.compare_digest(
            session["csrf_hash"], digest(request.headers["x-csrf-token"])
        ):
            deny(403)
        await context(conn, session["user_id"], session["organization_id"])
        member = await conn.scalar(
            sa.select(memberships.c.active).where(
                memberships.c.organization_id == session["organization_id"],
                memberships.c.user_id == session["user_id"],
            )
        )
        if not member:
            deny()
        used = await conn.scalar(
            sa.select(refresh_tokens.c.used).where(refresh_tokens.c.token_hash == token_hash)
        )
        if used:
            await conn.execute(sessions.update().where(sessions.c.id == sid).values(revoked=True))
            await record(
                conn,
                request,
                session["user_id"],
                session["organization_id"],
                "session.refresh_replay",
                sid,
            )
            replay = True
        else:
            await conn.execute(
                refresh_tokens.update()
                .where(refresh_tokens.c.token_hash == token_hash)
                .values(used=True)
            )
            replacement = secrets.token_urlsafe(48)
            await conn.execute(
                refresh_tokens.insert().values(
                    token_hash=digest(replacement), session_id=sid, used=False
                )
            )
    # Revocation must commit before rejecting a replay (including concurrent refresh losers).
    if replay:
        deny()
    access_cookie(request, response, session)
    cookie(
        response,
        request,
        REFRESH,
        replacement,
        max(0, int((session["expires_at"] - now()).total_seconds())),
    )
    return {"message": "Session refreshed."}


@router.get("/auth/me", response_model=AccountView)
async def me(p: Auth) -> dict[str, Any]:
    return await account(p.conn, p.user, p.session)


@router.patch("/auth/profile", response_model=Message)
async def profile(body: ProfileInput, request: Request, p: Auth) -> dict[str, str]:
    await p.conn.execute(users.update().where(users.c.id == p.user["id"]).values(name=body.name))
    await record(p.conn, request, p.user["id"], p.session["organization_id"], "profile.updated")
    return {"message": "Profile updated."}


@router.post("/auth/switch", response_model=AccountView)
async def switch(
    body: SwitchInput, request: Request, response: Response, p: Auth
) -> dict[str, Any]:
    membership = (
        (
            await p.conn.execute(
                sa.select(memberships).where(
                    memberships.c.organization_id == body.organization_id,
                    memberships.c.user_id == p.user["id"],
                    memberships.c.active,
                )
            )
        )
        .mappings()
        .first()
    )
    if not membership:
        deny(404)
    await context(p.conn, p.user["id"], body.organization_id, membership["role"])
    await p.conn.execute(
        sessions.update()
        .where(sessions.c.id == p.session["id"])
        .values(organization_id=body.organization_id)
    )
    updated = {**p.session, "organization_id": body.organization_id}
    await record(p.conn, request, p.user["id"], body.organization_id, "organization.switched")
    access_cookie(request, response, updated)
    return await account(p.conn, p.user, updated)


@router.post("/auth/logout", response_model=Message)
async def logout(request: Request, response: Response, p: Auth) -> dict[str, str]:
    await p.conn.execute(
        sessions.update().where(sessions.c.id == p.session["id"]).values(revoked=True)
    )
    await record(p.conn, request, p.user["id"], p.session["organization_id"], "session.logout")
    for key in (ACCESS, REFRESH, CSRF):
        cookie(response, request, key, "", 0, key != CSRF)
    return {"message": "Signed out."}


@router.get("/auth/sessions", response_model=SessionsView)
async def list_sessions(p: Auth) -> dict[str, Any]:
    rows = (
        await p.conn.execute(
            sa.select(sessions)
            .where(
                sessions.c.user_id == p.user["id"],
                ~sessions.c.revoked,
                sessions.c.expires_at > now(),
            )
            .order_by(sessions.c.created_at.desc())
            .limit(100)
        )
    ).mappings()
    return {
        "items": [
            {
                "id": r["id"],
                "created_at": r["created_at"],
                "expires_at": r["expires_at"],
                "current": r["id"] == p.session["id"],
            }
            for r in rows
        ]
    }


@router.delete("/auth/sessions/{session_id}", response_model=Message)
async def revoke(session_id: UUID, request: Request, p: Auth) -> dict[str, str]:
    found = await p.conn.scalar(
        sessions.update()
        .where(sessions.c.id == session_id, sessions.c.user_id == p.user["id"])
        .values(revoked=True)
        .returning(sessions.c.id)
    )
    if not found:
        deny(404)
    await record(
        p.conn, request, p.user["id"], p.session["organization_id"], "session.revoked", session_id
    )
    return {"message": "Session revoked."}


@router.post("/auth/reset-request", response_model=Message)
async def reset_request(body: EmailInput, request: Request) -> dict[str, str]:
    email = str(body.email).lower()
    await limited(request, "reset", email, 3)
    await limited(request, "reset-peer", request.client.host if request.client else "unknown", 30)
    async with request.app.state.engine.begin() as conn:
        uid = await conn.scalar(
            sa.select(users.c.id).where(users.c.email == email, users.c.verified)
        )
        if uid:
            await issue_challenge(conn, request.app.state.settings, email, "reset")
    return {
        "message": "If the account is eligible, recovery instructions are in the local mailbox."
    }


@router.post("/auth/complete", response_model=Message)
async def complete(body: CompleteChallenge, request: Request) -> dict[str, str]:
    await limited(
        request, "complete-peer", request.client.host if request.client else "unknown", 30
    )
    async with request.app.state.engine.begin() as conn:
        challenge = (
            (
                await conn.execute(
                    sa.select(challenges)
                    .where(challenges.c.token_hash == digest(body.token))
                    .with_for_update()
                )
            )
            .mappings()
            .first()
        )
        if not challenge or challenge["used"] or challenge["expires_at"] <= now():
            deny(400)
        email = challenge["email"]
        # Serialize account creation/activation across different challenges for the same email.
        await conn.execute(
            sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:email, 0))"), {"email": email}
        )
        user = (
            (await conn.execute(sa.select(users).where(users.c.email == email).with_for_update()))
            .mappings()
            .first()
        )
        uid = user["id"] if user else uuid4()
        oid = challenge["organization_id"]
        if challenge["kind"] == "invite":
            await context(conn, challenge["inviter_id"], oid, "Admin")
            await conn.execute(
                sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org, 2))"),
                {"org": str(oid)},
            )
            inviter = (
                await conn.execute(
                    sa.select(memberships).where(
                        memberships.c.organization_id == oid,
                        memberships.c.user_id == challenge["inviter_id"],
                        memberships.c.active,
                        memberships.c.role == "Admin",
                    )
                )
            ).first()
            if not inviter:
                deny(400)
            if user and user["verified"]:
                if not await password_matches(body.password, user["password_hash"]):
                    deny(400)
            else:
                hashed = await password_hash(body.password)
                if user:
                    await conn.execute(
                        users.update()
                        .where(users.c.id == uid)
                        .values(password_hash=hashed, verified=True, name=body.name)
                    )
                else:
                    await conn.execute(
                        users.insert().values(
                            id=uid,
                            email=email,
                            name=body.name,
                            password_hash=hashed,
                            verified=True,
                            created_at=now(),
                        )
                    )
            existing = (
                await conn.execute(
                    sa.select(memberships).where(
                        memberships.c.organization_id == oid, memberships.c.user_id == uid
                    )
                )
            ).first()
            if existing:
                # Invitations cannot silently restore removed users or overwrite current roles.
                deny(409)
            await conn.execute(
                memberships.insert().values(
                    organization_id=oid,
                    user_id=uid,
                    role=challenge["role"],
                    active=True,
                    revision=1,
                )
            )
            await record(conn, request, challenge["inviter_id"], oid, "invitation.accepted", uid)
        else:
            if not user or (challenge["kind"] == "activate" and user["verified"]):
                deny(400)
            hashed = await password_hash(body.password)
            await conn.execute(
                users.update()
                .where(users.c.id == uid)
                .values(password_hash=hashed, verified=True, name=body.name)
            )
            await conn.execute(
                sessions.update().where(sessions.c.user_id == uid).values(revoked=True)
            )
            await context(conn, uid)
            orgs = (
                (
                    await conn.execute(
                        sa.select(memberships.c.organization_id).where(
                            memberships.c.user_id == uid, memberships.c.active
                        )
                    )
                )
                .scalars()
                .all()
            )
            for org in orgs:
                await context(conn, uid, org)
                await record(conn, request, uid, org, "account." + challenge["kind"])
            await conn.execute(
                challenges.update()
                .where(challenges.c.email == email, challenges.c.kind.in_(["reset", "activate"]))
                .values(used=True)
            )
        await conn.execute(
            challenges.update()
            .where(challenges.c.token_hash == digest(body.token))
            .values(used=True)
        )
    return {"message": "Account verified. You can sign in now."}


@router.get("/organization/members", response_model=MembersView)
async def member_list(p: Auth, after: UUID | None = None) -> dict[str, Any]:
    await admin(p)
    query = (
        sa.select(memberships, users.c.email, users.c.name)
        .join(users)
        .where(memberships.c.organization_id == p.session["organization_id"])
    )
    if after:
        query = query.where(memberships.c.user_id > after)
    rows = (await p.conn.execute(query.order_by(memberships.c.user_id).limit(101))).mappings().all()
    return {
        "items": [dict(r) for r in rows[:100]],
        "as_of": now(),
        "next_cursor": str(rows[99]["user_id"]) if len(rows) > 100 else None,
    }


@router.post("/organization/invitations", response_model=Message, status_code=201)
async def invite(body: InviteInput, request: Request, p: Auth) -> dict[str, str]:
    await admin(p)
    await limited(request, "invite", str(p.user["id"]), 20)
    await issue_challenge(
        p.conn,
        request.app.state.settings,
        str(body.email).lower(),
        "invite",
        p.session["organization_id"],
        p.user["id"],
        body.role,
    )
    await record(p.conn, request, p.user["id"], p.session["organization_id"], "invitation.created")
    return {"message": "Invitation created in the local mailbox."}


@router.patch("/organization/members/{user_id}", response_model=MemberView)
async def change_member(
    user_id: UUID,
    body: MemberInput,
    request: Request,
    p: Auth,
    if_match: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    await admin(p)
    oid = p.session["organization_id"]
    member = (
        (
            await p.conn.execute(
                sa.select(memberships).where(
                    memberships.c.organization_id == oid, memberships.c.user_id == user_id
                )
            )
        )
        .mappings()
        .first()
    )
    if not member:
        deny(404)
    if if_match is None:
        deny(428)
    if if_match != str(member["revision"]):
        deny(412)
    if member["active"] and member["role"] == "Admin" and (body.role != "Admin" or not body.active):
        count = await p.conn.scalar(
            sa.select(sa.func.count())
            .select_from(memberships)
            .where(
                memberships.c.organization_id == oid,
                memberships.c.active,
                memberships.c.role == "Admin",
            )
        )
        if count == 1:
            deny(409)
    await p.conn.execute(
        memberships.update()
        .where(memberships.c.organization_id == oid, memberships.c.user_id == user_id)
        .values(role=body.role, active=body.active, revision=member["revision"] + 1)
    )
    # Live policy is re-read on every request. Removed memberships invalidate their sessions.
    if not body.active:
        await p.conn.execute(
            sessions.update()
            .where(sessions.c.user_id == user_id, sessions.c.organization_id == oid)
            .values(revoked=True)
        )
    await record(p.conn, request, p.user["id"], oid, "membership.updated", user_id)
    user = (await p.conn.execute(sa.select(users).where(users.c.id == user_id))).mappings().one()
    return {
        "user_id": user_id,
        "email": user["email"],
        "name": user["name"],
        "role": body.role,
        "active": body.active,
        "revision": member["revision"] + 1,
    }


@router.get("/organization/audit", response_model=AuditsView)
async def audit_list(p: Auth, after: UUID | None = None) -> dict[str, Any]:
    await admin(p)
    query = sa.select(audit).where(audit.c.organization_id == p.session["organization_id"])
    if after:
        query = query.where(audit.c.id > after)
    rows = (await p.conn.execute(query.order_by(audit.c.id).limit(101))).mappings().all()
    return {
        "items": [dict(r) for r in rows[:100]],
        "as_of": now(),
        "next_cursor": str(rows[99]["id"]) if len(rows) > 100 else None,
    }
