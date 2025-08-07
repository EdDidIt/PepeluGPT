#!/usr/bin/env python3
"""
Audit command handler for PepeluGPT CLI.
Provides security and compliance auditing capabilities.
"""

import argparse
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, cast


class AuditResult:
    """Represents a single audit finding."""

    def __init__(
        self,
        category: str,
        severity: str,
        title: str,
        description: str,
        recommendation: str = "",
        file_path: str = "",
    ):
        self.category = category
        self.severity = severity
        self.title = title
        self.description = description
        self.recommendation = recommendation
        self.file_path = file_path
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "file_path": self.file_path,
            "timestamp": self.timestamp,
        }


class SecurityAuditor:
    """Security audit functionality."""

    def __init__(self):
        self.results: List[AuditResult] = []

    def audit_file_permissions(self) -> List[AuditResult]:
        """Audit file permissions for sensitive files."""
        findings: List[AuditResult] = []

        # Check sensitive files and directories
        sensitive_paths = [
            "config/",
            "logs/",
            "storage/",
            "cyber_vector_db/",
            ".env",
            "*.key",
            "*.pem",
        ]

        for path_pattern in sensitive_paths:
            if path_pattern.startswith("*."):
                # Handle wildcard patterns
                for file_path in Path(".").rglob(path_pattern):
                    if file_path.exists():
                        stat = file_path.stat()
                        # Check if file is world-readable (simplified check)
                        if oct(stat.st_mode)[-1] in ["4", "5", "6", "7"]:
                            findings.append(
                                AuditResult(
                                    category="security",
                                    severity="medium",
                                    title="World-readable sensitive file",
                                    description=f"File {file_path} may be readable by other users",
                                    recommendation="Consider restricting file permissions",
                                    file_path=str(file_path),
                                )
                            )
            else:
                path = Path(path_pattern)
                if path.exists():
                    # Basic permission check
                    if path.is_dir() and not path_pattern.endswith("/"):
                        continue

                    # Add informational finding about sensitive file locations
                    findings.append(
                        AuditResult(
                            category="security",
                            severity="low",
                            title="Sensitive path detected",
                            description=f"Sensitive path {path} exists and should be monitored",
                            recommendation="Ensure proper access controls are in place",
                            file_path=str(path),
                        )
                    )

        return findings

    def audit_configuration_security(self, config_path: str) -> List[AuditResult]:
        """Audit configuration for security issues."""
        findings: List[AuditResult] = []

        try:
            from cli.runner import load_config

            config = load_config(config_path)

            if not config:
                findings.append(
                    AuditResult(
                        category="security",
                        severity="high",
                        title="Configuration load failure",
                        description=f"Could not load configuration from {config_path}",
                        recommendation="Verify configuration file exists and is valid YAML",
                        file_path=config_path,
                    )
                )
                return findings

            # Check for debug mode in production
            if config.get("logging", {}).get("level") == "DEBUG":
                findings.append(
                    AuditResult(
                        category="security",
                        severity="medium",
                        title="Debug logging enabled",
                        description="Debug logging may expose sensitive information",
                        recommendation="Use INFO or WARNING level for production",
                        file_path=config_path,
                    )
                )

            # Check for insecure database settings
            db_config = config.get("vector_db", {})
            if db_config.get("host") == "0.0.0.0":
                findings.append(
                    AuditResult(
                        category="security",
                        severity="high",
                        title="Database bound to all interfaces",
                        description="Database is configured to listen on all network interfaces",
                        recommendation="Bind to localhost or specific interfaces only",
                        file_path=config_path,
                    )
                )

            # Check for API keys in config (should be in env vars)
            def check_for_keys(obj: Any, path: str = "") -> None:
                if isinstance(obj, dict):
                    dict_obj = cast(Dict[str, Any], obj)
                    for key, value in dict_obj.items():
                        new_path = f"{path}.{key}" if path else key
                        if isinstance(value, str) and any(
                            word in key.lower()
                            for word in ["key", "token", "secret", "password"]
                        ):
                            if value and not value.startswith(
                                "${"
                            ):  # Not an env var reference
                                findings.append(
                                    AuditResult(
                                        category="security",
                                        severity="critical",
                                        title="Hardcoded credential in config",
                                        description=f"Found potential credential in config at {new_path}",
                                        recommendation="Use environment variables for credentials",
                                        file_path=config_path,
                                    )
                                )
                        elif isinstance(value, dict):
                            check_for_keys(value, new_path)

            check_for_keys(config)

        except Exception as e:
            findings.append(
                AuditResult(
                    category="security",
                    severity="medium",
                    title="Configuration audit error",
                    description=f"Error auditing configuration: {str(e)}",
                    recommendation="Investigate configuration file structure",
                    file_path=config_path,
                )
            )

        return findings


