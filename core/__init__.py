"""
PepeluGPT Core Module
=====================

Central nervous system of PepeluGPT containing main application logic,
orchestration, and core utilities.

Modules:
    - orchestrator: Central coordinator for all system components
    - pepelugpt: Main application entry point and CLI interface  
    - pepelugpt_engine: Core engine with business logic implementation
    - security: Security validation and compliance enforcement
    - utilities: Shared utility functions and helper classes
"""

from .orchestrator import *
from .pepelugpt_engine import *
from .utilities import *
from .security import *

__version__ = "2.0.0"
__author__ = "PepeluGPT Team"
