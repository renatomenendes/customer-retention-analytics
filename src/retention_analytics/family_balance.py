# ruff: noqa: E501
"""Product-family imbalance and model sensitivity for retained funnel records.

Observational study: no direct offer-acceptance measurement. Each family has a
separate binary outcome, restricted to those possessing the family in M0.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from retention_analytics.audit import PRODUCTS
from retention_analytics.study_profiles import _pipeline, extract
from retention_analytics.xlsx_stream import iter_worksheet_rows

SPLITS = {
    "train": ("2025-06", "2025-09"),
    "val": ("2025-10", "2025-10"),
    "test": ("2025-11", "2025-12"),
}


def family_exposure(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per-family movements over holders in initial portfolio."""
    counts = {family: Counter() for family in PRODUCTS}
    for row in rows:
        if row is None:
            continue
        for j, family in enumerate(PRODUCTS):
            if row["x"][7 + j]:
                counts[family]["n"] += 1
                counts[family]["positive"] += bool(row["moves"][family])
                counts[family]["negative"] += not bool(row["moves"][family])
    return {
        f: {
            "n": c["n"],
            "positive": c["positive"],
            "negative": c["negative"],
            "rate": c["positive"] / c["n"] if c["n"] else None,
        }
        for f, c in counts.items()
    }


def scores(y: np.ndarray, p: np.ndarray, top_share: float = 0.1) -> dict[str, Any]:
    """AUC, AP relative to prevalence, Brier and fixed-capacity precision/recall."""
    if not 0 < top_share <= 1:
        raise ValueError("top_share must be in (0, 1]")
    y, p = np.asarray(y, int), np.asarray(p, float)
    if len(y) == 0 or set(np.unique(y)) != {0, 1}:
        raise ValueError("both target classes needed")
    n = max(1, int(np.ceil(len(y) * top_share)))
    rank = np.argsort(-p, kind="stable")[:n]
    prevalence = float(y.mean())
    precision = prevalence if np.all(p == p[0]) else float(y[rank].mean())
    recall = top_share if np.all(p == p[0]) else float(y[rank].sum() / y.sum())
    ap = float(average_precision_score(y, p))
    return {
        "n": len(y),
        "positive": int(y.sum()),
        "prevalence": prevalence,
        "auc": float(roc_auc_score(y, p)),
        "average_precision": ap,
        "ap_lift": ap / prevalence,
        "brier": float(brier_score_loss(y, p)),
        "precision_top10": precision,
        "recall_top10": recall,
        "lift_top10": precision / prevalence,
    }


def prepare_splits(records: list[dict[str, Any]]) -> tuple[dict[str, list], dict[str, int]]:
    """Chronological evaluation with customer-disjoint splits."""
    pools: dict[str, list] = {k: [] for k in SPLITS}
    for row in records:
        if not row["id"]:
            continue
        month = row["month"]
        part = next(k for k, (lo, hi) in SPLITS.items() if lo <= month <= hi)
        pools[part].append(row)
    ids_test = {r["id"] for r in pools["test"]}
    ids_val = {r["id"] for r in pools["val"]}
    purged = {
        "train": sum(r["id"] in ids_test or r["id"] in ids_val for r in pools["train"]),
        "val": sum(r["id"] in ids_test for r in pools["val"]),
    }
    pools["train"] = [r for r in pools["train"] if r["id"] not in (ids_test | ids_val)]
    pools["val"] = [r for r in pools["val"] if r["id"] not in ids_test]
    return pools, purged


def evaluate_family_models(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-family prior vs natural/balanced logistic, common temporal test."""
    pools, purged = prepare_splits(records)
    result: dict[str, Any] = {
        "split_rule": "train Jun-Sep; val Oct; test Nov-Dec; client-disjoint",
        "purge_counts": purged,
        "families": {},
    }
    for j, family in enumerate(PRODUCTS):
        eligible = {k: [r for r in pool if r["x"][7 + j]] for k, pool in pools.items()}
        y = {
            k: np.asarray([int(row["moves"][family]) for row in group], dtype=int)
            for k, group in eligible.items()
        }
        x = {
            k: np.asarray([row["x"] for row in group], dtype=object)
            for k, group in eligible.items()
        }
        if any(len(np.unique(y[k])) < 2 for k in SPLITS):
            raise ValueError(f"both classes required for {family}")
        preprocess = _pipeline(DummyClassifier(strategy="prior")).named_steps["features"]
        z_train = preprocess.fit_transform(x["train"], y["train"])
        z_val = preprocess.transform(x["val"])
        z_test = preprocess.transform(x["test"])
        models = {
            "prior": DummyClassifier(strategy="prior"),
            "logistic_natural": SGDClassifier(
                loss="log_loss", penalty="l2", alpha=0.0001,
                max_iter=70, tol=0.001, random_state=42,
            ),
            "logistic_balanced": SGDClassifier(
                loss="log_loss", penalty="l2", alpha=0.0001,
                max_iter=70, tol=0.001, class_weight="balanced", random_state=42,
            ),
        }
        comparisons = {}
        for name, estimator in models.items():
            estimator.fit(z_train, y["train"])
            comparisons[name] = {
                "val": scores(y["val"], estimator.predict_proba(z_val)[:, 1]),
                "test": scores(y["test"], estimator.predict_proba(z_test)[:, 1]),
            }
        result["families"][family] = {
            "split_n": {k: len(y[k]) for k in SPLITS},
            "prevalence": {k: float(y[k].mean()) for k in SPLITS},
            "model_comparisons": comparisons,
            "grouping": "products are overlapping labels; not mutually exclusive classes",
        }
    return result


def analyze_workbook(source: str | Path, output: str | Path) -> dict[str, Any]:
    """Read private source locally; persist aggregated measures only."""
    records = []
    for row in iter_worksheet_rows(source):
        rec = extract(row)
        if rec is not None:
            records.append({
                "id": rec["id"], "month": rec["month"],
                "x": rec["x"], "moves": rec["moves"],
            })
    result = {
        "metadata": {
            "source": "confidential case XLSX, 2025-06..2025-12",
            "grain": "retained funnel record, client IDs may repeat",
            "population": "RETIDO and family present in M0",
            "repeated_family_membership": True,
            "decision": "observational retrospective analysis; offer acceptance unobserved",
        },
        "exposures": family_exposure(records),
        "models": evaluate_family_models(records),
    }
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
