#!/usr/bin/env python3
"""
PepeluGPT - Core Engine
Central logic and orchestration module for cybersecurity intelligence operations.

This module handles the core functionality including:
- Configuration management
- Component orchestration
- System health monitoring
- Security validation
"""

import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

class PepeluCore:
    """Central orchestration engine for PepeluGPT operations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the core engine with configuration."""
        self.config_path = config_path or "config/default_config.json"
        self.paths_config = "config/paths.yaml"
        self.config = self.load_config()
        self.paths = self.load_paths()
        self.logger = self.setup_logging()
        
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            return self.get_default_config()
        except json.JSONDecodeError as e:
            return self.get_default_config()
    
    def load_paths(self) -> Dict[str, str]:
        """Load path configuration from YAML file."""
        try:
            with open(self.paths_config, 'r') as f:
                paths = yaml.safe_load(f)
            return paths
        except FileNotFoundError:
            return self.get_default_paths()
    
    def setup_logging(self) -> logging.Logger:
        """Configure logging based on application settings."""
        logger = logging.getLogger('PepeluGPT')
        logger.setLevel(getattr(logging, self.config.get('logging', {}).get('level', 'INFO')))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler if enabled
        if self.config.get('logging', {}).get('enable_file_logging', True):
            log_dir = Path(self.paths.get('logs', './logs'))
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"pepelugpt_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if config file is unavailable."""
        return {
            "application": {"name": "PepeluGPT", "version": "1.0.0", "mode": "local"},
            "parsing": {"chunk_size": 1000, "chunk_overlap": 200},
            "vector_database": {"embedding_model": "sentence-transformers/all-MiniLM-L6-v2"},
            "chat": {"max_tokens": 2048, "temperature": 0.7},
            "logging": {"level": "INFO", "enable_file_logging": True},
            "security": {"offline_mode": True, "sanitize_inputs": True}
        }
    
    def get_default_paths(self) -> Dict[str, str]:
        """Return default paths if paths config is unavailable."""
        return {
            "cyber_documents": "./cyber_documents",
            "data": "./data",
            "vector_db": "./cyber_vector_db",
            "logs": "./logs",
            "core": "./core",
            "interface": "./interface"
        }
    
    def validate_environment(self) -> Dict[str, bool]:
        """Validate that all required components are available."""
        validation_results = {}
        
        # Check critical directories
        critical_paths = [
            'cyber_documents', 'data', 'vector_db', 'logs'
        ]
        
        for path_key in critical_paths:
            path = Path(self.paths.get(path_key, f'./{path_key}'))
            validation_results[f"dir_{path_key}"] = path.exists()
            if not path.exists():
                self.logger.warning(f"Missing directory: {path}")
        
        # Check for documents
        doc_path = Path(self.paths.get('cyber_documents', './cyber_documents'))
        if doc_path.exists():
            doc_count = len(list(doc_path.glob("*.*")))
            validation_results["documents_available"] = doc_count > 0
            self.logger.info(f"Found {doc_count} documents")
        else:
            validation_results["documents_available"] = False
        
        # Check vector database
        vector_path = Path(self.paths.get('vector_db', './cyber_vector_db'))
        validation_results["vector_db_ready"] = (
            vector_path.exists() and 
            (vector_path / "faiss_index.bin").exists()
        )
        
        return validation_results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        validation = self.validate_environment()
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "application": self.config.get("application", {}),
            "environment_validation": validation,
            "ready_for_chat": all([
                validation.get("documents_available", False),
                validation.get("vector_db_ready", False)
            ])
        }
        
        return status
    
    def initialize_directories(self) -> bool:
        """Create necessary directories if they don't exist."""
        try:
            for path_key, path_value in self.paths.items():
                if isinstance(path_value, str) and not path_value.endswith('.json'):
                    path = Path(path_value)
                    path.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Ensured directory exists: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize directories: {e}")
            return False
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key."""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_path(self, key: str) -> Path:
        """Get path object for a configured path."""
        path_str = self.paths.get(key, f'./{key}')
        return Path(path_str)

# Global core instance
core = None

def get_core() -> PepeluCore:
    """Get or create the global core instance."""
    global core
    if core is None:
        core = PepeluCore()
    return core

def initialize_pepelu_core(config_path: Optional[str] = None) -> PepeluCore:
    """Initialize and return the core engine."""
    global core
    core = PepeluCore(config_path)
    return core
