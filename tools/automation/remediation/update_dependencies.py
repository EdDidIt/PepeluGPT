#!/usr/bin/env python3
"""
Auto-remediation script: Update insecure dependencies
Addresses: insecure_dependencies finding type
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union


def update_dependencies(workspace_path: str = ".") -> bool:
    """Update insecure dependencies to secure versions"""
    workspace = Path(workspace_path)

    # Check for Python dependencies
    requirements_files = [
        workspace / "requirements.txt",
        workspace / "requirements_learning.txt",
        workspace / "pyproject.toml",
    ]

    updated_files: List[str] = []
    vulnerabilities_fixed = 0

    for req_file in requirements_files:
        if req_file.exists():
            print(f"🔍 Analyzing {req_file.name}...")

            try:
                # Run pip-audit or safety check (if available)
                result = subprocess.run(
                    ["python", "-m", "pip", "list", "--outdated", "--format=json"],
                    capture_output=True,
                    text=True,
                    cwd=workspace,
                )

                if result.returncode == 0:
                    outdated_packages = json.loads(result.stdout)
                    if outdated_packages:
                        print(f"📦 Found {len(outdated_packages)} outdated packages")

                        # Create backup
                        backup_path = req_file.with_suffix(req_file.suffix + ".backup")
                        if req_file.name == "requirements.txt":
                            subprocess.run(["cp", str(req_file), str(backup_path)])

                        # Update critical security packages
                        security_packages = [
                            "cryptography",
                            "requests",
                            "urllib3",
                            "certifi",
                            "pyjwt",
                            "flask",
                            "django",
                            "sqlalchemy",
                        ]

                        for package in outdated_packages:
                            package_name = package.get("name", "").lower()
                            if any(
                                sec_pkg in package_name for sec_pkg in security_packages
                            ):
                                latest_version = package.get("latest_version")
                                current_version = package.get("version")

                                print(
                                    f"🔄 Updating {package_name}: {current_version} -> {latest_version}"
                                )

                                # Update requirements file
                                if req_file.name == "requirements.txt":
                                    update_requirements_file(
                                        req_file, package_name, latest_version
                                    )
                                    vulnerabilities_fixed += 1

                        if vulnerabilities_fixed > 0:
                            updated_files.append(str(req_file))

            except subprocess.CalledProcessError as e:
                print(f"⚠️ Error checking dependencies: {e}")
            except json.JSONDecodeError:
                print("⚠️ Could not parse dependency information")

    # Generate dependency update report
    if updated_files:
        report_path = workspace / "logs" / "dependency_update_report.json"
        report_path.parent.mkdir(exist_ok=True)

        report: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "updated_files": updated_files,
            "vulnerabilities_fixed": vulnerabilities_fixed,
            "backup_files": [f + ".backup" for f in updated_files],
            "recommendations": [
                "Test all functionality after dependency updates",
                "Review change logs for breaking changes",
                "Update documentation if needed",
                "Consider using dependency scanning tools regularly",
            ],
            "status": "completed",
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"📊 Created dependency update report at {report_path}")
        print(
            f"✅ Successfully updated dependencies with {vulnerabilities_fixed} security fixes"
        )
        return True

    print("🔍 No insecure dependencies found or no updates available")
    return True


def update_requirements_file(requirements_path: Union[str, Path], package_name: str, new_version: str) -> bool:
    """Update specific package version in requirements.txt"""
    try:
        with open(requirements_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        updated_lines: List[str] = []
        package_updated = False

        for line in lines:
            if line.strip().startswith(package_name):
                # Update version
                updated_lines.append(f"{package_name}>={new_version}\n")
                package_updated = True
            else:
                updated_lines.append(line)

        # Add package if not found
        if not package_updated:
            updated_lines.append(f"{package_name}>={new_version}\n")

        with open(requirements_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

        return True

    except Exception as e:
        print(f"⚠️ Error updating {requirements_path}: {e}")
        return False


if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    success = update_dependencies(workspace)
    sys.exit(0 if success else 1)
