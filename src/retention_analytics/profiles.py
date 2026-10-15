"""Privacy-preserving profile and economic analysis of the retention sample.

No individual rows or client identifiers are written by this module.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Mapping

from retention_analytics.audit import (
    PRODUCTS,
    _flag,
    _month,
    _mplay,
    _number,
    _product_id,
)
from retention_analytics.xlsx_stream import iter_worksheet_rows

DATE_RANGE = ("2025-06", "2025-12")
PROFILE_DIMENSIONS = (
    "family_count_m0",
    "origin",
    "uf",
    "regional_group",
    "classification",
    "mplay_m0",
    "mobile_flag",
)


def record_profile(row: Mapping[str, str | None]) -> dict[str, Any] | None:
    """Derive an episode-level analysis record without retaining its raw fields."""
    month = _month(row.get("DATA_FUNIL_SOLAR"))
    if month is None or not DATE_RANGE[0] <= month <= DATE_RANGE[1]:
        return None
    state = (row.get("NM_SUB_INDICADOR_NEGOCIO") or "UNKNOWN").strip()
    moving = any(_flag(row.get(f"FLAG_MOV_{p}")) for p in PRODUCTS)
    canceled = any(_flag(row.get(f"FLAG_CANC_{p}")) for p in PRODUCTS)
    initial_families = tuple(
        p for p in PRODUCTS if _product_id(row, p, "M0") is not None
    )
    amounts = {}
    for period in ("M0", "M30"):
        values = [_number(row.get(f"VALOR_{p}_{period}")) for p in PRODUCTS]
        amounts[period] = sum(values) if all(v is not None for v in values) else None
    return {
        "month": month,
        "client_id": str(row.get("id_cliente") or ""),
        "state": state,
        "movement": moving,
        "cancellation": canceled,
        "retained_movement": state == "RETIDO" and moving,
        "origin": (row.get("FLAG_ORIGEM") or "UNKNOWN").strip(),
        "uf": (row.get("SGL_UF") or "UNKNOWN").strip(),
        "regional_group": (row.get("NM_GRUPO_REGIONAL") or "UNKNOWN").strip(),
        "classification": (row.get("CLASSIFICACAO") or "UNKNOWN").strip(),
        "mplay_m0": _mplay(row.get("DSC_CLI_MPLAY_M0")),
        "mobile_flag": (row.get("flag_movel") or "UNKNOWN").strip(),
        "family_count_m0": str(len(initial_families)),
        "family_mix_m0": "+".join(initial_families) or "NONE",
        "value_m0": amounts["M0"],
        "value_m30": amounts["M30"],
        "product_moves": {p: _flag(row.get(f"FLAG_MOV_{p}")) for p in PRODUCTS},
        "product_cancels": {p: _flag(row.get(f"FLAG_CANC_{p}")) for p in PRODUCTS},
        "features": {
            "origin": (row.get("FLAG_ORIGEM") or "UNKNOWN").strip(),
            "uf": (row.get("SGL_UF") or "UNKNOWN").strip(),
            "family_count_m0": len(initial_families),
            "mplay_m0": _mplay(row.get("DSC_CLI_MPLAY_M0")),
            "classification": (row.get("CLASSIFICACAO") or "UNKNOWN").strip(),
            "mobile_flag": (row.get("flag_movel") or "UNKNOWN").strip(),
            "has_bl_m0": int("BL" in initial_families),
            "has_tv_m0": int("TV" in initial_families),
            "has_fone_m0": int("FONE" in initial_families),
            "has_mv_m0": int("MV" in initial_families),
            "value_bl_m0": _number(row.get("VALOR_BL_M0")),
            "value_tv_m0": _number(row.get("VALOR_TV_M0")),
            "value_mv_m0": _number(row.get("VALOR_MV_M0")),
        },
    }


def wilson_interval(
    count: int, n: int, z: float = 1.95996398454
) -> tuple[float | None, float | None]:
    """Binomial Wilson interval; descriptive, not adjusted for repeated customers."""
    if n <= 0:
        return None, None
    p = count / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return center - radius, center + radius


def summarize_profiles(
    records: Iterable[dict[str, Any]], min_group_n: int = 100
) -> dict[str, Any]:
    """Summarize sample groups and value differences without exposing raw records."""
    if min_group_n < 30:
        raise ValueError("Minimum group size must be at least 30")
    counts = Counter()
    segments: dict[tuple[str, str], Counter] = defaultdict(Counter)
    values: dict[str, list[float]] = defaultdict(list)
    value_counts: dict[str, Counter] = defaultdict(Counter)
    movements: dict[str, Counter] = defaultdict(Counter)
    for rec in records:
        counts["eligible"] += 1
        state = rec["state"]
        retained = state == "RETIDO"
        moving = bool(rec["movement"])
        if retained:
            counts["retained"] += 1
        elif state == "NAO RETIDO":
            counts["not_retained"] += 1
        elif state == "LEAD EM ABERTO":
            counts["open"] += 1
        if retained and moving:
            counts["retained_movement"] += 1
        if moving:
            counts["all_movement"] += 1
        for family in PRODUCTS:
            if rec["product_moves"][family]:
                movements[family]["moved"] += 1
                if retained:
                    movements[family]["retained_moved"] += 1
            if rec["product_cancels"][family]:
                movements[family]["cancelled"] += 1
        for dim in PROFILE_DIMENSIONS + ("family_mix_m0", "month"):
            value = str(rec[dim])
            c = segments[(dim, value)]
            c["n"] += 1
            c["retained"] += retained
            c["closed"] += state in ("RETIDO", "NAO RETIDO")
            c["target"] += retained and moving
            c["retained_and_moved"] += retained and moving
            c["retained_and_not_moved"] += retained and not moving
        a, b = rec["value_m0"], rec["value_m30"]
        if a is None or b is None:
            counts["missing_value_comparison"] += 1
            continue
        change = b - a
        cohort = (
            "retained_movement" if retained and moving
            else "retained_no_movement" if retained
            else "not_retained" if state == "NAO RETIDO"
            else "open"
        )
        for category in ("all", cohort):
            values[category].append(change)
            value_counts[category]["n"] += 1
            value_counts[category]["sum_m0_cents"] += round(a * 100)
            value_counts[category]["sum_m30_cents"] += round(b * 100)
            value_counts[category]["positive"] += change > 1e-8
            value_counts[category]["negative"] += change < -1e-8
            value_counts[category]["zero"] += abs(change) <= 1e-8
    result_groups = []
    for (dim, category), c in sorted(segments.items()):
        if c["n"] < min_group_n:
            continue
        n_ret = c["retained"]
        n_closed = c["closed"]
        lo, hi = wilson_interval(c["retained_and_moved"], n_ret)
        result_groups.append({
            "dimension": dim,
            "category": category,
            "n": c["n"],
            "n_closed": n_closed,
            "n_retained": n_ret,
            "n_retained_movement": c["retained_and_moved"],
            "retention_among_closed": (n_ret / n_closed if n_closed else None),
            "movement_among_retained": (
                c["retained_and_moved"] / n_ret if n_ret else None
            ),
            "movement_wilson_interval_naive": [lo, hi],
            "composite_event_among_closed": (
                c["retained_and_moved"] / n_closed if n_closed else None
            ),
        })
    economics = {}
    for key, data in values.items():
        sorted_changes = sorted(data)
        n = len(sorted_changes)
        c = value_counts[key]
        economics[key] = {
            "n": n,
            "mean_change": sum(sorted_changes) / n,
            "median_change": median(sorted_changes),
            "p10_change": sorted_changes[int(0.10 * (n - 1))],
            "p90_change": sorted_changes[int(0.90 * (n - 1))],
            "share_positive": c["positive"] / n,
            "share_negative": c["negative"] / n,
            "share_zero": c["zero"] / n,
            "sum_m0": c["sum_m0_cents"] / 100,
            "sum_m30": c["sum_m30_cents"] / 100,
            "relative_sum_change": (
                (c["sum_m30_cents"] / c["sum_m0_cents"] - 1)
                if c["sum_m0_cents"] else None
            ),
        }
    return {
        "definitions": "PROVISIONAL; observational sample at spreadsheet-row grain",
        "minimum_group_n": min_group_n,
        "overall": dict(counts),
        "segments": result_groups,
        "movements_by_family": {k: dict(v) for k, v in movements.items()},
        "value_snapshot_comparison": economics,
        "limitations": [
            "Row-level episodes are not officially identified and may repeat clients.",
            "Wilson intervals assume independent records and are "
            "optimistic under repeated IDs.",
            "M0/M30 value is not a validated measure of realized revenue.",
            "Status RETIDO represents a funnel outcome, not long-run survival.",
            "Observed associations do not establish causal effects of offers.",
        ],
    }


def analyze_workbook(path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Stream a local case workbook and write only aggregate private results."""
    result = summarize_profiles(
        rec for row in iter_worksheet_rows(path)
        if (rec := record_profile(row)) is not None
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result
