"""Checks on artificial analysis records; no customer data or production outputs."""

import pytest

from retention_analytics.deep_diagnostics import analyze_opportunity


def _record(initial: tuple[str, ...], moving: tuple[str, ...], status="RETIDO"):
    return {
        "state": status,
        "origin": "SOLAR",
        "month": "2025-07",
        "movement": bool(moving),
        "features": {
            f"has_{family.lower()}_m0": int(family in initial)
            for family in ("BL", "TV", "FONE", "MV")
        },
        "product_moves": {
            family: family in moving
            for family in ("BL", "TV", "FONE", "MV")
        },
    }


def test_stratification_and_exposure_normalization():
    records = [
        _record(("BL",), ("BL",)),
        _record(("BL", "TV"), ("TV",)),
        _record(("BL", "TV"), ()),
        _record(("BL",), (), "NAO RETIDO"),
    ] * 30
    result = analyze_opportunity(records, min_records=30)
    subset = [
        x for x in result["movement_by_initial_portfolio_size"]
        if x["dimension"] == "family_count" and x["category"] == "2"
    ][0]
    assert subset["retained"] == 60
    assert subset["retained_movement"] == 30
    assert subset["m0_family_opportunities"] == 120
    assert subset["moved_family_flags"] == 30
    assert subset["movement_given_retained"] == 0.5
    assert subset["movement_flags_per_m0_family_opportunity"] == 0.25


def test_movement_without_m0_presence_is_flagged():
    result = analyze_opportunity(
        [_record(("BL",), ("MV",))] * 30, min_records=30
    )
    subset = next(
        x for x in result["movement_by_initial_portfolio_size"]
        if x["dimension"] == "family_count" and x["category"] == "1"
    )
    assert subset["move_flags_absent_from_m0"] == 30
    mobile = result["movement_by_product_given_m0_presence"]["MV"]
    assert mobile["moved_when_absent"] == 30


def test_small_groups_suppressed_and_invalid_minimum_rejected():
    result = analyze_opportunity([_record(("BL",), ())] * 5, min_records=30)
    assert result["movement_by_initial_portfolio_size"] == []
    with pytest.raises(ValueError):
        analyze_opportunity([], min_records=10)
