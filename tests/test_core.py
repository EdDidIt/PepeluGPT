#!/usr/bin/env python3
"""
Comprehensive Test Suite for PepeluGPT
Tests all major components and functionality
"""

import sys
import os
import json
from pathlib import Path
sys.path.append(os.path.dirname(__file__))

def test_environment():
    """Test environment setup"""
    print("🧪 Testing Environment Setup")
    print("-" * 30)
    
    tests = {
        "Documents folder exists": Path("cyber_documents").exists(),
        "Has documents": len(list(Path("cyber_documents").glob("*.*"))) > 0 if Path("cyber_documents").exists() else False,
        "File parser module": Path("file_parser").exists(),
        "Requirements available": Path("requirements.txt").exists(),
    }
    
    passed = 0
    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Environment Tests: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_document_parsing():
    """Test document parsing functionality"""
    print("\n🧪 Testing Document Parsing")
    print("-" * 30)
    
    if not Path("parsed_cyber_documents.json").exists():
        print("❌ No parsed documents found. Run setup first.")
        return False
    
    try:
        with open("parsed_cyber_documents.json", 'r', encoding='utf-8') as f:
            parsed_docs = json.load(f)
        
        successful = sum(1 for doc in parsed_docs if doc['status'] == 'success')
        total = len(parsed_docs)
        success_rate = successful / total * 100 if total > 0 else 0
        
        print(f"  ✅ Parsed documents loaded: {total} total")
        print(f"  ✅ Success rate: {success_rate:.1f}% ({successful}/{total})")
        
        # Test content quality
        total_chars = sum(len(doc.get('content', '')) for doc in parsed_docs if doc['status'] == 'success')
        avg_chars = total_chars / successful if successful > 0 else 0
        
        print(f"  ✅ Total content: {total_chars:,} characters")
        print(f"  ✅ Average per doc: {avg_chars:,.0f} characters")
        
        return success_rate > 80  # Require 80% success rate
        
    except Exception as e:
        print(f"  ❌ Error loading parsed documents: {e}")
        return False

def test_vector_database():
    """Test vector database functionality"""
    print("\n🧪 Testing Vector Database")
    print("-" * 30)
    
    if not Path("cyber_vector_db").exists():
        print("❌ Vector database not found. Run setup first.")
        return False
    
    try:
        from build_vector_db import CyberVectorDB
        
        db = CyberVectorDB()
        db.load()
        
        print(f"  ✅ Database loaded: {len(db.chunks)} chunks")
        if db.index and hasattr(db.index, 'ntotal'):
            print(f"  ✅ Index ready: {db.index.ntotal} vectors")
        else:
            print("  ✅ Index ready")
        
        return len(db.chunks) > 1000  # Require meaningful content
        
    except Exception as e:
        print(f"  ❌ Error loading vector database: {e}")
        return False

def test_search_functionality():
    """Test search functionality with sample queries"""
    print("\n🧪 Testing Search Functionality")
    print("-" * 30)
    
    try:
        from build_vector_db import CyberVectorDB
        
        db = CyberVectorDB()
        db.load()
        
        # Test queries with expected topics
        test_queries = [
            ("RMF process", ["rmf", "risk management framework", "authorization"]),
            ("STIG compliance", ["stig", "security technical", "compliance"]),
            ("NIST framework", ["nist", "cybersecurity framework", "csf"]),
        ]
        
        passed_tests = 0
        
        for query, expected_terms in test_queries:
            results = db.search(query, top_k=3)
            
            if results and len(results) > 0:
                # Check if results contain expected terms
                combined_content = " ".join([r['content'].lower() for r in results])
                term_matches = sum(1 for term in expected_terms if term in combined_content)
                
                if term_matches > 0:
                    print(f"  ✅ '{query}': {len(results)} results, {results[0]['score']:.1%} relevance")
                    passed_tests += 1
                else:
                    print(f"  ⚠️  '{query}': Results found but no relevant terms")
            else:
                print(f"  ❌ '{query}': No results found")
        
        print(f"\n📊 Search Tests: {passed_tests}/{len(test_queries)} passed")
        return passed_tests >= len(test_queries) * 0.8  # 80% pass rate
        
    except Exception as e:
        print(f"  ❌ Search test error: {e}")
        return False

def test_chat_interface():
    """Test chat interface components"""
    print("\n🧪 Testing Chat Interface")
    print("-" * 30)
    
    try:
        from chat import PepeluGPT
        
        chat = PepeluGPT()
        
        # Test database loading
        if chat.load_database():
            print("  ✅ Chat interface can load database")
        else:
            print("  ❌ Chat interface failed to load database")
            return False
        
        # Test search functionality
        results = chat.search_knowledge("test query", num_results=2)
        if isinstance(results, list):
            print(f"  ✅ Search function returns results: {len(results)} items")
        else:
            print("  ❌ Search function failed")
            return False
        
        # Test response formatting
        response = chat.format_response("test", results)
        if response and len(response) > 10:
            print("  ✅ Response formatting works")
        else:
            print("  ❌ Response formatting failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Chat interface test error: {e}")
        return False

def test_pepelugpt():
    """Main test function"""
    print("🚀 PepeluGPT Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Document Parsing", test_document_parsing),
        ("Vector Database", test_vector_database),
        ("Search Functionality", test_search_functionality),
        ("Chat Interface", test_chat_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
    
    print(f"\n🎯 Final Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! PepeluGPT is ready for production use.")
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. System should work but may have minor issues.")
    else:
        print("❌ Multiple test failures. Please run setup or check configuration.")
    
    return passed >= total * 0.8

if __name__ == "__main__":
    test_pepelugpt()
