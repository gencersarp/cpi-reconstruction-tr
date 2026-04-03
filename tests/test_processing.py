import unittest

from cpi_reconstruction_tr.processing.normalize import normalize_price_records


class TestProcessing(unittest.TestCase):
    def test_normalization_and_fx(self) -> None:
        rows = [
            {
                "date": "2025-01-15",
                "item_id": "A",
                "category": "Food",
                "source": "market",
                "price": "10",
                "currency": "USD",
                "unit": "kg",
            }
        ]

        normalized = normalize_price_records(rows, fx_rates={("USD", "TRY"): 30.0})
        self.assertEqual(normalized[0]["date"], "2025-01-15")
        self.assertEqual(normalized[0]["currency"], "TRY")
        self.assertEqual(normalized[0]["price"], 300.0)


if __name__ == "__main__":
    unittest.main()