class DependencyAuditor:
    """Dependency audit functionality."""

    def audit_dependencies(self) -> List[AuditResult]:
        """Audit Python dependencies for known vulnerabilities."""
        findings: List[AuditResult] = []

        # Check for requirements files
        req_files = ["requirements.txt", "requirements_learning.txt"]

        for req_file in req_files:
            if Path(req_file).exists():
                findings.append(
                    AuditResult(
                        category="dependencies",
                        severity="low",
                        title="Requirements file found",
                        description=f"Dependency file {req_file} should be regularly audited",
                        recommendation="Use 'pip audit' or 'safety check' to scan for vulnerabilities",
                        file_path=req_file,
                    )
                )

        # Check for common vulnerable patterns
        try:
            with open("requirements.txt", "r") as f:
                content = f.read()

                # Check for unpinned versions
                lines = [
                    line.strip()
                    for line in content.split("\n")
                    if line.strip() and not line.startswith("#")
                ]
                unpinned = [
                    line for line in lines if "==" not in line and ">=" not in line
                ]

                if unpinned:
                    findings.append(
                        AuditResult(
                            category="dependencies",
                            severity="medium",
                            title="Unpinned dependencies detected",
                            description=f"Found {len(unpinned)} unpinned dependencies",
                            recommendation="Pin dependency versions for reproducible builds",
                            file_path="requirements.txt",
                        )
                    )

        except FileNotFoundError:
            findings.append(
                AuditResult(
                    category="dependencies",
                    severity="low",
                    title="No requirements.txt found",
                    description="No dependency file found for audit",
                    recommendation="Create requirements.txt for dependency tracking",
                )
            )

        return findings


class DocumentAuditor:
    """Document audit functionality."""

    def audit_documents(self) -> List[AuditResult]:
        """Audit documents for potential security concerns."""
        findings: List[AuditResult] = []

        # Check cyber_documents directory
        docs_dir = Path("cyber_documents")
        if docs_dir.exists():
            doc_files = list(docs_dir.glob("*"))

            findings.append(
                AuditResult(
                    category="documents",
                    severity="low",
                    title="Document collection detected",
                    description=f"Found {len(doc_files)} files in cyber_documents directory",
                    recommendation="Ensure all documents are properly classified and access-controlled",
                    file_path=str(docs_dir),
                )
            )

            # Check for potentially sensitive file types
            sensitive_extensions = [".pdf", ".docx", ".xlsx", ".pptx"]
            sensitive_files = [
                f for f in doc_files if f.suffix.lower() in sensitive_extensions
            ]

            if sensitive_files:
                findings.append(
                    AuditResult(
                        category="documents",
                        severity="medium",
                        title="Sensitive document formats detected",
                        description=f"Found {len(sensitive_files)} potentially sensitive documents",
                        recommendation="Review document access controls and content classification",
                        file_path=str(docs_dir),
                    )
                )

        return findings


