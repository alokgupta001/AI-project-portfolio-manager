"""Private account delivery outbox. Provider failures expose only bounded error codes."""

import asyncio
import json
import os
import smtplib
import ssl
from datetime import timedelta
from email.message import EmailMessage
from email.utils import formatdate, parseaddr
from typing import Any
from uuid import uuid4

import sqlalchemy as sa

from ppm_api.identity_tables import challenges, memberships, users
from ppm_api.pilot_tables import mail


def local_delivery(settings: Any, payload: dict, delivery_id: Any) -> None:
    folder = settings.storage_root / "__identity_mailbox__"
    folder.mkdir(parents=True, exist_ok=True)
    folder.chmod(0o700)
    path = folder / (str(delivery_id) + ".json")
    try:
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as output:
            output.write(json.dumps(payload))
    except FileExistsError:
        pass  # Stable delivery identifier makes local retries idempotent.


def account_message(settings: Any, payload: dict, delivery_id: Any) -> EmailMessage:
    """Render private, plain-text account instructions without logging the challenge."""
    from urllib.parse import urlsplit

    kind = payload["kind"]
    organization = payload.get("organization_name") or "your organization"
    origin = urlsplit(payload["link"])
    website = f"{origin.scheme}://{origin.netloc}"
    if kind == "invite":
        subject = "Enterprise PPM: invitation to " + organization
        instruction = (
            f"You have been invited to {organization} as {payload.get('role') or 'a member'}.\n"
            "Open the link below to accept. New users choose a display name and password. "
            "If you already have a verified account, enter your existing password.\n"
            "If this link expires or is cancelled, ask your organization Admin "
            "for a new invitation."
        )
    elif kind == "reset":
        subject = "Enterprise PPM: reset your password"
        instruction = (
            "A password reset was requested for your account. Open the link below and choose "
            "a new password. Changing your password signs out existing sessions.\n"
            f"If the link expires, request a replacement at {website}/account/reset."
        )
    elif kind == "register":
        subject = "Enterprise PPM: verify your email"
        instruction = (
            f"Verify your email to create {organization}. Open the link below, enter your "
            "display name and choose a password. Your organization is created after verification.\n"
            f"If the link expires, request verification again at {website}/signup."
        )
    elif kind == "activate":
        subject = "Enterprise PPM: activate your account"
        instruction = (
            "Open the link below to activate your account with a display name and password.\n"
            "If the link expires, ask your organization Admin for help."
        )
    else:
        raise ValueError("Unsupported account message")
    message = EmailMessage()
    message["From"] = settings.mail_sender
    message["To"] = payload["to"]
    # Organization names are user input; normalize line breaks before creating a header.
    message["Subject"] = " ".join(subject.splitlines())
    domain = parseaddr(settings.mail_sender)[1].rsplit("@", 1)[-1]
    message["Message-ID"] = f"<{delivery_id}@{domain}>"
    message["Date"] = formatdate(localtime=False, usegmt=True)
    message.set_content(
        instruction
        + "\n\n"
        + payload["link"]
        + "\n\nExpires at: "
        + payload["expires_at"]
        + " (timestamp includes timezone).\n"
        + "This link is private and can be used once. Do not forward it.\n"
        + "For a new password, use at least 12 characters and no more than 72 UTF-8 bytes.\n"
        + f"After completing the form, sign in at {website}/login.\n"
        + "If you did not request this message or expect an invitation, you can ignore it.\n"
    )
    return message


def smtp_delivery(settings: Any, payload: dict, delivery_id: Any) -> None:
    if not settings.smtp_host or not settings.mail_sender:
        raise RuntimeError("PROVIDER_DISABLED")
    message = account_message(settings, payload, delivery_id)
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
        server.starttls(context=ssl.create_default_context())
        if settings.smtp_user:
            server.login(settings.smtp_user, settings.smtp_password.get_secret_value())
        refused = server.send_message(message)
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)


async def enqueue(conn: Any, settings: Any, token_hash: str, payload: dict) -> None:
    from ppm_api.identity import now

    id_ = uuid4()
    await conn.execute(
        mail.insert().values(
            id=id_,
            token_hash=token_hash,
            payload=payload,
            status="queued",
            attempts=0,
            available_at=now(),
            created_at=now(),
        )
    )
    if settings.mail_mode == "local":
        # Operator preview only; a rolled-back/expired challenge can never grant access.
        await asyncio.to_thread(local_delivery, settings, payload, id_)
        await conn.execute(
            mail.update()
            .where(mail.c.id == id_)
            .values(status="local_preview", attempts=1, payload={})
        )


async def deliver_due(engine: Any, settings: Any) -> int:
    from ppm_api.identity import context, now

    delivered = 0
    for _ in range(20):
        async with engine.begin() as conn:
            row = (
                (
                    await conn.execute(
                        sa.select(mail)
                        .where(mail.c.status == "queued", mail.c.available_at <= now())
                        .order_by(mail.c.available_at, mail.c.id)
                        .with_for_update(skip_locked=True)
                        .limit(1)
                    )
                )
                .mappings()
                .first()
            )
            if not row:
                break
            challenge = (
                (
                    await conn.execute(
                        sa.select(challenges).where(challenges.c.token_hash == row["token_hash"])
                    )
                )
                .mappings()
                .one()
            )
            valid = not challenge["used"] and challenge["expires_at"] > now()
            if valid and challenge["kind"] == "invite":
                await context(conn, challenge["inviter_id"], challenge["organization_id"], "Admin")
                await conn.execute(
                    sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"),
                    {"org": str(challenge["organization_id"])},
                )
                valid = bool(
                    await conn.scalar(
                        sa.select(memberships.c.active)
                        .join(users, users.c.id == memberships.c.user_id)
                        .where(
                            memberships.c.organization_id == challenge["organization_id"],
                            memberships.c.user_id == challenge["inviter_id"],
                            memberships.c.active,
                            memberships.c.role == "Admin",
                            users.c.active,
                            users.c.verified,
                        )
                    )
                )
            if not valid:
                await conn.execute(
                    mail.update()
                    .where(mail.c.id == row["id"])
                    .values(status="cancelled", payload={})
                )
                continue
            attempts = row["attempts"] + 1
            try:
                adapter = local_delivery if settings.mail_mode == "local" else smtp_delivery
                await asyncio.to_thread(adapter, settings, row["payload"], row["id"])
            except Exception:
                await conn.execute(
                    mail.update()
                    .where(mail.c.id == row["id"])
                    .values(
                        attempts=attempts,
                        status="failed" if attempts >= 5 else "queued",
                        error_code="DELIVERY_UNCONFIRMED",
                        payload={} if attempts >= 5 else row["payload"],
                        available_at=now() + timedelta(seconds=min(600, 15 * 2**attempts)),
                    )
                )
            else:
                await conn.execute(
                    mail.update()
                    .where(mail.c.id == row["id"])
                    .values(
                        status="local_preview"
                        if settings.mail_mode == "local"
                        else "provider_accepted",
                        attempts=attempts,
                        error_code=None,
                        payload={},
                    )
                )
                delivered += 1
    return delivered
