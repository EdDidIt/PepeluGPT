"""
Vector Database Retriever
Enhanced semantic search and retrieval functionality for PepeluGPT.
Professional cybersecurity intelligence platform.
"""

import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Conditional imports for robustness
try:
    import faiss  # type: ignore
    faiss_available = True
except ImportError:
    faiss_available = False
    logging.warning("🔴 FAISS not available - vector search disabled")

try:
    from sentence_transformers import SentenceTransformer
    transformers_available = True
except ImportError:
    transformers_available = False
    SentenceTransformer = None  # type: ignore
    logging.warning("🔴 SentenceTransformers not available - embedding disabled")

# Import system utilities
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from core.utilities import SystemLogger  # type: ignore
    system_available = True
except ImportError:
    # Fallback for standalone usage
    system_available = False
    
    class SystemConstants:
        SIMILARITY_THRESHOLD = 0.5
        STATUS_ICONS = {"ready": "🟢", "error": "🔴"}

class PepeluRetriever:
    """Advanced retrieval system for cybersecurity document search."""
    
    def __init__(self, vector_db_path: str = "cyber_vector_db"):
        """Initialize the professional retriever system."""
        self.vector_db_path = Path(vector_db_path)
        
        # Core components with proper initialization
        self.index: Optional[Any] = None
        self.chunks: List[str] = []
        self.metadata: List[Dict[str, Any]] = []
        self.config: Dict[str, Any] = {}
        self.model: Optional[Any] = None
        
        # Enhanced validation and trust scoring
        self.trust_scores: Dict[str, float] = {}
        self.validation_cache: Dict[str, Any] = {}
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Load database if available
        self._load_components()
        
        # Setup system logger if utilities available
        if system_available:
            try:
                from core.utilities import SystemLogger
                self.logger = SystemLogger.setup_logger(self.__class__.__name__)
            except ImportError:
                pass
    
    def _load_components(self) -> None:
        """Load all vector database components."""
        try:
            # Load FAISS index
            index_path = self.vector_db_path / "faiss_index.bin"
            if index_path.exists() and faiss_available:
                self.index = faiss.read_index(str(index_path))  # type: ignore
                if self.index:  # type: ignore
                    self.logger.info(f"Loaded FAISS index with {getattr(self.index, 'ntotal', 0)} vectors")  # type: ignore
            
            # Load chunks
            chunks_path = self.vector_db_path / "chunks.pkl"
            if chunks_path.exists():
                with open(chunks_path, 'rb') as f:
                    self.chunks = pickle.load(f)
                self.logger.info(f"Loaded {len(self.chunks)} text chunks")
            
            # Load metadata
            metadata_path = self.vector_db_path / "metadata.pkl"
            if metadata_path.exists():
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                self.logger.info(f"Loaded metadata for {len(self.metadata)} documents")
            
            # Load configuration
            config_path = self.vector_db_path / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                self.logger.info("Loaded vector database configuration")
            
            # Initialize embedding model
            if SentenceTransformer and self.config and transformers_available:
                model_name = self.config.get('model_name', 'sentence-transformers/all-MiniLM-L6-v2')
                self.model = SentenceTransformer(model_name)
                self.logger.info(f"Loaded embedding model: {model_name}")
            
        except Exception as e:
            self.logger.error(f"Error loading vector database components: {e}")
    
    def is_ready(self) -> bool:
        """Check if the retriever is ready for queries."""
        return all([
            self.index is not None,
            len(self.chunks) > 0,
            len(self.metadata) > 0,
            self.model is not None
        ])
    
    def search(self, query: str, top_k: int = 10, 
               similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Perform semantic search for the given query."""
        if not self.is_ready():
            self.logger.error("Retriever not ready - missing components")
            return []
        
        try:
            # Generate query embedding
            if self.model is None:
                return []
            query_embedding = self.model.encode([query])  # type: ignore
            
            # Search the index
            if self.index is None:
                return []
            distances, indices = self.index.search(  # type: ignore
                query_embedding.astype('float32'), 
                min(top_k * 2, getattr(self.index, 'ntotal', len(self.chunks)))  # Get more results for filtering
            )
            
            results: List[Dict[str, Any]] = []
            seen_documents: set[str] = set()
            
            for distance, idx in zip(distances[0], indices[0]):
                if idx == -1:  # Invalid index
                    continue
                
                # Convert distance to similarity score
                similarity = 1 / (1 + distance)
                
                if similarity < similarity_threshold:
                    continue
                
                # Get chunk and metadata
                chunk: str = self.chunks[idx]  # type: ignore
                chunk_metadata: Dict[str, Any] = self.metadata[idx]  # type: ignore
                
                # Avoid duplicate documents in top results
                doc_path: str = chunk_metadata.get('file_path', '')  # type: ignore
                if doc_path in seen_documents and len(results) >= top_k // 2:
                    continue
                
                seen_documents.add(doc_path)  # type: ignore
                
                result: Dict[str, Any] = {
                    "chunk_text": chunk,
                    "similarity_score": round(similarity, 4),
                    "rank": len(results) + 1,
                    "metadata": chunk_metadata,
                    "search_context": {
                        "query": query,
                        "chunk_index": int(idx),
                        "original_distance": float(distance)
                    }
                }
                
                results.append(result)
                
                if len(results) >= top_k:
                    break
            
            # Enhance results with document-level information
            enhanced_results = self._enhance_search_results(results, query)
            
            return enhanced_results
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return []
    
    def _enhance_search_results(self, results: List[Dict[str, Any]], 
                              query: str) -> List[Dict[str, Any]]:
        """Enhance search results with additional context and formatting."""
        enhanced: List[Dict[str, Any]] = []
        
        for result in results:
            metadata = result["metadata"]
            
            # Calculate quality indicators
            quality_score = self._calculate_quality_score(result, query)
            
            # Format filename for display
            filename = Path(metadata.get('file_path', '')).name
            
            # Determine document type based on extension
            file_ext = Path(metadata.get('file_path', '')).suffix.lower()
            doc_type = self._get_document_type(file_ext)
            
            # Create enhanced result by copying original result and adding display info
            enhanced_result: Dict[str, Any] = result.copy()
            enhanced_result["display"] = {
                "filename": filename,
                "document_type": doc_type,
                "quality_score": quality_score,
                "quality_label": self._get_quality_label(quality_score),
                "file_size": metadata.get('file_size', 0),
                "cybersecurity_confidence": metadata.get('cybersecurity_analysis', {}).get('confidence', 0)
            }
            
            enhanced.append(enhanced_result)
        
        return enhanced
    
    def _calculate_quality_score(self, result: Dict[str, Any], query: str) -> float:
        """Calculate a quality score for search results."""
        similarity = result["similarity_score"]
        
        # Base score from similarity
        quality = similarity * 100
        
        # Boost for cybersecurity content
        metadata = result["metadata"]
        cybersec_confidence = metadata.get('cybersecurity_analysis', {}).get('confidence', 0)
        if cybersec_confidence > 50:
            quality += min(cybersec_confidence * 0.1, 10)
        
        # Boost for query term matches in text
        chunk_text = result["chunk_text"].lower()
        query_terms = query.lower().split()
        term_matches = sum(1 for term in query_terms if term in chunk_text)
        if term_matches > 0:
            quality += min(term_matches * 5, 15)
        
        return min(quality, 100.0)
    
    def _get_quality_label(self, score: float) -> str:
        """Get quality label based on score."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Relevant"
    
    def _get_document_type(self, file_extension: str) -> str:
        """Get document type description."""
        type_mapping = {
            '.pdf': 'PDF Document',
            '.docx': 'Word Document',
            '.doc': 'Word Document',
            '.xlsx': 'Excel Spreadsheet',
            '.xls': 'Excel Spreadsheet',
            '.html': 'HTML Document',
            '.htm': 'HTML Document',
            '.txt': 'Text File',
            '.xml': 'XML Document',
            '.pptx': 'PowerPoint',
            '.ppt': 'PowerPoint'
        }
        return type_mapping.get(file_extension.lower(), 'Document')
    
    def get_document_summary(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get summary information for a specific document."""
        if not self.metadata:
            return None
        
        # Find chunks for this document
        doc_chunks = [
            chunk_meta for chunk_meta in self.metadata 
            if chunk_meta.get('file_path') == file_path
        ]
        
        if not doc_chunks:
            return None
        
        # Aggregate information
        first_chunk = doc_chunks[0]
        total_chunks = len(doc_chunks)
        total_content_length = sum(chunk.get('content_length', 0) for chunk in doc_chunks)
        
        cybersec_analysis = first_chunk.get('cybersecurity_analysis', {})
        
        return {
            "filename": Path(file_path).name,
            "file_path": file_path,
            "total_chunks": total_chunks,
            "total_content_length": total_content_length,
            "file_size": first_chunk.get('file_size', 0),
            "cybersecurity_confidence": cybersec_analysis.get('confidence', 0),
            "cybersecurity_indicators": cybersec_analysis.get('indicators', []),
            "processed_timestamp": first_chunk.get('processed_timestamp'),
            "document_type": self._get_document_type(Path(file_path).suffix)
        }
    
    def list_available_documents(self) -> List[Dict[str, Any]]:
        """List all available documents in the vector database."""
        if not self.metadata:
            return []
        
        # Group by document
        documents: Dict[str, List[Dict[str, Any]]] = {}
        for chunk_meta in self.metadata:
            file_path = chunk_meta.get('file_path', '')
            if file_path not in documents:
                documents[file_path] = []
            documents[file_path].append(chunk_meta)  # type: ignore
        
        # Create summary for each document
        doc_summaries: List[Dict[str, Any]] = []
        for file_path, chunks in documents.items():  # type: ignore
            if file_path:  # Skip empty paths
                summary = self.get_document_summary(file_path)  # type: ignore
                if summary:
                    doc_summaries.append(summary)  # type: ignore
        
        # Sort by cybersecurity confidence and filename
        doc_summaries.sort(  # type: ignore
            key=lambda x: (-x['cybersecurity_confidence'], x['filename'])  # type: ignore
        )
        
        return doc_summaries  # type: ignore
    
    def search_similar_chunks(self, chunk_index: int, top_k: int = 5) -> List[Dict[str, Any]]:
        """Find chunks similar to a given chunk."""
        if not self.is_ready() or chunk_index >= len(self.chunks):
            return []
        
        try:
            # Get embedding for the reference chunk
            chunk_text = self.chunks[chunk_index]
            if self.model is None:
                return []
            chunk_embedding = self.model.encode([chunk_text])  # type: ignore
            
            # Search for similar chunks
            if self.index is None:
                return []
            distances, indices = self.index.search(  # type: ignore
                chunk_embedding.astype('float32'), 
                top_k + 1  # +1 to exclude the original chunk
            )
            
            results: List[Dict[str, Any]] = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx == chunk_index or idx == -1:  # Skip self and invalid indices
                    continue
                
                similarity = 1 / (1 + distance)
                
                result: Dict[str, Any] = {
                    "chunk_text": self.chunks[idx],
                    "similarity_score": round(similarity, 4),
                    "metadata": self.metadata[idx],
                    "chunk_index": int(idx)
                }
                
                results.append(result)  # type: ignore
                
                if len(results) >= top_k:
                    break
            
            return results  # type: ignore
            
        except Exception as e:
            self.logger.error(f"Similar chunks search error: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        if not self.is_ready():
            return {"error": "Database not ready"}
        
        # Count documents
        unique_docs: set[str] = set()
        cybersec_docs = 0
        total_content_length = 0
        
        for chunk_meta in self.metadata:
            file_path = chunk_meta.get('file_path', '')
            if file_path:
                unique_docs.add(file_path)  # type: ignore
            
            total_content_length += chunk_meta.get('content_length', 0)
            
            if chunk_meta.get('cybersecurity_analysis', {}).get('is_cybersecurity', False):
                cybersec_docs += 1
        
        return {
            "total_documents": len(unique_docs),  # type: ignore
            "total_chunks": len(self.chunks),
            "cybersecurity_chunks": cybersec_docs,
            "total_content_length": total_content_length,
            "vector_dimension": getattr(self.index, 'd', 0) if self.index else 0,
            "model_name": self.config.get('model_name', 'unknown') if self.config else 'unknown',
            "last_updated": datetime.now().isoformat(),
            "database_ready": self.is_ready()
        }
