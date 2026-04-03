"""Data source registry and metadata for inflation reconstruction."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DataSource:
    """Declarative metadata for a data source."""

    source_id: str
    name: str
    methodology_role: str
    access_method: str
    reproducibility_notes: str


SOURCE_REGISTRY = [
    DataSource(
        source_id="tuik_cpi",
        name="TÜİK Official CPI",
        methodology_role="Benchmark comparison only",
        access_method="Download from official publication calendar or API if available",
        reproducibility_notes="Store release date, table identifier, and retrieval hash.",
    ),
    DataSource(
        source_id="ito_istanbul",
        name="ITO Istanbul Cost of Living Index",
        methodology_role="Alternative institutional benchmark",
        access_method="Download monthly reports/tables from ITO",
        reproducibility_notes="Version files by release month and document parsing assumptions.",
    ),
    DataSource(
        source_id="enag",
        name="ENAG Inflation Series",
        methodology_role="Alternative benchmark for triangulation",
        access_method="Collect published monthly values from ENAG releases",
        reproducibility_notes="Keep citation URL and retrieval timestamp.",
    ),
    DataSource(
        source_id="retail_prices",
        name="Retail and marketplace price observations",
        methodology_role="Independent bottom-up index construction",
        access_method="Scraping/public APIs/manual collection under legal terms",
        reproducibility_notes="Persist raw snapshots and extraction scripts with deterministic configs.",
    ),
    DataSource(
        source_id="proxy_series",
        name="Energy, FX, transport, second-hand market indicators",
        methodology_role="Proxy-based inflation nowcasting and stress testing",
        access_method="Public APIs, market data providers, downloadable CSV files",
        reproducibility_notes="Track data license, endpoint version, and units.",
    ),
]


def list_sources() -> list[DataSource]:
    """Return all configured data sources."""

    return SOURCE_REGISTRY.copy()
