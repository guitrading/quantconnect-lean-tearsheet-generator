"""Unit tests for CLI interface."""

import sys

import pytest

from lean_tearsheet.cli import main


def test_cli_help(capsys):
    """Test CLI help message."""
    sys.argv = ["lean-tearsheet", "--help"]

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Generate professional tearsheets" in captured.out


def test_cli_version(capsys):
    """Test CLI version output."""
    sys.argv = ["lean-tearsheet", "--version"]

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "0.1.0" in captured.out or "0.1.0" in captured.err


def test_cli_missing_backtest_dir(capsys):
    """Test CLI with missing backtest directory."""
    sys.argv = ["lean-tearsheet", "/nonexistent/path"]

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_cli_html_generation(mock_backtest_dir, tmp_path):
    """Test HTML generation via CLI."""
    output_file = tmp_path / "test_output.html"

    sys.argv = [
        "lean-tearsheet",
        str(mock_backtest_dir),
        "-o",
        str(output_file),
    ]
    main()

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_cli_format_auto_detection(mock_backtest_dir, tmp_path):
    """Test automatic format detection from filename."""
    output_file = tmp_path / "test_output.html"

    sys.argv = [
        "lean-tearsheet",
        str(mock_backtest_dir),
        "-o",
        str(output_file),
    ]
    main()

    assert output_file.exists()
    content = output_file.read_text()
    assert "plotly" in content.lower()
