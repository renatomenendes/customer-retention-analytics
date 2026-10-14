"""Synthetic, disclosure-safe tests of the audit semantics."""

import pytest

from retention_analytics.audit import _month, audit_records
from retention_analytics.xlsx_stream import excel_column_index


def make_record(client, date, status, movement=0, cancellation=0, p0=101, p30=101):
    record = {
        "id_cliente": client,
        "DATA_FUNIL_SOLAR": date,
        "NM_SUB_INDICADOR_NEGOCIO": status,
        "FLAG_ORIGEM": "SOLAR",
    }
    for family in ("BL", "TV", "FONE", "MV"):
        record[f"FLAG_MOV_{family}"] = str(movement if family == "BL" else 0)
        record[f"FLAG_CANC_{family}"] = str(cancellation if family == "BL" else 0)
        field = "COD_PLANO_MOVEL" if family == "MV" else f"ID_PRODUTO_{family}"
        record[f"{field}_M0"] = str(p0) if family == "BL" else "0"
        record[f"{field}_M30"] = str(p30) if family == "BL" else "0"
        for period in ("M0", "M30"):
            record[f"VALOR_{family}_{period}"] = "99" if family == "BL" else "0"
    return record


def test_column_address():
    assert excel_column_index("A42") == 0
    assert excel_column_index("AV1") == 47


def test_mixed_status_and_out_of_scope():
    rows = [
        make_record("a", "2025-06-10", "RETIDO", movement=1),
        make_record("a", "2025-07-02", "NAO RETIDO", cancellation=1, p30=0),
        make_record("b", "2025-09-01", "LEAD EM ABERTO"),
        make_record("c", "2025-05-31", "RETIDO"),
    ]
    result = audit_records(rows, minimum_group_size=2)
    assert result["overall"]["rows_total"] == 4
    assert result["overall"]["rows_in_scope"] == 3
    assert result["overall"]["retained_movement"] == 1
    assert result["status_in_scope"]["LEAD EM ABERTO"] == 1
    assert result["clients"]["ids_with_mixed_status"] == 1
    assert result["out_of_scope_months"]["2025-05"] == 1


def test_code_change_without_flag_is_reported():
    row = make_record("c", "2025-12-31", "RETIDO", p0=1, p30=2)
    result = audit_records([row], minimum_group_size=2)
    assert result["products"]["BL"]["changed_code_without_flag"] == 1


def test_empty_rejected():
    with pytest.raises(ValueError):
        audit_records([])


def test_month_parser():
    assert _month("2025-12-31") == "2025-12"
    assert _month("45901.75") == "2025-09"
