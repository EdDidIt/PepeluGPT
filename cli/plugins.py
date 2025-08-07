#!/usr/bin/env python3
"""
Plugin command handlers for PepeluGPT CLI.
Manages plugin installation, loading, and execution.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

# Add plugins directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from plugins.base import PluginFinding, PluginSeverity
from plugins.registry import PluginRegistry


class PluginAuditEngine:
    """Enhanced audit engine with plugin support."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.registry = PluginRegistry(plugins_dir)
        self.plugins_dir = plugins_dir

    def run_framework_audit(
        self,
        workspace_path: str,
        frameworks: Optional[List[str]] = None,
        controls: Optional[List[str]] = None,
        severity_filter: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> List[PluginFinding]:
        """
        Run audits using specified frameworks.

        Args:
            workspace_path: Path to workspace being audited
            frameworks: List of framework names to run (None for all)
            controls: List of specific controls to run (None for all)
            severity_filter: Minimum severity level
            config: Configuration dictionary

        Returns:
            List of findings from all plugins
        """
        if config is None:
            config = {}

        # Add workspace path to config
        config["workspace_path"] = workspace_path

        all_findings: List[PluginFinding] = []

        # Get active plugins
        if frameworks:
            active_plugins: List[Any] = []
            for framework in frameworks:
                try:
                    plugin = self.registry.load_plugin(framework)
                    if plugin:
                        active_plugins.append(plugin)
                except Exception as e:
                    print(f"⚠️ Could not load plugin '{framework}': {e}")
        else:
            # Load all enabled plugins
            active_plugins: List[Any] = []
            plugin_list = self.registry.list_plugins(enabled_only=True)
            for plugin_info in plugin_list:
                try:
                    plugin = self.registry.load_plugin(plugin_info["framework"])
                    if plugin:
                        active_plugins.append(plugin)
                except Exception as e:
                    print(f"⚠️ Could not load plugin '{plugin_info['framework']}': {e}")

        # Run each plugin
        for plugin in active_plugins:
            try:
                print(f"🔍 Running {plugin.metadata.name} audit...")

                # Pre-audit setup
                if not plugin.pre_audit_setup(workspace_path, config):
                    print(f"⚠️ Pre-audit setup failed for {plugin.metadata.name}")
                    continue

                # Run audit
                findings = plugin.audit(config)

                # Filter by controls if specified
                if controls:
                    findings = [f for f in findings if f.control in controls]

                # Filter by severity if specified
                if severity_filter:
                    findings = self._filter_by_severity(findings, severity_filter)

                all_findings.extend(findings)

                # Post-audit cleanup
                plugin.post_audit_cleanup(workspace_path, config)

                print(f"✅ {plugin.metadata.name}: {len(findings)} findings")

            except Exception as e:
                print(f"❌ Plugin {plugin.metadata.name} failed: {e}")

        return all_findings

    def _filter_by_severity(
        self, findings: List[PluginFinding], min_severity: str
    ) -> List[PluginFinding]:
        """Filter findings by minimum severity level."""
        severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

        min_level = severity_order.get(min_severity.lower(), 0)

        return [
            f
            for f in findings
            if severity_order.get(f.severity.value.lower(), 0) >= min_level
        ]


def handle_plugins_command(args: argparse.Namespace) -> None:
    """Handle the plugins subcommand."""
    registry = PluginRegistry()

    if not hasattr(args, "plugin_action") or args.plugin_action is None:
        args.plugin_action = "list"  # Default to list

    if args.plugin_action == "list":
        handle_plugins_list(args, registry)
    elif args.plugin_action == "install":
        handle_plugins_install(args, registry)
    elif args.plugin_action == "enable":
        handle_plugins_enable(args, registry)
    elif args.plugin_action == "disable":
        handle_plugins_disable(args, registry)
    elif args.plugin_action == "validate":
        handle_plugins_validate(args, registry)
    elif args.plugin_action == "register":
        handle_plugins_register(args, registry)
    else:
        print(f"❌ Unknown plugin action: {args.plugin_action}")
        print("Available actions: list, install, enable, disable, validate")


def handle_plugins_list(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """List all plugins."""
    print("🔌 Plugin Registry")
    print("=" * 40)

    plugins = registry.list_plugins()

    if not plugins:
        print("📭 No plugins registered")
        return

    # Group by category
    by_category: Dict[str, List[Any]] = {}
    for plugin in plugins:
        category: str = plugin["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(plugin)

    for category, category_plugins in by_category.items():
        print(f"\n📁 {category.title()} Plugins:")
        for plugin in category_plugins:
            status = "🟢" if plugin["enabled"] else "🔴"
            print(f"  {status} {plugin['name']} v{plugin['version']}")
            print(f"     Framework: {plugin['framework']}")
            print(f"     Controls: {', '.join(plugin['controls'][:5])}")  # Show first 5
            if len(plugin["controls"]) > 5:
                print(f"               ... and {len(plugin['controls']) - 5} more")
            print()


def handle_plugins_install(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """Install a plugin."""
    if not args.plugin_path:
        print("❌ Plugin path required")
        return

    print(f"📦 Installing plugin from {args.plugin_path}")

    category = getattr(args, "category", "custom")
    if registry.register_plugin(args.plugin_path, category):
        print("✅ Plugin installed successfully")
    else:
        print("❌ Plugin installation failed")


def handle_plugins_enable(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """Enable a plugin."""
    if not args.framework:
        print("❌ Framework name required")
        return

    registry.enable_plugin(args.framework)


def handle_plugins_disable(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """Disable a plugin."""
    if not args.framework:
        print("❌ Framework name required")
        return

    registry.disable_plugin(args.framework)


def handle_plugins_validate(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """Validate all plugins."""
    print("🔍 Validating all plugins...")
    print("=" * 40)

    results = registry.validate_all_plugins()

    valid_count = 0
    invalid_count = 0

    for plugin_name, is_valid in results.items():
        if is_valid:
            print(f"✅ {plugin_name}")
            valid_count += 1
        else:
            print(f"❌ {plugin_name}")
            invalid_count += 1

    print()
    print(f"📊 Validation Summary:")
    print(f"   ✅ Valid: {valid_count}")
    print(f"   ❌ Invalid: {invalid_count}")


def handle_plugins_register(args: argparse.Namespace, registry: PluginRegistry) -> None:
    """Register a plugin manually."""
    if not args.plugin_path:
        print("❌ Plugin path required")
        return

    category = getattr(args, "category", "custom")
    registry.register_plugin(args.plugin_path, category)


def handle_framework_audit_command(args: argparse.Namespace) -> None:
    """Handle framework-specific audit commands."""
    print("🔍 Framework-Based Security Audit")
    print("=" * 40)

    # Initialize plugin engine
    engine = PluginAuditEngine()

    # Parse frameworks
    frameworks: Optional[List[str]] = None
    if hasattr(args, "framework") and args.framework:
        frameworks = [f.strip() for f in args.framework.split(",")]

    # Parse controls
    controls: Optional[List[str]] = None
    if hasattr(args, "control") and args.control:
        controls = [c.strip() for c in args.control.split(",")]

    # Run audit
    try:
        findings = engine.run_framework_audit(
            workspace_path=".",
            frameworks=frameworks,
            controls=controls,
            severity_filter=getattr(args, "severity", None),
            config={},
        )

        # Generate report
        audit_report: Dict[str, Any] = {
            "audit_info": {
                "timestamp": "2025-08-02T18:00:00Z",  # TODO: Use actual timestamp
                "frameworks": frameworks or ["all"],
                "controls": controls or ["all"],
                "total_findings": len(findings),
            },
            "summary": {
                "critical": len(
                    [f for f in findings if f.severity == PluginSeverity.CRITICAL]
                ),
                "high": len([f for f in findings if f.severity == PluginSeverity.HIGH]),
                "medium": len(
                    [f for f in findings if f.severity == PluginSeverity.MEDIUM]
                ),
                "low": len([f for f in findings if f.severity == PluginSeverity.LOW]),
                "info": len([f for f in findings if f.severity == PluginSeverity.INFO]),
            },
            "findings": [f.to_dict() for f in findings],
        }

        # Output results
        output_format = getattr(args, "output", "text")
        if output_format == "json":
            output = json.dumps(audit_report, indent=2)
        else:
            output = format_framework_audit_text(audit_report)

        # Save to file if requested
        if hasattr(args, "save") and args.save:
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"📁 Framework audit report saved to {args.save}")
        else:
            print(output)

    except Exception as e:
        print(f"❌ Framework audit failed: {e}")


def format_framework_audit_text(audit_report: Dict[str, Any]) -> str:
    """Format framework audit results as text."""
    lines: List[str] = []

    # Summary
    summary = audit_report["summary"]
    total = audit_report["audit_info"]["total_findings"]

    lines.append(f"📊 Framework Audit Summary ({total} findings)")
    lines.append("-" * 40)

    if summary["critical"] > 0:
        lines.append(f"🔴 Critical: {summary['critical']}")
    if summary["high"] > 0:
        lines.append(f"🟠 High: {summary['high']}")
    if summary["medium"] > 0:
        lines.append(f"🟡 Medium: {summary['medium']}")
    if summary["low"] > 0:
        lines.append(f"🔵 Low: {summary['low']}")
    if summary["info"] > 0:
        lines.append(f"ℹ️ Info: {summary['info']}")

    # Detailed findings
    if audit_report["findings"]:
        lines.append("")
        lines.append("🔍 Framework Findings")
        lines.append("=" * 40)

        for i, finding in enumerate(audit_report["findings"], 1):
            severity_emoji = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🔵",
                "info": "ℹ️",
            }.get(finding["severity"], "❓")

            lines.append(
                f"{i}. {severity_emoji} {finding['title']} ({finding['severity'].upper()})"
            )
            lines.append(
                f"   Framework: {finding['framework']} | Control: {finding['control']}"
            )
            lines.append(f"   Category: {finding['category']}")
            lines.append(f"   Description: {finding['description']}")
            if finding.get("file_path"):
                lines.append(f"   File: {finding['file_path']}")
            lines.append(f"   💡 Remediation: {finding['remediation']}")
            lines.append("")

    return "\n".join(lines)


# Demo function for testing plugin system
def demo_plugin_system():
    """Demonstrate the plugin system capabilities."""
    print("🎮 Plugin System Demo")
    print("=" * 40)

    # Initialize registry
    registry = PluginRegistry()

    # Register built-in plugins
    print("📦 Registering NIST 800-53 plugin...")
    if registry.register_plugin("core/nist_800_53.py", "core"):
        print("✅ NIST plugin registered")

    # List plugins
    print("\n📋 Available plugins:")
    plugins = registry.list_plugins()
    for plugin in plugins:
        print(f"  • {plugin['name']} ({plugin['framework']})")

    # Run framework audit
    print("\n🔍 Running NIST 800-53 audit...")
    engine = PluginAuditEngine()
    findings = engine.run_framework_audit(
        workspace_path=".", frameworks=["NIST-800-53"], config={}
    )

    print(f"📊 Found {len(findings)} NIST compliance findings")

    # Show sample findings
    for finding in findings[:3]:  # Show first 3
        print(f"  • {finding.title} ({finding.severity.value})")


if __name__ == "__main__":
    demo_plugin_system()
