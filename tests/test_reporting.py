import unittest
from unittest.mock import patch
from cpi_reconstruction_tr.reporting.plots import plot_index_comparison

class TestReporting(unittest.TestCase):
    @patch('matplotlib.pyplot.show')
    def test_plot_index_comparison_no_output(self, mock_show) -> None:
        independent = {"2023-01": 100.0, "2023-02": 105.0}
        official = {"2023-01": 100.0, "2023-02": 103.0}
        # Should not raise any exception
        plot_index_comparison(independent, official)
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    def test_plot_index_comparison_with_output(self, mock_savefig) -> None:
        independent = {"2023-01": 100.0, "2023-02": 105.0}
        official = {"2023-01": 100.0, "2023-02": 103.0}
        plot_index_comparison(independent, official, output_path="test_plot.png")
        mock_savefig.assert_called_once_with("test_plot.png")

if __name__ == "__main__":
    unittest.main()
