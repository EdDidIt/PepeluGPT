#!/usr/bin/env python3
"""
Quick answer about NIST SP 800-53 Control Families
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.vector_db.retriever import PepeluRetriever

def get_control_families_info():
    retriever = PepeluRetriever()
    
    # Search for control families information
    results = retriever.search('NIST SP 800-53 control families', top_k=5, similarity_threshold=0.4)
    
    print("� NIST SP 800-53 Control Families Information:")
    print("=" * 60)
    
    if results:
        for i, result in enumerate(results, 1):
            filename = result['metadata']['filename']
            text = result['chunk_text']
            score = float(result['similarity_score']) * 100
            
            print(f"\n� Source {i}: {filename}")
            print(f"🔵 Relevance: {score:.1f}%")
            print(f"� Content: {text}")
            print("-" * 40)
    else:
        print("No results found.")
    
    # Also search for specific control family lists
    print("\n🔍 Searching for specific control family information...")
    family_results = retriever.search('AC AU AT CA CM CP IA IR MA MP PE PL PS RA SA SC SI SR control families', 
                                     top_k=3, similarity_threshold=0.3)
    
    if family_results:
        for i, result in enumerate(family_results, 1):
            filename = result['metadata']['filename']
            text = result['chunk_text']
            score = float(result['similarity_score']) * 100
            
            print(f"\n📄 Additional Source {i}: {filename}")
            print(f"🔵 Relevance: {score:.1f}%")
            print(f"📝 Content: {text}")

if __name__ == "__main__":
    get_control_families_info()
