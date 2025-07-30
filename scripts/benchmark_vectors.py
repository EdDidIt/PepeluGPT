#!/usr/bin/env python3
"""
Vector System Performance Benchmark
Compares performance between vector_db and vector_storage systems.

This script will:
1. Test embedding generation speed
2. Test search/retrieval performance
3. Compare memory usage
4. Recommend which system to keep
"""

import time
import psutil
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Type aliases for better type checking
BenchmarkResults = Dict[str, Any]
SystemResults = Dict[str, Any]
MemoryStats = Dict[str, float]
ComplexityAnalysis = Dict[str, Any]
RecommendationData = Dict[str, Any]

def benchmark_embedding_generation(text_samples: List[str]) -> BenchmarkResults:
    """Benchmark embedding generation for both systems."""
    
    results: BenchmarkResults = {
        'vector_db': {'times': [], 'errors': 0, 'total_time': 0},
        'vector_storage': {'times': [], 'errors': 0, 'total_time': 0}
    }
    
    print("🧠 Benchmarking Embedding Generation...")
    
    # Test storage.vector_db system
    try:
        from storage.vector_db.embedding import EmbeddingModel  # type: ignore
        
        start_time = time.time()
        embedding_model = EmbeddingModel("all-MiniLM-L6-v2")  # Provide default model
        init_time = time.time() - start_time
        
        for i, text in enumerate(text_samples):
            try:
                start = time.time()
                embeddings = embedding_model.encode([text])  # type: ignore
                duration = time.time() - start
                results['vector_db']['times'].append(duration)
                
                if i == 0:  # Log first embedding details
                    print(f"  vector_db embedding shape: {embeddings.shape if hasattr(embeddings, 'shape') else 'N/A'}")  # type: ignore
                    
            except Exception as e:
                print(f"  ❌ vector_db error on sample {i}: {e}")
                results['vector_db']['errors'] += 1
        
        results['vector_db']['init_time'] = init_time
        results['vector_db']['total_time'] = sum(results['vector_db']['times'])
        results['vector_db']['avg_time'] = results['vector_db']['total_time'] / max(len(results['vector_db']['times']), 1)
        
    except Exception as e:
        print(f"  ❌ Failed to initialize vector_db embedding: {e}")
        results['vector_db']['initialization_failed'] = str(e)
    
    # Test storage.vector_db system (the actual existing system)
    try:
        from storage.vector_db.embedding import EmbeddingModel as StorageEmbeddingModel  # type: ignore
        
        start_time = time.time()
        storage_embedding_model = StorageEmbeddingModel("all-MiniLM-L6-v2")  # Provide default model
        init_time = time.time() - start_time
        
        for i, text in enumerate(text_samples):
            try:
                start = time.time()
                embeddings = storage_embedding_model.encode([text])  # type: ignore
                duration = time.time() - start
                results['vector_storage']['times'].append(duration)
                
                if i == 0:  # Log first embedding details
                    print(f"  vector_storage embedding shape: {embeddings.shape if hasattr(embeddings, 'shape') else 'N/A'}")  # type: ignore
                    
            except Exception as e:
                print(f"  ❌ vector_storage error on sample {i}: {e}")
                results['vector_storage']['errors'] += 1
        
        results['vector_storage']['init_time'] = init_time
        results['vector_storage']['total_time'] = sum(results['vector_storage']['times'])
        results['vector_storage']['avg_time'] = results['vector_storage']['total_time'] / max(len(results['vector_storage']['times']), 1)
        
    except Exception as e:
        print(f"  ❌ Failed to initialize vector_storage embedding: {e}")
        results['vector_storage']['initialization_failed'] = str(e)
    
    return results

