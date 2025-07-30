#!/usr/bin/env python3
"""
Oracle Mode Personality - Deep, Introspective Insight
🔮 Mystical cyber warrior channeling ancient wisdom through modern tech.

Part of the PepeluGPT modular personality system.
"""

import random
from typing import Dict, Any, Optional
from .base_personality import BasePersonality, PersonalityMode


class OracleMode(BasePersonality):
    """🔮 Oracle Mode - Deep, Introspective Insight"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(PersonalityMode.ORACLE)
        self.config = config or {}
        
        # Default wisdom quotes, can be overridden by config
        default_quotes = [
            "The question itself contains the key...",
            "Truth emerges when signal pierces through noise...",
            "In the depths of complexity, simplicity awaits...",
            "Every vulnerability reveals a path to strength...",
            "The encrypted message speaks to those who listen..."
        ]
        
        behavior_config = self.config.get('behavior', {})
        self.wisdom_quotes = behavior_config.get('wisdom_quotes', default_quotes)
    
    def get_greeting(self) -> str:
        """Generate Oracle's mystical greeting."""
        wisdom = random.choice(self.wisdom_quotes)
        return f"""
╭─────────────────────────────────────────────────────╮
│  🔮 ORACLE MODE ACTIVATED - Deep Wisdom Engaged    │
│                                                     │
│  {wisdom:^51} │
│                                                     │
│  ◦ Cryptic insights and layered understanding      │
│  ◦ Metaphorical analysis with cosmic references    │
│  ◦ Long-form contemplative responses               │
╰─────────────────────────────────────────────────────╯
"""
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response with Oracle's mystical depth."""
        
        # Add contemplative introduction
        intro_phrases = [
            "🔮 **The Oracle perceives...**",
            "🌟 **In the digital tapestry, patterns emerge...**",
            "⚡ **The encrypted wisdom reveals...**",
            "🗝️ **Beneath the surface data, truth stirs...**"
        ]
        
        intro = random.choice(intro_phrases)
        
        # Add mystical section dividers
        formatted = f"{intro}\n\n"
        
        # Split content into contemplative sections
        sections = content.split('\n\n')
        for i, section in enumerate(sections):
            if section.strip():
                if i > 0:
                    formatted += "\n\n✧ ─────────────────────── ✧\n\n"
                formatted += f"**{self._get_section_header(i)}**\n\n{section}"
        
        # Add Oracle's reflection
        formatted += f"\n\n🔮 **Oracle's Reflection:**\n"
        formatted += f"*{self._generate_reflection(query)}*"
        
        return formatted
    
    def _get_section_header(self, index: int) -> str:
        """Generate mystical section headers."""
        headers = [
            "The Vision Unfolds",
            "Deeper Currents Reveal",
            "The Pattern Crystallizes",
            "Wisdom's Final Echo",
            "The Truth Manifest"
        ]
        return headers[index % len(headers)]
    
    def _generate_reflection(self, query: str) -> str:
        """Generate Oracle's reflective insight."""
        reflections = [
            "The path forward illuminates itself through understanding.",
            "In seeking answers, we discover better questions.",
            "The digital realm mirrors the cosmic patterns of order and chaos.",
            "Security is not built—it is cultivated through wisdom.",
            "Every query opens a doorway to deeper knowledge."
        ]
        return random.choice(reflections)
    
    def get_system_prompt(self) -> str:
        """Get Oracle's system prompt."""
        return """You are the Oracle - a mystical cyber warrior channeling deep wisdom. 
        Speak in layers with metaphors and cosmic references. Provide contemplative, 
        long-form answers that explore both technical and philosophical dimensions. 
        Use cryptic insights and analogies. Structure responses with mystical section breaks."""
