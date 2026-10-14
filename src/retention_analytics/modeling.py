"""Out-of-time diagnostic prediction for the composite funnel outcome.

This is experimental observational modeling, not a causal recommender.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from retention_analytics.profiles import record_profile
from retention_analytics.xlsx_stream import iter_worksheet_rows

CATEGORIES = ["origin", "uf", "mplay_m0", "classification", "mobile_flag"]
NUMBERS = [
    "family_count_m0", "has_bl_m0", "has_tv_m0", "has_fone_m0", "has_mv_m0",
    "value_bl_m0", "value_tv_m0", "value_mv_m0",
]
FEATURES = CATEGORIES + NUMBERS


def prepare_partitions(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Make train/validation/test client-disjoint and chronologically ordered."""
    grouped: dict[str, list[dict[str, Any]]] = {k: [] for k in ("train", "val", "test")}
    open_count = 0
    for record in records:
        if record["state"] not in ("RETIDO", "NAO RETIDO"):
            open_count += 1
            continue
        if not record["client_id"]:
            continue
        month = record["month"]
        if month <= "2025-09":
            split = "train"
        elif month == "2025-10":
            split = "val"
        else:
            split = "test"
        grouped[split].append(record)
    val_and_test_ids = {
        r["client_id"]
        for part in ("val", "test")
        for r in grouped[part]
    }
    test_ids = {r["client_id"] for r in grouped["test"]}
    removed_train = sum(r["client_id"] in val_and_test_ids for r in grouped["train"])
    removed_val = sum(r["client_id"] in test_ids for r in grouped["val"])
    grouped["train"] = [
        r for r in grouped["train"]
        if r["client_id"] not in val_and_test_ids
    ]
    grouped["val"] = [r for r in grouped["val"] if r["client_id"] not in test_ids]
    return {
        "partitions": grouped,
        "dropped_overlap_train": removed_train,
        "dropped_overlap_validation": removed_val,
        "excluded_open": open_count,
        "split_periods": {
            "train": "2025-06..2025-09",
            "val": "2025-10",
            "test": "2025-11..2025-12",
        },
    }


def evaluation(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    """Compute discrimination, calibration and fixed-capacity targeting metrics."""
    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)
    if y.size == 0 or set(np.unique(y)) != {0, 1}:
        raise ValueError("Evaluation needs nonempty samples with both target classes")
    top = max(1, int(np.ceil(y.size * 0.1)))
    rank = np.argsort(-p, kind="stable")[:top]
    baseline_rate = float(y.mean())
    # A constant score has no ranking; avoid arbitrary top-decile ordering.
    ranked_precision = baseline_rate if np.all(p == p[0]) else float(y[rank].mean())
    return {
        "n": int(len(y)),
        "prevalence": baseline_rate,
        "roc_auc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "precision_top_decile": ranked_precision,
        "lift_top_decile": ranked_precision / baseline_rate,
    }


def _matrix(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.array(
        [[r["features"][name] for name in FEATURES] for r in rows],
        dtype=object,
    )


def _model(estimator: Any) -> Pipeline:
    preprocess = ColumnTransformer(
        [
            ("categorical", Pipeline([
                ("impute", SimpleImputer(strategy="constant", fill_value="UNKNOWN")),
                ("encode", OneHotEncoder(handle_unknown="ignore", min_frequency=100)),
            ]), list(range(len(CATEGORIES)))),
            ("numeric", Pipeline([
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
            ]), list(range(len(CATEGORIES), len(FEATURES)))),
        ],
        sparse_threshold=0.3,
    )
    return Pipeline([("prepare", preprocess), ("classifier", estimator)])


def evaluate_models(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    partitions = prepare_partitions(records)
    data = partitions.pop("partitions")
    if any(not data[part] for part in ("train", "val", "test")):
        raise ValueError("At least one temporal split has no closed leads")
    x = {k: _matrix(v) for k, v in data.items()}
    y = {
        k: np.array([int(r["retained_movement"]) for r in v], dtype=int)
        for k, v in data.items()
    }
    models = {
        "baseline_constant": DummyClassifier(strategy="prior"),
        "logistic": _model(LogisticRegression(max_iter=700, C=0.2, random_state=42)),
        "interpretable_tree": _model(DecisionTreeClassifier(
            max_depth=5, min_samples_leaf=600, random_state=42,
        )),
    }
    valid_metrics = {}
    for name, estimator in models.items():
        estimator.fit(x["train"], y["train"])
        probabilities = estimator.predict_proba(x["val"])[:, 1]
        valid_metrics[name] = evaluation(y["val"], probabilities)
    winner = min(valid_metrics, key=lambda name: valid_metrics[name]["brier"])
    test_scores = {}
    for name in ("baseline_constant", winner):
        estimator = models[name]
        probability = estimator.predict_proba(x["test"])[:, 1]
        test_scores[name] = evaluation(y["test"], probability)
    counts = {
        k: {
            "n": len(v),
            "positive": int(y[k].sum()),
            "clients": len({r["client_id"] for r in v}),
        }
        for k, v in data.items()
    }
    return {
        "task": (
            "composite event RETIDO and any FLAG_MOV "
            "among leads with a closed status"
        ),
        "decision_time": "M0 (start of funnel); all predictors use M0 or static fields",
        "target_definition": "PROVISIONAL_NOT_VALIDATED",
        "splits": partitions,
        "split_counts": counts,
        "features": FEATURES,
        "validation_metrics": valid_metrics,
        "selected_by_validation_brier": winner,
        "test_metrics": test_scores,
        "limitations": [
            "Unknown official episode key; repeated episodes of a "
            "customer within a split remain.",
            "Cross-period customer IDs are purged to prevent direct "
            "leakage across splits.",
            "Open leads are excluded; closure/maturity selection bias is possible.",
            "Class labels and M0 availability are unvalidated, and "
            "observable period is only seven months.",
            "Predictive discrimination does not demonstrate causal "
            "uplift from an offer.",
            "Models have not been calibrated or validated on future unseen periods.",
        ],
    }


def model_workbook(source: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Run experimental models locally; persist metrics only, never IDs or rows."""
    records = (rec for row in iter_worksheet_rows(source)
               if (rec := record_profile(row)) is not None)
    metrics = evaluate_models(records)
    dst = Path(output_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics
