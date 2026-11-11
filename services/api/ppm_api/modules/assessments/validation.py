"""Framework structure, question lookup and answer validity rules."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from ppm_api.modules.delivery.service import fail


def questions(snapshot: Any) -> Any:
    return {str(q["id"]): q for d in snapshot["dimensions"] for q in d["questions"]}


def validate_definition(snapshot: Any) -> Any:
    dims = snapshot["dimensions"]
    if not dims or sum(Decimal(str(d["weight"])) for d in dims) != 1:
        fail(422, "Dimension weights must sum exactly to 1")
    for d in dims:
        if not any(q["answer_type"] != "text" for q in d["questions"]):
            fail(422, "Each dimension requires at least one numeric question")
        for q in d["questions"]:
            levels = [v["level"] for v in q.get("rubric_levels", [])]
            if q["answer_type"] == "rubric" and (
                len(levels) < 2 or len(set(levels)) != len(levels)
            ):
                fail(422, "Rubrics require at least two distinct levels")
            if q["answer_type"] != "rubric" and levels:
                fail(422, "Only rubric questions may define levels")


def valid_answer(q: Any, value: Any) -> Any:
    if value is None or not str(value).strip():
        return False
    if q["answer_type"] == "text":
        return True
    if q["answer_type"] == "boolean":
        return value in ("true", "false")
    return str(value) in {str(v["level"]) for v in q["rubric_levels"]}
