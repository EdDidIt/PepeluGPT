#!/usr/bin/env python3
"""
PepeluGPT Plugin Validator

Enhanced validation framework for plugin onboarding with emoji-based feedback.
Implements comprehensive checks for template compliance, security, and standards.
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.utils import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class PluginValidator:
    """Enhanced plugin validation with emoji-based feedback."""

    def __init__(self):
        self.approved_emojis = {"🔴", "🟢", "🔵", "🟡", "❌", "✅"}
        self.required_metadata = {
            "name",
            "version",
            "author",
            "description",
            "compatibility",
        }

    def validate_plugin(self, plugin_path: str) -> Dict[str, Any]:
        """
        🔵 Comprehensive plugin validation with emoji feedback.

        Args:
            plugin_path: Path to plugin file or directory

        Returns:
            Validation results with emoji status indicators
        """
        logger.info(f"🔵 Starting plugin validation: {plugin_path}")

        results: Dict[str, Any] = {
            "plugin_path": plugin_path,
            "overall_status": "🔵",  # Default: processing
            "checks": {},
        }

        try:
            # Template structure validation
            results["checks"]["template"] = self._check_template_structure(plugin_path)

            # Metadata validation
            results["checks"]["metadata"] = self._validate_metadata(plugin_path)

            # Emoji compliance check
            results["checks"]["emoji_compliance"] = self._check_emoji_usage(plugin_path)

            # Security validation
            results["checks"]["security"] = self._security_validation(plugin_path)

            # Code quality checks
            results["checks"]["code_quality"] = self._code_quality_checks(plugin_path)

            # Determine overall status
            results["overall_status"] = self._determine_overall_status(
                results["checks"]
            )

            status_emoji = results["overall_status"]
            logger.info(f"{status_emoji} Plugin validation completed: {plugin_path}")

        except Exception as e:
            results["overall_status"] = "🔴"
            results["error"] = str(e)
            logger.error(f"🔴 Plugin validation failed: {plugin_path} - {e}")

        return results

    def _check_template_structure(self, plugin_path: str) -> Dict[str, Any]:
        """Check if plugin follows PepeluGPT template structure."""
        result: Dict[str, Any] = {"status": "🔵", "issues": []}

        try:
            path = Path(plugin_path)

            # Check for required files
            required_files = ["__init__.py"] if path.is_dir() else [path.name]

            for req_file in required_files:
                file_path = path / req_file if path.is_dir() else path
                if not file_path.exists():
                    result["issues"].append(f"Missing required file: {req_file}")

            # Check for plugin class structure
            if self._has_valid_plugin_class(plugin_path):
                result["plugin_class"] = "🟢"
            else:
                result["plugin_class"] = "🔴"
                result["issues"].append("Missing or invalid plugin class structure")

            result["status"] = "🟢" if not result["issues"] else "🟡"

        except Exception as e:
            result["status"] = "🔴"
            result["issues"].append(f"Template check error: {e}")

        return result

    def _validate_metadata(self, plugin_path: str) -> Dict[str, Any]:
        """Validate plugin metadata completeness and format."""
        result: Dict[str, Any] = {"status": "🔵", "issues": [], "metadata": {}}

        try:
            metadata = self._extract_metadata(plugin_path)
            result["metadata"] = metadata

            # Check required fields
            missing_fields = self.required_metadata - set(metadata.keys())
            if missing_fields:
                result["issues"].extend(
                    [f"Missing metadata: {field}" for field in missing_fields]
                )

            # Validate version format
            if "version" in metadata:
                if not re.match(r"^\d+\.\d+\.\d+$", metadata["version"]):
                    result["issues"].append(
                        "Version must follow semantic versioning (x.y.z)"
                    )

            # Check description length
            if "description" in metadata and len(metadata["description"]) < 10:
                result["issues"].append("Description too short (minimum 10 characters)")

            result["status"] = "🟢" if not result["issues"] else "🟡"

        except Exception as e:
            result["status"] = "🔴"
            result["issues"].append(f"Metadata validation error: {e}")

        return result

    def _check_emoji_usage(self, plugin_path: str) -> Dict[str, Any]:
        """Validate emoji usage compliance with PepeluGPT standards."""
        result: Dict[str, Any] = {"status": "🔵", "issues": [], "violations": []}

        try:
            content = self._read_plugin_content(plugin_path)

            # Find all emojis in content
            emoji_pattern = r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF]"
            found_emojis = set(re.findall(emoji_pattern, content))

            # Check for unauthorized emojis
            unauthorized = found_emojis - self.approved_emojis
            if unauthorized:
                result["violations"] = list(unauthorized)
                result["issues"].append(
                    f"Unauthorized emojis found: {', '.join(unauthorized)}"
                )
                result["issues"].append("Only 🔴🟢🔵🟡❌✅ emojis are permitted")

            result["status"] = "🟢" if not result["issues"] else "🔴"

        except Exception as e:
            result["status"] = "🔴"
            result["issues"].append(f"Emoji validation error: {e}")

        return result

    def _security_validation(self, plugin_path: str) -> Dict[str, Any]:
        """Perform basic security validation checks."""
        result: Dict[str, Any] = {"status": "🔵", "issues": [], "warnings": []}

        try:
            content = self._read_plugin_content(plugin_path)

            # Check for dangerous imports
            dangerous_imports = [
                "os.system",
                "subprocess.call",
                "eval",
                "exec",
                "__import__",
            ]
            for dangerous in dangerous_imports:
                if dangerous in content:
                    result["issues"].append(f"Potentially dangerous code: {dangerous}")

            # Check for hardcoded secrets/passwords
            secret_patterns = [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
            ]

            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result["warnings"].append("Potential hardcoded secret detected")

            result["status"] = (
                "🟢" if not result["issues"] else ("🟡" if result["warnings"] else "🔴")
            )

        except Exception as e:
            result["status"] = "🔴"
            result["issues"].append(f"Security validation error: {e}")

        return result

    def _code_quality_checks(self, plugin_path: str) -> Dict[str, Any]:
        """Basic code quality and style checks."""
        result: Dict[str, Any] = {"status": "🔵", "issues": [], "suggestions": []}

        try:
            content = self._read_plugin_content(plugin_path)

            # Check for basic docstrings
            if "def " in content and '"""' not in content and "'''" not in content:
                result["suggestions"].append("Consider adding docstrings to functions")

            # Check for exception handling
            if "except:" in content:
                result["suggestions"].append(
                    "Use specific exception types instead of bare except"
                )

            # Check line length (basic)
            long_lines = [
                i + 1 for i, line in enumerate(content.split("\n")) if len(line) > 100
            ]
            if long_lines:
                result["suggestions"].append(
                    f"Consider shortening long lines: {long_lines[:5]}"
                )

            result["status"] = "🟢"  # Code quality issues are suggestions, not failures

        except Exception as e:
            result["status"] = "🔴"
            result["issues"].append(f"Code quality check error: {e}")

        return result

    def _determine_overall_status(self, checks: Dict[str, Any]) -> str:
        """Determine overall validation status based on individual checks."""
        statuses = [check["status"] for check in checks.values()]

        if "🔴" in statuses:
            return "🔴"  # Critical issues found
        elif "🟡" in statuses:
            return "🟡"  # Warnings or minor issues
        else:
            return "🟢"  # All checks passed

    def _has_valid_plugin_class(self, plugin_path: str) -> bool:
        """Check if plugin has valid class structure."""
        try:
            content = self._read_plugin_content(plugin_path)
            tree = ast.parse(content)

            # Look for class that inherits from AuditPlugin
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and "Plugin" in base.id:
                            return True
            return False

        except:
            return False

    def _extract_metadata(self, plugin_path: str) -> Dict[str, Any]:
        """Extract metadata from plugin file."""
        try:
            content = self._read_plugin_content(plugin_path)

            # Look for metadata dictionary or docstring
            if "__metadata__" in content:
                # Try to extract __metadata__ dict
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if (
                                isinstance(target, ast.Name)
                                and target.id == "__metadata__"
                            ):
                                return ast.literal_eval(node.value)

            # Fallback: extract from module docstring
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            if docstring:
                # Simple extraction - could be enhanced
                return {"description": docstring.split("\n")[0][:100]}

            return {}

        except:
            return {}

    def _read_plugin_content(self, plugin_path: str) -> str:
        """Read plugin file content."""
        path = Path(plugin_path)

        if path.is_dir():
            # Read __init__.py from directory
            init_file = path / "__init__.py"
            if init_file.exists():
                return init_file.read_text(encoding="utf-8")
            else:
                raise FileNotFoundError(f"No __init__.py found in {plugin_path}")
        else:
            return path.read_text(encoding="utf-8")

    def generate_validation_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable validation report with emoji formatting."""
        report: list[str] = []
        status = results["overall_status"]
        path = results["plugin_path"]

        report.append(f"{status} Plugin Validation Report: {path}")
        report.append("=" * 50)

        for check_name, check_result in results["checks"].items():
            check_status = check_result["status"]
            report.append(f"\n{check_status} {check_name.title().replace('_', ' ')}")

            if check_result.get("issues"):
                for issue in check_result["issues"]:
                    report.append(f"  🔴 {issue}")

            if check_result.get("warnings"):
                for warning in check_result["warnings"]:
                    report.append(f"  🟡 {warning}")

            if check_result.get("suggestions"):
                for suggestion in check_result["suggestions"]:
                    report.append(f"  🔵 {suggestion}")

        # Summary
        report.append(f"\n{status} Overall Status: ")
        if status == "🟢":
            report.append("✅ Plugin approved for deployment")
        elif status == "🟡":
            report.append("⚠️ Plugin approved with warnings")
        else:
            report.append("❌ Plugin rejected - critical issues found")

        return "\n".join(report)


def main():
    """CLI interface for plugin validation."""
    import argparse

    parser = argparse.ArgumentParser(description="PepeluGPT Plugin Validator")
    parser.add_argument("plugin_path", help="Path to plugin file or directory")
    parser.add_argument("--output", "-o", help="Output report to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    validator = PluginValidator()
    results = validator.validate_plugin(args.plugin_path)

    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = validator.generate_validation_report(results)

    if args.output:
        Path(args.output).write_text(output)
        print(f"🔵 Report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
