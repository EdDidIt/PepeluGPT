"""
PepeluGPT Tests Module
======================

Comprehensive testing suite ensuring system reliability and functionality.

Test Categories:
    - Unit Tests: Individual component testing
    - Integration Tests: Module interaction testing
    - Performance Tests: System performance validation
    - Security Tests: Security compliance verification

Usage:
    # Run all tests
    pytest tests/
    
    # Run specific test
    python tests/get_nist_families.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

__version__ = "2.0.0"
