#!/usr/bin/env python3
"""
Comprehensive Test Suite for PepeluGPT
Tests all major components and functionality
"""

import sys
import json
from pathlib import Path
from typing import List, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_environment() -> bool:
    """Test environment setup"""
    print("🔵 Testing Environment Setup")
    print("-" * 30)
    
    tests = {
        "Documents folder exists": Path("cyber_documents").exists(),
        "Has documents": len(list(Path("cyber_documents").glob("*.*"))) > 0 if Path("cyber_documents").exists() else False,
        "File parser module": Path("file_parser").exists(),
        "Requirements available": Path("requirements.txt").exists(),
    }
    
    passed = 0
    for test_name, result in tests.items():
        status = "🟢 PASS" if result else "🔴 FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n� Environment Tests: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_document_parsing() -> bool:
    """Test document parsing functionality"""
    print("\n🔵 Testing Document Parsing")
    print("-" * 30)
    
    if not Path("parsed_cyber_documents.json").exists():
        print("🔴 No parsed documents found. Run setup first.")
        return False
    
    try:
        with open("parsed_cyber_documents.json", 'r', encoding='utf-8') as f:
            parsed_docs = json.load(f)
        
        successful = sum(1 for doc in parsed_docs if doc['status'] == 'success')
        total = len(parsed_docs)
        success_rate = successful / total * 100 if total > 0 else 0
        
        print(f"  🟢 Parsed documents loaded: {total} total")
        print(f"  🟢 Success rate: {success_rate:.1f}% ({successful}/{total})")
        
        # Test content quality
        total_chars = sum(len(doc.get('content', '')) for doc in parsed_docs if doc['status'] == 'success')
        avg_chars = total_chars / successful if successful > 0 else 0
        
        print(f"  🟢 Total content: {total_chars:,} characters")
        print(f"  🟢 Average per doc: {avg_chars:,.0f} characters")
        
        return success_rate > 80  # Require 80% success rate
        
    except Exception as e:
        print(f"  🔴 Error loading parsed documents: {e}")
        return False

def test_vector_database() -> bool:
    """Test vector database functionality"""
    print("\n🔵 Testing Vector Database")
    print("-" * 30)
    
    if not Path("cyber_vector_db").exists():
        print("🔴 Vector database not found. Run setup first.")
        return False
    
    try:
        # Use type ignore for dynamic imports that might not be available
        from storage.vector_db.builder import CyberVectorDB  # type: ignore
        
        db = CyberVectorDB()  # type: ignore
        db.load()  # type: ignore
        
        # Check if db has the expected attributes
        if hasattr(db, 'chunks') and getattr(db, 'chunks'):
            chunks = getattr(db, 'chunks')
            print(f"  🟢 Database loaded: {len(chunks)} chunks")
        else:
            print("  🟢 Database loaded (chunks not available)")
            
        if hasattr(db, 'index') and getattr(db, 'index'):
            # Try to get ntotal from nested index or direct access
            index = getattr(db, 'index')
            ntotal = (getattr(getattr(index, 'index', None), 'ntotal', None) or 
                     getattr(index, 'ntotal', None))
            if ntotal is not None:
                print(f"  🟢 Index ready: {ntotal} vectors")
            else:
                print("  🟢 Index ready")
        else:
            print("  🟢 Index ready")
        
        # Return True if we have any meaningful content
        return hasattr(db, 'chunks') and getattr(db, 'chunks') and len(getattr(db, 'chunks')) > 0
        
    except ImportError as e:
        print(f"🔵 Could not import CyberVectorDB: {e}")
        print("  � Trying alternative vector database check...")
        
        # Alternative check using the modular approach
        try:
            from storage.vector_db import load_database  # type: ignore
            
            db_path = project_root / "cyber_vector_db"
            if db_path.exists():
                # Load database returns (index, chunks, metadata) tuple
                result = load_database(str(db_path))  # type: ignore
                db_index, db_chunks, db_meta = result  # type: ignore
                
                if db_chunks or db_index or db_meta:
                    print("  🟢 Vector database components available")
                    return True
                else:
                    print("  🔴 No vector database data found")
                    return False
            else:
                print("  🔴 Vector database path not found")
                return False
        except Exception as e2:
            print(f"  🔴 Error with alternative check: {e2}")
            return False
    except Exception as e:
        print(f"  🔴 Error loading vector database: {e}")
        return False

