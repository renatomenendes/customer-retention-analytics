# ruff: noqa: E501
import numpy as np
import pytest

from retention_analytics.extended_eda import (
    adjusted_channel_gap,
    analyze_records,
    retention_bounds,
)


def test_open_case_binary_bounds():
    a=retention_bounds(8, 2, 2)
    assert a["lower_if_all_open_not_retained"] == pytest.approx(8/12)
    assert a["upper_if_all_open_retained"] == pytest.approx(10/12)
    assert a["observed_among_closed"] == pytest.approx(.8)


def test_channel_standardization_on_synthetic_strata():
    # Both origins in same stratum with different event rates; no false causal label.
    mi=np.zeros(200,dtype=np.int8)
    k=np.ones(200,dtype=np.int8)
    origin=np.r_[np.zeros(100,dtype=np.int8),np.ones(100,dtype=np.int8)]
    y=np.r_[np.ones(20,dtype=np.int8),np.zeros(80,dtype=np.int8),
            np.ones(40,dtype=np.int8),np.zeros(60,dtype=np.int8)]
    ids=[f"synthetic{i}" for i in range(200)]
    res=adjusted_channel_gap(mi,k,origin,y,ids,draws=20)
    assert res["standardized_solar_minus_legado"]==pytest.approx(.2)
    assert res["bootstrap_draws"]==20
    assert res["common_support_coverage"]==pytest.approx(1.0)


def test_no_common_support():
    x=adjusted_channel_gap(np.zeros(5,dtype=np.int8),np.ones(5,dtype=np.int8),
                           np.ones(5,dtype=np.int8),np.ones(5,dtype=np.int8),
                           [str(i) for i in range(5)],draws=0)
    assert not x["identified"]


def test_analysis_observational_synthetic():
    rows=[dict(DATA_FUNIL_SOLAR="2025-06-10",NM_SUB_INDICADOR_NEGOCIO="RETIDO",
               FLAG_ORIGEM="SOLAR",id_cliente="syntheticA",ID_PRODUTO_BL_M0="BL1",
               ID_PRODUTO_BL_M30="BL2",FLAG_MOV_BL="1",FLAG_CANC_BL="0",
               VALOR_BL_M0="100",VALOR_BL_M30="80",
               **{f"VALOR_{f}_{t}":"0" for f in ["TV","FONE","MV"] for t in ["M0","M30"]}),
          dict(DATA_FUNIL_SOLAR="2025-06-10",NM_SUB_INDICADOR_NEGOCIO="LEAD EM ABERTO",
               FLAG_ORIGEM="SOLAR",id_cliente="syntheticB")]
    a=analyze_records(rows,bootstrap_draws=0)
    assert a["counts"]["scope"]==2
    assert a["counts"]["retained_movement"]==1
    assert a["retained_value_distributions"]=={} # suppressed: n < 500
    assert a["channel_comparison_standardized"]["identified"] is False
