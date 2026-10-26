"""Local identity, live session authorization and transaction-scoped tenant access."""

import asyncio
import hashlib
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, NoReturn
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

import bcrypt
import jwt
import sqlalchemy as sa
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncConnection

from ppm_api.errors import DomainError
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
    OrganizationProfileInput,
    ProfileInput,
    RegistrationInput,
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


def delivery_instructions(settings: Any, *, reset: bool = False) -> str:
    if settings.mail_mode == "local":
        return (
            "Email delivery is in local test mode; no inbox email will be sent. "
            "Ask the application operator for your private verification link."
        )
    return (
        "Check your inbox and spam folder. "
        + (
            "The recovery link expires in 30 minutes. "
            if reset
            else "The link expires in 24 hours. "
        )
        + "Email delivery may take a few minutes."
    )


def deny(status: int = 401, message: str | None = None) -> NoReturn:
    if message:
        raise DomainError(status, message)
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
            "org": str(session["organization_id"]) if session["organization_id"] else None,
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
    org: UUID | None,
    action: str,
    target: UUID | None = None,
) -> None:
    if org is None:
        return  # Tenant audit records require a membership; never invent an organization.
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
    organization_name: str | None = None,
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
            invitation_id=uuid4() if kind == "invite" else None,
            organization_name=organization_name,
        )
    )
    from ppm_api.account_mail import enqueue

    if org:
        organization_name = await conn.scalar(
            sa.select(organizations.c.name).where(organizations.c.id == org)
        )

    await enqueue(
        conn,
        settings,
        digest(token),
        {
            "to": email,
            "kind": kind,
            "expires_at": expires.isoformat(),
            "link": settings.web_origin + "/account/complete?action=" + kind + "#token=" + token,
            "organization_id": str(org) if org else None,
            "organization_name": organization_name,
            "role": role,
        },
    )


@dataclass
class Principal:
    conn: AsyncConnection
    user: Any
    session: Any
    role: str
    connector_id: UUID | None = None


@asynccontextmanager
async def authenticated(
    request: Request,
    x_organization_id: UUID | None = None,
    require_organization: bool = True,
) -> AsyncIterator[Principal]:
    try:
        claims = jwt.decode(
            request.cookies.get(ACCESS, ""),
            request.app.state.settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
            issuer="enterprise-ppm",
            audience="ppm-web",
            options={"require": ["exp", "iat", "sub", "sid", "jti"]},
        )
        uid, sid = UUID(claims["sub"]), UUID(claims["sid"])
        oid = UUID(claims["org"]) if claims["org"] else None
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
        user = (await conn.execute(sa.select(users).where(users.c.id == uid))).mappings().one()
        if not user["verified"] or not user["active"]:
            deny()
        if not member and require_organization:
            deny(
                403,
                "No active membership in this organization. Open Account and access to "
                "select another organization or ask an administrator for access.",
            )
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            if request.url.path.startswith("/api/v1/organization/") and x_organization_id != oid:
                # A precondition only, never tenant authority; rejects stale tabs after a switch.
                deny(409)
            if not secrets.compare_digest(
                session["csrf_hash"], digest(request.headers.get("x-csrf-token", ""))
            ):
                deny(403)
        role = member["role"] if member else ""
        effective = dict(session) if member else {**session, "organization_id": None}
        await context(conn, uid, effective["organization_id"], role)
        yield Principal(conn, user, effective, role)


async def principal(
    request: Request,
    x_organization_id: Annotated[UUID | None, Header()] = None,
) -> AsyncIterator[Principal]:
    async with authenticated(request, x_organization_id) as p:
        yield p


async def account_principal(request: Request) -> AsyncIterator[Principal]:
    async with authenticated(request, require_organization=False) as p:
        yield p


# Commit (or fail) the transaction before the response can trigger a follow-up read.
Auth = Annotated[Principal, Depends(principal, scope="function")]
AccountAuth = Annotated[Principal, Depends(account_principal, scope="function")]


