"""Unit tests for TearsheetGenerator."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from lean_tearsheet.generator import TearsheetGenerator


@pytest.fixture
def mock_backtest_data():
    """Create mock LEAN backtest data."""
    start_date = datetime(2024, 1, 1)
    hours = 24 * 365  # One year of hourly data

    timestamps = [
        int((start_date + timedelta(hours=i)).timestamp())
        for i in range(hours)
    ]

    # Create realistic equity curve with some volatility and trend
    initial_equity = 100000
    returns = np.random.normal(0.0001, 0.01, hours)  # Small positive drift
    equity_values = [initial_equity]

    for ret in returns[1:]:
        equity_values.append(equity_values[-1] * (1 + ret))

    # Format as LEAN output (timestamp, open, high, low, close)
    equity_series = []
    for i, (ts, equity) in enumerate(zip(timestamps, equity_values)):
        equity_series.append(
            [ts, equity, equity * 1.001, equity * 0.999, equity]
        )

    return {
        "charts": {
            "Strategy Equity": {
                "series": {"Equity": {"values": equity_series}}
            }
        },
        "algorithmConfiguration": {
            "startDate": "2024-01-01T00:00:00",
            "endDate": "2024-12-31T23:00:00",
        },
    }


@pytest.fixture
def mock_backtest_dir(mock_backtest_data):
    """Create temporary directory with mock backtest JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / "123456789.json"
        with open(json_path, "w") as f:
            json.dump(mock_backtest_data, f)
        yield tmpdir


def test_generator_initialization():
    """Test TearsheetGenerator initialization."""
    gen = TearsheetGenerator("/fake/path")
    assert gen.backtest_dir == Path("/fake/path")
    assert gen.benchmark_data_path is None


def test_load_backtest(mock_backtest_dir):
    """Test loading backtest data."""
    gen = TearsheetGenerator(mock_backtest_dir)
    data = gen.load_backtest()

    assert "charts" in data
    assert "Strategy Equity" in data["charts"]
    assert "algorithmConfiguration" in data


def test_extract_equity_curve(mock_backtest_dir):
    """Test extracting equity curve."""
    gen = TearsheetGenerator(mock_backtest_dir)
    equity = gen.extract_equity_curve()

    assert isinstance(equity, pd.Series)
    assert len(equity) > 0
    assert equity.index.dtype == "datetime64[ns]"


def test_get_returns(mock_backtest_dir):
    """Test calculating returns."""
    gen = TearsheetGenerator(mock_backtest_dir)
    returns = gen.get_returns()

    assert isinstance(returns, pd.Series)
    assert len(returns) > 0
    # First return should be dropped (NaN from pct_change)
    assert len(returns) == len(gen.extract_equity_curve()) - 1


def test_calculate_metrics(mock_backtest_dir):
    """Test performance metrics calculation."""
    gen = TearsheetGenerator(mock_backtest_dir)
    returns = gen.get_returns()
    metrics = gen.calculate_metrics(returns)

    # Check all expected metrics exist
    expected_keys = [
        "Total Return",
        "Annual Return",
        "Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
        "Calmar Ratio",
        "Max Drawdown",
        "Win Rate",
        "Total Trades",
        "Winning Trades",
        "Losing Trades",
    ]

    for key in expected_keys:
        assert key in metrics

    # Check metric types and reasonable ranges
    assert isinstance(metrics["Total Return"], float)
    assert isinstance(metrics["Sharpe Ratio"], float)
    assert 0 <= metrics["Win Rate"] <= 1
    assert metrics["Max Drawdown"] <= 0


def test_get_drawdown_series(mock_backtest_dir):
    """Test drawdown calculation."""
    gen = TearsheetGenerator(mock_backtest_dir)
    returns = gen.get_returns()
    drawdown = gen.get_drawdown_series(returns)

    assert isinstance(drawdown, pd.Series)
    assert len(drawdown) == len(returns)
    # Drawdowns should be <= 0
    assert (drawdown <= 0).all()


def test_get_rolling_sharpe(mock_backtest_dir):
    """Test rolling Sharpe calculation."""
    gen = TearsheetGenerator(mock_backtest_dir)
    returns = gen.get_returns()
    rolling_sharpe = gen.get_rolling_sharpe(returns, window=100)

    assert isinstance(rolling_sharpe, pd.Series)
    # First window-1 values will be NaN
    assert rolling_sharpe.notna().sum() > 0


def test_backtest_not_found():
    """Test error handling for missing backtest directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = TearsheetGenerator(tmpdir)
        with pytest.raises(
            FileNotFoundError, match="No backtest results JSON found"
        ):
            gen.load_backtest()


def test_get_config(mock_backtest_dir):
    """Test getting algorithm configuration."""
    gen = TearsheetGenerator(mock_backtest_dir)
    config = gen.get_config()

    assert "startDate" in config
    assert "endDate" in config
    assert config["startDate"] == "2024-01-01T00:00:00"
