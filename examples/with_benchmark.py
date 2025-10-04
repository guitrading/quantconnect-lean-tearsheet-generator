"""Example with benchmark comparison."""

from lean_tearsheet import TearsheetGenerator, HTMLTearsheet

# Initialize generator with benchmark data
backtest_dir = '/path/to/your/backtest'
benchmark_path = '/path/to/data/crypto/binance/hour/btcusdt_trade.zip'

generator = TearsheetGenerator(backtest_dir, benchmark_data_path=benchmark_path)

# Generate tearsheet with benchmark comparison
html_tearsheet = HTMLTearsheet(generator)
html_tearsheet.generate('tearsheet_with_benchmark.html')

print("Tearsheet generated with BTCUSDT benchmark comparison!")
