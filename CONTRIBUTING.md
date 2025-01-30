# Contributing to robotframework-fasthttpmock

Thank you for your interest in contributing to robotframework-fasthttpmock! This document provides guidelines and steps for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/robotframework-fasthttpmock.git
cd robotframework-fasthttpmock
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Tasks

We use `invoke` to manage development tasks. Here are the available commands:

```bash
# Format code
invoke format

# Run linting checks
invoke lint

# Run unit tests
invoke test-unit

# Run acceptance tests
invoke test-acceptance

# Run all tests
invoke test

# Generate documentation
invoke docs

# Clean build artifacts
invoke clean

# Build package
invoke build
```

## Code Style

- We use `black` for code formatting
- We use `ruff` for linting
- Maximum line length is 100 characters
- Follow Python naming conventions:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPERCASE` for constants

## Testing

1. Write unit tests for new features:
   - Put tests in `tests/` directory
   - Name test files with `test_` prefix
   - Use pytest fixtures when appropriate

2. Write acceptance tests:
   - Put tests in `atest/` directory
   - Follow Robot Framework best practices
   - Include documentation for test cases

3. Ensure all tests pass:
```bash
invoke test
```

## Documentation

1. Update docstrings for any modified code:
   - Use Robot Framework documentation format
   - Include examples where appropriate
   - Document all arguments and return values

2. Generate and check documentation:
```bash
invoke docs
```

## Pull Request Process

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
   - Write tests
   - Update documentation
   - Follow code style guidelines

3. Run quality checks:
```bash
invoke format  # Format code
invoke lint    # Check code style
invoke test    # Run all tests
```

4. Commit your changes:
   - Use clear commit messages
   - Reference any related issues

5. Push to your fork and create a Pull Request:
   - Describe your changes
   - Link any related issues
   - Ensure CI checks pass

## Release Process

1. Update version in `pyproject.toml`
2. Run release preparation:
```bash
invoke release
```
3. Create a new GitHub release
4. Publish to PyPI

## Questions or Problems?

- Check existing [issues](https://github.com/leelaprasadv/robotframework-fasthttpmock/issues)
- Create a new issue if needed
- Ask for help in the PR comments

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 