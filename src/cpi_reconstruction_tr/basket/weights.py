"""Basket and weight utilities."""

from __future__ import annotations


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    """Normalize expenditure shares to sum to one."""

    if not weights:
        raise ValueError("Weights cannot be empty")

    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weight sum must be positive")

    return {item: value / total for item, value in weights.items()}


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
