#!/usr/bin/env python3
"""
Setup script for PepeluGPT development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a command and handle errors."""
    print(f"🔵 {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"🟢 {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"🔴 {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🔵 PepeluGPT Development Setup")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("🔴 Python 3.8+ required")
        sys.exit(1)

    print(f"🟢 Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)

    # Create cache directory
    cache_dir = Path("cyber_vector_db")
    cache_dir.mkdir(exist_ok=True)
    print("🟢 Cache directory created")

    # Test basic functionality
    if not run_command("python tools/admin/data_cli.py status", "Testing admin tools"):
        print("🟡  Admin tools test failed, but setup completed")

    print("\n🟢 Setup completed successfully!")
    print("\n🟢 Quick start:")
    print("  python main.py                           # Start PepeluGPT")
    print("  python tools/admin/data_cli.py status    # Check system status")
    print("  python tools/demo/conditional_parsing_demo.py  # See demo")


if __name__ == "__main__":
    main()
