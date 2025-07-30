"""
File Parser Utilities
Common utilities and helper functions for document parsing operations.
"""

import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that interfere with processing
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for better retrieval."""
    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks: List[str] = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Find a good break point (sentence boundary)
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            break_point = text.rfind('.', start + chunk_size - 100, end)
            if break_point == -1:
                break_point = text.rfind(' ', start + chunk_size - 50, end)
            if break_point != -1 and break_point > start:
                end = break_point + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Set start position for next chunk with overlap
        start = max(start + 1, end - overlap)
        
        # Prevent infinite loops
        if start >= len(text):
            break
    
    return chunks

def generate_file_hash(file_path: Path) -> str:
    """Generate MD5 hash of file for change detection."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return ""

def extract_metadata(file_path: Path, content: str) -> Dict[str, Any]:
    """Extract metadata from file and content."""
    metadata: Dict[str, Any] = {
        "filename": file_path.name,
        "file_path": str(file_path),
        "file_size": file_path.stat().st_size if file_path.exists() else 0,
        "file_extension": file_path.suffix.lower(),
        "content_length": len(content),
        "word_count": len(content.split()) if content else 0,
        "file_hash": generate_file_hash(file_path),
        "processed_timestamp": datetime.now().isoformat()
    }
    
    # Try to extract creation/modification times
    try:
        stat = file_path.stat()
        # Use st_birthtime if available (newer systems), fallback to st_ctime
        if hasattr(stat, 'st_birthtime'):
            metadata["created"] = datetime.fromtimestamp(stat.st_birthtime).isoformat()
        else:
            metadata["created"] = datetime.fromtimestamp(stat.st_ctime).isoformat()  # type: ignore
        metadata["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
    except Exception:
        pass
    
    return metadata

def detect_cybersecurity_content(text: str) -> Dict[str, Any]:
    """Detect cybersecurity-specific content and patterns."""
    if not text:
        return {"is_cybersecurity": False, "confidence": 0.0, "indicators": []}
    
    # Cybersecurity keywords and patterns
    cybersec_patterns = {
        "frameworks": [
            r'\bNIST\b', r'\bRMF\b', r'\bSTIG\b', r'\bCCE\b', r'\bCCI\b',
            r'\bISO 27001\b', r'\bSOC 2\b', r'\bFISMA\b'
        ],
        "controls": [
            r'\bAC-\d+\b', r'\bAU-\d+\b', r'\bCA-\d+\b', r'\bCM-\d+\b',
            r'\bCP-\d+\b', r'\bIA-\d+\b', r'\bIR-\d+\b', r'\bMA-\d+\b',
            r'\bMP-\d+\b', r'\bPE-\d+\b', r'\bPL-\d+\b', r'\bPS-\d+\b',
            r'\bRA-\d+\b', r'\bSA-\d+\b', r'\bSC-\d+\b', r'\bSI-\d+\b'
        ],
        "security_terms": [
            r'\bcybersecurity\b', r'\binformation security\b', r'\bvulnerability\b',
            r'\bthreat\b', r'\brisk assessment\b', r'\bencryption\b',
            r'\bauthentication\b', r'\bauthorization\b', r'\baudit\b'
        ],
        "compliance": [
            r'\bcompliance\b', r'\bauthorization\b', r'\bcertification\b',
            r'\baccreditation\b', r'\bATTO\b', r'\bCATO\b'
        ]
    }
    
    
    indicators: List[Dict[str, Any]] = []
    total_matches = 0
    
    for category, patterns in cybersec_patterns.items():
        category_matches = 0
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                category_matches += matches
                total_matches += matches
        
        if category_matches > 0:
            indicators.append({
                "category": category,
                "matches": category_matches
            })
    
    # Calculate confidence based on match density
    word_count = len(text.split())
    match_density = total_matches / word_count if word_count > 0 else 0
    confidence = min(match_density * 100, 100.0)  # Cap at 100%
    
    is_cybersecurity = confidence > 5.0  # 5% threshold
    
    return {
        "is_cybersecurity": is_cybersecurity,
        "confidence": round(confidence, 2),
        "indicators": indicators,
        "total_matches": total_matches
    }

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def validate_file_format(file_path: Path, expected_formats: List[str]) -> bool:
    """Validate if file format is supported."""
    file_extension = file_path.suffix.lower()
    return file_extension in [f.lower() if f.startswith('.') else f'.{f.lower()}' 
                             for f in expected_formats]

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe processing."""
    # Remove or replace problematic characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:255]  # Limit length

class ParsingStats:
    """Track parsing statistics across documents."""
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.total_files = 0
        self.successful_files = 0
        self.failed_files = 0
        self.total_size = 0
        self.total_chunks = 0
        self.cybersecurity_files = 0
        self.processing_time = 0.0
        self.errors: List[str] = []
    
    def add_file_result(self, success: bool, file_size: int = 0, 
                       chunks: int = 0, is_cybersec: bool = False, 
                       error: Optional[str] = None) -> None:
        """Add a file processing result."""
        self.total_files += 1
        self.total_size += file_size
        self.total_chunks += chunks
        
        if success:
            self.successful_files += 1
        else:
            self.failed_files += 1
            if error:
                self.errors.append(error)
        
        if is_cybersec:
            self.cybersecurity_files += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        success_rate = (self.successful_files / self.total_files * 100) if self.total_files > 0 else 0
        cybersec_rate = (self.cybersecurity_files / self.total_files * 100) if self.total_files > 0 else 0
        
        return {
            "total_files": self.total_files,
            "successful_files": self.successful_files,
            "failed_files": self.failed_files,
            "success_rate": round(success_rate, 1),
            "total_size_formatted": format_file_size(self.total_size),
            "total_chunks": self.total_chunks,
            "cybersecurity_files": self.cybersecurity_files,
            "cybersecurity_rate": round(cybersec_rate, 1),
            "processing_time": round(self.processing_time, 2),
            "errors": self.errors[:10]  # Limit to first 10 errors
        }
