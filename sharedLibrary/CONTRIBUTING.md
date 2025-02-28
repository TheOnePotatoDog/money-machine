# Contributing to AI Shared Library

Thank you for considering contributing to the AI Shared Library! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/TheOnePotatoDog/sharedLibrary-.git
   cd sharedLibrary-
   ```

2. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests to ensure everything is working:
   ```bash
   pytest tests/
   ```

## Code Style

We follow PEP 8 style guidelines for Python code. Please ensure your code adheres to these standards.

- Use 4 spaces for indentation
- Use docstrings for all modules, classes, and functions
- Keep line length to a maximum of 100 characters
- Use meaningful variable and function names

You can use tools like `black` and `flake8` to help maintain code style:

```bash
black ai_shared/
flake8 ai_shared/
```

## Pull Request Process

1. Fork the repository and create a new branch for your feature or bug fix
2. Make your changes and add tests if applicable
3. Ensure all tests pass
4. Update documentation if necessary
5. Submit a pull request with a clear description of the changes

## Versioning

We use semantic versioning for this project. When making changes, consider whether they are:

- MAJOR version: incompatible API changes
- MINOR version: add functionality in a backwards-compatible manner
- PATCH version: backwards-compatible bug fixes

## Adding New Features

When adding new features to the shared library:

1. Create a new module in the `ai_shared` package if appropriate
2. Add comprehensive tests in the `tests` directory
3. Update documentation in the README.md
4. Consider the impact on dependent projects (Money Machine and Safety Machine)

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
