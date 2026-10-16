"""Seed/check a synthetic restored document through actual authenticated API and object bytes."""

import asyncio
import base64
import hashlib
import json
import os
import secrets
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from ppm_api.config import load_settings
from ppm_api.documents import document_worker
from ppm_api.identity import now, password_hash
from ppm_api.identity_tables import memberships, organizations, users
from ppm_api.main import create_app
from pydantic import SecretStr
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine


async def run() -> None:
    mode = os.environ.get("PPM_RECOVERY_PHASE", "")
    root = Path("/recovery")
    config = load_settings()
    source_url = make_url(config.database_url.get_secret_value())
    if (
        config.app_env != "test"
        or source_url.database != "ppm_test"
        or mode not in {"seed", "verify"}
    ):
        raise SystemExit("Recovery fixtures require test/ppm_test and explicit phase")
    fixture_file = root / "document-fixture.json"
    if mode == "seed":
        if fixture_file.exists():
            raise SystemExit("Refusing to overwrite recovery fixture")
        password, uid, org = secrets.token_urlsafe(24), uuid4(), uuid4()
        email = f"recovery-{uid}@example.com"
        engine = create_async_engine(os.environ["PPM_MIGRATION_DATABASE_URL"])
        try:
            async with engine.begin() as conn:
                await conn.execute(
                    organizations.insert().values(
                        id=org, name="Synthetic recovery", created_at=now()
                    )
                )
                await conn.execute(
                    users.insert().values(
                        id=uid,
                        name="Recovery fixture",
                        email=email,
                        verified=True,
                        active=True,
                        password_hash=await password_hash(password),
                        created_at=now(),
                    )
                )
                await conn.execute(
                    memberships.insert().values(
                        organization_id=org, user_id=uid, role="Admin", active=True, revision=1
                    )
                )
        finally:
            await engine.dispose()
        config.storage_root = root / "source-objects"
    else:
        fixture = json.loads(fixture_file.read_text())
        email, password, org, uid = (
            fixture["email"],
            fixture["password"],
            UUID(fixture["org"]),
            UUID(fixture["uid"]),
        )
        config.database_url = SecretStr(
            source_url.set(database="ppm_sprint09_documents_restore").render_as_string(
                hide_password=False
            )
        )
        config.storage_root = root / "restored-document-objects"
    app = create_app(config)
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="https://testserver"
        ) as client,
    ):
        await client.get("/api/v1/auth/csrf")

        async def send(method: str, path: str, **kwargs):
            return await client.request(
                method,
                "/api/v1" + path,
                headers={
                    "origin": config.web_origin,
                    "x-csrf-token": client.cookies.get("ppm_csrf"),
                    "x-organization-id": str(org),
                    "idempotency-key": str(uuid4()),
                },
                **kwargs,
            )

        login = await send("POST", "/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200
        if mode == "seed":
            upload = await send(
                "POST",
                "/documents",
                json={
                    "title": "Restorable synthetic policy",
                    "category": "policy",
                    "filename": "policy.txt",
                    "content_base64": base64.b64encode(
                        b"Recovery approval requires authorized source evidence."
                    ).decode(),
                },
            )
            assert upload.status_code == 202, upload.text
            accepted = upload.json()
            await document_worker(app.state.engine, UUID(accepted["job_id"]), org, uid, config)
            fixture = dict(
                email=email,
                password=password,
                org=str(org),
                uid=str(uid),
                document_id=accepted["document"]["id"],
                version_id=accepted["version_id"],
                sha256=hashlib.sha256(
                    b"Recovery approval requires authorized source evidence."
                ).hexdigest(),
            )
            fixture_file.write_text(json.dumps(fixture))
        ticket = await send("POST", f"/documents/versions/{fixture['version_id']}/download-ticket")
        assert ticket.status_code == 200, ticket.text
        download = await client.get(
            f"/api/v1/documents/versions/{fixture['version_id']}/download",
            params={"token": ticket.json()["token"]},
        )
        assert download.status_code == 200
        assert hashlib.sha256(download.content).hexdigest() == fixture["sha256"]
        result = await client.get("/api/v1/documents/search?q=Recovery")
        assert (
            result.status_code == 200
            and result.json()["items"][0]["document_id"] == fixture["document_id"]
        )
    print(
        f"PASS {mode}: authenticated signed original and keyword citation "
        "match restored fixture hash"
    )


asyncio.run(run())
