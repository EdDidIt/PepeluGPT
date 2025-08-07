"""
CLI module for PepeluGPT - Advanced Command Line Interface.

This module provides a comprehensive command-line interface for the PepeluGPT
cybersecurity assistant, including subcommands for chat, status, and configuration
management.

Available Commands:
- chat: Launch interactive chat session (default)
- status: Show system status and configuration
- config: Configuration management (validate, show, list)

Features:
- Mode switching (Adaptive vs Classic)
- Configuration validation
- JSON output support
- Comprehensive status reporting
- Debug logging
- Programmatic usage support
"""

from .args import parse_args
from .audit import handle_audit_command
from .commands import handle_config_command, handle_status_command
from .runner import load_config, resolve_mode, run_cli, setup_mode_and_config
from .utils import display_banner, get_mode_display_name, interactive_mode_selection

__version__ = "1.1.0"
__author__ = "PepeluGPT Team"

__all__ = [
    # Core CLI functions
    "parse_args",
    "run_cli",
    # Configuration & mode functions
    "load_config",
    "resolve_mode",
    "setup_mode_and_config",
    # UI utility functions
    "display_banner",
    "interactive_mode_selection",
    "get_mode_display_name",
    # Command handlers
    "handle_status_command",
    "handle_config_command",
    "handle_audit_command",
    # Metadata
    "__version__",
    "__author__",
]

from typing import Any

# CLI Information
CLI_INFO: dict[str, Any] = {
    "name": "PepeluGPT CLI",
    "version": __version__,
    "description": "Advanced command-line interface for PepeluGPT cybersecurity assistant",
    "commands": ["chat", "status", "config", "audit"],
    "modes": ["adaptive", "classic"],
    "features": [
        "Interactive chat sessions",
        "System status monitoring",
        "Configuration management",
        "Security auditing",
        "Mode switching",
        "JSON output",
        "Debug logging",
        "Programmatic usage",
    ],
}
