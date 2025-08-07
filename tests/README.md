# Test Suite for PepeluGPT

This directory contains the comprehensive test suite for PepeluGPT.

## Test Structure

```text
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── run_tests.py                # Test runner script
├── unit/                       # Unit tests
│   ├── core/                   # Core functionality tests
│   └── plugins/                # Plugin tests
├── integration/                # Integration tests
├── demo/                       # Demo and showcase tests
└── README.md                   # This file
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -m "unit"

# Integration tests only
pytest tests/integration/ -m "integration"

# Core functionality tests
pytest tests/ -m "core"

# Plugin tests
pytest tests/ -m "plugins"
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Categories

- **unit**: Fast, isolated tests for individual components
- **integration**: Tests for component interactions
- **core**: Tests for core system functionality
- **plugins**: Tests for plugin system
- **slow**: Tests that take longer to run

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Example Test

```python
import pytest

@pytest.mark.unit
def test_example_function(test_config):
    """Test description."""
    # Test implementation
    assert True
```

## Fixtures Available

- `test_config`: Basic test configuration
- `temp_workspace`: Temporary directory for tests
- `sample_query`: Sample queries for testing

## CI/CD Integration

Tests are designed to run in CI/CD environments with minimal dependencies.
Use `pytest tests/ --tb=short` for concise output in CI.
