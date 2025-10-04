# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-04

### Added
- Initial release of LEAN Tearsheet Generator
- Core `TearsheetGenerator` class for loading and processing LEAN backtest results
- Interactive HTML tearsheet generation with Plotly
- Static PDF tearsheet generation
- Command-line interface (CLI)
- Benchmark comparison support
- Comprehensive performance metrics:
  - Total return and annualized return
  - Volatility (annualized)
  - Sharpe ratio, Sortino ratio, Calmar ratio
  - Maximum drawdown
  - Win rate and trade statistics
- Rolling metrics support (e.g., rolling Sharpe ratio)
- Python API for programmatic usage
- Unit tests with pytest
- Example scripts and documentation
- MIT license

### Features
- Load LEAN backtest JSON results
- Extract equity curves and returns
- Calculate comprehensive performance metrics
- Generate interactive HTML reports with:
  - Performance metrics tables
  - Equity curve comparison charts
  - Drawdown comparison charts
  - Rolling Sharpe ratio charts
- Generate static PDF reports
- Compare strategy against benchmark data
- CLI with flexible options

[0.1.0]: https://github.com/guitrading/quantconnect-lean-tearsheet-generator/releases/tag/v0.1.0
