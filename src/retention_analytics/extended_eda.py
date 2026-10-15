# ruff: noqa: E501
"""Decision-centred exploration of the retention case.

Read-only processing of an authorized local workbook. No customer identifiers or
individual observations are persisted. This is descriptive observational work.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np

from retention_analytics.audit import PRODUCTS, _flag, _month, _mplay, _number, _product_id
from retention_analytics.xlsx_stream import iter_worksheet_rows

STATUS = ("RETIDO", "NAO RETIDO", "LEAD EM ABERTO")
ORIGINS = ("LEGADO", "SOLAR")


def retention_bounds(retained: int, not_retained: int, opened: int) -> dict[str, float | int | None]:
    """Sharp worst-case bounds when open cases have unknown binary outcome."""
    total = retained + not_retained + opened
    closed = retained + not_retained
    return {"n": total, "opened": opened,
            "lower_if_all_open_not_retained": retained / total if total else None,
            "upper_if_all_open_retained": (retained + opened) / total if total else None,
            "observed_among_closed": retained / closed if closed else None}


def _rate(rows: Mapping[str, int], a: str, b: str) -> float | None:
    return rows.get(a, 0) / rows.get(b, 0) if rows.get(b, 0) else None


def _summary(c: Counter) -> dict[str, Any]:
    return {**dict(c), "movement_rate": _rate(c, "movement", "retained")}


def adjusted_channel_gap(
    month_index: np.ndarray, family_count: np.ndarray, origin: np.ndarray,
    movement: np.ndarray, client_ids: list[str], draws: int = 200, seed: int = 2025,
) -> dict[str, Any]:
    """Direct standardization over month × M0 family count; client-cluster Poisson bootstrap.

    Common-support cells require at least 30 observations from each origin.
    Poisson bootstrap weights one per customer preserve correlations across
    repeated observed records. Intervals measure sampling uncertainty only;
    they do not correct channel selection or post-outcome conditioning.
    """
    n = len(movement)
    if not (len(month_index) == len(family_count) == len(origin) == len(client_ids) == n):
        raise ValueError("All inputs must have matching lengths")
    if n == 0:
        raise ValueError("Empty retained population")
    if any(not c for c in client_ids):
        raise ValueError("Cluster IDs missing; cannot claim clustered uncertainty")
    code = ((month_index.astype(np.int32) * 5 + family_count.astype(np.int32)) * 2
            + origin.astype(np.int32))
    if code.max() >= 70 or code.min() < 0:
        raise ValueError("Unexpected stratum or origin code")
    totals = np.bincount(code, minlength=70).reshape(35, 2)
    successes = np.bincount(code, weights=movement, minlength=70).reshape(35, 2)
    common = (totals[:, 0] >= 30) & (totals[:, 1] >= 30)
    if not common.any():
        return {"identified": False, "reason": "Insufficient common support"}
    population = totals.sum(axis=1)
    w = population[common] / population[common].sum()
    def contrast(nmat: np.ndarray, smat: np.ndarray) -> float:
        denominators = nmat[common]
        if (denominators <= 0).any():
            return float("nan")
        rates = smat[common] / denominators
        return float(np.dot(w, rates[:, 1] - rates[:, 0]))
    main = contrast(totals, successes)
    raw_count = totals.sum(axis=0)
    raw_success = successes.sum(axis=0)
    raw = float(raw_success[1] / raw_count[1] - raw_success[0] / raw_count[0])
    unique, inv = np.unique(client_ids, return_inverse=True)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(draws):
        weights = rng.poisson(1.0, size=len(unique))[inv]
        nn = np.bincount(code, weights=weights, minlength=70).reshape(35, 2)
        yy = np.bincount(code, weights=weights * movement, minlength=70).reshape(35, 2)
        delta = contrast(nn, yy)
        if np.isfinite(delta):
            estimates.append(delta)
    lo, hi = np.quantile(estimates, [0.025, 0.975]) if estimates else (float("nan"), float("nan"))
    return {
        "identified": True,
        "raw_solar_minus_legado": raw,
        "standardized_solar_minus_legado": main,
        "common_support_retained_records": int(population[common].sum()),
        "all_retained_records": n,
        "common_support_coverage": float(population[common].sum() / n),
        "strata_available": int(common.sum()),
        "strata_total": 35,
        "ci_95_cluster_poisson": [float(lo), float(hi)],
        "bootstrap_draws": len(estimates),
        "unique_clients_clustered": int(len(unique)),
        "noncausal_warning": "Channel assignment and retention status are not randomized; CI does not remove confounding.",
    }


def analyze_records(
    rows: Iterable[Mapping[str, str | None]], bootstrap_draws: int = 200,
) -> dict[str, Any]:
    overall = Counter()
    cohort = defaultdict(Counter)
    origin_cohort = defaultdict(Counter)
    profile = defaultdict(Counter)
    moved_families = Counter()
    transitions = defaultdict(Counter)
    money = defaultdict(Counter)
    products = defaultdict(Counter)
    revenue_deltas = defaultdict(list)
    client_ids: list[str] = []
    months: list[int] = []
    family_counts: list[int] = []
    origins: list[int] = []
    movements: list[int] = []
    for row in rows:
        m = _month(row.get("DATA_FUNIL_SOLAR"))
        if m is None or not "2025-06" <= m <= "2025-12":
            overall["excluded_outside_or_invalid_date"] += 1
            continue
        state = (row.get("NM_SUB_INDICADOR_NEGOCIO") or "UNKNOWN").strip()
        orig = (row.get("FLAG_ORIGEM") or "UNKNOWN").strip()
        overall["scope"] += 1
        cohort[m]["records"] += 1
        origin_cohort[(m, orig)]["records"] += 1
        cohort[m][state] += 1
        origin_cohort[(m, orig)][state] += 1
        overall[f"status_{state}"] += 1
        if state != "RETIDO":
            continue
        mix = tuple(f for f in PRODUCTS if _product_id(row, f, "M0") is not None)
        k = len(mix)
        moved = tuple(f for f in PRODUCTS if _flag(row.get(f"FLAG_MOV_{f}")))
        cancels = tuple(f for f in PRODUCTS if _flag(row.get(f"FLAG_CANC_{f}")))
        y = int(bool(moved))
        overall["retained"] += 1
        overall["retained_movement"] += y
        overall["retained_cancellation"] += bool(cancels)
        overall["retained_movement_and_cancellation"] += bool(cancels) and y
        moved_families["+".join(moved) or "NONE"] += 1
        for f in moved:
            products[f]["movement_flag"] += 1
            products[f]["movement_flag_with_initial_presence"] += f in mix
            products[f]["movement_flag_without_initial_presence"] += f not in mix
        for f in cancels:
            products[f]["cancellation_flag"] += 1
        for f in mix:
            products[f]["present_m0"] += 1
        for dim, label in (
            ("month", m), ("origin", orig), ("mix", "+".join(mix) or "NONE"),
            ("family_count", str(k)),
            ("mplay", _mplay(row.get("DSC_CLI_MPLAY_M0"))),
            ("mobile_flag", (row.get("flag_movel") or "UNKNOWN").strip() or "UNKNOWN"),
            ("uf", (row.get("SGL_UF") or "UNKNOWN").strip() or "UNKNOWN"),
            ("origin_family_count", f"{orig}|{k}"),
            ("origin_month", f"{orig}|{m}"),
        ):
            c = profile[(dim, label)]
            c["n"] += 1
            c["movement"] += y
        values_m0, values_m30 = [], []
        for f in PRODUCTS:
            before = _product_id(row, f, "M0")
            after = _product_id(row, f, "M30")
            transition = ("addition" if before is None and after is not None
                          else "removal" if before is not None and after is None
                          else "replacement" if before is not None and after is not None and before != after
                          else "unchanged" if before is not None and after is not None else "absent")
            cc = transitions[(f, transition)]
            cc["n"] += 1
            cc["move_flag"] += f in moved
            cc["cancel_flag"] += f in cancels
            a, b = _number(row.get(f"VALOR_{f}_M0")), _number(row.get(f"VALOR_{f}_M30"))
            if a is not None and b is not None:
                d = b - a
                cc["priced"] += 1
                cc["negative"] += d < -1e-8
                cc["positive"] += d > 1e-8
                cc["unchanged_value"] += abs(d) <= 1e-8
                cc["delta_cents"] += round(d * 100)
                values_m0.append(a)
                values_m30.append(b)
            else:
                overall["missing_product_value_pair"] += 1
        if len(values_m0) == 4:
            diff = sum(values_m30) - sum(values_m0)
            cat = ("moving_with_cancel" if y and cancels else
                   "moving_without_cancel" if y else
                   "no_movement_with_cancel" if cancels else "no_movement_no_cancel")
            for label in ("all_retained", cat, f"origin:{orig}", f"month:{m}"):
                cell = money[label]
                cell["n"] += 1
                cell["sum_m0_cents"] += round(sum(values_m0) * 100)
                cell["sum_m30_cents"] += round(sum(values_m30) * 100)
                cell["neg"] += diff < -1e-8
                cell["pos"] += diff > 1e-8
                cell["zero"] += abs(diff) <= 1e-8
                revenue_deltas[label].append(diff)
        ident = str(row.get("id_cliente") or "").strip()
        if orig in ORIGINS and ident and 0 <= k <= 4:
            client_ids.append(ident)
            months.append(int(m[-2:]) - 6)
            family_counts.append(k)
            origins.append(ORIGINS.index(orig))
            movements.append(y)
    reported_profiles = {}
    for (dimension, label), c in profile.items():
        if c["n"] < 500:
            continue
        reported_profiles.setdefault(dimension, []).append({"group": label, "n": c["n"],
                                                              "movement": c["movement"],
                                                              "rate": c["movement"] / c["n"]})
    for rows in reported_profiles.values():
        rows.sort(key=lambda e: (-e["n"], e["group"]))
    economic = {}
    for label, c in money.items():
        if c["n"] < 500:
            continue
        vals = np.asarray(revenue_deltas[label], dtype=float)
        economic[label] = {"n": c["n"], "negative": c["neg"] / c["n"],
                           "positive": c["pos"] / c["n"], "zero": c["zero"] / c["n"],
                           "median_delta": float(np.median(vals)),
                           "p10_delta": float(np.quantile(vals, .10)),
                           "p90_delta": float(np.quantile(vals, .90)),
                           "mean_delta": float(vals.mean()),
                           "relative_sum_delta": c["sum_m30_cents"] / c["sum_m0_cents"] - 1
                           if c["sum_m0_cents"] else None}
    transition_report={}
    for (f,s),c in transitions.items():
        if c["n"] < 500:
            continue
        transition_report.setdefault(f,{})[s] = {
            "n": c["n"], "move_flag": c["move_flag"], "cancel_flag": c["cancel_flag"],
            "priced": c["priced"], "negative_share_priced": c["negative"] / c["priced"] if c["priced"] else None,
            "average_delta_priced": c["delta_cents"] / 100 / c["priced"] if c["priced"] else None}
    cohorts = []
    for (m,orig),c in sorted(origin_cohort.items()):
        if c["records"] < 100:
            continue
        cohorts.append({"month":m,"origin":orig,
                        **retention_bounds(c["RETIDO"],c["NAO RETIDO"],c["LEAD EM ABERTO"]),
                        "retained":c["RETIDO"],"not_retained":c["NAO RETIDO"]})
    nrows = len(movements)
    channel = adjusted_channel_gap(np.asarray(months,dtype=np.int8),
                                   np.asarray(family_counts,dtype=np.int8),
                                   np.asarray(origins,dtype=np.int8),
                                   np.asarray(movements,dtype=np.int8),
                                   client_ids,draws=bootstrap_draws) if nrows else {"identified":False}
    return {
        "metadata":{"window":"2025-06..2025-12","grain":"spreadsheet row, repeated customer IDs",
                    "offer_acceptance":"unobserved","monetary_unit":"unconfirmed",
                    "causal_inference":"not identified", "min_published_group":500},
        "counts":dict(overall),
        "retention_bounds_by_month_origin":cohorts,
        "profiles":reported_profiles,
        "movement_combinations_retained": {
            **{key: count for key, count in moved_families.most_common() if count >= 500},
            "OTHER_SMALL_COMBINATIONS": sum(
                count for count in moved_families.values() if count < 500
            ),
        },
        "product_presence_and_flags":{f:dict(products[f]) for f in PRODUCTS},
        "product_transition_economics_retained":transition_report,
        "retained_value_distributions":economic,
        "channel_comparison_standardized":channel,
        "interpretation_notes":[
            "Status and offer acceptance are different constructs.",
            "Post-retention conditional associations do not identify effects of sales channels.",
            "Unknown event times and censoring prevent Kaplan-Meier or Cox survival estimation.",
            "Open-case bounds are binary-outcome sensitivity scenarios, not survival estimates.",
            "Values at M0 and M30 are not reconciled to billed revenue, cost or margin.",
            "Product transition counts and flag semantics must be validated by business owners.",
            "Bootstrap describes repeated-record sampling variation, not representativeness or hidden confounding."
        ]}


def analyze_workbook(source: str | Path, output: str | Path, bootstrap_draws:int=200)->dict[str,Any]:
    result=analyze_records(iter_worksheet_rows(source),bootstrap_draws=bootstrap_draws)
    target=Path(output)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result
