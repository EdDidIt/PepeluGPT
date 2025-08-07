#!/usr/bin/env python3
"""
Utility script to check and report system health.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict


def check_python_version() -> Dict[str, Any]:
    """Check Python version compatibility."""
    version = sys.version_info
    return {
        "name": "Python Version",
        "status": "🟢" if version >= (3, 8) else "🔴",
        "message": f"Python {version.major}.{version.minor}.{version.micro}",
        "required": "Python 3.8+",
    }


def check_dependencies() -> Dict[str, Any]:
    """Check if required packages are installed."""
    required_packages = [
        "yaml",
        "pickle",
        "hashlib",
        "pathlib",
        "argparse",
        "json",
        "time",
        "logging",
        "datetime",
    ]

    missing: list[str] = []
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing.append(package)

    return {
        "name": "Dependencies",
        "status": "🟢" if not missing else "🔴",
        "message": (
            "All required packages available"
            if not missing
            else f"Missing: {', '.join(missing)}"
        ),
        "required": "All core Python packages",
    }


def check_directories() -> Dict[str, Any]:
    """Check if required directories exist."""
    required_dirs = [
        "config",
        "core",
        "interface",
        "processing",
        "storage",
        "cyber_documents",
        "cyber_vector_db",
    ]

    missing: list[str] = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing.append(dir_name)

    return {
        "name": "Directory Structure",
        "status": "🟢" if not missing else "🔴",
        "message": (
            "All directories present"
            if not missing
            else f"Missing: {', '.join(missing)}"
        ),
        "required": "Core project directories",
    }


def check_config_files() -> Dict[str, Any]:
    """Check if configuration files exist."""
    config_files = ["config/default.yaml", "config/dev.yaml", "config/prod.yaml"]

    missing: list[str] = []
    for config_file in config_files:
        if not Path(config_file).exists():
            missing.append(config_file)

    return {
        "name": "Configuration Files",
        "status": "🟢" if not missing else "🟡",
        "message": (
            "All config files present"
            if not missing
            else f"Missing: {', '.join(missing)}"
        ),
        "required": "At least default.yaml",
    }


def main() -> None:
    """Main health check function."""
    print("🔵 PepeluGPT System Health Check")
    print("=" * 50)

    checks = [
        check_python_version(),
        check_dependencies(),
        check_directories(),
        check_config_files(),
    ]

    all_passed = True
    for check in checks:
        print(f"{check['status']} {check['name']}: {check['message']}")
        if check["status"] == "🔴":
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🟢 System health check passed!")
        print("🟢 PepeluGPT is ready to run")
    else:
        print("🟡  System health check found issues")
        print("🔵 Please resolve the above issues before running PepeluGPT")
        sys.exit(1)


if __name__ == "__main__":
    main()
