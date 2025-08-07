#!/usr/bin/env python3
"""
Demo Plugin for PepeluGPT Plugin Framework.
Simple example plugin for testing the plugin system.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add plugins directory to path for imports
current_dir = Path(__file__).parent
plugins_dir = current_dir.parent
sys.path.insert(0, str(plugins_dir))

from base import AuditPlugin, PluginFinding, PluginSeverity, create_finding  # type: ignore


class DemoPlugin(AuditPlugin):
    """
    Demo audit plugin for testing the framework.

    This plugin demonstrates the basic plugin structure and
    generates sample findings for testing purposes.
    """

    def get_metadata(self) -> Dict[str, Any]:
        """Return plugin metadata"""
        return {
            "name": "Demo Plugin",
            "version": "1.0.0",
            "framework": "DEMO",
            "description": "Demo plugin for testing the PepeluGPT plugin framework",
            "author": "PepeluGPT Development Team",
            "controls": ["DEMO-001", "DEMO-002", "DEMO-003"],
            "requirements": [],
        }

    def audit(self, config: Dict[str, Any]) -> List[PluginFinding]:
        """Execute demo audit with sample findings."""
        findings = []
        workspace_path = config.get("workspace_path", ".")

        # Demo finding 1: Info level
        findings.append(  # type: ignore
            create_finding(
                id="DEMO-001.1",
                title="Demo info finding",
                description="This is a demo information finding for testing",
                severity=PluginSeverity.INFO,
                category="demo",
                framework="DEMO",
                control="DEMO-001",
                remediation="This is just a demo - no action required",
                metadata={"demo": True, "test_data": "sample"},
            )
        )

        # Demo finding 2: Low severity
        findings.append(  # type: ignore
            create_finding(
                id="DEMO-002.1",
                title="Demo configuration issue",
                description="Sample configuration file detected in workspace",
                severity=PluginSeverity.LOW,
                category="configuration",
                framework="DEMO",
                control="DEMO-002",
                remediation="Review configuration file for sensitive information",
                file_path=os.path.join(workspace_path, "config"),
                metadata={"type": "config_check"},
            )
        )

        # Demo finding 3: Medium severity
        findings.append(  # type: ignore
            create_finding(
                id="DEMO-003.1",
                title="Demo security concern",
                description="Potential security issue detected for demonstration",
                severity=PluginSeverity.MEDIUM,
                category="security",
                framework="DEMO",
                control="DEMO-003",
                remediation="Implement proper security measures as per demo guidelines",
                metadata={"risk_score": 5.5, "category": "medium_risk"},
            )
        )

        return findings  # type: ignore

    def get_required_files(self) -> List[str]:
        """Files needed for demo audit."""
        return ["config/*", "*.py", "README.md"]

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate demo plugin configuration."""
        # Demo plugin accepts any configuration
        return True

    def pre_audit_setup(self, workspace_path: str, config: Dict[str, Any]) -> bool:
        """Demo pre-audit setup."""
        print(f"🎮 Demo plugin: Setting up audit for {workspace_path}")
        return True

    def post_audit_cleanup(self, workspace_path: str, config: Dict[str, Any]) -> None:
        """Demo post-audit cleanup."""
        print(f"🎮 Demo plugin: Cleanup complete for {workspace_path}")


# Make this plugin discoverable
__plugin_class__ = DemoPlugin