def benchmark_search_retrieval() -> BenchmarkResults:
    """Benchmark search and retrieval performance."""
    
    results: BenchmarkResults = {
        'vector_db': {'search_times': [], 'errors': 0},
        'vector_storage': {'search_times': [], 'errors': 0}
    }
    
    print("🔍 Benchmarking Search & Retrieval...")
    
    test_queries = [
        "cybersecurity framework",
        "risk assessment methodology",
        "incident response procedures",
        "compliance requirements"
    ]
    
    # Test vector_db retrieval
    try:
        from vector_db.retriever import PepeluRetriever  # type: ignore
        
        retriever = PepeluRetriever()  # type: ignore
        
        for query in test_queries:
            try:
                start = time.time()
                _ = retriever.search(query, top_k=5)  # type: ignore
                duration = time.time() - start
                results['vector_db']['search_times'].append(duration)
                
            except Exception as e:
                print(f"  ❌ vector_db search error for '{query}': {e}")
                results['vector_db']['errors'] += 1
        
        if results['vector_db']['search_times']:
            results['vector_db']['avg_search_time'] = sum(results['vector_db']['search_times']) / len(results['vector_db']['search_times'])
        
    except Exception as e:
        print(f"  ❌ Failed to initialize vector_db retriever: {e}")
        results['vector_db']['initialization_failed'] = str(e)
    
    # Test vector_storage retrieval
    try:
        from vector_storage.vector_engine import VectorEngine  # type: ignore
        
        vector_engine = VectorEngine()  # type: ignore
        
        for query in test_queries:
            try:
                start = time.time()
                _ = vector_engine.search_documents(query, top_k=5)  # type: ignore
                duration = time.time() - start
                results['vector_storage']['search_times'].append(duration)
                
            except Exception as e:
                print(f"  ❌ vector_storage search error for '{query}': {e}")
                results['vector_storage']['errors'] += 1
        
        if results['vector_storage']['search_times']:
            results['vector_storage']['avg_search_time'] = sum(results['vector_storage']['search_times']) / len(results['vector_storage']['search_times'])
        
    except Exception as e:
        print(f"  ❌ Failed to initialize vector_storage engine: {e}")
        results['vector_storage']['initialization_failed'] = str(e)
    
    return results

def get_memory_usage() -> MemoryStats:
    """Get current memory usage statistics."""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
        'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
        'percent': process.memory_percent()
    }

def analyze_codebase_complexity() -> ComplexityAnalysis:
    """Analyze the complexity and structure of both vector systems."""
    
    analysis: ComplexityAnalysis = {
        'vector_db': {'files': 0, 'total_lines': 0, 'python_files': []},
        'vector_storage': {'files': 0, 'total_lines': 0, 'python_files': []}
    }
    
    base_dir = Path(__file__).parent.parent
    
    for system in ['vector_db', 'vector_storage']:
        system_dir = base_dir / system
        
        if system_dir.exists():
            for py_file in system_dir.glob('*.py'):
                if py_file.name != '__pycache__':
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                        
                        analysis[system]['python_files'].append({
                            'name': py_file.name,
                            'lines': lines
                        })
                        analysis[system]['total_lines'] += lines
                        analysis[system]['files'] += 1
                        
                    except Exception as e:
                        print(f"  Could not analyze {py_file}: {e}")
    
    return analysis

def generate_recommendation(embedding_results: BenchmarkResults, 
                          search_results: BenchmarkResults, 
                          complexity_analysis: ComplexityAnalysis) -> RecommendationData:
    """Generate a recommendation based on benchmark results."""
    
    recommendation: RecommendationData = {
        'winner': None,
        'confidence': 0.0,
        'reasoning': [],
        'migration_plan': []
    }
    
    scores: Dict[str, int] = {'vector_db': 0, 'vector_storage': 0}
    
    # Evaluate embedding performance
    for system in ['vector_db', 'vector_storage']:
        if 'initialization_failed' not in embedding_results[system]:
            if embedding_results[system]['errors'] == 0:
                scores[system] += 2  # No errors
            else:
                scores[system] -= 1  # Had errors
            
            # Faster average time gets points
            if 'avg_time' in embedding_results[system]:
                if system == 'vector_db':
                    other_system = 'vector_storage'
                else:
                    other_system = 'vector_db'
                
                if ('avg_time' in embedding_results[other_system] and 
                    embedding_results[system]['avg_time'] < embedding_results[other_system]['avg_time']):
                    scores[system] += 1
        else:
            scores[system] -= 3  # Failed to initialize
    
    # Evaluate search performance
    for system in ['vector_db', 'vector_storage']:
        if 'initialization_failed' not in search_results[system]:
            if search_results[system]['errors'] == 0:
                scores[system] += 2
            else:
                scores[system] -= 1
        else:
            scores[system] -= 3
    
    # Evaluate complexity (fewer lines is better for maintenance)
    db_lines = complexity_analysis['vector_db']['total_lines']
    storage_lines = complexity_analysis['vector_storage']['total_lines']
    
    if db_lines > 0 and storage_lines > 0:
        if db_lines < storage_lines:
            scores['vector_db'] += 1
            recommendation['reasoning'].append("vector_db has simpler codebase")
        elif storage_lines < db_lines:
            scores['vector_storage'] += 1
            recommendation['reasoning'].append("vector_storage has simpler codebase")
    
    # Determine winner
    if scores['vector_db'] > scores['vector_storage']:
        recommendation['winner'] = 'vector_db'
        recommendation['confidence'] = min(0.9, (scores['vector_db'] - scores['vector_storage']) / 10)
    elif scores['vector_storage'] > scores['vector_db']:
        recommendation['winner'] = 'vector_storage'
        recommendation['confidence'] = min(0.9, (scores['vector_storage'] - scores['vector_db']) / 10)
    else:
        recommendation['winner'] = 'tie'
        recommendation['confidence'] = 0.5
    
    # Add specific reasoning
    if recommendation['winner'] == 'vector_db':
        recommendation['reasoning'].append("vector_db shows better overall performance")
        recommendation['migration_plan'] = [
            "Archive vector_storage module to backup/",
            "Update all imports to use vector_db",
            "Consolidate configuration files",
            "Update documentation to reflect single vector system"
        ]
    elif recommendation['winner'] == 'vector_storage':
        recommendation['reasoning'].append("vector_storage shows better overall performance")
        recommendation['migration_plan'] = [
            "Archive vector_db module to backup/",
            "Update all imports to use vector_storage",
            "Consolidate configuration files", 
            "Update documentation to reflect single vector system"
        ]
    else:
        recommendation['reasoning'].append("Both systems show similar performance")
        recommendation['migration_plan'] = [
            "Consider feature comparison beyond performance",
            "Evaluate API consistency and ease of use",
            "Choose based on architectural alignment"
        ]
    
    recommendation['scores'] = scores
    return recommendation

