"""Deterministic maturity scores, weighted coverage and reviewer adjustments."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from ppm_api.modules.assessments.validation import valid_answer


def _normalize_rubric(value: Any, minimum: Any, maximum: Any) -> Any:
    try:
        v = Decimal(str(value))
        if not v.is_finite() or v != int(v) or minimum >= maximum or (not minimum <= v <= maximum):
            return None
        return (v - minimum) / Decimal(maximum - minimum)
    except (ValueError, ArithmeticError):
        return None


def compute_scores(snapshot: Any, answer_map: Any, reviewer_adjustments: Any = None) -> Any:
    notes = []
    results = {}
    overall = Decimal(0)
    unknown = False
    for d in snapshot.get("dimensions", []):
        numerator = denominator = answered_weight = Decimal(0)
        total_weight = sum((Decimal(str(q["weight"])) for q in d["questions"]), Decimal(0))
        answered = evidence = 0
        for q in d["questions"]:
            aid = str(q["id"])
            a = answer_map.get(aid, {})
            if a.get("evidence_text", "").strip() or a.get("has_attachment"):
                evidence += 1
            if not valid_answer(q, a.get("value")):
                if q.get("required", True):
                    notes.append(f"Required answer missing: {(q['name'] if 'name' in q else aid)}")
                continue
            w = Decimal(str(q["weight"]))
            answered_weight += w
            answered += 1
            if q["answer_type"] == "text":
                continue
            if q["answer_type"] == "boolean":
                norm = Decimal(1 if a["value"] == "true" else 0)
            else:
                levels = [lv["level"] for lv in q["rubric_levels"]]
                norm = _normalize_rubric(a["value"], min(levels), max(levels))
            if norm is None:
                continue
            if reviewer_adjustments and aid in reviewer_adjustments:
                norm = Decimal(str(reviewer_adjustments[aid])) / 100
            numerator += w * norm
            denominator += w
        score = (100 * numerator / denominator).quantize(Decimal("0.0001")) if denominator else None
        weight = Decimal(str(d["weight"]))
        if score is None:
            unknown = True
        else:
            overall += weight * score
        results[str(d["id"])] = dict(
            dimension_id=str(d["id"]),
            dimension_name=d["name"],
            score=score,
            weight=weight,
            answered_count=answered,
            total_required=sum(q.get("required", True) for q in d["questions"]),
            coverage_percent=(100 * answered_weight / total_weight).quantize(Decimal(".01"))
            if total_weight
            else Decimal(0),
            evidence_coverage_percent=(Decimal(100 * evidence) / len(d["questions"])).quantize(
                Decimal(".01")
            )
            if d["questions"]
            else Decimal(0),
        )
    if sum(Decimal(str(d["weight"])) for d in snapshot.get("dimensions", [])) != 1:
        unknown = True
    return (None if unknown or not results else overall.quantize(Decimal(".0001")), results, notes)
