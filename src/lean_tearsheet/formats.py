"""Tearsheet format implementations (HTML and PDF)."""

from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .generator import TearsheetGenerator


class HTMLTearsheet:
    """Generate interactive HTML tearsheet using Plotly."""

    def __init__(self, generator: TearsheetGenerator):
        """
        Initialize HTML tearsheet generator.

        Args:
            generator: TearsheetGenerator instance with loaded backtest data
        """
        self.generator = generator

    def generate(self, output_file: str = "tearsheet.html") -> None:
        """
        Generate HTML tearsheet.

        Args:
            output_file: Output filename for HTML tearsheet
        """
        returns = self.generator.get_returns()
        equity = self.generator.extract_equity_curve()
        benchmark_returns = self.generator.get_benchmark_returns()

        # Calculate metrics
        strat_metrics = self.generator.calculate_metrics(returns)
        bench_metrics = (
            self.generator.calculate_metrics(benchmark_returns)
            if benchmark_returns is not None
            else {}
        )

        # Get config
        config = self.generator.get_config()
        start_date = config.get("startDate", "Unknown")
        end_date = config.get("endDate", "Unknown")

        # Create figure
        fig = self._create_figure(
            equity,
            returns,
            strat_metrics,
            benchmark_returns,
            bench_metrics,
            start_date,
            end_date,
        )

        # Save
        fig.write_html(output_file)

        print(f"HTML tearsheet generated: {output_file}")
        print(f"  Size: {Path(output_file).stat().st_size / 1024:.0f} KB")
        print(f"  Open in browser: file://{Path(output_file).absolute()}")

    def _create_figure(
        self,
        equity,
        returns,
        strat_metrics,
        benchmark_returns,
        bench_metrics,
        start_date,
        end_date,
    ):
        """Create plotly figure with all charts."""

        # Create subplots
        fig = make_subplots(
            rows=4,
            cols=2,
            subplot_titles=(
                "Strategy Performance",
                "Benchmark Performance",
                None,
                None,
                None,
                None,
                None,
                None,
            ),
            specs=[
                [{"type": "table"}, {"type": "table"}],
                [{"colspan": 2}, None],
                [{"colspan": 2}, None],
                [{"colspan": 2}, None],
            ],
            row_heights=[0.20, 0.27, 0.27, 0.27],
            vertical_spacing=0.10,
        )

        # Add metrics tables
        self._add_metrics_tables(fig, strat_metrics, bench_metrics)

        # Add equity curves
        self._add_equity_curves(fig, equity, returns, benchmark_returns)

        # Add drawdowns
        self._add_drawdowns(fig, returns, benchmark_returns)

        # Add rolling Sharpe
        self._add_rolling_sharpe(fig, returns, benchmark_returns)

        # Update layout
        self._update_layout(fig, start_date, end_date)

        return fig

    def _add_metrics_tables(self, fig, strat_metrics, bench_metrics):
        """Add performance metrics tables."""
        # Format strategy metrics for display
        strat_display = {
            "Total Return": f"{strat_metrics['Total Return'] * 100:.2f}%",
            "Annual Return": f"{strat_metrics['Annual Return'] * 100:.2f}%",
            "Volatility": f"{strat_metrics['Volatility'] * 100:.2f}%",
            "Sharpe Ratio": f"{strat_metrics['Sharpe Ratio']:.2f}",
            "Sortino Ratio": f"{strat_metrics['Sortino Ratio']:.2f}",
            "Calmar Ratio": f"{strat_metrics['Calmar Ratio']:.2f}",
            "Max Drawdown": f"{strat_metrics['Max Drawdown'] * 100:.2f}%",
            "Win Rate": f"{strat_metrics['Win Rate'] * 100:.1f}%",
            "Total Trades": f"{strat_metrics['Total Trades']:.0f}",
        }

        strat_table = go.Table(
            header=dict(
                values=["Metric", "Value"],
                fill_color="paleturquoise",
                align="left",
            ),
            cells=dict(
                values=[
                    list(strat_display.keys()),
                    list(strat_display.values()),
                ],
                fill_color="lavender",
                align="left",
            ),
        )
        fig.add_trace(strat_table, row=1, col=1)

        if bench_metrics:
            bench_display = {
                "Total Return": f"{bench_metrics['Total Return'] * 100:.2f}%",
                "Annual Return": (
                    f"{bench_metrics['Annual Return'] * 100:.2f}%"
                ),
                "Volatility": f"{bench_metrics['Volatility'] * 100:.2f}%",
                "Sharpe Ratio": f"{bench_metrics['Sharpe Ratio']:.2f}",
                "Sortino Ratio": f"{bench_metrics['Sortino Ratio']:.2f}",
                "Calmar Ratio": f"{bench_metrics['Calmar Ratio']:.2f}",
                "Max Drawdown": f"{bench_metrics['Max Drawdown'] * 100:.2f}%",
                "Win Rate": f"{bench_metrics['Win Rate'] * 100:.1f}%",
                "Total Trades": f"{bench_metrics['Total Trades']:.0f}",
            }

            bench_table = go.Table(
                header=dict(
                    values=["Metric", "Value"],
                    fill_color="lightblue",
                    align="left",
                ),
                cells=dict(
                    values=[
                        list(bench_display.keys()),
                        list(bench_display.values()),
                    ],
                    fill_color="aliceblue",
                    align="left",
                ),
            )
            fig.add_trace(bench_table, row=1, col=2)

    def _add_equity_curves(self, fig, equity, returns, benchmark_returns):
        """Add equity curve comparison."""
        # Normalize to 100
        equity_norm = equity / equity.iloc[0] * 100
        fig.add_trace(
            go.Scatter(
                x=equity.index,
                y=equity_norm,
                name="Strategy",
                line=dict(color="blue", width=2),
                legendgroup="equity",
                legendgrouptitle_text="Cumulative Returns",
            ),
            row=2,
            col=1,
        )

        if benchmark_returns is not None:
            bench_equity = (1 + benchmark_returns).cumprod() * equity.iloc[0]
            bench_equity_norm = bench_equity / bench_equity.iloc[0] * 100
            fig.add_trace(
                go.Scatter(
                    x=bench_equity.index,
                    y=bench_equity_norm,
                    name="Benchmark",
                    line=dict(color="orange", width=2),
                    legendgroup="equity",
                ),
                row=2,
                col=1,
            )

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Value ($100 start)", row=2, col=1)

    def _add_drawdowns(self, fig, returns, benchmark_returns):
        """Add drawdown comparison."""
        strat_dd = self.generator.get_drawdown_series(returns)
        fig.add_trace(
            go.Scatter(
                x=strat_dd.index,
                y=strat_dd * 100,
                name="Strategy DD",
                fill="tozeroy",
                line=dict(color="red"),
                legendgroup="drawdown",
                legendgrouptitle_text="Drawdown",
            ),
            row=3,
            col=1,
        )

        if benchmark_returns is not None:
            bench_dd = self.generator.get_drawdown_series(benchmark_returns)
            fig.add_trace(
                go.Scatter(
                    x=bench_dd.index,
                    y=bench_dd * 100,
                    name="Benchmark DD",
                    fill="tozeroy",
                    line=dict(color="blue", width=1),
                    opacity=0.3,
                    legendgroup="drawdown",
                ),
                row=3,
                col=1,
            )

        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=3, col=1)

    def _add_rolling_sharpe(self, fig, returns, benchmark_returns):
        """Add rolling Sharpe ratio comparison."""
        rolling_sharpe = self.generator.get_rolling_sharpe(returns)
        avg_sharpe = rolling_sharpe.mean()

        fig.add_trace(
            go.Scatter(
                x=rolling_sharpe.index,
                y=rolling_sharpe,
                name="Strategy",
                line=dict(color="blue", width=2),
                legendgroup="sharpe",
                legendgrouptitle_text="Rolling Sharpe",
            ),
            row=4,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=rolling_sharpe.index,
                y=[avg_sharpe] * len(rolling_sharpe),
                name=f"Strat Avg ({avg_sharpe:.2f})",
                line=dict(color="blue", dash="dash"),
                legendgroup="sharpe",
            ),
            row=4,
            col=1,
        )

        if benchmark_returns is not None:
            bench_rolling_sharpe = self.generator.get_rolling_sharpe(
                benchmark_returns
            )
            bench_avg_sharpe = bench_rolling_sharpe.mean()

            fig.add_trace(
                go.Scatter(
                    x=bench_rolling_sharpe.index,
                    y=bench_rolling_sharpe,
                    name="Benchmark",
                    line=dict(color="orange", width=2),
                    legendgroup="sharpe",
                ),
                row=4,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=bench_rolling_sharpe.index,
                    y=[bench_avg_sharpe] * len(bench_rolling_sharpe),
                    name=f"Bench Avg ({bench_avg_sharpe:.2f})",
                    line=dict(color="orange", dash="dash"),
                    legendgroup="sharpe",
                ),
                row=4,
                col=1,
            )

        fig.update_xaxes(title_text="Date", row=4, col=1)
        fig.update_yaxes(title_text="Sharpe Ratio", row=4, col=1)

    def _update_layout(self, fig, start_date, end_date):
        """Update figure layout with titles and legend."""
        fig.update_layout(
            title_text=(
                f"LEAN Strategy Tearsheet "
                f"({start_date[:10]} to {end_date[:10]})"
            ),
            height=1400,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="lightgray",
                borderwidth=1,
                tracegroupgap=30,
                groupclick="toggleitem",
            ),
        )

        # Add subplot titles as annotations
        fig.add_annotation(
            text="Cumulative Returns Comparison",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.765,
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=14),
        )
        fig.add_annotation(
            text="Drawdown Comparison",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.495,
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=14),
        )
        fig.add_annotation(
            text="Rolling 30-Day Sharpe Ratio",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.225,
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=14),
        )


