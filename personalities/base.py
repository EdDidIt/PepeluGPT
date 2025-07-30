#!/usr/bin/env python3
"""
Base Personality Module - Abstract interface for all personality modes.
Following PepeluGPT naming conventions and modular design.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class PersonalityMode(Enum):
    """Available response personality modes."""
    ORACLE = "oracle"
    COMPLIANCE = "compliance" 
    PROFESSIONAL = "professional"
    DEFAULT = "default"


class BasePersonality(ABC):
    """Abstract base class for response personality modules."""
    
    def __init__(self, mode: PersonalityMode):
        self.mode = mode
        self.active_since = datetime.now()
        self.config: Dict[str, Any] = {}
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update personality configuration."""
        self.config.update(config)
    
    @abstractmethod
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response according to personality style."""
        pass
    
    @abstractmethod
    def get_greeting(self) -> str:
        """Get personality-specific greeting."""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get personality-specific system prompt."""
        pass
