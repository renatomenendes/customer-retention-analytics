"""Synthetic-only tests for provisional case analysis."""

from retention_analytics.profiles import (
    record_profile,
    summarize_profiles,
    wilson_interval,
)


def _case(state="RETIDO", flag="1", client="TEST-001"):
    return {
        "DATA_FUNIL_SOLAR": "45810", "id_cliente": client,
        "NM_SUB_INDICADOR_NEGOCIO": state,
        "FLAG_ORIGEM": "SOLAR", "SGL_UF": "SP",
        "ID_PRODUTO_BL_M0": "11", "ID_PRODUTO_BL_M30": "12",
        "FLAG_MOV_BL": flag, "VALOR_BL_M0": "100", "VALOR_BL_M30": "80",
        "VALOR_TV_M0": "0", "VALOR_TV_M30": "0",
        "VALOR_FONE_M0": "0", "VALOR_FONE_M30": "0",
        "VALOR_MV_M0": "0", "VALOR_MV_M30": "0",
    }


def test_provisional_target_and_value_change():
    result = record_profile(_case())
    assert result["retained_movement"] is True
    assert result["family_count_m0"] == "1"
    assert result["value_m30"] - result["value_m0"] == -20


def test_non_retained_movement_not_positive_target():
    assert record_profile(_case(state="NAO RETIDO"))["retained_movement"] is False


def test_missing_value_not_silently_zeroed():
    record = _case()
    del record["VALOR_BL_M30"]
    assert record_profile(record)["value_m30"] is None


def test_suppressed_groups_and_economics():
    sample = [record_profile(_case(client=f"TEST-{i}")) for i in range(32)]
    result = summarize_profiles(sample, min_group_n=30)
    assert result["overall"]["retained_movement"] == 32
    movement = result["value_snapshot_comparison"]["retained_movement"]
    assert movement["median_change"] == -20
    assert all(item["n"] >= 30 for item in result["segments"])


def test_wilson_bounded():
    lo, hi = wilson_interval(2, 10)
    assert 0 <= lo <= 0.2 <= hi <= 1
