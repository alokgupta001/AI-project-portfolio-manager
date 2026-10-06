import logging
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from ppm_api.main import create_app


def test_liveness_survives_unavailable_dependencies(settings):
    with TestClient(create_app(settings)) as client:
        assert client.get("/api/v1/health/live").json()["status"] == "alive"
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 503
        assert response.json()["status"] == "not_ready"
        assert {d["name"]: d["status"] for d in response.json()["dependencies"]} == {
            "database": "unavailable",
            "redis": "unavailable",
            "storage": "ready",
        }


def test_correlation_and_error_envelope(settings):
    with TestClient(create_app(settings)) as client:
        request_id = str(uuid4())
        response = client.get("/not-found", headers={"X-Request-ID": request_id})
        assert response.status_code == 404
        assert response.json()["error"]["request_id"] == request_id
        assert response.headers["X-Request-ID"] == request_id
        response = client.get("/api/v1/health/live", headers={"X-Request-ID": "untrusted"})
        UUID(response.headers["X-Request-ID"])


def test_secret_values_not_in_error_or_request_logs(settings, caplog):
    app = create_app(settings)

    @app.get("/test-error")
    async def trigger():
        raise RuntimeError("password=TOP_SECRET_PAYLOAD")

    caplog.set_level(logging.INFO, logger="ppm.requests")
    with TestClient(app) as client:
        result = client.get(
            "/test-error?token=QUERY_SECRET", headers={"Authorization": "Bearer HEADER_SECRET"}
        )
    assert result.status_code == 500
    assert result.json()["error"]["code"] == "INTERNAL_ERROR"
    request_logs = "\n".join(r.message for r in caplog.records if r.name == "ppm.requests")
    for secret in ("TOP_SECRET_PAYLOAD", "QUERY_SECRET", "HEADER_SECRET"):
        assert secret not in result.text
        assert secret not in request_logs


def test_validation_details_do_not_echo_inputs(settings):
    app = create_app(settings)

    @app.get("/test-validation/{count}")
    async def validate(count: int):
        return {"count": count}

    with TestClient(app) as client:
        response = client.get("/test-validation/SECRET_INPUT")
    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["field"] == "path.count"
    assert "SECRET_INPUT" not in response.text
