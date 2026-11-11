"""Exact arithmetic audit for the original synthetic protocol; no human attestation."""

import re
from fractions import Fraction

from ppm_api.modules.ai.registry import digest
from ppm_api.modules.selection.protocol import protocol

CORPUS = "537f42bb85456da4e298ef97d3cf9cc46584f3f20b9509a157f83c4e69e7322a"
STRATEGY = "71c321aa1579a5e71c90eaa14a0b9c440c8f6837a9cd8fa8c5d29925bd8de4e0"


def audit(value: dict) -> dict:
    """Check a pinned CC0 numeric corpus with Fraction, independently of Decimal labeling."""
    if (
        value != protocol()
        or value.get("corpus_sha256") != CORPUS
        or value.get("strategy_sha256") != STRATEGY
        or value.get("lineage") != "synthetic"
        or value.get("license") != "CC0-1.0"
        or len(value.get("cases", [])) != 12
    ):
        raise ValueError("Automated audit requires the original synthetic protocol")
    checks = []
    for index, case in enumerate(value["cases"], 1):
        expected = []
        if case["id"] != f"f{index:02}" or case["split"] != (
            "calibration" if index <= 6 else "held_out"
        ):
            raise ValueError("Fixture identity or split changed")
        for ordinal, observation in enumerate(case["observations"], 1):
            if (
                observation["id"] != f"o{ordinal}"
                or not re.fullmatch(r"\d+\.\d{2}", observation["value"])
                or type(observation["partial"]) is not bool
            ):
                raise ValueError("Only bounded numeric fixtures may be audited")
            if observation["partial"] or Fraction(observation["value"]) >= 100:
                expected.append(observation["id"])
        if expected != case["expected"]:
            raise ValueError("Fixture label does not match the declared rule")
        checks.append(dict(case=case["id"], split=case["split"], expected=expected, matches=True))
    return dict(
        method="exact_fraction_rule_check_v1",
        corpus_sha256=CORPUS,
        strategy_sha256=STRATEGY,
        checked_cases=12,
        matching_cases=12,
        checks=checks,
        human_reviewed=False,
        evidence_sha256=digest(checks),
        lineage="synthetic",
    )
