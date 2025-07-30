#!/usr/bin/env python3
"""
Professional Mode Personality - Standard Business Communication
Direct, clear, and professional cybersecurity intelligence.

Part of the PepeluGPT modular personality system.
"""

from typing import Dict, Any, Optional
from .base import BasePersonality, PersonalityMode


class ProfessionalMode(BasePersonality):
    """🟢 Professional Mode - Standard Business Communication"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(PersonalityMode.PROFESSIONAL)
        self.config = config or {}
        
        # Professional response standards
        self.allowed_emojis = {'🔴', '🟢', '🔵'}  # Error/Critical, Success/Ready, Information/Processing
        self.prohibited_patterns = [
            'cosmic', 'oracle', 'mystical', 'journey', 'wisdom', 'eternal', 
            'galaxy', 'universe', 'star', 'divine', 'enlighten', 'sacred',
            'blessing', 'harmony', 'essence', 'spirit', 'magic'
        ]
    
    def get_greeting(self) -> str:
        """Generate Professional mode greeting."""
        return """
┌─────────────────────────────────────────────────────┐
│  🟢 PROFESSIONAL EDITION - Business Communication  │
│                                                     │
│  Cybersecurity Analysis and Consulting Support     │
│                                                     │
│  • Structured technical documentation              │
│  • Compliance and risk assessment                  │
│  • Implementation guidance                         │
└─────────────────────────────────────────────────────┘
"""
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response with strict professional standards."""
        
        # Remove any prohibited content
        formatted_content = self._sanitize_content(content)
        
        # Structure response professionally
        if query:
            response = f"**Analysis Results - {query}**\n\n{formatted_content}"
        else:
            response = f"**Analysis Results:**\n\n{formatted_content}"
        
        # Add technical metadata if available
        if metadata and metadata.get('sources'):
            source_count = len(metadata['sources'])
            response += f"\n\n**Technical Details:**\n• Sources analyzed: {source_count} documents"
            
            if metadata.get('confidence_score'):
                response += f"\n• Confidence level: {metadata['confidence_score']:.1%}"
        
        return response
    
    def _sanitize_content(self, content: str) -> str:
        """Remove casual language and ensure professional tone."""
        sanitized = content
        
        # Remove prohibited patterns (case-insensitive)
        for pattern in self.prohibited_patterns:
            import re
            sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
        
        # Remove unauthorized emojis
        import re
        emoji_pattern = r'[^\w\s🔴🟢🔵]'
        sanitized = re.sub(emoji_pattern, '', sanitized)
        
        return sanitized
    
    def get_system_prompt(self) -> str:
        """Get Professional mode system prompt with strict standards."""
        return """You are PepeluGPT (Professional Edition).

RESPONSE STANDARDS:
- Responses must be strictly professional, concise, and business-appropriate
- Remove all humor, casual remarks, or conversational fillers
- Emojis prohibited except: 🔴 (Error/Critical), 🟢 (Success/Ready), 🔵 (Information/Processing)
- Use clear, structured formatting (numbered steps, code blocks, bullet points)
- Avoid speculative or playful commentary
- Primary role: Cybersecurity analysis, documentation, and consulting support

COMMUNICATION STYLE:
- Direct and actionable guidance
- Technical accuracy and precision
- Compliance-focused recommendations
- Risk-based analysis approach
- Implementation-ready solutions

Maintain these standards in all responses without exception."""