def handle_audit_command(args: argparse.Namespace) -> None:
    """Handle the audit subcommand."""
    print("🔍 PepeluGPT Security Audit")
    print("=" * 40)

    # Initialize auditors
    security_auditor = SecurityAuditor()
    dependency_auditor = DependencyAuditor()
    document_auditor = DocumentAuditor()

    all_findings: List[AuditResult] = []

    # Run selected audits
    if args.type in ["security", "all"]:
        print("🛡️  Running security audit...")
        all_findings.extend(security_auditor.audit_file_permissions())
        all_findings.extend(security_auditor.audit_configuration_security(args.config))

    if args.type in ["dependencies", "all"]:
        print("📦 Running dependency audit...")
        all_findings.extend(dependency_auditor.audit_dependencies())

    if args.type in ["documents", "all"]:
        print("📄 Running document audit...")
        all_findings.extend(document_auditor.audit_documents())

    if args.type in ["config", "all"]:
        print("⚙️ Running configuration audit...")
        # Reuse security config audit
        all_findings.extend(security_auditor.audit_configuration_security(args.config))

    # Filter by severity if specified
    if args.severity:
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        min_level = severity_order[args.severity]
        all_findings = [
            f for f in all_findings if severity_order.get(f.severity, 0) >= min_level
        ]

    # Generate report
    audit_report: Dict[str, Any] = {
        "audit_info": {
            "timestamp": datetime.datetime.now().isoformat(),
            "audit_type": args.type,
            "severity_filter": args.severity,
            "total_findings": len(all_findings),
        },
        "summary": {
            "critical": len([f for f in all_findings if f.severity == "critical"]),
            "high": len([f for f in all_findings if f.severity == "high"]),
            "medium": len([f for f in all_findings if f.severity == "medium"]),
            "low": len([f for f in all_findings if f.severity == "low"]),
        },
        "findings": [f.to_dict() for f in all_findings],
    }

    # Save to audit history (Phase 4 preview)
    try:
        from cli.audit_history import AuditHistoryManager

        history_manager = AuditHistoryManager()
        history_file = history_manager.save_audit_report(audit_report, args.type)
        print(f"📝 Audit saved to history: {history_file}")
    except Exception as e:
        print(f"⚠️ Could not save to audit history: {e}")

    # Output results
    if args.output == "json":
        output = json.dumps(audit_report, indent=2)
    elif args.output == "markdown":
        output = format_audit_markdown(audit_report)
    else:  # text
        output = format_audit_text(audit_report)

    # Save to file if requested
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"📁 Audit report saved to {args.save}")
    else:
        print(output)


def format_audit_text(report: Dict[str, Any]) -> str:
    """Format audit report as human-readable text."""
    output: List[str] = []

    # Summary
    summary = report["summary"]
    total = sum(summary.values())

    output.append(f"\n📊 Audit Summary ({total} findings)")
    output.append("-" * 30)

    if summary["critical"] > 0:
        output.append(f"🔴 Critical: {summary['critical']}")
    if summary["high"] > 0:
        output.append(f"🟠 High: {summary['high']}")
    if summary["medium"] > 0:
        output.append(f"🟡 Medium: {summary['medium']}")
    if summary["low"] > 0:
        output.append(f"🔵 Low: {summary['low']}")

    if total == 0:
        output.append("✅ No findings detected!")
        return "\n".join(output)

    # Findings
    output.append(f"\n🔍 Detailed Findings")
    output.append("=" * 40)

    for i, finding in enumerate(report["findings"], 1):
        severity_icon = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🔵",
        }.get(finding["severity"], "⚪")

        output.append(
            f"\n{i}. {severity_icon} {finding['title']} ({finding['severity'].upper()})"
        )
        output.append(f"   Category: {finding['category']}")
        output.append(f"   Description: {finding['description']}")

        if finding["file_path"]:
            output.append(f"   File: {finding['file_path']}")

        if finding["recommendation"]:
            output.append(f"   💡 Recommendation: {finding['recommendation']}")

    return "\n".join(output)


def format_audit_markdown(report: Dict[str, Any]) -> str:
    """Format audit report as Markdown."""
    output: List[str] = []

    output.append("# 🔍 PepeluGPT Security Audit Report")
    output.append(f"\n**Generated:** {report['audit_info']['timestamp']}")
    output.append(f"**Audit Type:** {report['audit_info']['audit_type']}")

    # Summary
    summary = report["summary"]
    total = sum(summary.values())

    output.append(f"\n## 📊 Summary ({total} findings)")
    output.append("\n| Severity | Count |")
    output.append("|----------|-------|")
    output.append(f"| 🔴 Critical | {summary['critical']} |")
    output.append(f"| 🟠 High | {summary['high']} |")
    output.append(f"| 🟡 Medium | {summary['medium']} |")
    output.append(f"| 🔵 Low | {summary['low']} |")

    if total == 0:
        output.append("\n✅ **No security findings detected!**")
        return "\n".join(output)

    # Findings
    output.append(f"\n## 🔍 Detailed Findings")

    for i, finding in enumerate(report["findings"], 1):
        severity_icon = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🔵",
        }.get(finding["severity"], "⚪")

        output.append(f"\n### {i}. {severity_icon} {finding['title']}")
        output.append(f"\n**Severity:** {finding['severity'].upper()}")
        output.append(f"**Category:** {finding['category']}")
        output.append(f"**Description:** {finding['description']}")

        if finding["file_path"]:
            output.append(f"**File:** `{finding['file_path']}`")

        if finding["recommendation"]:
            output.append(f"**💡 Recommendation:** {finding['recommendation']}")

    return "\n".join(output)
