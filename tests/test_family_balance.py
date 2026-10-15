# ruff: noqa: E501
import numpy as np
import pytest

from retention_analytics.family_balance import family_exposure, scores


def test_eligibility_respects_initial_product_presence():
    a = ("SOLAR", "RJ", "NAO_ELEGIVEL", "G1", "0", "BL", 1, 1, 0, 0, 0, 100., 0., 0.)
    b = ("SOLAR", "RJ", "NAO_ELEGIVEL", "G1", "1", "BL+MV", 2, 1, 0, 0, 1, 100., 0., 50.)
    data = [
        {"x": a, "moves": {"BL": 1, "TV": 0, "FONE": 0, "MV": 0}},
        {"x": b, "moves": {"BL": 0, "TV": 0, "FONE": 0, "MV": 1}},
    ]
    result = family_exposure(data)
    assert result["BL"]["n"] == 2 and result["BL"]["positive"] == 1
    assert result["MV"]["n"] == 1 and result["MV"]["positive"] == 1
    assert result["TV"]["n"] == 0 and result["TV"]["rate"] is None


def test_top_decile_and_ap_relative_to_prevalence():
    actual = np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    probability = np.array([.9, .8, .7, .6, .5, .4, .3, .2, .1, .01])
    result = scores(actual, probability)
    assert result["precision_top10"] == 1
    assert result["recall_top10"] == .5
    assert result["ap_lift"] > 1


def test_constant_label_rejected():
    with pytest.raises(ValueError):
        scores(np.zeros(10), np.full(10, 0.5))


def test_client_overlap_removed_from_prior_temporal_splits():
    from retention_analytics.family_balance import prepare_splits

    rows = [
        {"id": "a", "month": "2025-06"},
        {"id": "b", "month": "2025-08"},
        {"id": "a", "month": "2025-10"},
        {"id": "c", "month": "2025-11"},
    ]
    pools, purged = prepare_splits(rows)
    assert purged == {"train": 1, "val": 0}
    assert [r["id"] for r in pools["train"]] == ["b"]
    train = {r["id"] for r in pools["train"]}
    val = {r["id"] for r in pools["val"]}
    test = {r["id"] for r in pools["test"]}
    assert train.isdisjoint(val)
    assert train.isdisjoint(test)
    assert val.isdisjoint(test)
