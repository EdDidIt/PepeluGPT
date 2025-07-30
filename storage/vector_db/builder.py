#!/usr/bin/env python3
"""
PepeluGPT - Vector Database Builder and Interface
Provides backward compatibility with the refactored vector_db module
"""

import os
import sys
from pathlib import Path

try:
    from vector_db import (
        build_vector_db, 
        load_database, 
        EmbeddingModel, 
        FaissIndex,
        PARSED_DOCS_FILE, 
        DB_PATH, 
        MODEL_NAME
    )
except ImportError as e:
    print(f"❌ Error importing vector_db modules: {e}")
    sys.exit(1)

class CyberVectorDB:
    """
    Backward-compatible interface for the vector database
    Wraps the new modular vector_db implementation
    """
    
    def __init__(self):
        self.model = None
        self.index = None
        self.chunks = []
        self.metadata = []
        self.db_path = DB_PATH
        
    def load(self):
        """Load the vector database from disk"""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Vector database not found at {self.db_path}")
        
        print(f"🔄 Loading vector database from {self.db_path}")
        
        # Load using the new database_io module
        self.index, self.chunks, self.metadata = load_database(self.db_path)
        
        # Create model instance for queries
        self.model = EmbeddingModel(MODEL_NAME)
        
        print(f"✅ Loaded {len(self.chunks)} chunks with {self.index.ntotal} vectors")
        
    def search(self, query, top_k=5):
        """Search the database for relevant chunks"""
        if not self.model or not self.index:
            raise RuntimeError("Database not loaded. Call load() first.")
        
        # Encode the query
        query_embedding = self.model.encode_query(query)
        
        # Ensure query_embedding is 2D (batch_size, embedding_dim)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search the index - use return-based method
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Extract first row results (remove the batch dimension)
        scores = scores[0]
        indices = indices[0]
        
        # Format results
        results = []
        for score, idx in zip(scores, indices):
            if idx >= 0 and idx < len(self.chunks):  # idx = -1 means no result found
                results.append({
                    'content': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'score': float(score),
                    'filename': self.metadata[idx].get('filename', 'unknown')
                })
        
        return results
    
    def build(self):
        """Build the vector database from parsed documents"""
        print("🔄 Building vector database...")
        
        # Use the new vector_builder module
        result = build_vector_db()
        
        if result:
            self.model, index_obj, self.chunks, self.metadata = result
            self.index = index_obj.index
            print("✅ Vector database built successfully")
        else:
            raise RuntimeError("Failed to build vector database")

def main():
    """
    Main entry point - builds the vector database
    Maintains compatibility with the original interface
    """
    try:
        # Check if parsed documents exist
        if not Path(PARSED_DOCS_FILE).exists():
            print(f"❌ Parsed documents not found: {PARSED_DOCS_FILE}")
            print("   Please run document parsing first")
            return False
        
        # Build the database using the new modular approach
        result = build_vector_db()
        
        if result:
            model, indexer, chunks, metadata = result
            print("🎉 Vector database build completed!")
            print(f"   📊 Processed {len(chunks)} chunks")
            print(f"   🧠 Created {indexer.index.ntotal} embeddings")
            print(f"   💾 Saved to {DB_PATH}/")
            return True
        else:
            print("❌ Vector database build returned no result")
            return False
        
    except Exception as e:
        print(f"❌ Error building vector database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
