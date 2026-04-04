"""Data ingestion helpers for CSV-based reproducible pipelines."""

from __future__ import annotations

import csv
from pathlib import Path


REQUIRED_PRICE_COLUMNS = {
    "date",
    "item_id",
    "category",
    "source",
    "price",
    "currency",
    "unit",
}


def read_price_csv(path: str | Path) -> list[dict[str, str]]:
    """Read price observations from CSV without mutating values."""

    path = Path(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")

        missing = REQUIRED_PRICE_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns {sorted(missing)} in {path}")

        return [dict(row) for row in reader]


def write_records_csv(path: str | Path, rows: list[dict[str, object]]) -> None:
    """Write normalized records to CSV in deterministic column order."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        raise ValueError("Cannot write empty record list.")

    fieldnames = sorted(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