async def admin(p: Principal) -> None:
    # Serialize all membership changes, preventing concurrent removal of the last admin.
    oid = p.session["organization_id"]
    await p.conn.execute(
        sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org, 2))"), {"org": str(oid)}
    )
    role = await p.conn.scalar(
        sa.select(memberships.c.role)
        .join(users, users.c.id == memberships.c.user_id)
        .where(
            memberships.c.organization_id == oid,
            memberships.c.user_id == p.user["id"],
            memberships.c.active,
            users.c.active,
            users.c.verified,
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
    role = next((r["role"] for r in rows if r["id"] == session["organization_id"]), None)
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
        if not user or not valid or not user["verified"] or not user["active"]:
            deny()
        await context(conn, user["id"])
        org = await conn.scalar(
            sa.select(memberships.c.organization_id)
            .where(memberships.c.user_id == user["id"], memberships.c.active)
            .order_by(memberships.c.organization_id)
            .limit(1)
        )
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
        user = (
            (await conn.execute(sa.select(users).where(users.c.id == session["user_id"])))
            .mappings()
            .one()
        )
        if not user["verified"] or not user["active"]:
            deny()
        if not member:
            await conn.execute(
                sessions.update().where(sessions.c.id == sid).values(organization_id=None)
            )
            session = {**session, "organization_id": None}
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
async def me(p: AccountAuth) -> dict[str, Any]:
    return await account(p.conn, p.user, p.session)


@router.patch("/auth/profile", response_model=Message)
async def profile(body: ProfileInput, request: Request, p: AccountAuth) -> dict[str, str]:
    await p.conn.execute(users.update().where(users.c.id == p.user["id"]).values(name=body.name))
    await record(p.conn, request, p.user["id"], p.session["organization_id"], "profile.updated")
    return {"message": "Profile updated."}


@router.post("/auth/switch", response_model=AccountView)
async def switch(
    body: SwitchInput, request: Request, response: Response, p: AccountAuth
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
async def logout(request: Request, response: Response, p: AccountAuth) -> dict[str, str]:
    await p.conn.execute(
        sessions.update().where(sessions.c.id == p.session["id"]).values(revoked=True)
    )
    await record(p.conn, request, p.user["id"], p.session["organization_id"], "session.logout")
    for key in (ACCESS, REFRESH, CSRF):
        cookie(response, request, key, "", 0, key != CSRF)
    return {"message": "Signed out."}


@router.get("/auth/sessions", response_model=SessionsView)
async def list_sessions(p: AccountAuth) -> dict[str, Any]:
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
async def revoke(session_id: UUID, request: Request, p: AccountAuth) -> dict[str, str]:
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
        "message": (
            "If the account is eligible, recovery instructions have been requested. "
            + delivery_instructions(request.app.state.settings, reset=True)
        )
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
        if user and not user["active"]:
            deny(400)
        oid = challenge["organization_id"]
        if challenge["kind"] == "register":
            if user:
                deny(400)
            oid = uuid4()
            await conn.execute(
                users.insert().values(
                    id=uid,
                    email=email,
                    name=body.name,
                    password_hash=await password_hash(body.password),
                    verified=True,
                    created_at=now(),
                )
            )
            await context(conn, uid, oid, "Admin")
            await conn.execute(
                organizations.insert().values(
                    id=oid, name=challenge["organization_name"], created_at=now()
                )
            )
            await conn.execute(
                memberships.insert().values(
                    organization_id=oid, user_id=uid, role="Admin", active=True, revision=1
                )
            )
            await record(conn, request, uid, oid, "registration.verified")
            await conn.execute(
                challenges.update()
                .where(challenges.c.email == email, challenges.c.kind == "register")
                .values(used=True)
            )
        elif challenge["kind"] == "invite":
            await context(conn, challenge["inviter_id"], oid, "Admin")
            await conn.execute(
                sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org, 2))"),
                {"org": str(oid)},
            )
            inviter = (
                await conn.execute(
                    sa.select(memberships)
                    .join(users)
                    .where(
                        memberships.c.organization_id == oid,
                        memberships.c.user_id == challenge["inviter_id"],
                        memberships.c.active,
                        memberships.c.role == "Admin",
                        users.c.active,
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
                deny(
                    409,
                    "This account already has a membership. An administrator must update its "
                    "role or active state instead of accepting another invitation.",
                )
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
    return {
        "message": "Password reset. You can sign in with your new password."
        if challenge["kind"] == "reset"
        else "Account verified. You can sign in now."
    }


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
    await p.conn.execute(
        challenges.update()
        .where(
            challenges.c.email == str(body.email).lower(),
            challenges.c.kind == "invite",
            challenges.c.organization_id == p.session["organization_id"],
        )
        .values(used=True)
    )
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
    return {"message": "Invitation requested. " + delivery_instructions(request.app.state.settings)}


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
            .select_from(memberships.join(users, users.c.id == memberships.c.user_id))
            .where(
                memberships.c.organization_id == oid,
                memberships.c.active,
                memberships.c.role == "Admin",
                users.c.active,
                users.c.verified,
            )
        )
        if (count or 0) <= 1:
            deny(
                409,
                "The final active administrator cannot be removed or demoted. "
                "Assign another administrator first.",
            )
    await p.conn.execute(
        memberships.update()
        .where(memberships.c.organization_id == oid, memberships.c.user_id == user_id)
        .values(role=body.role, active=body.active, revision=member["revision"] + 1)
    )
    # Live policy denies organization operations immediately. Preserve account sessions
    # so revoked members can manage their account and switch to another membership.
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


@router.post("/auth/register", response_model=Message)
async def register(body: RegistrationInput, request: Request) -> dict[str, str]:
    email = str(body.email).lower()
    await limited(request, "register", email, 3)
    await limited(
        request, "register-peer", request.client.host if request.client else "unknown", 30
    )
    async with request.app.state.engine.begin() as conn:
        await conn.execute(
            sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:email,0))"), {"email": email}
        )
        if not await conn.scalar(sa.select(users.c.id).where(users.c.email == email)):
            await conn.execute(
                challenges.update()
                .where(challenges.c.email == email, challenges.c.kind == "register")
                .values(used=True)
            )
            await issue_challenge(
                conn,
                request.app.state.settings,
                email,
                "register",
                organization_name=body.organization_name.strip(),
            )
    return {
        "message": (
            "If eligible, verification instructions have been requested. "
            "Existing accounts should sign in. " + delivery_instructions(request.app.state.settings)
        )
    }


@router.get("/organization/profile", response_model=dict)
async def organization_profile(p: Auth) -> dict:
    row = (
        (
            await p.conn.execute(
                sa.select(organizations).where(organizations.c.id == p.session["organization_id"])
            )
        )
        .mappings()
        .one()
    )
    admins = (
        (
            await p.conn.execute(
                sa.select(users.c.id, users.c.name)
                .join(memberships)
                .where(
                    memberships.c.organization_id == row["id"],
                    memberships.c.active,
                    memberships.c.role == "Admin",
                    users.c.active,
                )
                .order_by(users.c.name, users.c.id)
            )
        )
        .mappings()
        .all()
    )
    counts = (
        (
            await p.conn.execute(
                sa.select(
                    sa.func.count().label("members"),
                    sa.func.count().filter(memberships.c.active).label("active_members"),
                ).where(memberships.c.organization_id == row["id"])
            )
        )
        .mappings()
        .one()
    )
    from ppm_api.ppm_tables import TABLES

    settings = (
        (
            await p.conn.execute(
                sa.select(TABLES["settings"]).where(
                    TABLES["settings"].c.organization_id == row["id"]
                )
            )
        )
        .mappings()
        .first()
    )
    return {
        **{
            k: row[k]
            for k in ["name", "revision", "description", "industry", "website", "created_at"]
        },
        "administrators": [dict(a) for a in admins],
        **dict(counts),
        "timezone": settings["timezone"] if settings else None,
        "currency": settings["currency"] if settings else None,
        "setup_complete": bool(settings),
    }


@router.patch("/organization/profile", response_model=Message)
async def edit_organization(
    body: OrganizationProfileInput,
    request: Request,
    p: Auth,
    if_match: Annotated[int | None, Header()] = None,
) -> dict:
    await admin(p)
    row = await organization_profile(p)
    if if_match is None:
        deny(428)
    if if_match != row["revision"]:
        deny(412)
    values = body.model_dump(exclude_unset=True)
    if "name" in values and values["name"] is None:
        deny(422)
    values = {k: str(v).strip() or None if v is not None else None for k, v in values.items()}
    if all(row[k] == v for k, v in values.items()):
        return {"message": "Organization already up to date."}
    await p.conn.execute(
        organizations.update()
        .where(organizations.c.id == p.session["organization_id"])
        .values(**values, revision=if_match + 1)
    )
    await record(
        p.conn, request, p.user["id"], p.session["organization_id"], "organization.profile_updated"
    )
    return {"message": "Organization updated."}


def invitation_reference(row: Any) -> UUID:
    # Legacy invitations keep their original challenge/data; expose only an opaque reference.
    return row["invitation_id"] or uuid5(NAMESPACE_URL, "ppm:invitation:" + row["token_hash"])


@router.get("/organization/invitations", response_model=list[dict])
async def invitation_list(p: Auth) -> list[dict]:
    await admin(p)
    from ppm_api.pilot_tables import mail

    rows = (
        await p.conn.execute(
            sa.select(
                challenges.c.invitation_id,
                challenges.c.token_hash,
                challenges.c.email,
                challenges.c.role,
                challenges.c.expires_at,
                sa.func.coalesce(mail.c.status, "legacy_delivery_unverified").label(
                    "delivery_status"
                ),
            )
            .outerjoin(mail, mail.c.token_hash == challenges.c.token_hash)
            .where(
                challenges.c.organization_id == p.session["organization_id"],
                challenges.c.kind == "invite",
                ~challenges.c.used,
            )
            .order_by(challenges.c.expires_at, challenges.c.token_hash)
            .limit(100)
        )
    ).mappings()
    return [
        {k: v for k, v in dict(r).items() if k != "token_hash"}
        | {
            "invitation_id": invitation_reference(r),
            "delivery_status": (
                "acceptance_unverified"
                if r["delivery_status"] == "delivered"
                else r["delivery_status"]
            ),
        }
        for r in rows
    ]


@router.post("/organization/invitations/{invitation_id}/{operation}", response_model=Message)
async def invitation_action(invitation_id: UUID, operation: str, request: Request, p: Auth) -> dict:
    await admin(p)
    if operation not in {"resend", "cancel"}:
        deny(422)
    query = sa.select(challenges).where(
        challenges.c.organization_id == p.session["organization_id"],
        challenges.c.kind == "invite",
        ~challenges.c.used,
    )
    row = (
        (
            await p.conn.execute(
                query.where(challenges.c.invitation_id == invitation_id).with_for_update()
            )
        )
        .mappings()
        .first()
    )
    if row is None:
        candidates = (
            (
                await p.conn.execute(
                    query.where(challenges.c.invitation_id.is_(None))
                    .order_by(challenges.c.expires_at, challenges.c.token_hash)
                    .limit(100)
                    .with_for_update()
                )
            )
            .mappings()
            .all()
        )
        row = next((r for r in candidates if invitation_reference(r) == invitation_id), None)
    if not row:
        deny(404)
    await p.conn.execute(
        challenges.update().where(challenges.c.token_hash == row["token_hash"]).values(used=True)
    )
    if operation == "resend":
        await limited(request, "invite", str(p.user["id"]), 20)
        await issue_challenge(
            p.conn,
            request.app.state.settings,
            row["email"],
            "invite",
            p.session["organization_id"],
            p.user["id"],
            row["role"],
        )
    await record(
        p.conn, request, p.user["id"], p.session["organization_id"], "invitation." + operation
    )
    return {
        "message": "Invitation "
        + operation
        + " completed."
        + (" " + delivery_instructions(request.app.state.settings) if operation == "resend" else "")
    }
