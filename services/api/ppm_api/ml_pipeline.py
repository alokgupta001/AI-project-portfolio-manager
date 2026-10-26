"""Bounded offline dataset construction and deterministic CPU evaluation; no serving."""

import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ppm_api.ingestion import fingerprint
from ppm_api.ml_schemas import FEATURES, TARGETS, DatasetInput, HistoryInput, Observation

PIPELINE_VERSION = "local-baseline-v1"
SEED = 12


def label(row: Observation) -> float | None:
    """Compute a target only from compatible, explicitly recorded outcome facts."""
    o = row.outcome
    if not o:
        return None
    if o.target == "delay" and o.planned_finish and o.actual_finish:
        if o.actual_finish != o.occurred_at.date():
            raise ValueError("Actual finish must match the recorded outcome date")
        if o.planned_finish < row.observed_at.date():
            raise ValueError("Delay target must be prospective at observation")
        return float(max(0, (o.actual_finish - o.planned_finish).days))
    if o.target == "overrun" and o.budget and o.actual_spend is not None:
        return max(0.0, (o.actual_spend / o.budget - 1) * 100)
    if o.target == "failure" and o.disposition:
        return float(o.disposition != "accepted")
    if o.target == "risk" and o.adjudication and o.adverse_category is not None:
        return float(o.adverse_category)
    if o.target == "sentiment" and o.survey_mean is not None and o.respondents and o.consent:
        if row.entity_kind != "team":
            raise ValueError("Sentiment requires team aggregates")
        return float(o.survey_mean <= 2)
    raise ValueError("Outcome facts are unsuitable for the declared target")


def build_dataset(history: HistoryInput, spec: DatasetInput) -> tuple[dict, list[dict]]:
    """Purge boundary-crossing entities and embargo labels at each split boundary."""
    from datetime import UTC

    if spec.cutoff > datetime.now(UTC):
        raise ValueError("Dataset cutoff cannot be in the future")
    candidates: list[dict[str, Any]] = []
    excluded: Counter[str] = Counter()
    entity_splits: dict[str, set[str]] = {}
    for index, row in enumerate(history.records):
        partition = (
            "train"
            if row.observed_at < spec.train_end
            else "validation"
            if row.observed_at < spec.validation_end
            else "test"
        )
        entity_splits.setdefault(row.entity_id, set()).add(partition)
        boundary = {
            "train": spec.train_end,
            "validation": spec.validation_end,
            "test": spec.cutoff,
        }[partition]
        if row.observed_at + timedelta(days=spec.horizon_days) > boundary:
            excluded["horizon_crosses_boundary"] += 1
            continue
        o = row.outcome
        if not o or o.target != spec.target:
            excluded["missing_or_incompatible_outcome"] += 1
            continue
        if o.available_at > boundary:
            excluded["outcome_not_available_at_boundary"] += 1
            continue
        if o.occurred_at > row.observed_at + timedelta(days=spec.horizon_days):
            excluded["outside_target_horizon"] += 1
            continue
        y = label(row)
        candidates.append(
            dict(
                row_id=index,
                entity_id=row.entity_id,
                split=partition,
                observed_at=row.observed_at.isoformat(),
                label_available_at=o.available_at.isoformat(),
                evidence_ref=o.evidence_ref,
                x=row.features.model_dump(),
                y=y,
            )
        )
    records: list[dict[str, Any]] = []
    for r in candidates:
        if len(entity_splits[r["entity_id"]]) != 1:
            excluded["entity_crosses_splits"] += 1
        else:
            records.append(r)
    counts = dict(Counter(r["split"] for r in records))
    reasons = [
        f"{s}: requires at least {n} labeled rows"
        for s, n in (("train", 12), ("validation", 4), ("test", 4))
        if counts.get(s, 0) < n
    ]
    classification = spec.target in {"risk", "failure", "sentiment"}
    balance = {
        s: dict(Counter(str(r["y"]) for r in records if r["split"] == s))
        for s in ("train", "validation", "test")
    }
    if classification:
        reasons += [
            f"{s}: both classes required" for s, values in balance.items() if len(values) != 2
        ]
    if records and not any(
        r["x"][f] is not None for r in records if r["split"] == "train" for f in FEATURES
    ):
        reasons.append("No observed training features")
    manifest = dict(
        schema_version=1,
        target=spec.target,
        definition=TARGETS[spec.target],
        task="classification" if classification else "regression",
        horizon_days=spec.horizon_days,
        cutoff=spec.cutoff.isoformat(),
        train_end=spec.train_end.isoformat(),
        validation_end=spec.validation_end.isoformat(),
        features=list(FEATURES),
        feature_units={
            "velocity": "team points/period",
            "bugs": "count",
            "scope_change": "work item count delta",
            "spend_ratio": "ratio",
            "dependencies": "count",
            "allocation_percent": "percent",
        },
        lineage=history.lineage,
        origin=history.origin,
        license=history.license,
        label_declaration=history.label_declaration,
        privacy=history.privacy,
        entity_scope=(
            "pseudonymous entity IDs within owning project; no cross-team velocity comparison"
        ),
        split_counts=counts,
        class_balance=balance,
        excluded=dict(excluded),
        entity_overlap=0,
        temporal_policy="strict label-availability embargo; purge crossing entities",
        missing_values={f: sum(r["x"][f] is None for r in records) for f in FEATURES},
        eligibility="insufficient_data"
        if reasons
        else "demo_only"
        if history.lineage == "synthetic"
        else "research_only",
        reasons=reasons,
        text_policy="No raw text accepted; withdrawal invalidates all descendants",
        provenance=[
            dict(
                row_id=r["row_id"],
                evidence_ref=r["evidence_ref"],
                split=r["split"],
                label_available_at=r["label_available_at"],
            )
            for r in records
        ],
    )
    return manifest, records


