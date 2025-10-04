"""Core tearsheet generator module."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


class TearsheetGenerator:
    """Generate performance tearsheets from LEAN backtest results."""

    def __init__(self, backtest_dir: str, benchmark_data_path: Optional[str] = None):
        """
        Initialize the tearsheet generator.

        Args:
            backtest_dir: Path to LEAN backtest directory containing JSON results
            benchmark_data_path: Optional path to benchmark data (e.g., BTCUSDT trade data)
        """
        self.backtest_dir = Path(backtest_dir)
        self.benchmark_data_path = Path(benchmark_data_path) if benchmark_data_path else None
        self._backtest_data = None
        self._equity_curve = None
        self._returns = None
        self._benchmark_returns = None

    def load_backtest(self) -> Dict[str, Any]:
        """Load LEAN backtest results from JSON file."""
        if self._backtest_data is not None:
            return self._backtest_data

        json_files = list(self.backtest_dir.glob('[0-9]*.json'))
        if not json_files:
            raise FileNotFoundError(
                f"No backtest results JSON found in {self.backtest_dir}"
            )

        with open(json_files[0], 'r') as f:
            self._backtest_data = json.load(f)

        return self._backtest_data

    def extract_equity_curve(self) -> pd.Series:
        """Extract equity curve from LEAN backtest."""
        if self._equity_curve is not None:
            return self._equity_curve

        backtest_data = self.load_backtest()
        equity_values = backtest_data['charts']['Strategy Equity']['series']['Equity']['values']

        df = pd.DataFrame(equity_values, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='s')

        self._equity_curve = pd.Series(df['close'].values, index=df['date'])
        return self._equity_curve

    def get_returns(self) -> pd.Series:
        """Calculate returns from equity curve."""
        if self._returns is not None:
            return self._returns

        equity = self.extract_equity_curve()
        self._returns = equity.pct_change().dropna()
        return self._returns

    def load_benchmark(self, start_date: str, end_date: str) -> Optional[pd.Series]:
        """
        Load benchmark data for comparison.

        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)

        Returns:
            Benchmark price series or None if not available
        """
        if self.benchmark_data_path is None or not self.benchmark_data_path.exists():
            return None

        import zipfile

        with zipfile.ZipFile(self.benchmark_data_path, 'r') as zip_file:
            csv_name = [f for f in zip_file.namelist() if f.endswith('.csv')][0]
            with zip_file.open(csv_name) as csv_file:
                df = pd.read_csv(
                    csv_file,
                    names=['datetime', 'open', 'high', 'low', 'close', 'volume'],
                    parse_dates=['datetime'],
                    date_format='%Y%m%d %H:%M'
                )

        df.set_index('datetime', inplace=True)
        start = pd.to_datetime(start_date).tz_localize(None)
        end = pd.to_datetime(end_date).tz_localize(None)
        df = df[(df.index >= start) & (df.index <= end)]

        return df['close']

    def get_benchmark_returns(self) -> Optional[pd.Series]:
        """Get benchmark returns aligned with strategy returns."""
        if self._benchmark_returns is not None:
            return self._benchmark_returns

        config = self.load_backtest().get('algorithmConfiguration', {})
        start_date = config.get('startDate', '')
        end_date = config.get('endDate', '')

        benchmark_prices = self.load_benchmark(start_date, end_date)
        if benchmark_prices is None:
            return None

        benchmark_returns = benchmark_prices.pct_change().dropna()
        returns = self.get_returns()

        # Align benchmark with strategy returns
        benchmark_returns = benchmark_returns.reindex(returns.index, method='ffill').dropna()
        self._benchmark_returns = benchmark_returns

        return self._benchmark_returns

    def calculate_metrics(self, returns: pd.Series) -> Dict[str, Any]:
        """
        Calculate comprehensive performance metrics.

        Args:
            returns: Series of returns

        Returns:
            Dictionary of performance metrics
        """
        # Basic returns
        total_return = (1 + returns).prod() - 1
        days = (returns.index[-1] - returns.index[0]).days
        ann_return = (1 + total_return) ** (365.25 / days) - 1

        # Volatility and Sharpe
        # Assume hourly data: 365.25 * 24 periods per year
        periods_per_year = 365.25 * 24
        volatility = returns.std() * np.sqrt(periods_per_year)
        sharpe = ann_return / volatility if volatility > 0 else 0

        # Drawdown
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.expanding().max()
        drawdown = (cum_returns - running_max) / running_max
        max_dd = drawdown.min()

        # Win rate
        wins = (returns > 0).sum()
        losses = (returns < 0).sum()
        win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0

        # Sortino (downside deviation)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(periods_per_year)
        sortino = ann_return / downside_std if downside_std > 0 else 0

        # Calmar (return / max drawdown)
        calmar = ann_return / abs(max_dd) if max_dd < 0 else 0

        return {
            'Total Return': total_return,
            'Annual Return': ann_return,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe,
            'Sortino Ratio': sortino,
            'Calmar Ratio': calmar,
            'Max Drawdown': max_dd,
            'Win Rate': win_rate,
            'Total Trades': wins + losses,
            'Winning Trades': wins,
            'Losing Trades': losses,
        }

    def get_drawdown_series(self, returns: pd.Series) -> pd.Series:
        """Calculate drawdown series from returns."""
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.expanding().max()
        return (cum_returns - running_max) / running_max

    def get_rolling_sharpe(
        self, returns: pd.Series, window: int = 30 * 24
    ) -> pd.Series:
        """
        Calculate rolling Sharpe ratio.

        Args:
            returns: Returns series
            window: Rolling window in periods (default 30 days * 24 hours)

        Returns:
            Rolling Sharpe ratio series
        """
        periods_per_year = 365.25 * 24
        rolling_mean = returns.rolling(window).mean()
        rolling_std = returns.rolling(window).std()

        return (rolling_mean / rolling_std) * np.sqrt(periods_per_year)

    def get_config(self) -> Dict[str, Any]:
        """Get algorithm configuration from backtest."""
        return self.load_backtest().get('algorithmConfiguration', {})
