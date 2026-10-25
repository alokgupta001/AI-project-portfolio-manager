"""Check the real persisted guided-demo workflow using stdin credentials; never print secrets."""

import asyncio
import json
import sys
from uuid import uuid4

import httpx
from ppm_api.config import load_settings
from ppm_api.main import create_app
from setup_guided_demo import ident


async def run() -> None:
    """Submit three small demo runs through normal authentication, jobs and quota admission."""
    credentials = json.load(sys.stdin)
    settings = load_settings()
    if settings.app_env != "local" or credentials["email"] != "guided-demo@example.com":
        raise SystemExit("Requires the dedicated local synthetic demo")
    app = create_app(settings)
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="https://guided-local"
        ) as client:
            await client.get("/api/v1/auth/csrf")

            async def post(path: str, body: dict) -> httpx.Response:
                """Use the normal CSRF, origin and idempotency controls."""
                return await client.post(
                    "/api/v1" + path,
                    json=body,
                    headers={
                        "origin": settings.web_origin,
                        "x-csrf-token": client.cookies.get("ppm_csrf", ""),
                        "idempotency-key": str(uuid4()),
                    },
                )

            login = await post("/auth/login", credentials)
            if login.status_code != 200:
                raise SystemExit(
                    f"Demo login failed ({login.status_code}); no response body logged"
                )
            client.headers["x-organization-id"] = str(ident("organization"))
            for role in ("financial", "agile_coach", "executive"):
                response = await post(
                    "/agents/runs",
                    dict(
                        project_id=str(ident("project")),
                        runtime_version="v2",
                        analysis_mode="guided",
                        requested_agents=[role],
                    ),
                )
                if response.status_code != 202:
                    raise SystemExit(
                        f"Demo start failed ({response.status_code}); no response body logged"
                    )
                run_id = response.json()["run"]["id"]
                for _ in range(100):
                    await asyncio.sleep(1)
                    result = await client.get("/api/v1/agents/runs/" + run_id)
                    if result.status_code != 200:
                        raise SystemExit(f"Demo read failed ({result.status_code})")
                    data = result.json()
                    if data["run"]["status"] in {
                        "succeeded",
                        "partially_succeeded",
                        "failed",
                        "cancelled",
                    }:
                        guided = data.get("guided_review") or {}
                        print(
                            json.dumps(
                                dict(
                                    role=role,
                                    run_id=run_id,
                                    status=data["run"]["status"],
                                    guided_status=guided.get("status"),
                                    code=guided.get("code"),
                                    cards=len(guided.get("cards", [])),
                                    checklists=len(guided.get("checklists", [])),
                                    routes=[
                                        dict(
                                            provider=r["provider_id"],
                                            code=r["code"],
                                            finish=r["finish_category"],
                                        )
                                        for r in data["route_summary"]
                                    ],
                                    charged_usd=data["run"]["charged_usd"],
                                )
                            ),
                            flush=True,
                        )
                        break
                else:
                    raise SystemExit("Demo job did not finish within 100 seconds")
            await post("/auth/logout", {})


if __name__ == "__main__":
    asyncio.run(run())
