"""Bound HTTP input before JSON/model parsing, including chunked requests."""

from uuid import uuid4

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class IntegrationBodyLimit:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] != "http"
            or scope["method"] in {"GET", "HEAD", "OPTIONS"}
            or not scope["path"].startswith(
                ("/api/v1/integrations", "/api/v1/documents", "/api/v1/ai")
            )
        ):
            await self.app(scope, receive, send)
            return
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            limit = 11200000 if scope["path"].startswith("/api/v1/documents") else 650000
            if len(body) > limit:
                response = JSONResponse(
                    status_code=413,
                    content={
                        "error": {
                            "code": "INPUT_LIMIT",
                            "message": "Request exceeds the input limit.",
                            "request_id": scope.get("state", {}).get("request_id", str(uuid4())),
                            "details": [],
                        }
                    },
                )
                await response(scope, receive, send)
                return
            if not message.get("more_body", False):
                break
        delivered = False

        async def bounded_receive() -> Message:
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, bounded_receive, send)
