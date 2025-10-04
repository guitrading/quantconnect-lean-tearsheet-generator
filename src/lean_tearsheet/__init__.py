"""
LEAN Tearsheet Generator

A Python package for generating professional performance tearsheets from QuantConnect LEAN backtest results.
Supports both HTML (interactive) and PDF (static) output formats.
"""

__version__ = "0.1.0"

from .generator import TearsheetGenerator
from .formats import HTMLTearsheet, PDFTearsheet

__all__ = ['TearsheetGenerator', 'HTMLTearsheet', 'PDFTearsheet']
