#!/usr/bin/env python3
"""
NIST SP 800-53 Security Controls Plugin for PepeluGPT.
Implements key NIST security controls and assessments.
"""

import glob
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from base import (
    AuditPlugin,
    PluginFinding,
    PluginMetadata,
    PluginSeverity,
    create_finding,  # type: ignore
)


class NIST80053Plugin(AuditPlugin):
    """
    NIST SP 800-53 Security and Privacy Controls plugin.

    Implements automated assessment of key NIST 800-53 controls:
    - AC-2: Account Management
    - IA-5: Authenticator Management
    - SC-7: Boundary Protection
    - SI-2: Flaw Remediation
    """

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="NIST SP 800-53",
            version="1.0.0",
            framework="NIST-800-53",
            description="NIST Special Publication 800-53 Security and Privacy Controls",
            author="PepeluGPT Security Team",
            controls=[
                "AC-2",
                "AC-3",
                "AC-5",
                "AC-6",  # Access Control
                "IA-2",
                "IA-4",
                "IA-5",  # Identification and Authentication
                "SC-7",
                "SC-8",
                "SC-13",  # System and Communications Protection
                "SI-2",
                "SI-3",
                "SI-4",  # System and Information Integrity
            ],
            requirements=["pyyaml>=6.0"],
        )

    def run_audit(
        self, workspace_path: str, config: Dict[str, Any]
    ) -> List[PluginFinding]:
        """Execute NIST 800-53 compliance audit."""
        findings = []

        # AC-2: Account Management
        findings.extend(self._check_account_management(workspace_path))  # type: ignore

        # IA-5: Authenticator Management
        findings.extend(self._check_authenticator_management(workspace_path))  # type: ignore

        # SC-7: Boundary Protection
        findings.extend(self._check_boundary_protection(workspace_path))  # type: ignore

        # SI-2: Flaw Remediation
        findings.extend(self._check_flaw_remediation(workspace_path))  # type: ignore

        return findings  # type: ignore

    def get_required_files(self) -> List[str]:
        """Files needed for NIST 800-53 assessment."""
        return [
            "config/*.yaml",
            "config/*.yml",
            "requirements*.txt",
            "package.json",
            "Dockerfile*",
            ".env*",
            "docker-compose*.yml",
        ]

    def _check_account_management(self, workspace_path: str) -> List[PluginFinding]:
        """
        AC-2: Account Management

        Checks for:
        - Default credentials in configuration files
        - Hardcoded passwords or tokens
        - Weak authentication configurations
        """
        findings = []

        # Check configuration files for default credentials
        config_patterns = ["config/*.yaml", "config/*.yml", ".env*"]

        for pattern in config_patterns:
            for config_file in glob.glob(os.path.join(workspace_path, pattern)):
                findings.extend(self._scan_config_for_credentials(config_file))  # type: ignore

        return findings  # type: ignore

    def _scan_config_for_credentials(self, config_file: str) -> List[PluginFinding]:
        """Scan configuration file for credential issues."""
        findings = []

        try:
            # Detect file type and parse appropriately
            if config_file.endswith((".yaml", ".yml")):
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f)
                    findings.extend(  # type: ignore
                        self._check_yaml_credentials(config_data, config_file)
                    )

            elif config_file.endswith(".env") or ".env" in os.path.basename(
                config_file
            ):
                findings.extend(self._check_env_file(config_file))  # type: ignore

        except Exception as e:
            findings.append(  # type: ignore
                create_finding(
                    id="NIST-AC-2.ERROR",
                    title="Configuration file parsing error",
                    description=f"Could not parse {config_file}: {e}",
                    severity=PluginSeverity.LOW,
                    category="access_control",
                    framework="NIST-800-53",
                    control="AC-2",
                    remediation="Ensure configuration files are valid and accessible",
                    file_path=config_file,
                )
            )

        return findings  # type: ignore

    def _check_yaml_credentials(
        self, config_data: Any, file_path: str
    ) -> List[PluginFinding]:
        """Check YAML configuration for credential issues."""
        findings: List[PluginFinding] = []

        if not isinstance(config_data, dict):
            return findings  # type: ignore

        # Check for common default/weak credentials
        weak_credentials = [
            "admin",
            "password",
            "123456",
            "default",
            "changeme",
            "secret",
            "test",
            "demo",
            "guest",
            "root",
        ]

        def check_nested_dict(data: Dict[str, Any], path: str = ""):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key

                # Check for credential-related keys
                if any(
                    cred_key in key.lower()
                    for cred_key in [
                        "password",
                        "pass",
                        "secret",
                        "token",
                        "key",
                        "auth",
                    ]
                ):
                    if isinstance(value, str):
                        # Check for weak/default values
                        if value.lower() in weak_credentials:
                            findings.append(  # type: ignore
                                create_finding(
                                    id="NIST-AC-2.1",
                                    title="Weak credential detected",
                                    description=f"Configuration key '{current_path}' contains weak credential: '{value}'",
                                    severity=PluginSeverity.HIGH,
                                    category="access_control",
                                    framework="NIST-800-53",
                                    control="AC-2",
                                    remediation="Replace with strong, unique credentials and use secure storage",
                                    file_path=file_path,
                                    metadata={
                                        "config_path": current_path,
                                        "weak_value": value,
                                    },
                                )
                            )

                        # Check for hardcoded tokens/keys (basic pattern matching)
                        elif len(value) > 20 and any(
                            char in value for char in ["_", "-", "="]
                        ):
                            findings.append(  # type: ignore
                                create_finding(
                                    id="NIST-AC-2.2",
                                    title="Potential hardcoded credential",
                                    description=f"Configuration key '{current_path}' may contain hardcoded credential",
                                    severity=PluginSeverity.MEDIUM,
                                    category="access_control",
                                    framework="NIST-800-53",
                                    control="AC-2",
                                    remediation="Move credentials to environment variables or secure vault",
                                    file_path=file_path,
                                    metadata={"config_path": current_path},
                                )
                            )

                # Recurse into nested dictionaries
                elif isinstance(value, dict):
                    check_nested_dict(value, current_path)  # type: ignore

        check_nested_dict(config_data)  # type: ignore
        return findings  # type: ignore

    def _check_env_file(self, env_file: str) -> List[PluginFinding]:
        """Check environment file for credential issues."""
        findings: List[PluginFinding] = []

        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip("\"'")

                        # Check for exposed secrets
                        if any(
                            secret_key in key.upper()
                            for secret_key in ["API_KEY", "SECRET", "TOKEN", "PASSWORD"]
                        ):
                            if value and value != "your_secret_here":
                                findings.append(  # type: ignore
                                    create_finding(
                                        id="NIST-AC-2.3",
                                        title="Exposed credential in environment file",
                                        description=f"Environment variable '{key}' contains exposed credential",
                                        severity=PluginSeverity.HIGH,
                                        category="access_control",
                                        framework="NIST-800-53",
                                        control="AC-2",
                                        remediation="Use secure credential management and avoid committing .env files",
                                        file_path=env_file,
                                        line_number=line_num,
                                        metadata={"env_var": key},
                                    )
                                )

        except Exception:
            pass  # File might not be readable

        return findings  # type: ignore

    def _check_authenticator_management(
        self, workspace_path: str
    ) -> List[PluginFinding]:
        """
        IA-5: Authenticator Management

        Checks for:
        - Authentication configuration issues
        - Weak authentication mechanisms
        """
        findings: List[PluginFinding] = []

        # Check for authentication-related configurations
        config_files = glob.glob(os.path.join(workspace_path, "config/*.yaml"))

        for config_file in config_files:
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f)

                if isinstance(config_data, dict):
                    # Check for authentication settings
                    auth_keys = ["authentication", "auth", "login", "security"]
                    for key in auth_keys:
                        if key in config_data:
                            auth_config = config_data[key]  # type: ignore
                            if isinstance(auth_config, dict):
                                # Check for weak authentication methods
                                if auth_config.get("method") == "plain":  # type: ignore
                                    findings.append(  # type: ignore
                                        create_finding(
                                            id="NIST-IA-5.1",
                                            title="Weak authentication method",
                                            description="Plain text authentication method detected",
                                            severity=PluginSeverity.HIGH,
                                            category="identification_authentication",
                                            framework="NIST-800-53",
                                            control="IA-5",
                                            remediation="Use encrypted authentication methods (OAuth, SAML, etc.)",
                                            file_path=config_file,
                                        )
                                    )

            except Exception:
                continue

        return findings  # type: ignore

    def _check_boundary_protection(self, workspace_path: str) -> List[PluginFinding]:
        """
        SC-7: Boundary Protection

        Checks for:
        - Network configuration issues
        - Firewall and port configurations
        - Docker security configurations
        """
        findings: List[PluginFinding] = []

        # Check Docker configurations
        docker_files = glob.glob(os.path.join(workspace_path, "docker-compose*.yml"))
        docker_files.extend(glob.glob(os.path.join(workspace_path, "Dockerfile*")))

        for docker_file in docker_files:
            findings.extend(self._check_docker_security(docker_file))  # type: ignore

        return findings  # type: ignore

    def _check_docker_security(self, docker_file: str) -> List[PluginFinding]:
        """Check Docker configuration for security issues."""
        findings: List[PluginFinding] = []

        try:
            with open(docker_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Check for privileged containers
                if "privileged: true" in content or "--privileged" in content:
                    findings.append(  # type: ignore
                        create_finding(
                            id="NIST-SC-7.1",
                            title="Privileged container detected",
                            description="Container running in privileged mode poses security risk",
                            severity=PluginSeverity.HIGH,
                            category="system_communications_protection",
                            framework="NIST-800-53",
                            control="SC-7",
                            remediation="Remove privileged mode and use specific capabilities instead",
                            file_path=docker_file,
                        )
                    )

                # Check for exposed ports
                if "ports:" in content and "0.0.0.0:" in content:
                    findings.append(  # type: ignore
                        create_finding(
                            id="NIST-SC-7.2",
                            title="Unrestricted port binding",
                            description="Container ports bound to all interfaces (0.0.0.0)",
                            severity=PluginSeverity.MEDIUM,
                            category="system_communications_protection",
                            framework="NIST-800-53",
                            control="SC-7",
                            remediation="Bind ports to specific interfaces or use localhost",
                            file_path=docker_file,
                        )
                    )

        except Exception:
            pass

        return findings  # type: ignore

    def _check_flaw_remediation(self, workspace_path: str) -> List[PluginFinding]:
        """
        SI-2: Flaw Remediation

        Checks for:
        - Outdated dependencies
        - Missing security updates
        """
        findings: List[PluginFinding] = []

        # Check Python requirements
        req_files = glob.glob(os.path.join(workspace_path, "requirements*.txt"))
        for req_file in req_files:
            findings.extend(self._check_python_dependencies(req_file))  # type: ignore

        # Check Node.js dependencies
        package_json = os.path.join(workspace_path, "package.json")
        if os.path.exists(package_json):
            findings.extend(self._check_nodejs_dependencies(package_json))  # type: ignore

        return findings  # type: ignore

    def _check_python_dependencies(self, req_file: str) -> List[PluginFinding]:
        """Check Python dependencies for known issues."""
        findings: List[PluginFinding] = []

        try:
            with open(req_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Check for unpinned dependencies
                    if "==" not in line and ">=" not in line and "~=" not in line:
                        package_name = line.split("[")[0].strip()  # Remove extras
                        findings.append(  # type: ignore
                            create_finding(
                                id="NIST-SI-2.1",
                                title="Unpinned dependency",
                                description=f"Dependency '{package_name}' is not pinned to specific version",
                                severity=PluginSeverity.MEDIUM,
                                category="system_information_integrity",
                                framework="NIST-800-53",
                                control="SI-2",
                                remediation="Pin dependencies to specific versions for reproducible builds",
                                file_path=req_file,
                                line_number=line_num,
                                metadata={"package": package_name},
                            )
                        )

        except Exception:
            pass

        return findings  # type: ignore

    def _check_nodejs_dependencies(self, package_json: str) -> List[PluginFinding]:
        """Check Node.js dependencies for known issues."""
        findings: List[PluginFinding] = []

        try:
            with open(package_json, "r", encoding="utf-8") as f:
                package_data = json.load(f)

                # Check for dependencies without version constraints
                for dep_type in ["dependencies", "devDependencies"]:
                    if dep_type in package_data:
                        for package, version in package_data[dep_type].items():
                            if version == "*" or version == "latest":
                                findings.append(  # type: ignore
                                    create_finding(
                                        id="NIST-SI-2.2",
                                        title="Unpinned Node.js dependency",
                                        description=f"Package '{package}' uses wildcard or 'latest' version",
                                        severity=PluginSeverity.MEDIUM,
                                        category="system_information_integrity",
                                        framework="NIST-800-53",
                                        control="SI-2",
                                        remediation="Use specific version ranges for better security and stability",
                                        file_path=package_json,
                                        metadata={
                                            "package": package,
                                            "version": version,
                                        },
                                    )
                                )

        except Exception:
            pass

        return findings  # type: ignore
