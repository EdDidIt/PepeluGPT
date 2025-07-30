#!/usr/bin/env python3
"""
Personality Router - Central personality selection and management.
Implements the modular personality system for PepeluGPT.
"""

from typing import Dict, Optional, List, Any
from datetime import datetime
from .base import PersonalityMode, BasePersonality
from .oracle import OracleMode
from .compliance import ComplianceMode
from .professional import ProfessionalMode


class PersonalityRouter:
    """Routes requests to appropriate personality modes."""
    
    def __init__(self):
        self._personalities: Dict[PersonalityMode, BasePersonality] = {
            PersonalityMode.ORACLE: OracleMode(),
            PersonalityMode.COMPLIANCE: ComplianceMode(),
            PersonalityMode.PROFESSIONAL: ProfessionalMode()
        }
        self._current_mode: PersonalityMode = PersonalityMode.PROFESSIONAL
        self.mode_history: List[Dict[str, Any]] = []
    
    def get_personality(self, mode: PersonalityMode) -> BasePersonality:
        """Get personality instance by mode."""
        return self._personalities.get(mode, self._personalities[PersonalityMode.PROFESSIONAL])
    
    def switch_mode(self, mode: PersonalityMode) -> str:
        """Switch to specified personality mode."""
        if mode in self._personalities:
            old_mode = self._current_mode
            self._current_mode = mode
            self.mode_history.append({
                'from': old_mode,
                'to': mode,
                'timestamp': datetime.now()
            })
            
            return self._personalities[mode].get_greeting()
        else:
            return f"🔴 Unknown personality mode: {mode}"
    
    def get_current_personality(self) -> Optional[BasePersonality]:
        """Get the current active personality."""
        return self._personalities.get(self._current_mode)
    
    def get_current_mode(self) -> PersonalityMode:
        """Get the current personality mode."""
        return self._current_mode
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response using current personality."""
        personality = self.get_current_personality()
        if personality:
            return personality.format_response(content, query, metadata)
        return content
    
    def get_system_prompt(self) -> str:
        """Get system prompt for current personality."""
        personality = self.get_current_personality()
        if personality:
            return personality.get_system_prompt()
        return "You are PepeluGPT, a professional cybersecurity assistant."
    
    def list_available_modes(self) -> List[PersonalityMode]:
        """List all available personality modes."""
        return list(self._personalities.keys())
    
    def get_mode_info(self) -> Dict[str, Any]:
        """Get information about current mode and available modes."""
        return {
            'current_mode': self._current_mode.value,
            'available_modes': [mode.value for mode in self._personalities.keys()],
            'history_count': len(self.mode_history),
            'current_personality_class': self.get_current_personality().__class__.__name__
        }
    
    def reset_to_default(self) -> str:
        """Reset to professional mode."""
        return self.switch_mode(PersonalityMode.PROFESSIONAL)


# Global router instance
_router_instance: Optional[PersonalityRouter] = None

def get_router() -> PersonalityRouter:
    """Get or create the global personality router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = PersonalityRouter()
    return _router_instance

def set_personality_mode(mode: PersonalityMode) -> str:
    """Convenience function to set personality mode."""
    router = get_router()
    return router.switch_mode(mode)

def get_current_personality() -> Optional[BasePersonality]:
    """Convenience function to get current personality."""
    router = get_router()
    return router.get_current_personality()

def format_response(content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
    """Convenience function to format response with current personality."""
    router = get_router()
    return router.format_response(content, query, metadata)
