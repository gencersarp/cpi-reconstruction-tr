# Methodology

This project estimates inflation in Türkiye through independent methods and then compares outcomes with official publications without assuming any source is true by default.

## Core principles

- Transparency: every transformation is encoded in source-controlled code.
- Reproducibility: raw and processed data locations are explicit (`data/raw`, `data/processed`).
- Triangulation: multiple methods and proxy series are compared rather than relying on one number.
- Uncertainty reporting: sensitivity to basket assumptions is measured directly.

## Methods implemented

1. **Bottom-up basket index**
   - Build category/item basket with expenditure shares.
   - Convert shares into implied quantities using base prices.
   - Compute Laspeyres, Paasche, and Fisher indices.

2. **Chained index series**
   - Build time-evolving index levels from period relatives.
   - Supports rolling updates as new price observations arrive.

3. **Benchmark comparison**
   - Align independent and benchmark (TÜİK/ENAG/ITO) monthly series.
   - Report MAE, RMSE, and correlation over overlap periods.

4. **Sensitivity analysis**
   - Perturb basket shares in controlled ranges.
   - Recompute index outcomes to quantify uncertainty due to weights.

## Limitations

- Data coverage depends on legally collectible sources and update frequencies.
- Paasche requires current-period quantities; if unavailable, approximation choices must be documented.
- Proxies (FX/energy/second-hand markets) capture pressure signals, not headline CPI definitions.
