import math
import unittest

from cpi_reconstruction_tr.indices.calculate import chained_index, fisher_index, laspeyres_index, paasche_index


class TestIndices(unittest.TestCase):
    def test_laspeyres_and_paasche(self) -> None:
        base_prices = {"bread": 10.0, "milk": 20.0}
        current_prices = {"bread": 12.0, "milk": 24.0}
        q0 = {"bread": 2.0, "milk": 1.0}
        qt = {"bread": 2.0, "milk": 1.0}

        self.assertAlmostEqual(laspeyres_index(base_prices, current_prices, q0), 120.0)
        self.assertAlmostEqual(paasche_index(base_prices, current_prices, qt), 120.0)
        self.assertAlmostEqual(fisher_index(base_prices, current_prices, q0, qt), 120.0)

    def test_chained_index(self) -> None:
        result = chained_index([1.10, 1.05], base_value=100.0)
        self.assertEqual(len(result), 3)
        self.assertTrue(math.isclose(result[-1], 115.5, rel_tol=1e-9))


if __name__ == "__main__":
    unittest.main()
