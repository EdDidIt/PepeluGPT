#!/usr/bin/env python3
"""
PepeluGPT - Vector Database Builder and Interface
Provides backward compatibility with the refactored vector_db module
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from .vector_builder import build_vector_db
    from .database_io import load_database  # type: ignore  # Dynamic module with varying return types
    from .embedding import EmbeddingModel
    from .indexing import FaissIndex
    from .config import PARSED_DOCS_FILE, DB_PATH, MODEL_NAME
except ImportError as e:
    print(f"❌ Error importing vector_db modules: {e}")
    sys.exit(1)

class CyberVectorDB:
    """
    Backward-compatible interface for the vector database
    Wraps the new modular vector_db implementation
    """
    
    def __init__(self):
        """Initialize the CyberVectorDB instance"""
        self.model: Optional[EmbeddingModel] = None
        self.index: Optional[FaissIndex] = None
        self.chunks: List[str] = []
        self.metadata: List[Dict[str, Any]] = []
        self.db_path: str = DB_PATH
        
    def load(self) -> None:
        """Load the vector database from disk"""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Vector database not found at {self.db_path}")
        
        print(f"🔄 Loading vector database from {self.db_path}")
        
        # Load using the new database_io module
        raw_index, self.chunks, self.metadata = load_database(self.db_path)  # type: ignore
        
        # Wrap the raw FAISS index in our FaissIndex wrapper
        # Create a temporary FaissIndex wrapper and assign the loaded index
        self.index = FaissIndex(0)  # Dimension doesn't matter since we're replacing the index
        self.index.index = raw_index  # Replace with the loaded index
        
        # Create model instance for queries
        self.model = EmbeddingModel(MODEL_NAME)
        
        print(f"✅ Loaded {len(self.chunks)} chunks with embeddings")
        
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search the database for relevant chunks"""
        if not self.model or not self.index:
            raise RuntimeError("Database not loaded. Call load() first.")
        
        # Encode the query
        query_embedding = self.model.encode_query(query)  # type: ignore
        
        # Ensure query_embedding is 2D (batch_size, embedding_dim)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search the index - use return-based method
        scores, indices = self.index.search(query_embedding, top_k)  # type: ignore
        
        # Extract first row results (remove the batch dimension)
        scores = scores[0]  # type: ignore
        indices = indices[0]  # type: ignore
        
        # Format results
        results: List[Dict[str, Any]] = []
        for score, idx in zip(scores, indices):  # type: ignore
            if idx >= 0 and idx < len(self.chunks):  # idx = -1 means no result found
                results.append({
                    'content': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'score': float(score),  # type: ignore
                    'filename': self.metadata[idx].get('filename', 'unknown')  # type: ignore
                })
        
        return results
    
    def build(self) -> None:
        """Build the vector database from parsed documents"""
        print("🔄 Building vector database...")
        
        # Use the new vector_builder module
        result = build_vector_db()  # type: ignore
        
        if result:
            self.model, index_obj, self.chunks, self.metadata = result  # type: ignore
            self.index = index_obj  # Store the FaissIndex wrapper, not the raw index
            print("✅ Vector database built successfully")
        else:
            raise RuntimeError("Failed to build vector database")

def main() -> bool:
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
        result = build_vector_db()  # type: ignore
        
        if result:
            _model, indexer, chunks, _metadata = result  # type: ignore
            print("🎉 Vector database build completed!")
            print(f"   📊 Processed {len(chunks)} chunks")  # type: ignore
            if hasattr(indexer, 'index') and hasattr(indexer.index, 'ntotal'):
                print(f"   🧠 Created {indexer.index.ntotal} embeddings")  # type: ignore
            else:
                print(f"   🧠 Created embeddings for all chunks")
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
