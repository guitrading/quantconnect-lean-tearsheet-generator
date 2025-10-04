"""Basic usage example for lean-tearsheet-generator."""

from lean_tearsheet import TearsheetGenerator, HTMLTearsheet, PDFTearsheet

# Initialize generator with backtest directory
backtest_dir = '/path/to/your/backtest'
generator = TearsheetGenerator(backtest_dir)

# Generate HTML tearsheet (interactive)
html_tearsheet = HTMLTearsheet(generator)
html_tearsheet.generate('my_tearsheet.html')

# Generate PDF tearsheet (static)
pdf_tearsheet = PDFTearsheet(generator)
pdf_tearsheet.generate('my_tearsheet.pdf')
