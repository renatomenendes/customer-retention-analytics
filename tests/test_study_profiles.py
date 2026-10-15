"""Tests prevent interpreting offer acceptance as an observed event."""
from retention_analytics.study_profiles import analyze_retained, extract


def _row(**overrides):
    data={
        "DATA_FUNIL_SOLAR":"2025-08-09", "NM_SUB_INDICADOR_NEGOCIO":"RETIDO",
        "id_cliente":"123", "FLAG_ORIGEM":"SOLAR", "SGL_UF":"RJ",
        "ID_PRODUTO_BL_M0":"10","ID_PRODUTO_BL_M30":"20",
        "FLAG_MOV_BL":"1","FLAG_CANC_BL":"0", "VALOR_BL_M0":"100",
        "VALOR_BL_M30":"80",
    }
    data.update(overrides)
    return data


def test_strict_proxy_only_for_moved_changed_non_cancelled_product():
    assert extract(_row())["strict_proxy"]==1
    assert extract(_row(FLAG_CANC_BL="1"))["strict_proxy"]==0
    assert extract(_row(ID_PRODUTO_BL_M30="10"))["strict_proxy"]==0
    assert extract(_row(FLAG_MOV_BL="0"))["strict_proxy"]==0


def test_offer_acceptance_never_assumed_observed():
    study=analyze_retained([_row(),_row(id_cliente="124",FLAG_MOV_BL="0")],fit_models=False)
    assert study["totals"]["total"]==2
    assert study["totals"]["moved"]==1
    assert study["rates"]["movement_given_retained"]==.5
    assert "NOT_OBSERVED" in study["definitions"]["offer_acceptance"]


def test_nonretained_and_out_of_window_excluded():
    study=analyze_retained([_row(),_row(NM_SUB_INDICADOR_NEGOCIO="NAO RETIDO"),
                             _row(DATA_FUNIL_SOLAR="2025-05-01")],fit_models=False)
    assert study["totals"]["total"]==1


def test_first_record_sensitivity_does_not_extrapolate_to_unique_lead():
    study=analyze_retained([_row(DATA_FUNIL_SOLAR="2025-09-10"),
                            _row(DATA_FUNIL_SOLAR="2025-06-10",FLAG_MOV_BL="0"),
                            _row(id_cliente="222")],fit_models=False)
    assert study["first_retained_record_per_client_sensitivity"]["n"]==2
    assert study["first_retained_record_per_client_sensitivity"]["movement_rate"]==.5


def test_blank_mplay_means_ineligible_not_unknown():
    assert extract(_row())["x"][2] == "NAO_ELEGIVEL"
    assert extract(_row(DSC_CLI_MPLAY_M0="  "))["x"][2] == "NAO_ELEGIVEL"
    assert extract(_row(DSC_CLI_MPLAY_M0="MARCADO"))["x"][2] == "MARCADO"
    assert extract(_row(DSC_CLI_MPLAY_M0="NAO-MARCADO"))["x"][2] == "NAO-MARCADO"
