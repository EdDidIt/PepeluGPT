"""
Utility functions for PepeluGPT core functionality.
"""

import logging

from core.logging_config import get_logger as get_enhanced_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance - delegates to enhanced logging system."""
    return get_enhanced_logger(name)
