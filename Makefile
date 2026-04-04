.PHONY: install test plot clean

install:
	pip install -e .

test:
	export PYTHONPATH=src:$$PYTHONPATH && python3 -m unittest discover -s tests

plot:
	export PYTHONPATH=src:$$PYTHONPATH && python3 -m cpi_reconstruction_tr.pipeline plot \
		--independent-series data/raw/independent_series.json \
		--official-series data/raw/official_series.json \
		--output sample_comparison.png

clean:
	rm -rf `find . -name __pycache__`
	rm -f sample_comparison.png test_plot.png
