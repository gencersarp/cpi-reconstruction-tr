import unittest

from cpi_reconstruction_tr.analysis.comparison import compare_series, sensitivity_to_weights


class TestAnalysis(unittest.TestCase):
    def test_compare_series(self) -> None:
        independent = {"2025-01": 150.0, "2025-02": 153.0}
        official = {"2025-01": 149.0, "2025-02": 152.0}
        result = compare_series(independent, official)
        self.assertEqual(result["n_periods"], 2.0)
        self.assertAlmostEqual(result["mae"], 1.0)

    def test_sensitivity(self) -> None:
        stats = sensitivity_to_weights(
            base_prices={"bread": 10.0, "milk": 20.0},
            current_prices={"bread": 11.0, "milk": 22.0},
            base_weights={"bread": 0.5, "milk": 0.5},
            n_runs=10,
        )
        self.assertGreaterEqual(stats["max"], stats["min"])


if __name__ == "__main__":
    unittest.main()
