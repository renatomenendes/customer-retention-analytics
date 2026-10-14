# ruff: noqa: E501
"""Evidence-focused study of movement *among retained funnel records*.

Input is local and confidential. Returned outputs contain no client identifiers.
Offer acceptance is unobserved: contract-change proxies are NOT acceptance labels.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from retention_analytics.audit import PRODUCTS, _flag, _month, _number, _product_id
from retention_analytics.xlsx_stream import iter_worksheet_rows

CAT = ("origin", "uf", "mplay_m0", "classification", "mobile_flag", "family_mix_m0")
NUM = ("family_count_m0", "has_bl", "has_tv", "has_fone", "has_mv", "value_bl", "value_tv", "value_mv")
FEATURES = CAT + NUM
SMALL_GROUP = 500


def extract(row: Mapping[str, str | None]) -> dict[str, Any] | None:
    month = _month(row.get("DATA_FUNIL_SOLAR"))
    if month is None or not "2025-06" <= month <= "2025-12":
        return None
    if (row.get("NM_SUB_INDICADOR_NEGOCIO") or "").strip() != "RETIDO":
        return None
    existing = {f: _product_id(row, f, "M0") for f in PRODUCTS}
    ending = {f: _product_id(row, f, "M30") for f in PRODUCTS}
    has = {f: int(existing[f] is not None) for f in PRODUCTS}
    moved = {f: _flag(row.get(f"FLAG_MOV_{f}")) for f in PRODUCTS}
    cancelled = {f: _flag(row.get(f"FLAG_CANC_{f}")) for f in PRODUCTS}
    feature = (
        (row.get("FLAG_ORIGEM") or "UNKNOWN").strip() or "UNKNOWN",
        (row.get("SGL_UF") or "UNKNOWN").strip() or "UNKNOWN",
        (row.get("DSC_CLI_MPLAY_M0") or "UNKNOWN").strip() or "UNKNOWN",
        (row.get("CLASSIFICACAO") or "UNKNOWN").strip() or "UNKNOWN",
        (row.get("flag_movel") or "UNKNOWN").strip() or "UNKNOWN",
        "+".join(f for f in PRODUCTS if has[f]) or "NONE",
        sum(has.values()), has["BL"], has["TV"], has["FONE"], has["MV"],
        _number(row.get("VALOR_BL_M0")), _number(row.get("VALOR_TV_M0")),
        _number(row.get("VALOR_MV_M0")),
    )
    # A strict *contract-change-compatible* flag is observable; offer acceptance is not.
    contract_change = {
        f: bool(moved[f] and not cancelled[f] and ending[f] is not None
                and ending[f] != existing[f])
        for f in PRODUCTS
    }
    values = {
        f: (
            _number(row.get(f"VALOR_{f}_M0")),
            _number(row.get(f"VALOR_{f}_M30")),
        ) for f in PRODUCTS
    }
    transitions = {
        f: (
            "addition" if existing[f] is None and ending[f] is not None
            else "removal" if existing[f] is not None and ending[f] is None
            else "replacement" if existing[f] is not None and ending[f] is not None and existing[f] != ending[f]
            else "unchanged" if existing[f] is not None and ending[f] is not None
            else "absent"
        ) for f in PRODUCTS
    }
    return {
        "id": str(row.get("id_cliente") or ""),
        "month": month,
        "date": str(row.get("DATA_FUNIL_SOLAR") or ""),
        "x": feature,
        "y": int(any(moved.values())),
        "strict_proxy": int(any(contract_change.values())),
        "has_cancel": int(any(cancelled.values())),
        "moves": moved,
        "cancel": cancelled,
        "values": values,
        "transitions": transitions,
    }


def _evalu(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    if len(np.unique(y)) != 2:
        raise ValueError("Both classes required")
    top = max(1, int(np.ceil(0.1 * len(y))))
    rank = np.argsort(-p, kind="stable")[:top]
    prior = float(y.mean())
    precision = prior if np.all(p == p[0]) else float(y[rank].mean())
    return {
        "n": len(y), "prevalence": prior,
        "roc_auc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "precision_top_decile": precision,
        "lift_top_decile": precision / prior,
    }


def _pipeline(est: Any, hist: bool = False) -> Pipeline:
    if hist:
        transform = ColumnTransformer([
            ("categorical", Pipeline([
                ("imp", SimpleImputer(strategy="constant", fill_value="UNKNOWN")),
                ("ord", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
            ]), list(range(len(CAT)))),
            ("numeric", SimpleImputer(strategy="median"), list(range(len(CAT), len(FEATURES)))),
        ], sparse_threshold=0)
    else:
        transform = ColumnTransformer([
            ("categorical", Pipeline([
                ("imp", SimpleImputer(strategy="constant", fill_value="UNKNOWN")),
                ("ohe", OneHotEncoder(handle_unknown="ignore", min_frequency=80)),
            ]), list(range(len(CAT)))),
            ("numeric", Pipeline([
                ("imp", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
            ]), list(range(len(CAT), len(FEATURES)))),
        ], sparse_threshold=0.3)
    return Pipeline([("features", transform), ("estimator", est)])


def _calibration(y: np.ndarray, p: np.ndarray, bins: int = 10) -> dict[str, Any]:
    # Fixed-width bands disclose actual group sizes; suppress small bands in public output.
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, bins - 1)
    rows, absolute = [], 0.0
    for b in range(bins):
        ind = idx == b
        if int(ind.sum()) < 100:
            continue
        observed = float(y[ind].mean())
        predicted = float(p[ind].mean())
        rows.append({"range": f"{edges[b]:.1f}-{edges[b+1]:.1f}", "n": int(ind.sum()),
                     "predicted": predicted, "observed": observed})
        absolute += float(ind.sum()) / len(y) * abs(predicted - observed)
    return {"bins_at_least_100": rows, "partial_ece": absolute,
            "limitation": "ECE covers published bins only; unreleased bins excluded"}


def _summary_group(recs: list[dict[str, Any]], which: int) -> list[dict[str, Any]]:
    agg = defaultdict(Counter)
    for r in recs:
        key = str(r["x"][which])
        agg[key]["n"] += 1
        agg[key]["movement"] += r["y"]
        agg[key]["strict"] += r["strict_proxy"]
    ans = []
    for k, c in agg.items():
        if c["n"] >= SMALL_GROUP:
            ans.append({"group": k, "n": c["n"], "movement": c["movement"],
                        "movement_rate": c["movement"] / c["n"],
                        "strict_proxy_rate": c["strict"] / c["n"]})
    return sorted(ans, key=lambda x: (-x["n"], x["group"]))


def analyze_retained(records: Iterable[Mapping[str, str | None]], fit_models: bool = True) -> dict[str, Any]:
    retained = [r for row in records if (r := extract(row)) is not None]
    if not retained:
        raise ValueError("No eligible retained records")
    outcome = Counter()
    breakdown = {f: defaultdict(Counter) for f in PRODUCTS}
    bymonth = defaultdict(Counter)
    byorigin = defaultdict(Counter)
    group = defaultdict(Counter)
    for r in retained:
        outcome["total"] += 1
        outcome["moved"] += r["y"]
        outcome["strict_contract_change_compatible"] += r["strict_proxy"]
        outcome["any_product_cancellation"] += r["has_cancel"]
        outcome["moved_with_any_cancellation"] += r["y"] and r["has_cancel"]
        for name,key in (("month",r["month"]),("origin",r["x"][0]),
                         ("family_count_origin",f"{r['x'][6]}|{r['x'][0]}")):
            col = bymonth if name == "month" else byorigin if name == "origin" else group
            col[key]["n"] += 1
            col[key]["moved"] += r["y"]
        for fam in PRODUCTS:
            tab = breakdown[fam]
            m, e = r["values"][fam]
            state = r["transitions"][fam]
            c = tab[state]
            c["n"] += 1
            c["flag_movement"] += r["moves"][fam]
            c["flag_cancellation"] += r["cancel"][fam]
            if m is not None and e is not None:
                c["priced"] += 1
                c["delta_sum_cents"] += int(round((e-m)*100))
                c["negative_delta"] += e < m-1e-9
                c["positive_delta"] += e > m+1e-9
    n = outcome["total"]
    ans: dict[str, Any] = {
        "study": "2025 retention funnel: movement conditioned on RETIDO",
        "grain": "worksheet record; client ID not unique episode",
        "definitions": {
            "retained": "literal status RETIDO",
            "movement": "one or more FLAG_MOV_* = 1",
            "offer_acceptance": "NOT_OBSERVED; neither proxy proves acceptance",
            "strict_proxy": "a FLAG_MOV with noncancelled changed/added product at M30",
            "period": "2025-06..2025-12 inclusive",
        },
        "totals": dict(outcome),
        "rates": {"movement_given_retained": outcome["moved"]/n,
                  "strict_contract_change_proxy_given_retained": outcome["strict_contract_change_compatible"]/n,
                  "movement_with_cancellation_given_movement": outcome["moved_with_any_cancellation"]/outcome["moved"]},
        "segments": {name:_summary_group(retained,i) for name,i in [
            ("origin",0),("uf",1),("mplay_m0",2),("classification",3),
            ("mobile_flag",4),("family_mix_m0",5),("family_count_m0",6)]},
        "month": {k:{"n":v["n"],"movement_rate":v["moved"]/v["n"]}
                  for k,v in sorted(bymonth.items())},
        "origin": {k:{"n":v["n"],"movement_rate":v["moved"]/v["n"]}
                   for k,v in sorted(byorigin.items())},
        "family_count_by_origin": {k:{"n":v["n"],"movement_rate":v["moved"]/v["n"]}
                                  for k,v in sorted(group.items()) if v["n"]>=SMALL_GROUP},
        "product_transitions": {f:{k:{**dict(v),"mean_delta_when_priced":v["delta_sum_cents"]/100/v["priced"] if v["priced"] else None}
                               for k,v in kinds.items() if v["n"]>=SMALL_GROUP}
                               for f,kinds in breakdown.items()},
        "limitations": [
            "Offer acceptance is latent: its probability is not identifiable from movement flags alone.",
            "Contract-change proxy is not a bound on the true acceptance rate.",
            "All findings are conditioned on observed RETIDO outcomes, so not deployable ex-ante as customer scores.",
            "Regression coefficients and feature associations are observational, not causal.",
            "Monetary deltas are from recorded M0/M30 values without accounting reconciliation.",
            "Same client can have multiple records; repeated episodes need sensitivity and client-cluster uncertainty.",
        ],
    }
    # Sensitivity: select chronologically first observed *retained* record per client.
    first = {}
    for r in retained:
        rid = r["id"]
        if rid and (rid not in first or (r["month"],r["date"]) < (first[rid]["month"],first[rid]["date"])):
            first[rid] = r
    ans["first_retained_record_per_client_sensitivity"] = {
        "n": len(first), "movement_rate":sum(r["y"] for r in first.values())/len(first),
        "note": "first retained record only, not first event or unique lead; excludes missing IDs",
    }
    if not fit_models:
        return ans
    split_names = ("train","validation","test")
    buckets = {k:[] for k in split_names}
    for r in retained:
        split = "train" if r["month"]<="2025-09" else "validation" if r["month"]=="2025-10" else "test"
        buckets[split].append(r)
    later = {r["id"] for k in ("validation","test") for r in buckets[k] if r["id"]}
    testid = {r["id"] for r in buckets["test"] if r["id"]}
    excluded_train = sum(r["id"] in later for r in buckets["train"])
    excluded_validation = sum(r["id"] in testid for r in buckets["validation"])
    buckets["train"] = [r for r in buckets["train"] if r["id"] and r["id"] not in later]
    buckets["validation"] = [r for r in buckets["validation"] if r["id"] and r["id"] not in testid]
    buckets["test"] = [r for r in buckets["test"] if r["id"]]
    x = {k:np.asarray([r["x"] for r in buckets[k]],dtype=object) for k in split_names}
    y = {k:np.asarray([r["y"] for r in buckets[k]],dtype=int) for k in split_names}
    models = {
        "prior":DummyClassifier(strategy="prior"),
        "logistic":_pipeline(LogisticRegression(max_iter=120,C=.2,solver="liblinear",tol=.001,random_state=42)),
        "small_tree":_pipeline(DecisionTreeClassifier(max_depth=5,min_samples_leaf=450,random_state=42)),
        "hist_boosting":_pipeline(HistGradientBoostingClassifier(max_iter=55,learning_rate=.07,max_leaf_nodes=15,min_samples_leaf=180,l2_regularization=8,random_state=42),hist=True),
    }
    results = {}
    test_probs={}
    for name,estimator in models.items():
        estimator.fit(x["train"],y["train"])
        pv=estimator.predict_proba(x["validation"])[:,1]
        pt=estimator.predict_proba(x["test"])[:,1]
        test_probs[name]=pt
        results[name]={"validation":_evalu(y["validation"],pv),
                       "test":_evalu(y["test"],pt),
                       "test_calibration":_calibration(y["test"],pt)}
    best=min((k for k in models if k!="prior"),key=lambda k:results[k]["validation"]["brier"])
    selected_scores=test_probs[best]
    by_month={}
    for period in ("2025-11","2025-12"):
        idx=np.fromiter((r["month"]==period for r in buckets["test"]),dtype=bool,count=len(buckets["test"]))
        if idx.sum()>500:
            by_month[period]=_evalu(y["test"][idx], selected_scores[idx])
    by_origin={}
    for origin in ("LEGADO","SOLAR"):
        idx=np.fromiter((r["x"][0]==origin for r in buckets["test"]),dtype=bool,count=len(buckets["test"]))
        if idx.sum()>500 and len(np.unique(y["test"][idx]))==2:
            by_origin[origin]=_evalu(y["test"][idx],selected_scores[idx])
    # Train versus test populations, by feature. No customer ID is persisted.
    ans["model"]={
        "target":"FLAG_MOV among records classified RETIDO (ex-post conditional characterization)",
        "audience":"profile explanation only; cannot score an unknown future RETIDO subset before closure",
        "features":list(FEATURES),
        "split_rule":{"train":"Jun-Sep","validation":"Oct","test":"Nov-Dec",
                      "client_disjoint_across_splits":True,
                      "train_excluded_for_overlap":excluded_train,
                      "validation_excluded_for_overlap":excluded_validation},
        "split_n":{k:len(v) for k,v in buckets.items()},
        "split_prevalence":{k:float(y[k].mean()) for k in split_names},
        "comparisons":results,
        "best_nontrivial_by_validation_brier":best,
        "chosen_test_by_month":by_month,
        "chosen_test_by_origin":by_origin,
        "interpretation":"benchmark uses the same test set for every model; predictive association != offer acceptance or uplift",
    }
    return ans


def analyze_workbook(source: str | Path, output: str | Path, fit_models: bool=True) -> dict[str, Any]:
    study=analyze_retained(iter_worksheet_rows(source),fit_models=fit_models)
    dest=Path(output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(study,ensure_ascii=False,indent=2),encoding="utf-8")
    return study
