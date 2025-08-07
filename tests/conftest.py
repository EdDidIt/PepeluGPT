"""
PepeluGPT Test Suite Configuration
Pytest configuration and shared test fixtures
"""

import sys
import tempfile
import pytest
from pathlib import Path
from typing import Dict, Any, List, Generator

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Provide test configuration for all tests."""
    return {
        "data_management": {
            "cache_dir": "test_cache",
            "source_dir": "cyber_documents",
            "enable_caching": True,
            "cache_validation": "hash",
        },
        "logging": {
            "level": "INFO"
        },
        "model": {
            "name": "test-model",
            "parameters": {
                "temperature": 0.7
            }
        },
        "learning": {
            "enabled": False
        }
    }


@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_query() -> List[str]:
    """Provide sample queries for testing."""
    return [
        "What is NIST?",
        "cybersecurity framework",
        "access control",
        "RMF",
    ]


# Test configuration
pytest_plugins = []

def pytest_configure(config: Any) -> None:
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "core: mark test as core functionality"
    )
    config.addinivalue_line(
        "markers", "plugins: mark test as plugin functionality"
    )
