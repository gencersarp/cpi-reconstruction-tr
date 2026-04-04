"""Visualization utilities for inflation estimates."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path


def plot_index_comparison(
    independent: dict[str, float],
    official: dict[str, float],
    output_path: str | Path | None = None,
    title: str = "CPI Reconstruction: Independent vs. Official",
) -> None:
    """Plot comparison between independent and official series."""
    df_ind = pd.Series(independent, name="Independent").to_frame()
    df_off = pd.Series(official, name="Official").to_frame()

    df = df_ind.join(df_off, how="outer")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["Independent"], marker="o", label="Independent Index")
    plt.plot(df.index, df["Official"], marker="x", label="Official Index")

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Index Level")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    if output_path:
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
    else:
        plt.show()
