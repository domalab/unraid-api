---
title: Contributing
description: Guidelines for contributing to the Unraid API project
---

# Contributing to Unraid API

Thank you for your interest in contributing to the Unraid API project! This guide will help you get started with the development process.

## Setting Up a Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally
   ```bash
   git clone https://github.com/yourusername/unraid-api.git
   cd unraid-api
   ```
3. Create a virtual environment and install development dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"  # Install the package in development mode with dev dependencies
   ```

## Development Process

### Branching Strategy

- `main` - Main development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `release/*` - Release preparation

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

### Coding Style

This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. We use:

- [Black](https://black.readthedocs.io/) for code formatting
- [Flake8](https://flake8.pycqa.org/) for linting
- [isort](https://pycqa.github.io/isort/) for import sorting

You can apply these tools to your code with:

```bash
# Format code
black unraid_api tests

# Sort imports
isort unraid_api tests

# Lint code
flake8 unraid_api tests
```

### Type Checking

The project uses [mypy](http://mypy-lang.org/) for static type checking. Run it with:

```bash
mypy unraid_api
```

## Testing

### Running Tests

We use [pytest](https://docs.pytest.org/) for testing. To run the tests:

```bash
pytest
```

### Adding Tests

All new features should include tests. Place them in the `tests/` directory, following the existing structure:

- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`

## Documentation

### Building the Documentation

Documentation is built using [MkDocs](https://www.mkdocs.org/) with the [Material](https://squidfunk.github.io/mkdocs-material/) theme:

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Serve the documentation locally
mkdocs serve
```

### Documentation Style

- Use clear, concise language
- Include code examples for all features
- Document all parameters, return values, and exceptions
- Follow the existing structure

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the documentation if needed
3. Add your changes to the [changelog](../about/changelog.md)
4. Submit a pull request to the `main` branch
5. Address any review comments

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](../about/license.md). 