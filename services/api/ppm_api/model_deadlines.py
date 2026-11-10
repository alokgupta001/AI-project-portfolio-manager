"""Freeze longer waits only for ordinary cloud guided reviews, never fixture pilots."""

from ppm_api.config import Settings
from ppm_api.model_contracts import ModelFailure


def ordinary_guided(snapshot: dict) -> bool:
    """Recognize the run input, excluding the separate measured fixture journey."""
    return (
        snapshot.get("operation") == "agents"
        and snapshot.get("analysis_mode") == "guided"
        and not snapshot.get("guided_pilot_id")
    )


def completion_timeout(settings: Settings, run: dict, provider: str, guided: bool) -> int:
    """Honor a frozen bound; legacy, fixture, local and semantic runs retain 22s."""
    if guided and provider != "ollama" and ordinary_guided(run["snapshot"]):
        frozen = run["versions"].get("guided_cloud_timeout_seconds", 22)
        if type(frozen) is not int or not 1 <= frozen <= 60:
            raise ModelFailure("CONFIGURATION")
        return min(frozen, settings.ai_guided_cloud_timeout_seconds)
    return min(settings.ai_local_completion_timeout_seconds, 22)
