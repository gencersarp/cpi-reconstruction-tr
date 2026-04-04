"""Cleaning and normalization routines for price observations."""

from __future__ import annotations

from datetime import datetime


def _parse_iso_date(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.date().isoformat()


def normalize_price_records(
    rows: list[dict[str, str]],
    fx_rates: dict[tuple[str, str], float] | None = None,
    target_currency: str = "TRY",
) -> list[dict[str, object]]:
    """Normalize raw rows into typed records with currency harmonization."""

    fx_rates = fx_rates or {}
    normalized: list[dict[str, object]] = []

    for row in rows:
        raw_currency = row["currency"].upper().strip()
        rate = 1.0
        if raw_currency != target_currency:
            key = (raw_currency, target_currency)
            if key not in fx_rates:
                raise ValueError(f"Missing FX rate for {key}")
            rate = fx_rates[key]

        price = float(row["price"])
        if price < 0:
            raise ValueError(f"Negative price is not allowed: {price}")

        normalized.append(
            {
                "date": _parse_iso_date(row["date"]),
                "item_id": row["item_id"].strip(),
                "category": row["category"].strip().lower(),
                "source": row["source"].strip(),
                "unit": row["unit"].strip().lower(),
                "currency": target_currency,
                "price": round(price * rate, 6),
                "region": row.get("region", "TR").strip() or "TR",
            }
        )

    return normalized
