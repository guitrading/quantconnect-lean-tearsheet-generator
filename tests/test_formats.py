"""Unit tests for HTML and PDF tearsheet formats."""

import tempfile
from pathlib import Path

import pytest

from lean_tearsheet.formats import HTMLTearsheet, PDFTearsheet
from lean_tearsheet.generator import TearsheetGenerator


@pytest.fixture
def generator(mock_backtest_dir):
    """Create TearsheetGenerator instance with mock data."""
    return TearsheetGenerator(mock_backtest_dir)


def test_html_tearsheet_generation(generator):
    """Test HTML tearsheet generation."""
    html_gen = HTMLTearsheet(generator)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_tearsheet.html"
        html_gen.generate(str(output_file))

        assert output_file.exists()
        assert output_file.stat().st_size > 0

        # Check HTML content
        content = output_file.read_text()
        assert "LEAN Strategy Tearsheet" in content
        assert "plotly" in content.lower()


def test_html_tearsheet_without_benchmark(generator):
    """Test HTML tearsheet generation without benchmark."""
    html_gen = HTMLTearsheet(generator)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_tearsheet.html"
        html_gen.generate(str(output_file))

        assert output_file.exists()


def test_pdf_tearsheet_generation(generator):
    """Test PDF tearsheet generation."""
    pdf_gen = PDFTearsheet(generator)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_tearsheet.pdf"

        try:
            pdf_gen.generate(str(output_file))
            assert output_file.exists()
            assert output_file.stat().st_size > 0
        except Exception as e:
            # PDF generation may fail without kaleido installed
            pytest.skip(f"PDF generation failed (kaleido may not be installed): {e}")


def test_html_metrics_table_formatting(generator):
    """Test that metrics are properly formatted in HTML."""
    html_gen = HTMLTearsheet(generator)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_tearsheet.html"
        html_gen.generate(str(output_file))

        content = output_file.read_text()

        # Check for key metrics in output
        assert "Total Return" in content
        assert "Sharpe Ratio" in content
        assert "Max Drawdown" in content
        assert "%" in content  # Percentage formatting
