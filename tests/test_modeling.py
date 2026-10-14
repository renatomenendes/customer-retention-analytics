"""Validation design tests on synthetic, non-client observations."""
import numpy as np

from retention_analytics.modeling import evaluation, prepare_partitions


def make_record(month, customer):
    return {"month": month, "client_id": customer, "state": "RETIDO"}


def test_splits_purge_repeated_client_across_periods():
    cases = [make_record("2025-06", "A"), make_record("2025-10", "A"),
             make_record("2025-11", "A"), make_record("2025-09", "B"),
             make_record("2025-10", "C"), make_record("2025-12", "D")]
    result = prepare_partitions(cases)
    assert result["dropped_overlap_train"] == 1
    assert result["dropped_overlap_validation"] == 1
    assert [r["client_id"] for r in result["partitions"]["train"]] == ["B"]
    assert [r["client_id"] for r in result["partitions"]["val"]] == ["C"]


def test_evaluation_known_ranking():
    metrics = evaluation(np.array([0, 1, 0, 1]), np.array([0.1, 0.9, 0.2, 0.8]))
    assert metrics["roc_auc"] == 1.0
    assert metrics["average_precision"] == 1.0


def test_tied_scores_do_not_invent_rank_lift():
    score = evaluation(
        np.array([0, 1, 0, 1, 0, 1]), np.full(6, 0.5)
    )
    assert score["lift_top_decile"] == 1.0
    assert score["precision_top_decile"] == 0.5
