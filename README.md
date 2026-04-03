# cpi-reconstruction-tr

Independent, data-driven estimation of inflation in Türkiye using market-based price signals.

## Why this project exists

The objective is to reconstruct inflation with transparent and reproducible methods, then compare outputs to official and alternative indices without assuming any source is inherently right or wrong.

## Repository structure

```text
cpi-reconstruction-tr/
├── data/
│   ├── raw/                  # source snapshots (not fabricated)
│   └── processed/            # normalized/derived datasets
├── docs/
│   ├── methodology.md        # assumptions, methods, limitations
│   └── data_sources.md       # acquisition and source governance
├── src/cpi_reconstruction_tr/
│   ├── data/
│   │   ├── ingest.py         # CSV ingestion/writing for reproducible pipelines
│   │   └── sources.py        # canonical source registry
│   ├── processing/
│   │   └── normalize.py      # cleaning, typing, currency normalization
│   ├── basket/
│   │   └── weights.py        # share normalization and implied quantities
│   ├── indices/
│   │   └── calculate.py      # Laspeyres, Paasche, Fisher, chained indices
│   ├── analysis/
│   │   └── comparison.py     # benchmark comparison + sensitivity analysis
│   └── pipeline.py           # CLI for staged execution
├── tests/
│   ├── test_analysis.py
│   ├── test_indices.py
│   └── test_processing.py
└── pyproject.toml
```

## Incremental development plan with rationale and commit messages

### 1) Project setup
- **Why**: establishes reproducible structure and coding boundaries.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/__init__.py
__version__ = "0.1.0"
```
- **Commit message**: `chore: scaffold reproducible inflation reconstruction package`

### 2) Data source identification
- **Why**: ensures transparent provenance and objective triangulation.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/data/sources.py
@dataclass(frozen=True)
class DataSource:
    source_id: str
    name: str
    methodology_role: str
```
- **Commit message**: `feat: add canonical registry for benchmark and market data sources`

### 3) Data collection pipeline
- **Why**: separates raw extraction from downstream calculations.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/data/ingest.py
rows = read_price_csv("data/raw/prices.csv")
```
- **Commit message**: `feat: add deterministic CSV ingestion and export utilities`

### 4) Data cleaning and normalization
- **Why**: inflation estimates are sensitive to units, currency, and date quality.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/processing/normalize.py
normalized = normalize_price_records(rows, fx_rates={("USD", "TRY"): 30.0})
```
- **Commit message**: `feat: implement typed normalization and FX harmonization for price records`

### 5) Basket construction
- **Why**: transparent weights are required for defensible index design.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/basket/weights.py
base_quantities = shares_to_base_quantities(base_prices, expenditure_shares)
```
- **Commit message**: `feat: add basket share normalization and implied quantity conversion`

### 6) Index calculation
- **Why**: multiple index formulas reduce methodological single-point failure.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/indices/calculate.py
fisher = fisher_index(base_prices, current_prices, q0, qt)
```
- **Commit message**: `feat: implement Laspeyres Paasche Fisher and chained index calculators`

### 7) Validation and sensitivity analysis
- **Why**: quantify uncertainty and benchmark divergence objectively.
- **Code snippet**:
```python
# src/cpi_reconstruction_tr/analysis/comparison.py
metrics = compare_series(independent, official)
```
- **Commit message**: `feat: add benchmark comparison metrics and basket sensitivity simulation`

### 8) Visualization and reporting (next step)
- **Why**: makes outputs interpretable for researchers and decision-makers.
- **Code snippet (planned)**:
```python
# planned module: src/cpi_reconstruction_tr/reporting/plots.py
# def plot_index_comparison(...):
#     ...
```
- **Commit message**: `feat: add reproducible reporting visuals for inflation estimates`

## Quick start

```bash
python -m unittest discover -s tests
python -m cpi_reconstruction_tr.pipeline list-sources
```

### Example index run

Prepare JSON files for `base_prices`, `current_prices`, and `base_shares`:

```bash
python -m cpi_reconstruction_tr.pipeline compute-indices \
  --base-prices /absolute/path/base_prices.json \
  --current-prices /absolute/path/current_prices.json \
  --base-shares /absolute/path/base_shares.json \
  --use-base-quantities-for-paasche
```

## Methodological safeguards

- No fabricated data is included.
- Assumptions are documented in `docs/methodology.md`.
- Source acquisition requirements are documented in `docs/data_sources.md`.
- Benchmarks are used for comparison, not as truth labels.
