#!/bin/bash
# CLI usage examples for lean-tearsheet-generator

# Basic HTML tearsheet generation
lean-tearsheet /path/to/backtest -o tearsheet.html

# PDF tearsheet generation
lean-tearsheet /path/to/backtest -o tearsheet.pdf --format pdf

# With benchmark comparison
lean-tearsheet /path/to/backtest \
  -o tearsheet_with_benchmark.html \
  --benchmark /path/to/data/crypto/binance/hour/btcusdt_trade.zip

# Explicit format specification
lean-tearsheet /path/to/backtest \
  --output my_report.html \
  --format html

# Get help
lean-tearsheet --help

# Get version
lean-tearsheet --version
