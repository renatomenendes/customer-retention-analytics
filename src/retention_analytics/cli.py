"""Local-only CLI for the retention data quality audit."""

from __future__ import annotations

import argparse
from pathlib import Path

from retention_analytics.audit import audit_workbook, write_private_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only audit of case XLSX")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path,
        default=Path("reports/private/audit_summary.json"),
    )
    parser.add_argument("--min-group-size", type=int, default=30)
    args = parser.parse_args()
    output = audit_workbook(args.input, args.min_group_size)
    write_private_json(output, args.output)
    print("Rows:", output["overall"]["rows_total"])
    print("In scope:", output["overall"]["rows_in_scope"])
    print("Private result:", args.output)
    print("Status: descriptive quality audit; business definitions pending")


if __name__ == "__main__":
    main()