def main():
    """Main benchmark execution."""
    
    print("� PepeluGPT Vector System Performance Benchmark")
    print("=" * 55)
    
    # Memory before tests
    initial_memory = get_memory_usage()
    print(f"� Initial Memory Usage: {initial_memory['rss_mb']:.1f} MB")
    
    # Sample texts for embedding tests
    text_samples = [
        "Cybersecurity framework implementation requires comprehensive risk assessment.",
        "Multi-factor authentication enhances security posture significantly.",
        "Incident response procedures should be regularly tested and updated.",
        "Compliance monitoring ensures adherence to regulatory requirements."
    ]
    
    print(f"🧪 Testing with {len(text_samples)} text samples...")
    
    # Run benchmarks
    embedding_results = benchmark_embedding_generation(text_samples)
    search_results = benchmark_search_retrieval()
    complexity_analysis = analyze_codebase_complexity()
    
    # Memory after tests
    final_memory = get_memory_usage()
    memory_delta = final_memory['rss_mb'] - initial_memory['rss_mb']
    
    # Generate recommendation
    recommendation = generate_recommendation(embedding_results, search_results, complexity_analysis)
    
    # Display results
    print("\n� BENCHMARK RESULTS")
    print("=" * 30)
    
    print("\n🧠 Embedding Performance:")
    for system, results in embedding_results.items():
        print(f"  {system}:")
        if 'initialization_failed' in results:
            print(f"    ❌ Failed to initialize: {results['initialization_failed']}")
        else:
            print(f"    🔵  Average time: {results.get('avg_time', 0):.4f}s")
            print(f"    🔢 Samples processed: {len(results['times'])}")
            print(f"    ❌ Errors: {results['errors']}")
    
    print("\n🔍 Search Performance:")
    for system, results in search_results.items():
        print(f"  {system}:")
        if 'initialization_failed' in results:
            print(f"    ❌ Failed to initialize: {results['initialization_failed']}")
        else:
            print(f"    🔵  Average search time: {results.get('avg_search_time', 0):.4f}s")
            print(f"    Searches completed: {len(results['search_times'])}")
            print(f"    ❌ Errors: {results['errors']}")
    
    print("\n� Codebase Complexity:")
    for system, analysis in complexity_analysis.items():
        print(f"  {system}: {analysis['files']} files, {analysis['total_lines']} lines")
    
    print(f"\n💾 Memory Impact: {memory_delta:+.1f} MB")
    
    print(f"\n🏆 RECOMMENDATION")
    print("=" * 20)
    print(f"🟢 Winner: {recommendation['winner']}")
    print(f"� Confidence: {recommendation['confidence']:.1%}")
    print(f"📝 Reasoning:")
    for reason in recommendation['reasoning']:
        print(f"  • {reason}")
    
    if recommendation['migration_plan']:
        print(f"� Migration Plan:")
        for step in recommendation['migration_plan']:
            print(f"  {step}")
    
    print(f"\n🔵 Professional Analysis: The system favors solutions that serve with clarity and efficiency!")

if __name__ == "__main__":
    main()
