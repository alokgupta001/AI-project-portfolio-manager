"""Bounded recovery policy; retry budget lives in PostgreSQL, not this process."""

from ppm_api.model_contracts import ModelFailure


def recovery(
    error: ModelFailure, section_attempts: int, run_attempts: int, remaining: float
) -> str:
    if error.certainty == "unknown":
        return "stop"
    if section_attempts >= 2 or run_attempts >= 4 or remaining < 27:
        return "stop"
    if error.code in ("TRUNCATED", "INVALID_OUTPUT", "CONTEXT_LIMIT"):
        return "repair"
    if error.code == "UNAVAILABLE" and error.certainty == "not_sent":
        return "retry"
    if error.code in (
        "QUOTA_EXHAUSTED",
        "AUTHENTICATION",
        "LOCAL_RESOURCE",
        "MODEL_NOT_INSTALLED",
        "TIMEOUT",
    ):
        return "fallback"
    return "stop"
