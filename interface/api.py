"""
PepeluGPT API Interface
Future-ready API endpoint for expanding PepeluGPT functionality.
This module provides a foundation for web interfaces, REST APIs, or integrations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from pathlib import Path

# Future imports for API framework (when implemented)
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

class PepeluAPI:
    """API interface for PepeluGPT functionality."""
    
    def __init__(self) -> None:
        """Initialize the API interface."""
        self.logger = logging.getLogger(__name__)
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Import core components
        try:
            import sys
            sys.path.append(str(Path(__file__).parent.parent))
            from core.core import get_core  # type: ignore
            from storage.vector_db.retriever import PepeluRetriever  # type: ignore
            
            self.core = get_core()  # type: ignore
            self.retriever = PepeluRetriever()  # type: ignore
            
        except ImportError as e:
            self.logger.error(f"Failed to import core components: {e}")
            self.core = None
            self.retriever = None
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        if not self.core:  # type: ignore
            return {"error": "Core system not available"}
        
        try:
            status = self.core.get_system_status()  # type: ignore
            db_stats = self.retriever.get_database_stats() if self.retriever else {}  # type: ignore
            
            return {
                "system_status": status,
                "database_stats": db_stats,
                "api_version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to get system info: {e}"}
    
    def search_documents(self, query: str, top_k: int = 10, 
                        threshold: float = 0.7) -> Dict[str, Any]:
        """Search documents using semantic search."""
        if not self.retriever or not self.retriever.is_ready():  # type: ignore
            return {
                "error": "Search system not ready",
                "suggestion": "Run setup to initialize the vector database"
            }
        
        try:
            results = self.retriever.search(query, top_k, threshold)  # type: ignore
            
            return {
                "query": query,
                "total_results": len(results),
                "results": results,
                "search_metadata": {
                    "top_k": top_k,
                    "threshold": threshold,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {"error": f"Search failed: {e}"}
    
    def list_documents(self) -> Dict[str, Any]:
        """List all available documents."""
        if not self.retriever:
            return {"error": "Retriever not available"}
        
        try:
            documents = self.retriever.list_available_documents()  # type: ignore
            
            return {
                "total_documents": len(documents),
                "documents": documents,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to list documents: {e}"}
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """Get detailed information about a specific document."""
        if not self.retriever:
            return {"error": "Retriever not available"}
        
        try:
            doc_summary = self.retriever.get_document_summary(file_path)  # type: ignore
            
            if not doc_summary:
                return {"error": "Document not found"}
            
            return {
                "document_info": doc_summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get document info: {e}"}
    
    def validate_setup(self) -> Dict[str, Any]:
        """Validate system setup and readiness."""
        if not self.core:  # type: ignore
            return {"error": "Core system not available"}
        
        try:
            validation = self.core.validate_environment()  # type: ignore
            config = self.core.config  # type: ignore
            
            setup_status: Dict[str, Any] = {
                "environment_valid": all(validation.values()),  # type: ignore
                "components": validation,
                "configuration": {
                    "app_name": config.get("application", {}).get("name", "PepeluGPT"),  # type: ignore
                    "version": config.get("application", {}).get("version", "unknown"),  # type: ignore
                    "mode": config.get("application", {}).get("mode", "local"),  # type: ignore
                    "offline_mode": config.get("security", {}).get("offline_mode", True)  # type: ignore
                },
                "recommendations": self._get_setup_recommendations(validation)  # type: ignore
            }
            
            return setup_status
            
        except Exception as e:
            return {"error": f"Setup validation failed: {e}"}
    
    def _get_setup_recommendations(self, validation: Dict[str, bool]) -> List[str]:  # type: ignore
        """Generate setup recommendations based on validation results."""
        recommendations: List[str] = []
        
        if not validation.get("documents_available", False):  # type: ignore
            recommendations.append("Add cybersecurity documents to the cyber_documents/ folder")
        
        if not validation.get("vector_db_ready", False):  # type: ignore
            recommendations.append("Run 'python core/cli.py setup' to  Build the vector database")
        
        if not validation.get("dir_data", False):  # type: ignore
            recommendations.append("Ensure data directory exists and is writable")
        
        if not validation.get("dir_logs", False):  # type: ignore
            recommendations.append("Ensure logs directory exists for system logging")
        
        if not recommendations:
            recommendations.append("System is ready! Try running 'python core/cli.py chat'")
        
        return recommendations
    
    def create_chat_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new chat session."""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session: Dict[str, Any] = {
            "session_id": session_id,
            "created": datetime.now().isoformat(),
            "messages": [],
            "context": {}
        }
        
        self.active_sessions[session_id] = session
        
        return {
            "session_id": session_id,
            "status": "created",
            "timestamp": session["created"]
        }
    
    def chat_message(self, session_id: str, message: str, 
                    context_search: bool = True) -> Dict[str, Any]:
        """Process a chat message within a session."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found", "session_id": session_id}
        
        session = self.active_sessions[session_id]
        
        # Add user message to session
        user_message: Dict[str, Any] = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        session["messages"].append(user_message)  # type: ignore
        
        response_data: Dict[str, Any] = {
            "session_id": session_id,
            "user_message": message,
            "response": "Chat processing not yet implemented in API mode",
            "timestamp": datetime.now().isoformat(),
            "context_documents": []
        }
        
        # If context search is enabled, include relevant documents
        if context_search and self.retriever and self.retriever.is_ready():  # type: ignore
            search_results = self.retriever.search(message, top_k=3)  # type: ignore
            response_data["context_documents"] = search_results
        
        # Add assistant response to session
        assistant_message: Dict[str, Any] = {
            "role": "assistant", 
            "content": response_data["response"],
            "timestamp": response_data["timestamp"],
            "context_documents": response_data.get("context_documents", [])
        }
        session["messages"].append(assistant_message)  # type: ignore
        
        return response_data
    
    def get_session_history(self, session_id: str) -> Dict[str, Any]:
        """Get chat session history."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "created": session["created"],  # type: ignore
            "message_count": len(session["messages"]),  # type: ignore
            "messages": session["messages"]  # type: ignore
        }
    
    def export_session(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """Export chat session data."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        if format.lower() == "json":
            return {
                "export_format": "json",
                "session_data": session,
                "exported_at": datetime.now().isoformat()
            }
        else:
            return {"error": f"Unsupported export format: {format}"}
    
    def get_api_endpoints(self) -> Dict[str, Any]:
        """Get list of available API endpoints."""
        endpoints = {
            "system": {
                "/system/info": "Get system information and status",
                "/system/validate": "Validate system setup"
            },
            "search": {
                "/search": "Search documents semantically",
                "/documents": "List all available documents",
                "/documents/{file_path}": "Get specific document information"
            },
            "chat": {
                "/chat/session": "Create new chat session",
                "/chat/{session_id}/message": "Send message to session",
                "/chat/{session_id}/history": "Get session history",
                "/chat/{session_id}/export": "Export session data"
            },
            "meta": {
                "/api/endpoints": "This endpoint - list all endpoints"
            }
        }
        
        return {
            "api_version": "1.0.0",
            "endpoints": endpoints,
            "documentation": "Future: Swagger/OpenAPI documentation will be available",
            "timestamp": datetime.now().isoformat()
        }

# Global API instance
api_instance = None

def get_api() -> PepeluAPI:
    """Get or create the global API instance."""
    global api_instance
    if api_instance is None:
        api_instance = PepeluAPI()
    return api_instance

# Future FastAPI implementation template
"""
app = FastAPI(title="PepeluGPT API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "PepeluGPT API", "version": "1.0.0"}

@app.get("/system/info")
async def system_info():
    api = get_api()
    return api.get_system_info()

@app.post("/search")
async def search_documents(query: str, top_k: int = 10, threshold: float = 0.7):
    api = get_api()
    return api.search_documents(query, top_k, threshold)

# Add more endpoints as needed...
"""
