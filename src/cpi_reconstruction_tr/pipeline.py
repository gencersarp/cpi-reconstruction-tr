"""CLI entrypoints for reproducible incremental workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cpi_reconstruction_tr.analysis.comparison import compare_series
from cpi_reconstruction_tr.basket.weights import shares_to_base_quantities
from cpi_reconstruction_tr.data.sources import list_sources
from cpi_reconstruction_tr.indices.calculate import chained_index, fisher_index, laspeyres_index, paasche_index


def _read_json(path: str | Path) -> dict[str, float]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(k): float(v) for k, v in payload.items()}


def _cmd_list_sources(_: argparse.Namespace) -> None:
    for source in list_sources():
        print(f"{source.source_id}: {source.name} | role={source.methodology_role}")


def _cmd_compute_indices(args: argparse.Namespace) -> None:
    base_prices = _read_json(args.base_prices)
    current_prices = _read_json(args.current_prices)
    shares = _read_json(args.base_shares)

    base_quantities = shares_to_base_quantities(base_prices, shares)
    current_quantities = base_quantities if args.use_base_quantities_for_paasche else _read_json(args.current_quantities)

    results = {
        "laspeyres": laspeyres_index(base_prices, current_prices, base_quantities),
        "paasche": paasche_index(base_prices, current_prices, current_quantities),
        "fisher": fisher_index(base_prices, current_prices, base_quantities, current_quantities),
    }
    print(json.dumps(results, indent=2, sort_keys=True))


def _cmd_chain(args: argparse.Namespace) -> None:
    relatives = [float(value) for value in args.relatives]
    print(json.dumps(chained_index(relatives), indent=2))


def _cmd_compare(args: argparse.Namespace) -> None:
    independent = _read_json(args.independent_series)
    official = _read_json(args.official_series)
    print(json.dumps(compare_series(independent, official), indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CPI Reconstruction TR CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-sources", help="List configured data sources")
    list_parser.set_defaults(func=_cmd_list_sources)

    index_parser = subparsers.add_parser("compute-indices", help="Compute independent price indices")
    index_parser.add_argument("--base-prices", required=True)
    index_parser.add_argument("--current-prices", required=True)
    index_parser.add_argument("--base-shares", required=True)
    index_parser.add_argument("--current-quantities")
    index_parser.add_argument(
        "--use-base-quantities-for-paasche",
        action="store_true",
        help="If set, use base-implied quantities as a simplifying approximation.",
    )
    index_parser.set_defaults(func=_cmd_compute_indices)

    chain_parser = subparsers.add_parser("chain", help="Chain period relatives into index levels")
    chain_parser.add_argument("relatives", nargs="+")
    chain_parser.set_defaults(func=_cmd_chain)

    compare_parser = subparsers.add_parser("compare", help="Compare independent and official series")
    compare_parser.add_argument("--independent-series", required=True)
    compare_parser.add_argument("--official-series", required=True)
    compare_parser.set_defaults(func=_cmd_compare)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
