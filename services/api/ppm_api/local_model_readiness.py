"""Read-only host memory and private Ollama inventory; never load or pull models."""

import ctypes
import json
import platform
import re
from urllib.parse import urlparse

import httpx

from ppm_api.model_registry import digest


def windows_memory() -> dict:
    """Read physical host RAM through Windows without estimating container memory."""
    if platform.system() != "Windows":
        raise OSError("Windows host memory measurement required")

    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
            (name, ctypes.c_ulonglong)
            for name in (
                "total",
                "available",
                "total_page",
                "available_page",
                "total_virtual",
                "available_virtual",
                "extended",
            )
        ]

    status = MemoryStatus()
    status.length = ctypes.sizeof(status)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
        raise OSError("Host memory unavailable")
    return dict(total_mb=status.total // 1048576, available_mb=status.available // 1048576)


def readiness(
    model: str,
    origin: str = "http://127.0.0.1:11434",
    reservation_mb: int = 4096,
    transport: httpx.BaseTransport | None = None,
) -> dict:
    """Inspect private Ollama inventory and host headroom without loading any model."""
    parsed = urlparse(origin)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in ("localhost", "127.0.0.1")
        or parsed.username
        or parsed.password
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Private host origin required")
    if ":cloud" in model or not 1024 <= reservation_mb <= 12000:
        raise ValueError("Bounded local profile required")
    hardware: dict = dict(
        os=platform.system(), os_version=platform.version(), architecture=platform.machine()
    )
    blocked = []
    try:
        hardware["memory"] = windows_memory()
        if hardware["memory"]["available_mb"] < reservation_mb + 2048:
            blocked.append("LOCAL_RESOURCE")
    except OSError:
        blocked.append("HOST_MEMORY_UNAVAILABLE")
    result = dict(
        schema_version="local-readiness-v1",
        hardware=hardware,
        hardware_record_sha256=digest(hardware),
        model=model,
        model_digest=None,
        reservation_mb=reservation_mb,
        headroom_mb=2048,
        inference_requests=0,
        qualified=False,
        blocked=blocked,
    )

    def read(client: httpx.Client, path: str) -> dict:
        """Read a bounded JSON object from a fixed local inventory endpoint."""
        with client.stream("GET", origin.rstrip("/") + path) as response:
            response.raise_for_status()
            raw = bytearray()
            for chunk in response.iter_bytes():
                raw.extend(chunk)
                if len(raw) > 1000000:
                    raise ValueError
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError
            return data

    try:
        with httpx.Client(
            transport=transport, timeout=3, trust_env=False, follow_redirects=False
        ) as client:
            result["ollama_version"] = read(client, "/api/version").get("version")
            models = read(client, "/api/tags").get("models", [])
            installed = [row for row in models if row.get("name") == model]
            if not installed:
                blocked.append("MODEL_NOT_INSTALLED")
            else:
                result["model_digest"] = installed[0].get("digest")
                result["model_details"] = installed[0].get("details")
                if not isinstance(result["model_digest"], str) or not re.fullmatch(
                    r"[a-f0-9]{64}", result["model_digest"]
                ):
                    blocked.append("MODEL_DIGEST_UNVERIFIED")
            running = read(client, "/api/ps").get("models", [])
            if len(running) > 1 or any(row.get("name") != model for row in running):
                blocked.append("OTHER_MODEL_RESIDENT")
    except (httpx.HTTPError, ValueError, TypeError, AttributeError):
        blocked.append("RUNTIME_UNAVAILABLE")
    return result
