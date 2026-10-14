"""Portfolio opportunity and outcome diagnostics on confidential local records.

All output is aggregated and provisional. This is not causal inference or
an official operational retention KPI.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from retention_analytics.audit import PRODUCTS
from retention_analytics.profiles import record_profile
from retention_analytics.xlsx_stream import iter_worksheet_rows


def analyze_opportunity(
    records: Iterable[dict[str, Any]], min_records: int = 100
) -> dict[str, Any]:
    """Analyze whether larger portfolios mechanically offer more move opportunities.

    Flags signal product changes, not confirmed offer acceptances. Product-level
    eligible denominators count families present at M0. A flag on a family not
    present at M0 is tracked separately and never silently excluded.
    """
    if min_records < 30:
        raise ValueError("min_records must be at least 30")
    strata = defaultdict(Counter)
    within_family = defaultdict(Counter)
    mixtures = defaultdict(Counter)
    outcomes = defaultdict(Counter)
    totals = Counter()
    for rec in records:
        state = rec["state"]
        if state not in ("RETIDO", "NAO RETIDO", "LEAD EM ABERTO"):
            totals["unknown_status"] += 1
            continue
        totals["rows"] += 1
        is_retained = state == "RETIDO"
        is_closed = state in ("RETIDO", "NAO RETIDO")
        moved = bool(rec["movement"])
        families = tuple(
            f for f in PRODUCTS if rec["features"][f"has_{f.lower()}_m0"]
        )
        k = len(families)
        count_move = sum(bool(rec["product_moves"][f]) for f in PRODUCTS)
        keys = [("family_count", str(k)), ("month", rec["month"])]
        keys.append(("origin", rec["origin"]))
        keys.append(("family_count_origin", f"{k}|{rec['origin']}"))
        for dimension, category in keys:
            row = strata[(dimension, category)]
            row["rows"] += 1
            row["closed"] += is_closed
            row["retained"] += is_retained
            row["retained_movement"] += is_retained and moved
            row["not_retained"] += state == "NAO RETIDO"
            row["open"] += state == "LEAD EM ABERTO"
            if is_retained:
                row["moved_family_flags"] += count_move
                row["m0_family_opportunities"] += k
                row["move_flags_absent_from_m0"] += sum(
                    rec["product_moves"][f] for f in PRODUCTS if f not in families
                )
        if is_retained:
            mixtures["+".join(families) or "NONE"]["n"] += 1
            mixtures["+".join(families) or "NONE"]["moved"] += moved
            for family in PRODUCTS:
                cell = within_family[family]
                if family in families:
                    cell["m0_present"] += 1
                    cell["moved_when_present"] += rec["product_moves"][family]
                else:
                    cell["m0_absent"] += 1
                    cell["moved_when_absent"] += rec["product_moves"][family]
        outcomes[(rec["month"], rec["origin"])][state] += 1
    family_rates = {
        family: {
            **counter,
            "movement_conditional_on_m0_presence": (
                counter["moved_when_present"] / counter["m0_present"]
                if counter["m0_present"] else None
            ),
        }
        for family, counter in within_family.items()
    }
    segments = []
    for (dimension, category), row in sorted(strata.items()):
        if row["rows"] < min_records:
            continue
        retained = row["retained"]
        opportunities = row["m0_family_opportunities"]
        segments.append({
            "dimension": dimension,
            "category": category,
            **dict(row),
            "movement_given_retained": (
                row["retained_movement"] / retained if retained else None
            ),
            "movement_flags_per_m0_family_opportunity": (
                row["moved_family_flags"] / opportunities
                if opportunities else None
            ),
            "retention_given_closed": (
                retained / row["closed"] if row["closed"] else None
            ),
        })
    monthly_origin = []
    for (month, origin), row in sorted(outcomes.items()):
        if sum(row.values()) < min_records:
            continue
        closed = row["RETIDO"] + row["NAO RETIDO"]
        monthly_origin.append({
            "month": month,
            "origin": origin,
            "retained": row["RETIDO"],
            "not_retained": row["NAO RETIDO"],
            "open": row["LEAD EM ABERTO"],
            "open_share": row["LEAD EM ABERTO"] / sum(row.values()),
            "retention_among_closed": row["RETIDO"] / closed if closed else None,
        })
    return {
        "protocol": "exploratory; data labels and episode key unvalidated",
        "minimum_group_size": min_records,
        "totals": dict(totals),
        "movement_by_initial_portfolio_size": segments,
        "movement_by_product_given_m0_presence": family_rates,
        "monthly_origin_outcomes": monthly_origin,
        "limits": [
            "Probability of any move rises with the number of available families; "
            "naive portfolio size comparisons may be opportunity biased.",
            "Flags are not independently verified offer-acceptance events.",
            "Per-family opportunity normalization is descriptive, "
            "not a causal adjustment.",
            "Repeated clients violate naive row independence; formal uncertainty "
            "requires client-cluster resampling.",
            "Open leads differ across origin/month; retention among closed is "
            "conditional on case resolution.",
            "No business population weighting is available.",
        ],
    }


def analyze_workbook(path: str | Path, output: str | Path) -> dict[str, Any]:
    """Run local, aggregated portfolio opportunity diagnostics."""
    result = analyze_opportunity(
        rec for row in iter_worksheet_rows(path)
        if (rec := record_profile(row)) is not None
    )
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result