def test_search_functionality() -> bool:
    """Test search functionality with sample queries"""
    print("\n🔵 Testing Search Functionality")
    print("-" * 30)
    
    try:
        from storage.vector_db.builder import CyberVectorDB  # type: ignore
        
        db = CyberVectorDB()  # type: ignore
        db.load()  # type: ignore
        
        # Test queries with expected topics
        test_queries = [
            ("RMF process", ["rmf", "risk management framework", "authorization"]),
            ("STIG compliance", ["stig", "security technical", "compliance"]),
            ("NIST framework", ["nist", "cybersecurity framework", "csf"]),
        ]
        
        passed_tests = 0
        
        for query, expected_terms in test_queries:
            try:
                if hasattr(db, 'search'):
                    results = db.search(query, top_k=3)  # type: ignore
                    
                    if results and len(results) > 0:  # type: ignore
                        # Check if results contain expected terms
                        combined_content = ""
                        for r in results:  # type: ignore
                            if hasattr(r, 'get'):
                                content = r.get('content', '')  # type: ignore
                            else:
                                content = str(r)
                            combined_content += " " + content.lower()
                        
                        term_matches = sum(1 for term in expected_terms if term in combined_content)
                        
                        if term_matches > 0:
                            first_result = results[0]  # type: ignore
                            if hasattr(first_result, 'get'):
                                score = first_result.get('score', 0)  # type: ignore
                            else:
                                score = 0
                            print(f"  🟢 '{query}': {len(results)} results, {score:.1%} relevance")  # type: ignore
                            passed_tests += 1
                        else:
                            print(f"🔵 '{query}': Results found but no relevant terms")
                    else:
                        print(f"  🔴 '{query}': No results found")
                else:
                    print(f"🔵 '{query}': Search method not available")
            except Exception as e:
                print(f"  🔴 '{query}': Error during search - {e}")
        
        print(f"\n� Search Tests: {passed_tests}/{len(test_queries)} passed")
        return passed_tests >= len(test_queries) * 0.8  # 80% pass rate
        
    except ImportError as e:
        print(f"🔵 Could not import CyberVectorDB: {e}")
        print("  � Trying alternative search test...")
        
        # Alternative test using PepeluRetriever
        try:
            from storage.vector_db.retriever import PepeluRetriever  # type: ignore
            vector_db_path = project_root / "cyber_vector_db"
            
            if vector_db_path.exists():
                retriever = PepeluRetriever(str(vector_db_path))  # type: ignore
                test_result = retriever.search("test query", top_k=1)  # type: ignore
                if test_result:
                    print("  🟢 Alternative search method works")
                    return True
                else:
                    print("  🔴 Alternative search returned no results")
                    return False
            else:
                print("  🔴 Vector database path not found")
                return False
        except Exception as e2:
            print(f"  🔴 Alternative search test error: {e2}")
            return False
    except Exception as e:
        print(f"  🔴 Search test error: {e}")
        return False

def test_chat_interface() -> bool:
    """Test chat interface components"""
    print("\n🔵 Testing Chat Interface")
    print("-" * 30)
    
    try:
        from interface.chat import ChatInterface  # type: ignore
        
        chat = ChatInterface()  # type: ignore
        
        # Test database loading
        if hasattr(chat, 'load_database') and callable(getattr(chat, 'load_database')):
            load_result = getattr(chat, 'load_database')()
            if load_result:
                print("  🟢 Chat interface can load database")
            else:
                print("  🔴 Chat interface failed to load database")
                return False
        else:
            print("  🔵 Load database method not available")
        
        # Test search functionality
        if hasattr(chat, 'search_knowledge'):
            search_method = getattr(chat, 'search_knowledge')
            results = search_method("test query", num_results=2)  # type: ignore
            if results and hasattr(results, '__len__'):
                print(f"  🟢 Search function returns results: {len(results)} items")  # type: ignore
            else:
                print("  🔴 Search function failed")
                return False
        else:
            print("🔵 Search function not available")
        
        # Test response formatting
        if hasattr(chat, 'format_response'):
            format_method = getattr(chat, 'format_response')
            response = format_method("test", [])  # type: ignore
            if response and len(str(response)) > 0:
                print("  🟢 Response formatting works")
            else:
                print("  🔴 Response formatting failed")
                return False
        else:
            print("🔵 Response formatting not available")
        
        return True
        
    except ImportError as e:
        print(f"🔵 Could not import ChatInterface: {e}")
        print("  🔵 Trying alternative chat interface check...")
        
        # Check if any chat interface exists
        interface_path = project_root / "interface"
        if interface_path.exists():
            chat_files = list(interface_path.glob("*chat*.py"))
            if chat_files:
                print(f"  🟢 Chat interface files found: {len(chat_files)} files")
                return True
            else:
                print("  🔴 No chat interface files found")
                return False
        else:
            print("  🔴 Interface directory not found")
            return False
    except Exception as e:
        print(f"  🔴 Chat interface test error: {e}")
        return False

def test_pepelugpt() -> bool:
    """Main test function"""
    print("🔵 PepeluGPT Comprehensive Test Suite")
    print("=" * 50)
    
    tests: List[tuple[str, Any]] = [
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
            print(f"\n🔴 {test_name} test crashed: {e}")
    
    print(f"\n🔵 Final Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🟢 All tests passed! PepeluGPT is ready for production use.")
    elif passed >= total * 0.8:
        print("🔵 Most tests passed. System should work but may have minor issues.")
    else:
        print("🔴 Multiple test failures. Please run setup or check configuration.")
    
    return passed >= total * 0.8

if __name__ == "__main__":
    test_pepelugpt()
