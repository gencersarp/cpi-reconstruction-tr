"""Index number calculations used by the reconstruction framework."""

from __future__ import annotations

import math


def _validate_inputs(
    base_prices: dict[str, float],
    current_prices: dict[str, float],
    quantities: dict[str, float],
) -> None:
    if not base_prices or not current_prices or not quantities:
        raise ValueError("Input mappings cannot be empty")

    for item in quantities:
        if item not in base_prices or item not in current_prices:
            raise ValueError(f"Item '{item}' missing in price dictionaries")
        if base_prices[item] <= 0 or current_prices[item] <= 0:
            raise ValueError(f"Prices must be positive for item '{item}'")
        if quantities[item] < 0:
            raise ValueError(f"Quantities must be non-negative for item '{item}'")


def laspeyres_index(
    base_prices: dict[str, float],
    current_prices: dict[str, float],
    base_quantities: dict[str, float],
) -> float:
    """Compute Laspeyres price index with base-period quantities."""

    _validate_inputs(base_prices, current_prices, base_quantities)
    numerator = sum(current_prices[i] * base_quantities[i] for i in base_quantities)
    denominator = sum(base_prices[i] * base_quantities[i] for i in base_quantities)
    return 100.0 * numerator / denominator


def paasche_index(
    base_prices: dict[str, float],
    current_prices: dict[str, float],
    current_quantities: dict[str, float],
) -> float:
    """Compute Paasche price index with current-period quantities."""

    _validate_inputs(base_prices, current_prices, current_quantities)
    numerator = sum(current_prices[i] * current_quantities[i] for i in current_quantities)
    denominator = sum(base_prices[i] * current_quantities[i] for i in current_quantities)
    return 100.0 * numerator / denominator


def fisher_index(
    base_prices: dict[str, float],
    current_prices: dict[str, float],
    base_quantities: dict[str, float],
    current_quantities: dict[str, float],
) -> float:
    """Compute Fisher ideal index as geometric mean of Laspeyres and Paasche."""

    l_value = laspeyres_index(base_prices, current_prices, base_quantities)
    p_value = paasche_index(base_prices, current_prices, current_quantities)
    return math.sqrt(l_value * p_value)


def chained_index(period_relatives: list[float], base_value: float = 100.0) -> list[float]:
    """Chain monthly/period relatives (e.g., 1.03 for +3%) into an index level."""

    if base_value <= 0:
        raise ValueError("base_value must be positive")

    result = [base_value]
    level = base_value

    for relative in period_relatives:
        if relative <= 0:
            raise ValueError("All period relatives must be positive")
        level *= relative
        result.append(level)

    return result
