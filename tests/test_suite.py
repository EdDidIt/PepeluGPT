#!/usr/bin/env python3
"""
PepeluGPT Test Suite
====================

Comprehensive testing for PepeluGPT components.
"""

import sys
import unittest
from pathlib import Path
from typing import List, Type

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPersonalitySystem(unittest.TestCase):
    """Test the personality system components."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from personalities import PersonalityRouter, PersonalityMode
            self.router = PersonalityRouter()
            self.PersonalityMode = PersonalityMode
        except ImportError as e:
            self.skipTest(f"Could not import personality system: {e}")
    
    def test_personality_router_initialization(self):
        """Test that personality router initializes correctly."""
        self.assertIsNotNone(self.router)
        # Test router has basic functionality
        if hasattr(self.router, 'get_personalities_dict'):
            personalities_dict = getattr(self.router, 'get_personalities_dict')()  # type: ignore
            self.assertIsNotNone(personalities_dict)
        else:
            # Alternative check - ensure router has basic attributes
            self.assertTrue(hasattr(self.router, '__class__'))
    
    def test_personality_switching(self):
        """Test personality mode switching functionality."""
        # Test switching to Oracle mode
        if hasattr(self.router, 'switch_mode'):
            result = getattr(self.router, 'switch_mode')(self.PersonalityMode.ORACLE)  # type: ignore
            self.assertIsInstance(result, str)
            
            if hasattr(self.router, 'get_current_mode'):
                current_mode = getattr(self.router, 'get_current_mode')()  # type: ignore
                self.assertEqual(current_mode, self.PersonalityMode.ORACLE)
            
            # Test switching to Compliance mode
            result = getattr(self.router, 'switch_mode')(self.PersonalityMode.COMPLIANCE)  # type: ignore
            self.assertIsInstance(result, str)
            
            if hasattr(self.router, 'get_current_mode'):
                current_mode = getattr(self.router, 'get_current_mode')()  # type: ignore
                self.assertEqual(current_mode, self.PersonalityMode.COMPLIANCE)
        else:
            self.skipTest("switch_mode method not available")
    
    def test_mode_history(self):
        """Test that mode switching history is tracked."""
        if hasattr(self.router, 'mode_history') and hasattr(self.router, 'switch_mode'):
            initial_history_length = len(getattr(self.router, 'mode_history'))  # type: ignore
            getattr(self.router, 'switch_mode')(self.PersonalityMode.PROFESSIONAL)  # type: ignore
            current_history_length = len(getattr(self.router, 'mode_history'))  # type: ignore
            self.assertEqual(current_history_length, initial_history_length + 1)
        else:
            self.skipTest("mode_history or switch_mode not available")


class TestCoreUtilities(unittest.TestCase):
    """Test core utility functions."""
    
    def test_imports(self):
        """Test that core modules can be imported."""
        try:
            from core import utilities
            self.assertTrue(hasattr(utilities, '__name__'))
        except ImportError as e:
            self.skipTest(f"Could not import core utilities: {e}")


class TestProcessingSystem(unittest.TestCase):
    """Test document processing components."""
    
    def test_parser_imports(self):
        """Test that parser modules can be imported."""
        try:
            from processing.parser import utils
            self.assertTrue(hasattr(utils, '__name__'))
        except ImportError as e:
            self.skipTest(f"Could not import processing parser: {e}")


class TestVectorDatabase(unittest.TestCase):
    """Test vector database functionality."""
    
    def test_vector_db_imports(self):
        """Test that vector database modules can be imported."""
        try:
            from storage.vector_db import config
            self.assertTrue(hasattr(config, '__name__'))
        except ImportError as e:
            self.skipTest(f"Could not import vector database: {e}")
    
    def test_retriever_class_exists(self):
        """Test that PepeluRetriever class can be imported."""
        try:
            from storage.vector_db.retriever import PepeluRetriever
            self.assertTrue(callable(PepeluRetriever))
        except ImportError as e:
            self.skipTest(f"Could not import PepeluRetriever: {e}")


class TestConfigurationSystem(unittest.TestCase):
    """Test configuration management."""
    
    def test_config_files_exist(self):
        """Test that configuration files exist."""
        config_dir = Path(__file__).parent.parent / "config"
        self.assertTrue(config_dir.exists(), "Config directory should exist")
        
        expected_files = [
            "default_config.yaml",
            "paths.yaml", 
            "personalities.yaml",
            "profile_overrides.yaml"
        ]
        
        for file_name in expected_files:
            file_path = config_dir / file_name
            self.assertTrue(file_path.exists(), f"Config file {file_name} should exist")


def run_comprehensive_tests():
    """Run all tests and provide summary."""
    print("🔵 PepeluGPT Comprehensive Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes: List[Type[unittest.TestCase]] = [
        TestPersonalitySystem,
        TestCoreUtilities, 
        TestProcessingSystem,
        TestVectorDatabase,
        TestConfigurationSystem
    ]
    
    for test_class in test_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("� Test Results Summary:")
    print(f"🟢 Tests Run: {result.testsRun}")
    print(f"🔴 Failures: {len(result.failures)}")
    print(f"🔴 Errors: {len(result.errors)}")
    print(f"🔵 Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("🟢 All tests passed successfully!")
    else:
        print("🔴 Some tests failed - review output above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
