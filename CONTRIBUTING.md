# Contributing to PepeluGPT

Thank you for your interest in contributing to PepeluGPT! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized development)
- Git

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/PepeluGPT.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python -m pytest tests/`

## 📋 Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

### Documentation

- Document all public functions and classes
- Use docstrings following Google style
- Update README.md for significant changes

### Testing

- Write unit tests for new features
- Maintain minimum 80% code coverage
- Use pytest for testing framework

## 🔄 Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** with clear, descriptive commits
3. **Write/update tests** for your changes
4. **Update documentation** if needed
5. **Run the test suite** to ensure nothing breaks
6. **Submit a pull request** with a clear title and description

### PR Guidelines

- Link to relevant issues
- Provide clear description of changes
- Include screenshots for UI changes
- Ensure CI checks pass

## 🐛 Bug Reports

When filing bug reports, please include:

- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

## 💡 Feature Requests

For new features:

- Check existing issues first
- Provide clear use case and rationale
- Consider implementation complexity
- Be open to discussion and iteration

## 📁 Project Structure

```text
PepeluGPT/
├── core/           # Core engine and orchestration
├── cli/            # Command-line interface
├── plugins/        # Plugin system
├── interface/      # API and web interfaces
├── tests/          # Test suite
├── docs/           # Documentation
└── tools/          # Utilities and scripts
```

## 🔒 Security

Please report security vulnerabilities privately to the maintainers before creating public issues.

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

## 📞 Getting Help

- Check the documentation in `/docs`
- Search existing issues
- Join our community discussions
- Contact maintainers

Thank you for contributing to PepeluGPT! 🎉
