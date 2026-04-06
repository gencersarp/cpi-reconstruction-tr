"""Basket and weight utilities."""

from __future__ import annotations

import math


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    """Normalize expenditure shares to sum to one."""

    if not weights:
        raise ValueError("Weights cannot be empty")

    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weight sum must be positive")

    return {item: value / total for item, value in weights.items()}


def geometric_mean_weights(
    weight_series: list[dict[str, float]],
) -> dict[str, float]:
    """Compute geometric mean weights from a time series of expenditure shares.

    Used in superlative index construction (e.g. Törnqvist) and for
    producing a single representative basket from multiple period shares.
    Each dict must cover the same set of items. The result is normalised
    to sum to one.

    Raises ``ValueError`` if the series is empty or item sets are inconsistent.
    """
    if not weight_series:
        raise ValueError("weight_series cannot be empty")

    items = set(weight_series[0].keys())
    for i, w in enumerate(weight_series[1:], start=1):
        if set(w.keys()) != items:
            raise ValueError(f"Item set at index {i} differs from index 0")

    n = len(weight_series)
    geo: dict[str, float] = {}
    for item in items:
        log_sum = sum(math.log(max(w[item], 1e-300)) for w in weight_series)
        geo[item] = math.exp(log_sum / n)

    return normalize_weights(geo)


def shares_to_base_quantities(
    base_prices: dict[str, float],
    expenditure_shares: dict[str, float],
) -> dict[str, float]:
    """Convert base-period shares into implied base-period quantities."""

    normalized = normalize_weights(expenditure_shares)
    quantities: dict[str, float] = {}

    for item, share in normalized.items():
        if item not in base_prices:
            raise ValueError(f"Missing base price for item '{item}'")
        price = base_prices[item]
        if price <= 0:
            raise ValueError(f"Base price must be positive for item '{item}'")
        quantities[item] = share / price

    return quantities
