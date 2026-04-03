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
