# API and CLI Reference

## CLI Usage

The `inflation-pipeline` command (or `python -m cpi_reconstruction_tr.pipeline`) provides several subcommands:

### `list-sources`
Lists all configured data sources.
```bash
inflation-pipeline list-sources
```

### `compute-indices`
Computes Laspeyres, Paasche, and Fisher indices.
```bash
inflation-pipeline compute-indices \
  --base-prices data/raw/base_prices.json \
  --current-prices data/raw/current_prices.json \
  --base-shares data/raw/base_shares.json
```

### `plot`
Generates a comparison plot.
```bash
inflation-pipeline plot \
  --independent-series data/raw/independent_series.json \
  --official-series data/raw/official_series.json \
  --output plot.png
```

## Python API

### `cpi_reconstruction_tr.indices.calculate`
Functions for calculating inflation indices:
- `laspeyres_index(p0, p1, q0)`
- `paasche_index(p0, p1, q1)`
- `fisher_index(p0, p1, q0, q1)`

### `cpi_reconstruction_tr.reporting.plots`
- `plot_index_comparison(independent, official, output_path=None)`
