#!/usr/bin/env python3
"""
Unit tests for the core Engine functionality.
"""

import pytest
from typing import Dict, Any

from core.data_manager import DataManager
from core.engine import Engine
from core.logging_config import setup_enhanced_logging


@pytest.mark.unit
@pytest.mark.core
class TestEngine:
    """Test cases for the core Engine class."""

    def test_engine_initialization(self, test_config: Dict[str, Any]) -> None:
        """Test that the engine initializes correctly."""
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        assert engine is not None
        assert engine.config == test_config
        assert engine.data_manager == data_manager

    def test_process_query_basic(self, test_config: Dict[str, Any]) -> None:
        """Test basic query processing."""
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        # Test basic query
        response = engine.process_query("What is NIST?")
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

    @pytest.mark.parametrize("query", [
        "What is NIST?",
        "cybersecurity framework",
        "access control",
        "RMF"
    ])
    def test_process_multiple_queries(self, test_config: Dict[str, Any], query: str) -> None:
        """Test processing various types of queries."""
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        response = engine.process_query(query)
        assert response is not None
        assert isinstance(response, str)

    def test_logging_integration(self, test_config: Dict[str, Any]) -> None:
        """Test that logging is properly integrated."""
        setup_enhanced_logging(test_config, debug=True)
        
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        # This should not raise any exceptions
        response = engine.process_query("test query")
        assert response is not None
