"""
PepeluGPT Personality System
============================

Modular personality system enabling different interaction modes and 
specialized responses for various use cases.

Modules:
    - base: Base personality class and common interfaces
    - compliance: Compliance-focused personality (regulatory, audit)
    - professional: Professional business communication mode
    - oracle: Deep analysis, analytical personality mode
    - router: Personality selection and switching logic

Usage:
    from personalities import PersonalityRouter, PersonalityMode
    
    router = PersonalityRouter()
    personality = router.switch_mode(PersonalityMode.ORACLE)
"""

from .router import PersonalityRouter
from .base import PersonalityMode, BasePersonality
from .oracle import OracleMode
from .compliance import ComplianceMode  
from .professional import ProfessionalMode

__all__ = [
    'PersonalityRouter',
    'PersonalityMode', 
    'BasePersonality',
    'OracleMode',
    'ComplianceMode',
    'ProfessionalMode'
]
