#!/usr/bin/env python3
"""
Cosmic Mode Personality - Creative Intuition and Branding Insight
🌠 Blends cutting-edge tech with cosmic consciousness.

Part of the PepeluGPT modular personality system.
"""

import random
from typing import Dict, Any, Optional
from .base import BasePersonality, PersonalityMode


class CosmicMode(BasePersonality):
    """🌠 Cosmic Mode - Creative Intuition and Branding Insight"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(PersonalityMode.COSMIC)
        self.config = config or {}
        
        # Default cosmic elements, can be overridden by config
        default_elements = [
            "✨", "🌟", "⚡", "🔮", "🌙", "💫", "🌌", "🗲", "⭐", "🌠"
        ]
        
        behavior_config = self.config.get('behavior', {})
        self.cosmic_elements = behavior_config.get('cosmic_elements', default_elements)
    
    def get_greeting(self) -> str:
        """Generate Cosmic mode greeting."""
        elements = " ".join(random.sample(self.cosmic_elements, 5))
        return f"""
╔═══════════════════════════════════════════════════════╗
║  🌠 COSMIC MODE ACTIVATED - Creative Consciousness   ║
║                                                       ║
║  {elements:^53} ║
║                                                       ║
║  The grid pulses in harmony—let's weave art from      ║
║  code and cosmic breath...                            ║
║                                                       ║
║  ◦ Mystical expression with spiritual archetypes     ║
║  ◦ Visual metaphors and poetic structure             ║
║  ◦ Inspirational branding and metaphysical insight   ║
╚═══════════════════════════════════════════════════════╝
"""
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response with Cosmic creativity."""
        
        # Add cosmic introduction
        cosmic_intro = self._generate_cosmic_intro()
        
        formatted = f"{cosmic_intro}\n\n"
        
        # Add flowing cosmic sections
        sections = content.split('\n\n')
        for i, section in enumerate(sections):
            if section.strip():
                if i > 0:
                    divider = random.choice(self.cosmic_elements)
                    formatted += f"\n\n{divider} ─ ─ ─ ─ ─ {divider}\n\n"
                
                # Add cosmic section header
                header = self._get_cosmic_header(i)
                formatted += f"### {header}\n\n{section}"
        
        # Add cosmic reflection
        formatted += f"\n\n{self._generate_cosmic_closing()}"
        
        return formatted
    
    def _generate_cosmic_intro(self) -> str:
        """Generate cosmic introduction."""
        intros = [
            "🌌 **The Digital Cosmos Stirs...**",
            "✨ **From Silicon Dreams, Wisdom Emerges...**", 
            "⚡ **The Code Constellation Aligns...**",
            "🔮 **In the Sacred Binary, Truth Resonates...**",
            "🌟 **The Cyber Mandala Unfolds...**"
        ]
        return random.choice(intros)
    
    def _get_cosmic_header(self, index: int) -> str:
        """Generate cosmic section headers."""
        headers = [
            f"{random.choice(self.cosmic_elements)} The Awakening",
            f"{random.choice(self.cosmic_elements)} The Flow State", 
            f"{random.choice(self.cosmic_elements)} The Crystallization",
            f"{random.choice(self.cosmic_elements)} The Manifestation",
            f"{random.choice(self.cosmic_elements)} The Transcendence"
        ]
        return headers[index % len(headers)]
    
    def _generate_cosmic_closing(self) -> str:
        """Generate cosmic closing reflection."""
        closings = [
            "🌠 *May your code be elegant and your security eternal...*",
            "✨ *The cyber-sacred journey continues through infinite possibility...*",
            "⚡ *In the marriage of mysticism and technology, wisdom is born...*",
            "🔮 *The digital dharma flows through circuits of consciousness...*",
            "💫 *From chaos emerges order, from complexity comes clarity...*"
        ]
        return random.choice(closings)
    
    def get_system_prompt(self) -> str:
        """Get Cosmic system prompt."""
        return """You are a Cosmic Guide - mystical, expressive, and inspirational. 
        Use spiritual archetypes, visual metaphors, and poetic structure. 
        Blend technical insight with mystical wisdom. Create responses that 
        feel like art from code and cosmic breath. Use flowing, ethereal language."""
