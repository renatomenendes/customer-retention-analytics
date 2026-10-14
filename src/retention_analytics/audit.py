"""Privacy-preserving, episode-level descriptive audit of retention data.

All observed records are retained during counting. No deduplication is
performed because the supplied client ID does not define a unique episode.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from retention_analytics.xlsx_stream import iter_worksheet_rows

PRODUCTS = ("BL", "TV", "FONE", "MV")
STATUS = "NM_SUB_INDICADOR_NEGOCIO"
ORIGIN = "FLAG_ORIGEM"
DATE = "DATA_FUNIL_SOLAR"
CLIENT = "id_cliente"
START = "2025-06"
END = "2025-12"
BASIC_COLUMNS = (CLIENT, DATE, STATUS, ORIGIN)
EPOCH = datetime(1899, 12, 30)


def _flag(value: str | None) -> bool:
    return value in ("1", "1.0")


def _number(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _month(value: str | None) -> str | None:
    number = _number(value)
    if number is not None:
        try:
            return (EPOCH + timedelta(days=number)).strftime("%Y-%m")
        except (OverflowError, ValueError):
            return None
    try:
        return datetime.fromisoformat(str(value)).strftime("%Y-%m")
    except (TypeError, ValueError):
        return None


def _presence(value: str | None) -> bool:
    return value is not None and str(value).strip() not in ("", "0", "0.0")


def _product_id(
    record: Mapping[str, str | None], family: str, period: str
) -> str | None:
    field = (
        f"COD_PLANO_MOVEL_{period}" if family == "MV"
        else f"ID_PRODUTO_{family}_{period}"
    )
    value = record.get(field)
    return str(value) if _presence(value) else None


def _hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_records(
    records: Iterable[Mapping[str, str | None]],
    minimum_group_size: int = 30,
) -> dict[str, Any]:
    """Aggregate raw record stream; never return customer identifiers.

    Status and flags follow *provisional* operational interpretations.
    This function reports lead/row-level sample frequencies, not a customer
    survival rate or financial effect.
    """
    if minimum_group_size < 2:
        raise ValueError("minimum_group_size must be at least 2")
    overall = Counter()
    months = Counter()
    outside = Counter()
    status = Counter()
    monthly_status = Counter()
    origins = Counter()
    monthly_origin = Counter()
    clients = Counter()
    statuses_by_client: dict[str, set[str]] = defaultdict(set)
    client_month_time = Counter()
    missing = Counter()
    products = {family: Counter() for family in PRODUCTS}
    initial_mix = Counter()
    segment = defaultdict(Counter)
    income = {f"{family}_{period}": {"count": 0, "sum": 0.0, "negative": 0}
              for family in PRODUCTS for period in ("M0", "M30")}
    headers: set[str] | None = None
    for record in records:
        if headers is None:
            headers = set(record)
            missing_required = set(BASIC_COLUMNS).difference(headers)
            if missing_required:
                raise ValueError(
                    f"Missing mandatory fields: {sorted(missing_required)}"
                )
        overall["rows_total"] += 1
        for column in headers:
            if record.get(column) in (None, ""):
                missing[column] += 1
        month = _month(record.get(DATE))
        if month is None:
            overall["invalid_date"] += 1
            continue
        if not START <= month <= END:
            outside[month] += 1
            continue
        overall["rows_in_scope"] += 1
        state = (record.get(STATUS) or "<NULL>").strip()
        origin = (record.get(ORIGIN) or "<NULL>").strip()
        status[state] += 1
        origins[origin] += 1
        months[month] += 1
        monthly_status[(month, state)] += 1
        monthly_origin[(month, origin, state)] += 1
        client_id = record.get(CLIENT)
        if client_id not in (None, ""):
            clients[str(client_id)] += 1
            statuses_by_client[str(client_id)].add(state)
            client_month_time[(str(client_id), record.get(DATE))] += 1
        else:
            overall["missing_client_id"] += 1
        movement = any(_flag(record.get(f"FLAG_MOV_{fam}")) for fam in PRODUCTS)
        cancellation = any(_flag(record.get(f"FLAG_CANC_{fam}")) for fam in PRODUCTS)
        if movement:
            overall["movement_any"] += 1
        if cancellation:
            overall["cancellation_any"] += 1
        if state == "RETIDO":
            overall["retained"] += 1
            if movement:
                overall["retained_movement"] += 1
            if cancellation:
                overall["retained_cancellation"] += 1
            if movement and cancellation:
                overall["retained_mov_and_canc"] += 1
        num_initial = 0
        for family in PRODUCTS:
            p0 = _product_id(record, family, "M0")
            p30 = _product_id(record, family, "M30")
            p = products[family]
            if p0 is not None:
                p["present_m0"] += 1
                num_initial += 1
            if p30 is not None:
                p["present_m30"] += 1
            if p0 is None and p30 is not None:
                p["added"] += 1
            elif p0 is not None and p30 is None:
                p["removed"] += 1
            elif p0 and p30 and p0 != p30:
                p["changed_code"] += 1
            flag_mov = _flag(record.get(f"FLAG_MOV_{family}"))
            flag_canc = _flag(record.get(f"FLAG_CANC_{family}"))
            if flag_mov:
                p["flag_movement"] += 1
            if flag_canc:
                p["flag_cancellation"] += 1
            if p0 != p30 and not (flag_mov or flag_canc):
                p["changed_code_without_flag"] += 1
            if p0 == p30 and (flag_mov or flag_canc):
                p["flag_without_code_change"] += 1
            a = _number(record.get(f"VALOR_{family}_M0"))
            b = _number(record.get(f"VALOR_{family}_M30"))
            if p0 and p0 == p30 and a is not None and b is not None and abs(a-b)>1e-8:
                p["same_code_different_value"] += 1
            for label, amount in (("M0", a), ("M30", b)):
                if amount is not None:
                    x = income[f"{family}_{label}"]
                    x["count"] += 1
                    x["sum"] += amount
                    x["negative"] += amount < 0
        initial_mix[num_initial] += 1
        for dimension, category in (("month", month), ("origin", origin),
                                    ("initial_families", str(num_initial))):
            counts = segment[(dimension, category)]
            counts["total"] += 1
            counts["closed"] += state in ("RETIDO", "NAO RETIDO")
            counts["retained"] += state == "RETIDO"
            counts["retained_movement"] += state == "RETIDO" and movement
    if overall["rows_total"] == 0:
        raise ValueError("Workbook contains no data rows")
    exact_duplicates = sum(max(0, n - 1) for n in client_month_time.values())
    repeated = sum(n > 1 for n in clients.values())
    mixed_status = sum(len(s) > 1 for s in statuses_by_client.values())
    groups = []
    for (dimension, category), counts in sorted(segment.items()):
        total = counts["total"]
        if total < minimum_group_size:
            continue
        ret = counts["retained"]
        group = {
            "dimension": dimension,
            "category": category,
            "n_records": total,
            "n_closed": counts["closed"],
            "n_retained": ret,
            "n_retained_movement": counts["retained_movement"],
            "retained_movement_given_retained": (
                counts["retained_movement"] / ret if ret else None
            ),
        }
        groups.append(group)
    return {
        "grain": "source row / provisional funnel episode, not unique customer",
        "period": {"start": START, "end": END},
        "definitions_status": "PROVISIONAL_UNVALIDATED",
        "overall": dict(overall),
        "out_of_scope_months": dict(sorted(outside.items())),
        "missing_all_rows": dict(sorted(missing.items())),
        "status_in_scope": dict(status),
        "monthly_rows": dict(sorted(months.items())),
        "monthly_status": [
            {"month": m, "status": s, "n_records": n}
            for (m, s), n in sorted(monthly_status.items())
        ],
        "monthly_origin_status": [
            {"month": m, "origin": o, "status": s, "n_records": n}
            for (m, o, s), n in sorted(monthly_origin.items())
            if n >= minimum_group_size
        ],
        "origins_in_scope": dict(origins),
        "clients": {
            "distinct_in_scope": len(clients),
            "repeated_ids_in_scope": repeated,
            "extra_records_same_id_in_scope": sum(clients.values()) - len(clients),
            "ids_with_mixed_status": mixed_status,
            "additional_duplicate_id_and_timestamp": exact_duplicates,
        },
        "products": {key: dict(value) for key, value in products.items()},
        "initial_family_counts": dict(sorted(initial_mix.items())),
        "monetary_fields": income,
        "segment_profiles_suppressed_below_n": minimum_group_size,
        "segment_profiles": groups,
        "limitations": [
            "Unit of record is not an officially validated episode key.",
            "Status RETIDO does not demonstrate long-run client survival.",
            "Movement flags are not documented as accepted offers.",
            "VALOR fields have no confirmed billing period or revenue meaning.",
            "Unweighted sample frequencies must not be generalized.",
            "M30 is a process snapshot, not independently timestamped "
            "30-day follow-up.",
        ],
    }


def audit_workbook(path: str | Path, minimum_group_size: int = 30) -> dict[str, Any]:
    """Read and audit the full source worksheet and attach provenance."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    result = audit_records(iter_worksheet_rows(source), minimum_group_size)
    result["provenance"] = {
        "source_sha256": _hash_file(source),
        "size_bytes": source.stat().st_size,
        "source_sheet": "sheet1.xml (first worksheet)",
        "engine": "lxml ZIP/XML streaming, read only",
    }
    return result


def write_private_json(result: dict[str, Any], path: str | Path) -> None:
    """Persist results in a directory excluded from Git."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
