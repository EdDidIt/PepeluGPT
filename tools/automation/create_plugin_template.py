#!/usr/bin/env python3
"""
Plugin Template Generator for PepeluGPT
Creates scaffolding for new security compliance plugins
"""

import json
from pathlib import Path
from typing import List, Optional

TEMPLATE_CONTENT = '''"""
{name} Security Plugin for PepeluGPT
{description}

Author: {author}
Version: {version}
Framework: {framework}
"""

from typing import Dict, Any, List
from plugins.base import AuditPlugin, PluginSeverity, PluginFinding


class {class_name}(AuditPlugin):
    """
    {framework} compliance plugin
    
    Implements security controls for {framework} framework:
    {controls_description}
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.metadata = {{
            "name": "{name}",
            "version": "{version}",
            "framework": "{framework}",
            "author": "{author}",
            "description": "{description}",
            "controls": {controls}
        }}
    
    def audit(self, config: Dict[str, Any]) -> List[PluginFinding]:
        """
        Execute {framework} compliance audit
        
        Args:
            config: PepeluGPT configuration dictionary
            
        Returns:
            List of audit findings
        """
        findings = []
        
        # TODO: Implement specific {framework} controls
        {control_implementations}
        
        return findings
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return plugin metadata"""
        return self.metadata
{helper_methods}

# Plugin class export (required for dynamic loading)
__plugin_class__ = {class_name}
'''


def generate_control_implementations(controls: List[str]) -> str:
    """Generate template control implementation methods"""
    implementations: List[str] = []
    for control in controls:
        safe_name = control.replace("-", "_").replace(".", "_").lower()
        implementations.append(
            f"""
        # {control}: TODO - Add control description
        findings.extend(self._check_{safe_name}())"""
        )

    return "\n".join(implementations)


def generate_helper_methods(controls: List[str]) -> str:
    """Generate template helper methods for controls"""
    methods: List[str] = []
    for control in controls:
        safe_name = control.replace("-", "_").replace(".", "_").lower()
        methods.append(
            f"""
    def _check_{safe_name}(self) -> List[PluginFinding]:
        \"\"\"
        Check {control} compliance
        
        Returns:
            List of findings for {control}
        \"\"\"
        findings = []
        
        # TODO: Implement {control} specific checks
        # Example:
        # if condition_not_met:
        #     findings.append(self.create_finding(
        #         control_id="{control}",
        #         title="Control {control} Violation",
        #         description="Detailed description of the issue",
        #         severity=PluginSeverity.HIGH,
        #         location="specific/file/path",
        #         remediation="Steps to fix the issue"
        #     ))
        
        return findings"""
        )

    return "\n".join(methods)


def create_plugin_template(
    name: str,
    framework: str,
    author: str,
    version: str = "1.0.0",
    description: str = "",
    controls: Optional[List[str]] = None,
) -> str:
    """Create plugin template with specified parameters"""

    if controls is None:
        controls = ["EXAMPLE-001", "EXAMPLE-002"]

    if not description:
        description = f"Security compliance plugin for {framework}"

    class_name = f"{framework.replace(' ', '').replace('-', '')}Plugin"
    controls_description = "\\n    - " + "\\n    - ".join(controls)
    control_implementations = generate_control_implementations(controls)
    helper_methods = generate_helper_methods(controls)

    return TEMPLATE_CONTENT.format(
        name=name,
        class_name=class_name,
        framework=framework,
        author=author,
        version=version,
        description=description,
        controls=json.dumps(controls),
        controls_description=controls_description,
        control_implementations=control_implementations,
        helper_methods=helper_methods,
    )


def main() -> None:
    """Interactive plugin template generator"""
    print("🔌 PepeluGPT Plugin Template Generator")
    print("=" * 40)

    # Collect plugin information
    name = input("Plugin name: ").strip()
    framework = input(
        "Security framework (e.g., NIST-800-53, STIG, ISO27001): "
    ).strip()
    author = input("Author name: ").strip()
    version = input("Version (default: 1.0.0): ").strip() or "1.0.0"
    description = input("Description: ").strip()

    # Controls input
    print("\\nEnter security controls (one per line, empty line to finish):")
    controls: List[str] = []
    while True:
        control = input("Control ID: ").strip()
        if not control:
            break
        controls.append(control)

    if not controls:
        controls = ["EXAMPLE-001", "EXAMPLE-002"]

    # Generate template
    template_content = create_plugin_template(
        name=name,
        framework=framework,
        author=author,
        version=version,
        description=description,
        controls=controls,
    )

    # Save template
    safe_name = framework.lower().replace(" ", "_").replace("-", "_")
    filename = f"plugins/custom/{safe_name}_plugin.py"

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(template_content)

    print(f"\\n✅ Plugin template created: {filename}")
    print(f"📝 Next steps:")
    print(f"   1. Edit {filename} to implement control checks")
    print(f"   2. Register plugin: python main.py plugins validate {safe_name}")
    print(f"   3. Test plugin: python main.py plugins audit {framework.lower()}")


if __name__ == "__main__":
    main()
