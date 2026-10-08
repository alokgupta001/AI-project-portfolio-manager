"""Shared deterministic arithmetic for delivery DTOs and command-center consumers."""

from decimal import Decimal
from typing import Any


def budget_usage(spend: Decimal, budget: Decimal, complete: bool) -> Decimal | None:
    return (spend * 100 / budget).quantize(Decimal(".01")) if budget and complete else None


def alignment_score(goals: Any) -> Decimal | None:
    if not goals or sum(g["weight"] for g in goals) != 1:
        return None
    return sum((g["weight"] * g["contribution"] for g in goals), Decimal(0)) * 100
