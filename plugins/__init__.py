"""
PepeluGPT Plugin Framework
==========================

Extensible audit plugin system for compliance frameworks.

Available Modules:
- base: Core plugin classes and interfaces
- registry: Plugin discovery and management
- core: Built-in compliance plugins (NIST, STIG, etc.)
- custom: Organization-specific plugins
- community: Community-contributed plugins

Usage:
    from plugins.base import AuditPlugin, PluginFinding
    from plugins.registry import PluginRegistry

    # Create a plugin
    class MyPlugin(AuditPlugin):
        # Implementation...

    # Register and use
    registry = PluginRegistry()
    registry.register_plugin("my_plugin.py")
"""

__version__ = "1.0.0"
__author__ = "PepeluGPT Security Team"

# Core exports
from .base import (
    AuditPlugin,
    PluginFinding,
    PluginLoadError,
    PluginMetadata,
    PluginNotFoundError,
    PluginSeverity,
    PluginValidationError,
    create_finding,
    validate_plugin_class,
)
from .registry import PluginRegistry

__all__ = [
    # Base classes
    "AuditPlugin",
    "PluginFinding",
    "PluginMetadata",
    "PluginSeverity",
    # Utility functions
    "create_finding",
    "validate_plugin_class",
    # Registry
    "PluginRegistry",
    # Exceptions
    "PluginLoadError",
    "PluginNotFoundError",
    "PluginValidationError",
    # Metadata
    "__version__",
    "__author__",
]