def evaluate(manifest: dict, records: list[dict], digest: str) -> tuple[dict, dict]:
    """Fit imputation on training only; select on validation, report held-out test once."""
    import numpy as np
    import pandas as pd
    import sklearn
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.metrics import (
        average_precision_score,
        brier_score_loss,
        mean_absolute_error,
        recall_score,
    )
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    code_hash = hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    card: dict[str, Any] = dict(
        pipeline_version=PIPELINE_VERSION,
        dataset_hash=digest,
        code_hash=code_hash,
        seed=SEED,
        library_versions={
            "pandas": pd.__version__,
            "scikit-learn": sklearn.__version__,
            "numpy": np.__version__,
        },
        eligibility=manifest["eligibility"],
        promotion="BLOCKED — Sprint 13 is not authorized",
        target=manifest["target"],
        definition=manifest["definition"],
        horizon_days=manifest["horizon_days"],
        lineage=manifest["lineage"],
        source_provenance={
            k: manifest.get(k)
            for k in (
                "origin",
                "license",
                "privacy",
                "label_declaration",
                "history_hash",
                "history_version",
                "cutoff",
                "train_end",
                "validation_end",
                "temporal_policy",
                "entity_scope",
            )
        },
        counts=manifest["split_counts"],
        class_balance=manifest["class_balance"],
        missing_data=(
            "Training-median imputation; empty training columns use zero; missing indicators"
        ),
        reasons=manifest["reasons"],
        tolerance=1e-10,
        limitations=[
            "Synthetic metrics demonstrate the pipeline only; no real-world accuracy claim.",
            "Imported real outcomes are organization-attested, not independently verified.",
            "Small, observational samples do not establish calibration or deployment suitability.",
            "Velocity is meaningful only within a compatible team/period.",
            "No forecasts are served. AT17 remains BLOCKED.",
            "MLflow-compatible JSON export only; native MLflow tracking/import remains deferred.",
            "XGBoost and DistilBERT deferred: no suitable genuine labels; no model downloads.",
        ],
        metrics={},
        candidates={},
    )
    if manifest["reasons"]:
        return card, {"tracking": {"params": {"seed": SEED}, "status": "insufficient_data"}}
    frame = pd.DataFrame([r["x"] for r in records], columns=list(FEATURES), dtype=float)
    y = np.array([r["y"] for r in records], dtype=float)
    indices = {
        s: np.array([i for i, r in enumerate(records) if r["split"] == s])
        for s in ("train", "validation", "test")
    }
    classification = manifest["task"] == "classification"
    estimators = (
        {
            "constant_prior": DummyClassifier(strategy="prior"),
            "logistic": LogisticRegression(random_state=SEED, max_iter=500),
            "random_forest": RandomForestClassifier(
                n_estimators=32, max_depth=4, min_samples_leaf=2, random_state=SEED, n_jobs=1
            ),
        }
        if classification
        else {
            "constant_mean": DummyRegressor(),
            "ridge": Ridge(alpha=1),
            "random_forest": RandomForestRegressor(
                n_estimators=32, max_depth=4, min_samples_leaf=2, random_state=SEED, n_jobs=1
            ),
        }
    )
    models = {}
    predictions = {}

    def metrics(actual: Any, pred: Any) -> dict:
        if not classification:
            return {"mae": float(mean_absolute_error(actual, pred))}
        return dict(
            pr_auc=float(average_precision_score(actual, pred)),
            recall=float(recall_score(actual, pred >= 0.5, zero_division=0)),
            brier=float(brier_score_loss(actual, pred)),
            calibration=[
                dict(
                    n=int(mask.sum()),
                    predicted=float(pred[mask].mean()),
                    observed=float(actual[mask].mean()),
                )
                for lo, hi in [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.00001)]
                if (mask := (pred >= lo) & (pred < hi)).any()
            ],
        )

    for name, estimator in estimators.items():
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            StandardScaler(),
            estimator,
        )
        train = indices["train"]
        model.fit(frame.iloc[train], y[train])
        results = {}
        for s in ("validation", "test"):
            idx = indices[s]
            pred = (
                model.predict_proba(frame.iloc[idx])[:, 1]
                if classification
                else model.predict(frame.iloc[idx])
            )
            results[s] = metrics(y[idx], pred)
            if s == "test":
                predictions[name] = pred.tolist()
        card["candidates"][name] = results
        models[name] = model
    metric = "brier" if classification else "mae"
    selected = min(estimators, key=lambda n: (card["candidates"][n]["validation"][metric], n))
    card["selected"] = selected
    card["selection_rule"] = (
        f"Minimum validation {metric}; deterministic name tie-break; test excluded from selection"
    )
    card["metrics"] = card["candidates"][selected]["test"]
    baseline = "constant_prior" if classification else "constant_mean"
    card["baseline_comparison"] = dict(
        metric=metric,
        baseline=card["candidates"][baseline]["test"][metric],
        selected=card["metrics"][metric],
    )
    actual = y[indices["test"]]
    pred = np.array(predictions[selected])
    errors = (actual - pred) ** 2 if classification else np.abs(actual - pred)
    rng = np.random.default_rng(SEED)
    samples = [float(rng.choice(errors, size=len(errors), replace=True).mean()) for _ in range(200)]
    card["uncertainty"] = dict(
        metric=metric,
        bootstrap_95_percentile=np.quantile(samples, [0.025, 0.975]).tolist(),
        repetitions=200,
        caveat="Descriptive row bootstrap; not population or causal confidence",
    )
    forest = models["random_forest"][-1]
    trees = [
        dict(
            children_left=e.tree_.children_left.tolist(),
            children_right=e.tree_.children_right.tolist(),
            feature=e.tree_.feature.tolist(),
            threshold=e.tree_.threshold.tolist(),
            value=e.tree_.value.tolist(),
        )
        for e in forest.estimators_
    ]
    artifacts = dict(
        predictions=predictions,
        test_row_ids=[records[i]["row_id"] for i in indices["test"]],
        random_forest_trees=trees,
        preprocessing={
            name: dict(
                statistics=model[0].statistics_.tolist(),
                indicator_features=model[0].indicator_.features_.tolist(),
                scale=model[1].scale_.tolist(),
                mean=model[1].mean_.tolist(),
            )
            for name, model in models.items()
        },
        coefficients={
            name: dict(
                coef=model[-1].coef_.tolist(), intercept=np.asarray(model[-1].intercept_).tolist()
            )
            for name, model in models.items()
            if hasattr(model[-1], "coef_")
        },
        tracking=dict(
            format="mlflow-compatible-json-v1",
            experiment_id="local-sprint12",
            params={"seed": SEED, "trees": 32, "max_depth": 4, "n_jobs": 1},
            metrics=card["metrics"],
            tags={"dataset_hash": digest, "code_hash": code_hash, "lineage": manifest["lineage"]},
        ),
    )
    card["artifact_hash"] = fingerprint(artifacts)
    card["result_hash"] = fingerprint(card)
    # Round-trip guarantees artifacts are finite JSON, with no executable model deserialization.
    json.dumps(artifacts, allow_nan=False)
    return card, artifacts
