#!/usr/bin/env python3
"""
Personality Router - Central personality selection and management.
Implements the modular personality system for PepeluGPT.
"""

from typing import Dict, Optional, List
from datetime import datetime
from .base_personality import PersonalityMode, BasePersonality
from .oracle_mode import OracleMode
from .compliance_mode import ComplianceMode
from .cosmic_mode import CosmicMode


class PersonalityRouter:
    """Routes requests to appropriate personality modes."""
    
    def __init__(self):
        self._personalities = {
            PersonalityMode.ORACLE: OracleMode(),
            PersonalityMode.COMPLIANCE: ComplianceMode(),
            PersonalityMode.COSMIC: CosmicMode()
        }
        self._current_mode = PersonalityMode.ORACLE
        self.mode_history = []
    
    def get_personality(self, mode: PersonalityMode) -> BasePersonality:
        """Get personality instance by mode."""
        return self._personalities.get(mode, self._personalities[PersonalityMode.ORACLE])
    
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
            
            if mode == PersonalityMode.DEFAULT:
                return "🔄 **Switched to Default Mode** - Standard PepeluGPT responses"
            else:
                return self._personalities[mode].get_greeting()
        else:
            return f"❌ Unknown personality mode: {mode}"
    
    def get_current_personality(self) -> Optional[BasePersonality]:
        """Get the current active personality."""
        if self._current_mode in self._personalities:
            return self._personalities[self._current_mode]
        return None
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict] = None) -> str:
        """Format response using current personality."""
        personality = self.get_current_personality()
        if personality:
            return personality.format_response(content, query, metadata)
        return content
    
    def auto_detect_mode(self, query: str) -> PersonalityMode:
        """Auto-detect personality mode based on query keywords."""
        query_lower = query.lower()
        
        # Compliance keywords
        compliance_keywords = ["audit", "control", "framework", "risk", "policy", "compliance"]
        if any(keyword in query_lower for keyword in compliance_keywords):
            return PersonalityMode.COMPLIANCE
            
        # Cosmic keywords  
        cosmic_keywords = ["quantum", "dimension", "possibility", "consciousness", "cosmic"]
        if any(keyword in query_lower for keyword in cosmic_keywords):
            return PersonalityMode.COSMIC
            
        # Default to Oracle
        return PersonalityMode.ORACLE
    
    def get_available_modes(self) -> List[str]:
        """Get list of available personality modes."""
        return [mode.value for mode in PersonalityMode]
    
    def get_mode_status(self) -> str:
        """Get current mode status."""
        if self._current_mode == PersonalityMode.DEFAULT:
            return "🤖 **Current Mode:** Default"
        
        personality = self.get_current_personality()
        if personality:
            active_time = datetime.now() - personality.active_since
            minutes = int(active_time.total_seconds() / 60)
            return f"🎭 **Current Mode:** {self._current_mode.value.title()} (Active: {minutes}m)"
        
        return "❓ **Current Mode:** Unknown"


# Global personality router instance
personality_router = PersonalityRouter()


def switch_personality_mode(mode_name: str) -> str:
    """Switch personality mode by name."""
    try:
        mode = PersonalityMode(mode_name.lower())
        return personality_router.switch_mode(mode)
    except ValueError:
        available = ", ".join(personality_router.get_available_modes())
        return f"❌ Invalid mode '{mode_name}'. Available: {available}"


def get_personality_help() -> str:
    """Get help text for personality modes."""
    return """
🎭 **PepeluGPT Response Personalities**

**Available Modes:**
• `/mode oracle` - 🔮 Deep, mystical insights with cosmic wisdom
• `/mode compliance` - 📊 Precise audit-ready analysis with risk focus  
• `/mode cosmic` - 🌠 Creative, inspirational responses with spiritual flow
• `/mode default` - 🤖 Standard PepeluGPT responses

**Commands:**
• `/mode [name]` - Switch personality mode
• `/mode status` - Show current mode and duration
• `/mode help` - Show this help message

Each mode channels a different facet of the cyber warrior spirit! 🛡️✨
"""
