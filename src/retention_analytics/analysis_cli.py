"""Local-only CLI for the case's private profile and modeling analysis."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from retention_analytics.modeling import evaluate_models
from retention_analytics.profiles import record_profile, summarize_profiles
from retention_analytics.xlsx_stream import iter_worksheet_rows


def _fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    """Read the full XLSX once and persist only local aggregate artifacts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out-dir", default=Path("reports/private"), type=Path)
    parser.add_argument("--min-group-n", type=int, default=100)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error("Input workbook does not exist")
    if args.min_group_n < 30:
        parser.error("At least 30 records are required for displayed groups")
    output = args.out_dir
    output.mkdir(parents=True, exist_ok=True)
    records = [
        profile for row in iter_worksheet_rows(args.input)
        if (profile := record_profile(row)) is not None
    ]
    provenance = {
        "file_sha256": _fingerprint(args.input),
        "source_sheet": "first worksheet; verify business identity externally",
    }
    profiles = summarize_profiles(records, min_group_n=args.min_group_n)
    profiles["provenance"] = provenance
    metrics = evaluate_models(records)
    metrics["provenance"] = provenance
    for name, document in (
        ("profiles_summary.json", profiles),
        ("model_validation.json", metrics),
    ):
        (output / name).write_text(
            json.dumps(document, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    print("Local aggregates and model metrics written to", output)


if __name__ == "__main__":
    main()
