#!/usr/bin/env python3
"""
Base Plugin API for PepeluGPT Audit Framework.
Foundation for extensible security compliance plugins.
"""

import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PluginSeverity(Enum):
    """Standardized severity levels for all plugins."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class PluginFinding:
    """Standardized finding structure for all plugins."""

    id: str  # Unique finding identifier
    title: str  # Human-readable title
    description: str  # Detailed description
    severity: PluginSeverity  # Risk level
    category: str  # Finding category
    framework: str  # Source framework
    control: str  # Framework control reference
    remediation: str  # How to fix the issue
    file_path: Optional[str] = None  # Related file
    line_number: Optional[int] = None  # Specific line
    metadata: Dict[str, Any] = field(default_factory=dict)  # type: ignore
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary format."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category,
            "framework": self.framework,
            "control": self.control,
            "remediation": self.remediation,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


@dataclass
class PluginMetadata:
    """Plugin metadata and registration information."""

    name: str
    version: str
    framework: str
    description: str
    author: str
    controls: List[str] = field(default_factory=list)  # type: ignore
    requirements: List[str] = field(default_factory=list)  # type: ignore
    enabled: bool = True
    last_updated: str = field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary format."""
        return {
            "name": self.name,
            "version": self.version,
            "framework": self.framework,
            "description": self.description,
            "author": self.author,
            "controls": self.controls,
            "requirements": self.requirements,
            "enabled": self.enabled,
            "last_updated": self.last_updated,
        }


class AuditPlugin(ABC):
    """
    Base class for all audit plugins.

    All audit plugins must inherit from this class and implement
    the required abstract methods.
    """

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return plugin metadata."""
        pass

    @abstractmethod
    def audit(self, config: Dict[str, Any]) -> List[PluginFinding]:
        """
        Execute the audit and return findings.

        Args:
            config: Configuration dictionary for the audit

        Returns:
            List of PluginFinding objects
        """
        pass

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate plugin-specific configuration.

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if configuration is valid, False otherwise
        """
        return True

    def get_required_files(self) -> List[str]:
        """
        Return list of files this plugin needs to audit.

        Returns:
            List of file patterns (supports glob patterns)
        """
        return []

    def pre_audit_setup(self, workspace_path: str, config: Dict[str, Any]) -> bool:
        """
        Setup operations before running audit.

        Args:
            workspace_path: Path to the workspace being audited
            config: Configuration dictionary

        Returns:
            True if setup successful, False otherwise
        """
        return True

    def post_audit_cleanup(self, workspace_path: str, config: Dict[str, Any]) -> None:
        """
        Cleanup operations after running audit.

        Args:
            workspace_path: Path to the workspace being audited
            config: Configuration dictionary
        """
        pass


class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""

    pass


class PluginNotFoundError(Exception):
    """Raised when a requested plugin is not found."""

    pass


class PluginValidationError(Exception):
    """Raised when plugin validation fails."""

    pass


# Utility functions for plugin developers
def create_finding(
    id: str,
    title: str,
    description: str,
    severity: PluginSeverity,
    category: str,
    framework: str,
    control: str,
    remediation: str,
    file_path: Optional[str] = None,
    line_number: Optional[int] = None,
    **metadata: Any
) -> PluginFinding:
    """Helper function to create standardized findings."""
    return PluginFinding(
        id=id,
        title=title,
        description=description,
        severity=severity,
        category=category,
        framework=framework,
        control=control,
        remediation=remediation,
        file_path=file_path,
        line_number=line_number,
        metadata=metadata,
    )


def validate_plugin_class(plugin_class: type) -> bool:
    """
    Validate that a class is a proper audit plugin.

    Args:
        plugin_class: Class to validate

    Returns:
        True if valid plugin class, False otherwise
    """
    if not issubclass(plugin_class, AuditPlugin):
        return False

    # Check required methods are implemented
    required_methods = ["metadata", "run_audit"]
    for method in required_methods:
        if not hasattr(plugin_class, method):
            return False

        # Check if method is properly implemented (not abstract)
        method_obj = getattr(plugin_class, method)
        if (
            hasattr(method_obj, "__isabstractmethod__")
            and method_obj.__isabstractmethod__
        ):
            return False

    return True


# Example severity mapping for different frameworks
SEVERITY_MAPPINGS = {
    "NIST-800-53": {
        "P0": PluginSeverity.CRITICAL,
        "P1": PluginSeverity.HIGH,
        "P2": PluginSeverity.MEDIUM,
        "P3": PluginSeverity.LOW,
    },
    "DOD-STIG": {
        "CAT I": PluginSeverity.CRITICAL,
        "CAT II": PluginSeverity.HIGH,
        "CAT III": PluginSeverity.MEDIUM,
    },
    "CIS": {"Level 1": PluginSeverity.MEDIUM, "Level 2": PluginSeverity.HIGH},
}
