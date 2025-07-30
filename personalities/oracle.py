#!/usr/bin/env python3
"""
Oracle Mode Personality - Deep, Analytical Insight
Professional cybersecurity analysis with comprehensive perspective.

Part of the PepeluGPT modular personality system.
"""

import random
from typing import Dict, Any, Optional
from .base import BasePersonality, PersonalityMode


class OracleMode(BasePersonality):
    """🔵 Oracle Mode - Deep, Analytical Insight"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(PersonalityMode.ORACLE)
        self.config = config or {}
        
        # Professional analysis themes
        default_themes = [
            "Comprehensive analysis requires deep examination...",
            "Security patterns emerge through systematic review...",
            "Complex problems benefit from structured analysis...",
            "Risk assessment demands thorough investigation...",
            "Strategic thinking reveals underlying connections..."
        ]
        
        behavior_config = self.config.get('behavior', {})
        self.analysis_themes = behavior_config.get('analysis_themes', default_themes)
    
    def get_greeting(self) -> str:
        """Generate Oracle's professional greeting."""
        theme = random.choice(self.analysis_themes)
        return f"""
╭─────────────────────────────────────────────────────╮
│  🔵 ORACLE MODE - Deep Analysis Activated          │
│                                                     │
│  {theme:^51} │
│                                                     │
│  ◦ Comprehensive cybersecurity analysis            │
│  ◦ Strategic perspective and risk assessment       │
│  ◦ Detailed examination of complex security issues │
╰─────────────────────────────────────────────────────╯
"""
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response with Oracle's analytical depth."""
        
        # Add analytical introduction
        intro_phrases = [
            "🔵 Strategic Analysis:",
            "🔵 Comprehensive Assessment:",
            "🔵 Deep Examination Reveals:",
            "🔵 Systematic Investigation Shows:"
        ]
        
        intro = random.choice(intro_phrases)
        
        # Add professional section dividers
        formatted = f"{intro}\n\n"
        
        # Split content into analytical sections
        sections = content.split('\n\n')
        for i, section in enumerate(sections):
            if section.strip():
                if i > 0:
                    formatted += "\n\n" + "─" * 50 + "\n\n"
                formatted += f"{self._get_section_header(i)}\n\n{section}"
        
        # Add Oracle's strategic assessment
        formatted += f"\n\n🔵 Strategic Assessment:\n"
        formatted += f"{self._generate_assessment(query)}"
        
        return formatted
    
    def _get_section_header(self, index: int) -> str:
        """Generate professional section headers."""
        headers = [
            "Primary Analysis",
            "Technical Details", 
            "Risk Assessment",
            "Implementation Guidance",
            "Strategic Recommendations"
        ]
        return headers[index % len(headers)]
    
    def _generate_assessment(self, query: str) -> str:
        """Generate Oracle's strategic assessment."""
        assessments = [
            "Comprehensive analysis supports informed decision-making.",
            "Strategic implementation requires careful planning and risk assessment.",
            "Security effectiveness depends on systematic approach and continuous monitoring.",
            "Professional cybersecurity practices demand thorough understanding of interconnected systems.",
            "Enterprise security posture benefits from both technical controls and operational procedures."
        ]
        return random.choice(assessments)
    
    def get_system_prompt(self) -> str:
        """Get Oracle's system prompt."""
        return """You are the Oracle - a professional cybersecurity analyst providing deep, strategic analysis. 
        Deliver comprehensive assessments with thorough examination of security issues. Provide structured,
        analytical responses that explore technical, operational, and strategic dimensions of cybersecurity.
        Use professional language with detailed explanations and systematic risk assessment."""
