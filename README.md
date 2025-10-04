# LEAN Tearsheet Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Professional performance tearsheet generator for [QuantConnect LEAN](https://github.com/QuantConnect/Lean) backtest results. Generate beautiful, interactive HTML reports or static PDF tearsheets with comprehensive performance metrics and benchmark comparisons.

## Features

- **Interactive HTML tearsheets** with Plotly charts
- **Static PDF tearsheets** for presentations and reports
- **Comprehensive metrics**: Sharpe, Sortino, Calmar, drawdown, win rate, and more
- **Benchmark comparison**: Compare your strategy against buy-and-hold benchmarks
- **Python API and CLI**: Use programmatically or via command line
- **Well-tested**: Comprehensive unit test coverage

## Installation

```bash
pip install lean-tearsheet-generator
```

For PDF generation support (optional):
```bash
pip install lean-tearsheet-generator[dev]
```

## Quick Start

### Command Line Interface

```bash
# Generate HTML tearsheet
lean-tearsheet /path/to/backtest -o tearsheet.html

# Generate PDF tearsheet
lean-tearsheet /path/to/backtest -o tearsheet.pdf --format pdf

# With benchmark comparison
lean-tearsheet /path/to/backtest -o tearsheet.html \
  --benchmark /path/to/btcusdt_trade.zip
```

### Python API

```python
from lean_tearsheet import TearsheetGenerator, HTMLTearsheet

# Initialize generator
generator = TearsheetGenerator('/path/to/backtest')

# Generate HTML tearsheet
html_tearsheet = HTMLTearsheet(generator)
html_tearsheet.generate('tearsheet.html')
```

## Examples

### Basic Usage

```python
from lean_tearsheet import TearsheetGenerator, HTMLTearsheet, PDFTearsheet

# Initialize generator
backtest_dir = '/path/to/your/backtest'
generator = TearsheetGenerator(backtest_dir)

# Generate interactive HTML
html_tearsheet = HTMLTearsheet(generator)
html_tearsheet.generate('my_strategy.html')

# Generate static PDF
pdf_tearsheet = PDFTearsheet(generator)
pdf_tearsheet.generate('my_strategy.pdf')
```

### With Benchmark Comparison

```python
from lean_tearsheet import TearsheetGenerator, HTMLTearsheet

# Initialize with benchmark data
generator = TearsheetGenerator(
    backtest_dir='/path/to/backtest',
    benchmark_data_path='/path/to/btcusdt_trade.zip'
)

# Generate tearsheet with benchmark comparison
html_tearsheet = HTMLTearsheet(generator)
html_tearsheet.generate('tearsheet_with_benchmark.html')
```

### Custom Metrics Analysis

```python
from lean_tearsheet import TearsheetGenerator

# Initialize generator
generator = TearsheetGenerator('/path/to/backtest')

# Get equity curve and returns
equity = generator.extract_equity_curve()
returns = generator.get_returns()

# Calculate comprehensive metrics
metrics = generator.calculate_metrics(returns)
print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {metrics['Max Drawdown'] * 100:.2f}%")

# Get drawdown series
drawdowns = generator.get_drawdown_series(returns)

# Get rolling Sharpe (30-day window)
rolling_sharpe = generator.get_rolling_sharpe(returns, window=30*24)
```

More examples in the [`examples/`](examples/) directory.

## Performance Metrics

The tearsheet includes the following metrics:

- **Returns**: Total return, annualized return
- **Risk**: Volatility (annualized)
- **Risk-adjusted**: Sharpe ratio, Sortino ratio, Calmar ratio
- **Drawdown**: Maximum drawdown
- **Trade statistics**: Win rate, total trades, winning/losing trades

## CLI Reference

```
usage: lean-tearsheet [-h] [-o OUTPUT] [-f {html,pdf}] [-b BENCHMARK] [-v]
                      backtest_dir

Generate professional tearsheets from QuantConnect LEAN backtest results

positional arguments:
  backtest_dir          Path to LEAN backtest directory containing JSON results

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filename (default: tearsheet.html)
  -f {html,pdf}, --format {html,pdf}
                        Output format (default: html)
  -b BENCHMARK, --benchmark BENCHMARK
                        Path to benchmark data file (e.g., btcusdt_trade.zip)
  -v, --version         show program's version number and exit
```

## Requirements

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.21.0
- plotly >= 5.0.0
- kaleido >= 0.2.1 (for PDF generation)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/guitrading/quantconnect-lean-tearsheet-generator.git
cd lean-tearsheet-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lean_tearsheet --cov-report=html

# Run specific test file
pytest tests/test_generator.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
lean-tearsheet-generator/
├── src/
│   └── lean_tearsheet/
│       ├── __init__.py       # Package initialization
│       ├── generator.py      # Core generator logic
│       ├── formats.py        # HTML and PDF implementations
│       └── cli.py            # Command-line interface
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── test_generator.py    # Generator tests
│   ├── test_formats.py      # Format tests
│   └── test_cli.py          # CLI tests
├── examples/
│   ├── basic_usage.py
│   ├── with_benchmark.py
│   ├── custom_metrics.py
│   └── cli_examples.sh
├── output/                   # Generated tearsheets
├── setup.py                  # Package setup
├── pyproject.toml           # Project configuration
├── LICENSE                  # MIT license
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for [QuantConnect LEAN](https://github.com/QuantConnect/Lean) algorithmic trading engine
- Powered by [Plotly](https://plotly.com/) for interactive visualizations
- Inspired by quantitative finance tearsheet tools like [pyfolio](https://github.com/quantopian/pyfolio)

## Related Projects

- [QuantConnect LEAN](https://github.com/QuantConnect/Lean) - Algorithmic trading engine
- [LEAN CLI](https://github.com/QuantConnect/lean-cli) - Local development CLI
- [Binance LEAN Data Downloader](https://github.com/guitrading/binance-lean-data-downloader) - Download Binance data in LEAN format

## Support

- [Documentation](https://github.com/guitrading/quantconnect-lean-tearsheet-generator#readme)
- [Issue Tracker](https://github.com/guitrading/quantconnect-lean-tearsheet-generator/issues)
- [Discussions](https://github.com/guitrading/quantconnect-lean-tearsheet-generator/discussions)

---

Made for the quantitative trading community
