# Quick Start Guide

Get up and running with LEAN Tearsheet Generator in 5 minutes.

## Installation

```bash
# Install from PyPI (when published)
pip install lean-tearsheet-generator

# OR install from source (for development)
cd lean-tearsheet-generator
pip install -e .

# OR install with all dev dependencies
pip install -e ".[dev]"
```

## Basic Usage

### 1. Command Line (Easiest)

```bash
# Generate HTML tearsheet
lean-tearsheet /path/to/your/backtest -o my_tearsheet.html

# Generate PDF tearsheet
lean-tearsheet /path/to/your/backtest -o my_tearsheet.pdf --format pdf

# With benchmark comparison
lean-tearsheet /path/to/backtest -o tearsheet.html \
  --benchmark /path/to/btcusdt_trade.zip
```

### 2. Python Script

Create a file `generate_my_tearsheet.py`:

```python
from lean_tearsheet import TearsheetGenerator, HTMLTearsheet

# Point to your LEAN backtest directory
backtest_dir = '/home/gui/qc/v2-opt/backtests/2025-10-04_09-22-50'

# Initialize generator
generator = TearsheetGenerator(backtest_dir)

# Generate tearsheet
html = HTMLTearsheet(generator)
html.generate('my_strategy_tearsheet.html')

print("Done! Open my_strategy_tearsheet.html in your browser")
```

Run it:
```bash
python generate_my_tearsheet.py
```

### 3. With Benchmark

```python
from lean_tearsheet import TearsheetGenerator, HTMLTearsheet

# Initialize with benchmark
generator = TearsheetGenerator(
    backtest_dir='/path/to/backtest',
    benchmark_data_path='/path/to/data/crypto/binance/hour/btcusdt_trade.zip'
)

# Generate
html = HTMLTearsheet(generator)
html.generate('tearsheet_vs_btc.html')
```

## What You Get

Your tearsheet includes:

- **Performance Metrics**: Returns, Sharpe, Sortino, Calmar ratios
- **Equity Curve**: Interactive chart showing strategy performance
- **Drawdown Chart**: Visualize peak-to-trough declines
- **Rolling Sharpe**: See risk-adjusted performance over time
- **Benchmark Comparison**: Compare against buy-and-hold (if provided)

## Directory Structure

```
lean-tearsheet-generator/
├── src/lean_tearsheet/     # Package source code
├── tests/                  # Unit tests
├── examples/               # Usage examples
├── output/                 # Generated tearsheets go here
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
└── setup.py               # Package configuration
```

## Development Setup

```bash
# Clone repository
git clone https://github.com/guitrading/quantconnect-lean-tearsheet-generator.git
cd lean-tearsheet-generator

# Install with dev dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

## Common Issues

### "No backtest results JSON found"
- Make sure you're pointing to a LEAN backtest directory
- The directory should contain a timestamped JSON file (e.g., `123456789.json`)

### "ModuleNotFoundError: No module named 'lean_tearsheet'"
- Make sure you installed the package: `pip install -e .`
- Activate your virtual environment if using one

### PDF generation fails
- Install kaleido: `pip install kaleido`
- Or use HTML format instead: `--format html`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for more usage patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Need Help?

- [Full Documentation](README.md)
- [Report Issues](https://github.com/guitrading/quantconnect-lean-tearsheet-generator/issues)
- [Discussions](https://github.com/guitrading/quantconnect-lean-tearsheet-generator/discussions)

---

Happy backtesting!
