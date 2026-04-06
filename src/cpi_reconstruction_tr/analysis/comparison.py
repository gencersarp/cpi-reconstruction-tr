"""Comparison and uncertainty helpers."""

from __future__ import annotations

import random
import statistics

from cpi_reconstruction_tr.basket.weights import normalize_weights
from cpi_reconstruction_tr.indices.calculate import laspeyres_index


def compare_series(
    independent: dict[str, float],
    official: dict[str, float],
) -> dict[str, float]:
    """Compare aligned series and return objective error statistics."""

    common_dates = sorted(set(independent).intersection(official))
    if not common_dates:
        raise ValueError("No overlapping dates between series")

    residuals = [independent[d] - official[d] for d in common_dates]
    abs_residuals = [abs(value) for value in residuals]

    mae = statistics.mean(abs_residuals)
    rmse = (statistics.mean(value * value for value in residuals)) ** 0.5

    if len(common_dates) > 1:
        left = [independent[d] for d in common_dates]
        right = [official[d] for d in common_dates]
        if len(set(left)) > 1 and len(set(right)) > 1:
            corr = statistics.correlation(left, right)
        else:
            corr = 0.0
    else:
        corr = 0.0

    return {
        "n_periods": float(len(common_dates)),
        "mae": mae,
        "rmse": rmse,
        "correlation": corr,
    }


def mean_absolute_percentage_error(
    independent: dict[str, float],
    official: dict[str, float],
) -> float:
    """Compute MAPE between two aligned index series.

    Returns the mean absolute percentage error as a fraction (0.05 = 5 %).
    More interpretable than MAE when the series are in index-point units
    because it normalises each residual by the official reference value.

    Raises ``ValueError`` if the two series share no common dates.
    """
    common_dates = sorted(set(independent).intersection(official))
    if not common_dates:
        raise ValueError("No overlapping dates between series")

    pct_errors = [
        abs(independent[d] - official[d]) / max(abs(official[d]), 1e-9)
        for d in common_dates
    ]
    return statistics.mean(pct_errors)


def sensitivity_to_weights(
    base_prices: dict[str, float],
    current_prices: dict[str, float],
    base_weights: dict[str, float],
    n_runs: int = 250,
    shock: float = 0.1,
    seed: int = 42,
) -> dict[str, float]:
    """Stress-test Laspeyres index against random basket perturbations."""

    if n_runs <= 0:
        raise ValueError("n_runs must be positive")
    if shock < 0:
        raise ValueError("shock must be non-negative")

    rng = random.Random(seed)
    base_weights = normalize_weights(base_weights)

    outcomes: list[float] = []
    for _ in range(n_runs):
        perturbed = {
            item: max(1e-12, weight * (1 + rng.uniform(-shock, shock)))
            for item, weight in base_weights.items()
        }
        norm = normalize_weights(perturbed)
        base_quantities = {item: norm[item] / base_prices[item] for item in norm}
        outcomes.append(laspeyres_index(base_prices, current_prices, base_quantities))

    return {
        "mean": statistics.mean(outcomes),
        "stdev": statistics.pstdev(outcomes),
        "min": min(outcomes),
        "max": max(outcomes),
    }
