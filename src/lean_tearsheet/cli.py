"""Command-line interface for lean-tearsheet-generator."""

import argparse
import sys
from pathlib import Path

from .generator import TearsheetGenerator
from .formats import HTMLTearsheet, PDFTearsheet


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate professional tearsheets from QuantConnect LEAN backtest results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate HTML tearsheet
  lean-tearsheet /path/to/backtest -o tearsheet.html

  # Generate PDF tearsheet
  lean-tearsheet /path/to/backtest -o tearsheet.pdf --format pdf

  # Include benchmark comparison
  lean-tearsheet /path/to/backtest -o tearsheet.html \\
    --benchmark /path/to/btcusdt_trade.zip
        """
    )

    parser.add_argument(
        'backtest_dir',
        type=str,
        help='Path to LEAN backtest directory containing JSON results'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='tearsheet.html',
        help='Output filename (default: tearsheet.html)'
    )

    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['html', 'pdf'],
        default='html',
        help='Output format (default: html)'
    )

    parser.add_argument(
        '-b', '--benchmark',
        type=str,
        help='Path to benchmark data file (e.g., btcusdt_trade.zip)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )

    args = parser.parse_args()

    # Validate backtest directory
    backtest_path = Path(args.backtest_dir)
    if not backtest_path.exists():
        print(f"Error: Backtest directory not found: {args.backtest_dir}", file=sys.stderr)
        sys.exit(1)

    if not backtest_path.is_dir():
        print(f"Error: Not a directory: {args.backtest_dir}", file=sys.stderr)
        sys.exit(1)

    # Validate benchmark if provided
    if args.benchmark:
        benchmark_path = Path(args.benchmark)
        if not benchmark_path.exists():
            print(f"Error: Benchmark file not found: {args.benchmark}", file=sys.stderr)
            sys.exit(1)

    # Auto-detect format from output filename if not explicitly set
    if args.format == 'html' and args.output.endswith('.pdf'):
        args.format = 'pdf'
    elif args.format == 'pdf' and args.output.endswith('.html'):
        args.format = 'html'

    try:
        # Initialize generator
        print(f"Loading backtest from {args.backtest_dir}...")
        generator = TearsheetGenerator(args.backtest_dir, args.benchmark)

        # Generate tearsheet
        if args.format == 'html':
            html_gen = HTMLTearsheet(generator)
            html_gen.generate(args.output)
        else:
            pdf_gen = PDFTearsheet(generator)
            pdf_gen.generate(args.output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
