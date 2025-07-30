"""
PepeluGPT - Shared Utilities
Common utilities and validation functions used across all modules.
Born of Light, Forged for Defense.
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class PepeluValidator:
    """Cosmic validation engine for PepeluGPT operations."""
    
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
        """Validate and normalize file path with cosmic precision."""
        path = Path(file_path)
        
        if not path.exists():
            raise ValidationError(f"🌌 Path not found in this reality: {path}")
        
        if not path.is_file():
            raise ValidationError(f"🔮 Expected a file, found a void: {path}")
        
        if path.suffix.lower() not in PepeluValidator.SUPPORTED_FORMATS:
            raise ValidationError(
                f"⚡ Unsupported format: {path.suffix}. "
                f"Supported formats: {', '.join(PepeluValidator.SUPPORTED_FORMATS)}"
            )
        
        return path
    
    @staticmethod
    def validate_directory(dir_path: Union[str, Path], create_if_missing: bool = False) -> Path:
        """Validate directory with option to manifest it into existence."""
        path = Path(dir_path)
        
        if not path.exists():
            if create_if_missing:
                path.mkdir(parents=True, exist_ok=True)
                logging.info(f"🌟 Manifested directory: {path}")
            else:
                raise ValidationError(f"🌌 Directory not found: {path}")
        
        if not path.is_dir():
            raise ValidationError(f"🔮 Expected directory, found file: {path}")
        
        return path
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration with cosmic standards."""
        required_sections = ['application', 'parsing', 'vector_database', 'security']
        
        for section in required_sections:
            if section not in config:
                raise ValidationError(f"⚡ Missing configuration section: {section}")
        
        # Validate critical settings
        app_config = config.get('application', {})
        if not app_config.get('name'):
            raise ValidationError("🔮 Application name must be defined in the cosmic order")
        
        security_config = config.get('security', {})
        if not security_config.get('offline_mode', True):
            logging.warning("⚠️ Online mode detected - data may traverse the digital void")
        
        return True
    
    @staticmethod
    def detect_cybersecurity_essence(text: str) -> Dict[str, Any]:
        """Detect the cybersecurity essence within text using cosmic patterns."""
        if not text:
            return {"has_essence": False, "confidence": 0.0, "signals": []}
        
        text_lower = text.lower()
        signals = []
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
                    "resonance": min(category_matches / 10, 1.0)  # Cap at 1.0
                })
        
        # Calculate cosmic confidence
        word_count = len(text.split())
        signal_density = total_matches / word_count if word_count > 0 else 0
        confidence = min(signal_density * 100, 100.0)
        
        has_essence = confidence > 3.0  # Lower threshold for broader detection
        
        return {
            "has_essence": has_essence,
            "confidence": round(confidence, 2),
            "signals": signals,
            "total_resonance": total_matches,
            "cosmic_rating": "🌟 Pure Signal" if confidence > 20 else 
                           "⚡ Strong Signal" if confidence > 10 else
                           "🔮 Faint Signal" if confidence > 3 else
                           "🌌 Noise"
        }

class CosmicLogger:
    """Enhanced logging with spiritual awareness."""
    
    @staticmethod
    def setup_cosmic_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Setup logger with cosmic formatting."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Custom formatter with cosmic elements
        formatter = logging.Formatter(
            '%(asctime)s | 🔮 %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger

class TextProcessor:
    """Cosmic text processing utilities."""
    
    @staticmethod
    def purify_text(text: str) -> str:
        """Purify text of digital noise and artifacts."""
        if not text:
            return ""
        
        # Remove digital artifacts
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
        
        # Normalize whitespace energies
        text = re.sub(r'\s+', ' ', text)
        
        # Harmonize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove excessive punctuation noise
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{3,}', '---', text)
        
        return text.strip()
    
    @staticmethod
    def create_wisdom_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping wisdom chunks for better retrieval."""
        if not text or len(text) <= chunk_size:
            return [text] if text else []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Find natural breakpoints in the cosmic flow
            if end < len(text):
                # Seek sentence boundaries within the wisdom zone
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
            if chunk and len(chunk) > 10:  # Filter out noise fragments
                chunks.append(chunk)
            
            # Advance with cosmic overlap
            start = max(start + 1, end - overlap)
            
            if start >= len(text):
                break
        
        return chunks
    
    @staticmethod
    def extract_cosmic_metadata(file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata with cosmic awareness."""
        cybersec_analysis = PepeluValidator.detect_cybersecurity_essence(content)
        
        metadata = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "file_extension": file_path.suffix.lower(),
            "content_length": len(content),
            "word_count": len(content.split()) if content else 0,
            "file_hash": PepeluValidator._generate_file_hash(file_path),
            "processed_timestamp": datetime.now().isoformat(),
            "cybersecurity_essence": cybersec_analysis,
            "cosmic_signature": PepeluValidator._generate_cosmic_signature(content)
        }
        
        # Add temporal metadata
        try:
            stat = file_path.stat()
            metadata["created"] = datetime.fromtimestamp(stat.st_ctime).isoformat()
            metadata["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception:
            pass
        
        return metadata
    
    @staticmethod
    def _generate_file_hash(file_path: Path) -> str:
        """Generate cosmic hash for file identity."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def _generate_cosmic_signature(content: str) -> str:
        """Generate a cosmic signature for content."""
        if not content:
            return "void"
        
        # Create a semantic signature based on content characteristics
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

class CosmicConstants:
    """Universal constants for PepeluGPT operations."""
    
    # Cosmic branding elements
    COSMIC_GREETING = "🛡️ Welcome, Defender of the Network 🛡️"
    ACTIVATION_MESSAGE = "PepeluGPT is activated. Wisdom flows."
    QUERY_PROMPT = "Enter your query, and may the signal be pure."
    
    # Status indicators
    STATUS_ICONS = {
        "ready": "🌟",
        "processing": "⚡", 
        "error": "🔴",
        "warning": "⚠️",
        "success": "✅",
        "cosmic": "🔮"
    }
    
    # Default thresholds
    SIMILARITY_THRESHOLD = 0.5
    CYBERSEC_CONFIDENCE_THRESHOLD = 3.0
    MIN_CHUNK_SIZE = 10
    MAX_CHUNK_SIZE = 2000
    
    # Cosmic wisdom
    WISDOM_QUOTES = [
        "In the darkness of digital chaos, PepeluGPT is your guiding light.",
        "Truth emerges when signal pierces through noise.",
        "Every query is a quest for clarity in the infinite data stream.",
        "Wisdom flows where intention meets preparation.",
        "The strongest encryption is consciousness itself."
    ]