class PDFTearsheet:
    """Generate static PDF tearsheet using Plotly + Kaleido."""

    def __init__(self, generator: TearsheetGenerator):
        """
        Initialize PDF tearsheet generator.

        Args:
            generator: TearsheetGenerator instance with loaded backtest data
        """
        self.generator = generator

    def generate(self, output_file: str = "tearsheet.pdf") -> None:
        """
        Generate PDF tearsheet.

        Args:
            output_file: Output filename for PDF tearsheet
        """
        # Create HTML tearsheet first
        html_generator = HTMLTearsheet(self.generator)
        returns = self.generator.get_returns()
        equity = self.generator.extract_equity_curve()
        benchmark_returns = self.generator.get_benchmark_returns()

        strat_metrics = self.generator.calculate_metrics(returns)
        bench_metrics = (
            self.generator.calculate_metrics(benchmark_returns)
            if benchmark_returns is not None
            else {}
        )

        config = self.generator.get_config()
        start_date = config.get("startDate", "Unknown")
        end_date = config.get("endDate", "Unknown")

        fig = html_generator._create_figure(
            equity,
            returns,
            strat_metrics,
            benchmark_returns,
            bench_metrics,
            start_date,
            end_date,
        )

        # Export to PDF
        fig.write_image(output_file, width=1200, height=1400)

        print(f"PDF tearsheet generated: {output_file}")
        print(f"  Size: {Path(output_file).stat().st_size / 1024:.0f} KB")
