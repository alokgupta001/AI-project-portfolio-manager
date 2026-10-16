"""Versioned deterministic release gates. These fixtures do not measure a real model."""

import json
from pathlib import Path
from uuid import UUID

from ppm_api.ai_provider import ProviderError
from ppm_api.ai_retrieval import evaluate
from ppm_api.ai_schemas import AIOutput


def run_evaluation() -> dict:
    document = json.loads(
        Path(__file__).with_name("ai_evaluation_v1.json").read_text(encoding="utf-8")
    )
    failures = []
    for case in document["cases"]:
        rows = [
            {**row, "id": UUID(row["id"]), "version_id": UUID(row["version_id"])}
            for row in case["evidence"]
        ]
        accepted = False
        try:
            evaluate(AIOutput.model_validate(case["output"]), rows)
            accepted = True
        except (ValueError, ProviderError):
            pass
        if accepted != case["accept"]:
            failures.append(case["id"])
    count = len(document["cases"])
    return dict(
        version=document["version"],
        environment="deterministic-fixtures-only",
        thresholds=document["thresholds"],
        count=count,
        passed=count - len(failures),
        failures=failures,
        eligible=not failures,
        real_provider_acceptance="BLOCKED",
        limitation="Passing these gates is not model accuracy or Sprint 11 acceptance",
    )
