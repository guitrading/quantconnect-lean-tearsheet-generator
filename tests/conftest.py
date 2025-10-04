"""Shared pytest fixtures for all tests."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pytest


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
