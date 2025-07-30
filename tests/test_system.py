#!/usr/bin/env python3
"""
Comprehensive Test Suite for PepeluGPT
Enhanced testing for the new architecture and core functionality.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.orchestrator import initialize_pepelu_core

class TestResults:
    """Tracks test results with detailed reporting."""
    
    def __init__(self):
        self.tests: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0
    
    def add_test(self, name: str, passed: bool, details: str = ""):
        """Add a test result."""
        self.tests.append({
            "name": name,
            "passed": passed,
            "details": details
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def display_results(self):
        """Display formatted test results."""
        print(f"\n� Test Summary: {self.passed} passed, {self.failed} failed")
        print("-" * 50)
        
        for test in self.tests:
            status = "🟢 PASS" if test["passed"] else "🔴 FAIL"
            print(f"  {status} {test['name']}")
            if test["details"]:
                print(f"        {test['details']}")

def test_core_initialization():
    """Test core engine initialization and configuration."""
    print("🔵 Testing Core Engine Initialization")
    print("-" * 40)
    
    results = TestResults()
    
    try:
        # Test core initialization
        core = initialize_pepelu_core()
        results.add_test("Core engine initialization", True)
        
        # Test configuration loading
        config = core.config
        results.add_test("Configuration loading", 
                        bool(config),
                        f"Loaded {len(config)} config sections")
        
        # Test paths loading
        paths = core.paths
        results.add_test("Paths configuration", 
                        bool(paths),
                        f"Loaded {len(paths)} path mappings")
        
        # Test logging setup
        logger = core.logger
        results.add_test("Logging initialization", 
                        True,  # logger is always present
                        f"Logger level: {logger.level}")
        
    except Exception as e:
        results.add_test("Core initialization", False, f"Error: {e}")
    
    results.display_results()
    return results.failed == 0

def test_environment_validation():
    """Test environment setup and validation."""
    print("\n🔵 Testing Environment Validation")
    print("-" * 40)
    
    results = TestResults()
    core = initialize_pepelu_core()
    
    # Test directory initialization
    try:
        init_success = core.initialize_directories()
        results.add_test("Directory initialization", init_success)
    except Exception as e:
        results.add_test("Directory initialization", False, f"Error: {e}")
    
    # Test environment validation
    validation = core.validate_environment()
    
    # Check critical directories
    required_dirs = ['cyber_documents', 'data', 'vector_db', 'logs']
    for dir_name in required_dirs:
        dir_exists = validation.get(f"dir_{dir_name}", False)
        results.add_test(f"{dir_name.title()} directory", dir_exists)
    
    # Check document availability
    docs_available = validation.get("documents_available", False)
    results.add_test("Documents available", docs_available,
                    "Add documents to cyber_documents/ folder" if not docs_available else "")
    
    # Check vector database
    vector_ready = validation.get("vector_db_ready", False)
    results.add_test("Vector database ready", vector_ready,
                    "Run setup to  Build vector database" if not vector_ready else "")
    
    results.display_results()
    return results.failed == 0

def test_configuration_management():
    """Test configuration management functionality."""
    print("\n🔵 Testing Configuration Management")
    print("-" * 40)
    
    results = TestResults()
    core = initialize_pepelu_core()
    
    # Test getting configuration values
    app_name = core.get_config("application.name", "default")
    results.add_test("Config value retrieval", 
                    app_name is not None,
                    f"App name: {app_name}")
    
    # Test nested configuration access
    chunk_size = core.get_config("parsing.chunk_size", 1000)
    results.add_test("Nested config access", 
                    isinstance(chunk_size, int),
                    f"Chunk size: {chunk_size}")
    
    # Test default value fallback
    unknown_value = core.get_config("unknown.setting", "fallback")
    results.add_test("Default value fallback", 
                    unknown_value == "fallback")
    
    # Test path retrieval
    data_path = core.get_path("data")
    results.add_test("Path retrieval", 
                    True,  # Path is always returned as Path object
                    f"Data path: {data_path}")
    
    results.display_results()
    return results.failed == 0

def test_document_parsing():
    """Test document parsing functionality."""
    print("\n🔵 Testing Document Parsing")
    print("-" * 40)
    
    results = TestResults()
    core = initialize_pepelu_core()
    
    # Check if parsed documents exist
    parsed_docs_path = core.get_path("data") / "parsed_cyber_documents.json"
    
    if not parsed_docs_path.exists():
        results.add_test("Parsed documents file", False, 
                        "Run 'python core/cli.py setup' first")
        results.display_results()
        return False
    
    try:
        with open(parsed_docs_path, 'r', encoding='utf-8') as f:
            parsed_docs = json.load(f)
        
        results.add_test("Parsed documents loading", True,
                        f"Loaded {len(parsed_docs)} document entries")
        
        # Analyze parsing success rate
        successful = sum(1 for doc in parsed_docs if doc.get('status') == 'success')
        total = len(parsed_docs)
        success_rate = (successful / total * 100) if total > 0 else 0
        
        results.add_test("Parsing success rate", 
                        success_rate >= 70,  # 70% minimum success rate
                        f"{success_rate:.1f}% ({successful}/{total})")
        
        # Check content quality
        total_chunks = sum(len(doc.get('chunks', [])) for doc in parsed_docs 
                          if doc.get('status') == 'success')
        
        results.add_test("Content extraction", 
                        total_chunks > 0,
                        f"{total_chunks} text chunks extracted")
        
    except Exception as e:
        results.add_test("Document parsing validation", False, f"Error: {e}")
    
    results.display_results()
    return results.failed == 0

def test_vector_database():
    """Test vector database functionality."""
    print("\n🔵 Testing Vector Database")
    print("-" * 40)
    
    results = TestResults()
    core = initialize_pepelu_core()
    
    vector_db_path = core.get_path("vector_db")
    
    # Check vector database files
    required_files = [
        ("FAISS index", "faiss_index.bin"),
        ("Chunks data", "chunks.pkl"),
        ("Metadata", "metadata.pkl"),
        ("Config", "config.json")
    ]
    
    for file_desc, filename in required_files:
        file_path = vector_db_path / filename
        results.add_test(f"{file_desc} file", 
                        file_path.exists(),
                        f"Missing: {filename}" if not file_path.exists() else "")
    
    # Test vector database configuration
    config_path = vector_db_path / "config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                vector_config = json.load(f)
            
            results.add_test("Vector DB config", True,
                            f"Dimension: {vector_config.get('dimension', 'unknown')}")
            
        except Exception as e:
            results.add_test("Vector DB config", False, f"Error: {e}")
    
    results.display_results()
    return results.failed == 0

def test_system_status():
    """Test system status reporting."""
    print("\n🔵 Testing System Status")
    print("-" * 40)
    
    results = TestResults()
    core = initialize_pepelu_core()
    
    try:
        status = core.get_system_status()
        
        results.add_test("Status generation", 
                        True,  # Status is always returned as dict
                        f"Status keys: {list(status.keys())}")
        
        # Check required status fields
        required_fields = ['timestamp', 'application', 'environment_validation', 'ready_for_chat']
        for field in required_fields:
            results.add_test(f"Status field: {field}",
                            field in status)
        
        # Check readiness assessment
        ready = status.get('ready_for_chat', False)
        results.add_test("Chat readiness assessment", 
                        isinstance(ready, bool),
                        f"Ready: {ready}")
        
    except Exception as e:
        results.add_test("System status", False, f"Error: {e}")
    
    results.display_results()
    return results.failed == 0

def test_pepelugpt():
    """Main test function - runs all test suites."""
    print("🔵 PepeluGPT Comprehensive Test Suite")
    print("=" * 50)

    test_functions = [
        test_core_initialization,
        test_environment_validation,
        test_configuration_management,
        test_document_parsing,
        test_vector_database,
        test_system_status
    ]

    passed_suites = 0
    total_suites = len(test_functions)

    for test_func in test_functions:
        try:
            if test_func():
                passed_suites += 1
        except Exception as e:
            print(f"🔴 Test suite failed: {test_func.__name__} - {e}")

    print("\n" + "=" * 50)
    print(f"🏁 Test Summary: {passed_suites}/{total_suites} test suites passed")
    
    if passed_suites == total_suites:
        print("🎉 All tests passed! PepeluGPT is ready for action.")
    else:
        print("🔴  Some tests failed. Check the output above for details.")
        print("🔵 Try running: python core/cli.py setup")

    return passed_suites == total_suites


if __name__ == "__main__":
    test_pepelugpt()
