"""
PepeluGPT - Shared Utilities
Common utilities and validation functions used across all modules.
Professional cybersecurity intelligence platform.
"""

import re
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Union
from datetime import datetime
import logging

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class PepeluValidator:
    """Professional validation engine for PepeluGPT operations."""
    
    SUPPORTED_FORMATS = [
        '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.html', '.xml', 
        '.txt', '.md', '.pptx', '.ppt', '.csv', '.json'
    ]
    
    CYBERSECURITY_INDICATORS = {
        'frameworks': [
            r'\bNIST\b', r'\bRMF\b', r'\bSTIG\b', r'\bCCE\b', r'\bCCI\b',
            r'\bISO 27001\b', r'\bSOC 2\b', r'\bFISMA\b', r'\bCMVP\b'
        ],
        'controls': [
            r'\b[A-Z]{2}-\d+\b',  # AC-1, AU-2, etc.
            r'\bControl \d+\.\d+\b',  # Control 1.1, etc.
        ],
        'security_terms': [
            r'\bcybersecurity\b', r'\binformation security\b', r'\bvulnerability\b',
            r'\bthreat\b', r'\brisk assessment\b', r'\bencryption\b',
            r'\bauthentication\b', r'\bauthorization\b', r'\baudit\b',
            r'\bincident response\b', r'\bforensics\b'
        ]
    }
    
    @staticmethod
    def validate_file_path(file_path: Union[str, Path]) -> Path:
        """Validate and normalize file path."""
        path = Path(file_path)
        
        if not path.exists():
            raise ValidationError(f"Path not found: {path}")
        
        if not path.is_file():
            raise ValidationError(f"Expected a file, found directory: {path}")
        
        if path.suffix.lower() not in PepeluValidator.SUPPORTED_FORMATS:
            raise ValidationError(
                f"Unsupported format: {path.suffix}. "
                f"Supported formats: {', '.join(PepeluValidator.SUPPORTED_FORMATS)}"
            )
        
        return path
    
    @staticmethod
    def validate_directory(dir_path: Union[str, Path], create_if_missing: bool = False) -> Path:
        """Validate directory with option to create if missing."""
        path = Path(dir_path)
        
        if not path.exists():
            if create_if_missing:
                path.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory: {path}")
            else:
                raise ValidationError(f"Directory not found: {path}")
        
        if not path.is_dir():
            raise ValidationError(f"Expected directory, found file: {path}")
        
        return path
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration against required standards."""
        required_sections = ['application', 'parsing', 'vector_database', 'security']
        
        for section in required_sections:
            if section not in config:
                raise ValidationError(f"Missing configuration section: {section}")
        
        # Validate critical settings
        app_config = config.get('application', {})
        if not app_config.get('name'):
            raise ValidationError("Application name must be defined")
        
        security_config = config.get('security', {})
        if not security_config.get('offline_mode', True):
            logging.warning("Online mode detected - data may be transmitted externally")
        
        return True
    
    @staticmethod
    def detect_cybersecurity_content(text: str) -> Dict[str, Any]:
        """Detect cybersecurity content within text using pattern analysis."""
        if not text:
            return {"has_content": False, "confidence": 0.0, "signals": []}
        
        signals: List[Dict[str, Any]] = []
        total_matches = 0
        
        for category, patterns in PepeluValidator.CYBERSECURITY_INDICATORS.items():
            category_matches = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                if matches > 0:
                    category_matches += matches
                    total_matches += matches
            
            if category_matches > 0:
                signals.append({
                    "category": category,
                    "strength": category_matches,
                    "relevance": min(category_matches / 10, 1.0)  # Cap at 1.0
                })
        
        # Calculate confidence score
        word_count = len(text.split())
        signal_density = total_matches / word_count if word_count > 0 else 0
        confidence = min(signal_density * 100, 100.0)
        
        has_content = confidence > 3.0  # Lower threshold for broader detection
        
        return {
            "has_content": has_content,
            "confidence": round(confidence, 2),
            "signals": signals,
            "total_matches": total_matches,
            "rating": "High Relevance" if confidence > 20 else 
                     "Medium Relevance" if confidence > 10 else
                     "Low Relevance" if confidence > 3 else
                     "No Relevance"
        }

class SystemLogger:
    """Professional logging system."""
    
    @staticmethod
    def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Setup logger with professional formatting."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Custom formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger

class TextProcessor:
    """Professional text processing utilities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text of artifacts and normalize formatting."""
        if not text:
            return ""
        
        # Remove control characters and artifacts
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Clean up excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{3,}', '---', text)
        
        return text.strip()
    
    @staticmethod
    def create_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for better retrieval."""
        if not text or len(text) <= chunk_size:
            return [text] if text else []
        
        chunks: List[str] = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Find natural breakpoints for better chunking
            if end < len(text):
                # Seek sentence boundaries
                break_point = text.rfind('.', start + chunk_size - 100, end)
                if break_point == -1:
                    break_point = text.rfind('!', start + chunk_size - 100, end)
                if break_point == -1:
                    break_point = text.rfind('?', start + chunk_size - 100, end)
                if break_point == -1:
                    break_point = text.rfind(' ', start + chunk_size - 50, end)
                
                if break_point != -1 and break_point > start:
                    end = break_point + 1
            
            chunk = text[start:end].strip()
            if chunk and len(chunk) > 10:  # Filter out small fragments
                chunks.append(chunk)
            
            # Advance with overlap
            start = max(start + 1, end - overlap)
            
            if start >= len(text):
                break
        
        return chunks
    
    @staticmethod
    def extract_metadata(file_path: Path, content: str) -> Dict[str, Any]:
        """Extract file and content metadata."""
        cybersec_analysis = PepeluValidator.detect_cybersecurity_content(content)
        
        metadata: Dict[str, Any] = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "file_extension": file_path.suffix.lower(),
            "content_length": len(content),
            "word_count": len(content.split()) if content else 0,
            "file_hash": TextProcessor._generate_file_hash(file_path),
            "processed_timestamp": datetime.now().isoformat(),
            "cybersecurity_analysis": cybersec_analysis,
            "content_signature": TextProcessor._generate_content_signature(content)
        }
        
        # Add temporal metadata
        try:
            stat = file_path.stat()
            # Try to use st_birthtime first (creation time), fallback to st_ctime if not available
            try:
                metadata["created"] = datetime.fromtimestamp(stat.st_birthtime).isoformat()
            except AttributeError:
                # Fallback for systems that don't support st_birthtime
                # Using st_ctime as fallback (suppress deprecation warning as it's intentional)
                metadata["created"] = datetime.fromtimestamp(stat.st_ctime).isoformat()  # type: ignore[misc]
            metadata["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception:
            pass
        
        return metadata
    
    @staticmethod
    def _generate_file_hash(file_path: Path) -> str:
        """Generate hash for file identity verification."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def _generate_content_signature(content: str) -> str:
        """Generate a content signature for analysis."""
        if not content:
            return "empty"
        
        # Create a signature based on content characteristics
        word_count = len(content.split())
        char_count = len(content)
        unique_words = len(set(content.lower().split()))
        
        signature_components = [
            f"words:{word_count}",
            f"chars:{char_count}", 
            f"unique:{unique_words}",
            f"ratio:{unique_words/word_count:.2f}" if word_count > 0 else "ratio:0"
        ]
        
        return "|".join(signature_components)

class SystemConstants:
    """System constants for PepeluGPT operations."""
    
    # System messages
    SYSTEM_GREETING = "PepeluGPT Professional Cybersecurity Intelligence Platform"
    ACTIVATION_MESSAGE = "System initialized and ready."
    QUERY_PROMPT = "Enter your cybersecurity query:"
    
    # Status indicators
    STATUS_ICONS = {
        "ready": "🟢",
        "processing": "🔵", 
        "error": "🔴",
        "warning": "🔴",
        "success": "🟢",
        "info": "�"
    }
    
    # Default thresholds
    SIMILARITY_THRESHOLD = 0.5
    CYBERSEC_CONFIDENCE_THRESHOLD = 3.0
    MIN_CHUNK_SIZE = 10
    MAX_CHUNK_SIZE = 2000
    
    # Professional messages
    HELP_MESSAGES = [
        "Professional cybersecurity intelligence at your service.",
        "Accurate analysis based on processed documentation.",
        "Comprehensive cybersecurity guidance and compliance support.",
        "Enterprise-grade security intelligence platform.",
        "Reliable cybersecurity knowledge base and analysis."
    ]
