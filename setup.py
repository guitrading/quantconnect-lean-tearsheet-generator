"""Setup configuration for lean-tearsheet-generator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="lean-tearsheet-generator",
    version="0.1.0",
    author="Gui",
    author_email="contact@guitrading.com",
    description="Professional performance tearsheet generator for QuantConnect LEAN backtest results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guitrading/quantconnect-lean-tearsheet-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "plotly>=5.0.0",
        "kaleido>=0.2.1",  # For static image export
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lean-tearsheet=lean_tearsheet.cli:main",
        ],
    },
    include_package_data=True,
)
