# Contributing to LEAN Tearsheet Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/guitrading/quantconnect-lean-tearsheet-generator.git
   cd lean-tearsheet-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Add type hints where appropriate

3. **Write tests**
   - Add unit tests for new functionality
   - Ensure existing tests still pass
   - Aim for high test coverage

4. **Run quality checks**
   ```bash
   # Run tests
   pytest

   # Check code formatting
   black --check src/ tests/

   # Run linter
   flake8 src/ tests/

   # Type checking
   mypy src/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)
- Use meaningful variable and function names
- Write docstrings for all public functions and classes

### Docstring Format

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

## Testing

- Write unit tests for all new features
- Place tests in the `tests/` directory
- Use pytest fixtures for common test setup
- Aim for >80% code coverage

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=lean_tearsheet --cov-report=html

# Run specific test file
pytest tests/test_generator.py

# Run specific test function
pytest tests/test_generator.py::test_load_backtest
```

## Pull Request Guidelines

1. **PR Description**
   - Clearly describe what the PR does
   - Reference any related issues
   - Include examples if applicable

2. **PR Checklist**
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation updated (if applicable)
   - [ ] CHANGELOG.md updated (if applicable)
   - [ ] Type hints added
   - [ ] Docstrings added/updated

3. **Commit Messages**
   - Use clear, descriptive commit messages
   - Start with a verb (Add, Fix, Update, etc.)
   - Keep first line under 50 characters
   - Add detailed description if needed

## Reporting Issues

When reporting bugs, please include:

- Python version
- Package version
- Minimal reproducible example
- Expected vs actual behavior
- Error messages and stack traces

## Feature Requests

Feature requests are welcome! Please:

- Check if the feature already exists
- Clearly describe the use case
- Explain why it would be valuable
- Provide examples if possible

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

Feel free to open an issue for questions or clarifications. We're here to help!

---

Thank you for contributing!
