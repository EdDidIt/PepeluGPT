#!/usr/bin/env python3
"""
Integration tests for the complete PepeluGPT system.
"""

import pytest
import time
import yaml
from pathlib import Path
from typing import Dict, Any

from core.data_manager import DataManager
from core.engine import Engine
from core.logging_config import setup_enhanced_logging, get_logger


@pytest.mark.integration
@pytest.mark.slow
class TestSystemIntegration:
    """Integration tests for the complete system."""

    def test_full_system_workflow(self, test_config: Dict[str, Any], temp_workspace: Path) -> None:
        """Test complete system workflow from initialization to query processing."""
        # Setup logging
        setup_enhanced_logging(test_config, debug=True)
        logger = get_logger(__name__)
        
        logger.info("Starting integration test")
        
        # Initialize components
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        # Test multiple queries to verify system stability
        test_queries = [
            "What is NIST?",
            "cybersecurity framework",
            "DISA STIG",
            "RMF",
            "access control",
        ]
        
        for query in test_queries:
            start_time = time.time()
            
            response = engine.process_query(query)
            execution_time = time.time() - start_time
            
            # Verify response quality
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Verify reasonable performance
            assert execution_time < 30.0  # Should complete within 30 seconds
            
            logger.info(f"Query '{query}' processed in {execution_time:.2f}s")

    def test_config_loading_integration(self) -> None:
        """Test that system can load and use different configurations."""
        config_files = [
            "config/default.yaml",
            "config/adaptive.yaml", 
            "config/classic.yaml"
        ]
        
        for config_file in config_files:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                
                # Should be able to initialize system with each config
                data_manager = DataManager(config.get("data_management", {}))
                engine = Engine(config, data_manager)
                
                # Should be able to process a basic query
                response = engine.process_query("test query")
                assert response is not None

    def test_data_manager_engine_integration(self, test_config: Dict[str, Any]) -> None:
        """Test integration between DataManager and Engine."""
        data_manager = DataManager(test_config.get("data_management", {}))
        engine = Engine(test_config, data_manager)
        
        # Test that engine can access data manager features
        assert engine.data_manager is not None
        
        # Test query processing uses data manager
        response = engine.process_query("cybersecurity")
        assert response is not None
        
        # Multiple queries should work consistently
        for i in range(3):
            response = engine.process_query(f"test query {i}")
            assert response is not None
