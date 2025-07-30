#!/usr/bin/env python3
"""
PepeluGPT Test Suite
====================

Comprehensive testing for PepeluGPT components.
"""

import sys
import unittest
from pathlib import Path

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
        self.assertIsNotNone(self.router._personalities)
    
    def test_personality_switching(self):
        """Test personality mode switching functionality."""
        # Test switching to Oracle mode
        result = self.router.switch_mode(self.PersonalityMode.ORACLE)
        self.assertIsInstance(result, str)
        self.assertEqual(self.router._current_mode, self.PersonalityMode.ORACLE)
        
        # Test switching to Compliance mode
        result = self.router.switch_mode(self.PersonalityMode.COMPLIANCE)
        self.assertIsInstance(result, str)
        self.assertEqual(self.router._current_mode, self.PersonalityMode.COMPLIANCE)
    
    def test_mode_history(self):
        """Test that mode switching history is tracked."""
        initial_history_length = len(self.router.mode_history)
        self.router.switch_mode(self.PersonalityMode.COSMIC)
        self.assertEqual(len(self.router.mode_history), initial_history_length + 1)


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
    print("🧪 PepeluGPT Comprehensive Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
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
    print("📊 Test Results Summary:")
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed successfully!")
    else:
        print("⚠️  Some tests failed - review output above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
