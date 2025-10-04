"""Example showing how to access custom metrics."""

from lean_tearsheet import TearsheetGenerator

# Initialize generator
backtest_dir = '/path/to/your/backtest'
generator = TearsheetGenerator(backtest_dir)

# Load backtest data
backtest_data = generator.load_backtest()
print(f"Algorithm: {backtest_data.get('algorithmConfiguration', {})}")

# Get equity curve and returns
equity = generator.extract_equity_curve()
returns = generator.get_returns()

print(f"\nEquity curve: {len(equity)} data points")
print(f"Returns: {len(returns)} data points")

# Calculate comprehensive metrics
metrics = generator.calculate_metrics(returns)

print("\n=== Performance Metrics ===")
for key, value in metrics.items():
    if isinstance(value, float):
        if 'Rate' in key or 'Return' in key:
            print(f"{key}: {value * 100:.2f}%")
        else:
            print(f"{key}: {value:.4f}")
    else:
        print(f"{key}: {value}")

# Get drawdown series
drawdowns = generator.get_drawdown_series(returns)
print(f"\nMax drawdown occurred on: {drawdowns.idxmin()}")

# Get rolling Sharpe
rolling_sharpe = generator.get_rolling_sharpe(returns, window=30*24)  # 30 days
print(f"Average 30-day rolling Sharpe: {rolling_sharpe.mean():.2f}")
