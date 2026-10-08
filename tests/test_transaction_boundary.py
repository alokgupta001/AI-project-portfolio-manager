"""Authenticated transactions must finish before a success reaches the client."""

import httpx
import pytest
from fastapi import FastAPI
from ppm_api.identity import Auth, principal


@pytest.mark.parametrize("commit_fails", [False, True])
async def test_auth_transaction_finishes_before_response(commit_fails):
    app = FastAPI()
    events = []

    async def transaction():
        yield None
        events.append("commit")
        if commit_fails:
            raise RuntimeError("Commit failed")

    app.dependency_overrides[principal] = transaction

    @app.post("/write")
    async def write(p: Auth):
        return {"saved": True}

    async def observed(scope, receive, send):
        async def capture(message):
            if message["type"] == "http.response.start":
                events.append(message["status"])
            await send(message)

        await app(scope, receive, capture)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=observed, raise_app_exceptions=False),
        base_url="http://test",
    ) as client:
        response = await client.post("/write")
    expected = 500 if commit_fails else 200
    assert response.status_code == expected
    assert events == ["commit", expected]
