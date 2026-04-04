# Data Sources and Acquisition Plan

This repository does not fabricate data. If a dataset is not locally available, acquisition steps are specified.

## Benchmarks (comparison only)

- TÜİK CPI releases: retrieve published tables with release metadata.
- ITO index releases: retrieve monthly reports and parse reproducibly.
- ENAG published series: capture monthly values with URL/time references.

## Independent price observations

- Retail/e-commerce grocery prices (where terms permit).
- Rent and property listing aggregates (document sampling and location filters).
- Utilities and fuel prices from public tariff/market datasets.
- Transportation fares and second-hand market listings.

## Required metadata for each extract

- retrieval timestamp
- source URL/API endpoint
- units/currency
- parsing or scraping version/hash
- legal/usage notes
