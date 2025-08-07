#!/usr/bin/env python3
"""
Test runner for PepeluGPT test suite.
Provides convenient commands for running different types of tests.
"""

import argparse
import subprocess
import sys
from typing import List


def run_command(cmd: List[str], description: str) -> bool:
    """Run a command and report results."""
    print(f"🧪 {description}")
    print(f"📋 Command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
    else:
        print(f"❌ {description} - FAILED")
    
    print()
    return result.returncode == 0


def main() -> int:
    """Main test runner."""
    parser = argparse.ArgumentParser(description="PepeluGPT Test Runner")
    
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "core", "plugins", "demo"],
        default="all",
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "--coverage",
        action="store_true", 
        help="Run with coverage reporting"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run with verbose output"
    )

    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = [sys.executable, "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        base_cmd.extend(["-v"])
    else:
        base_cmd.extend(["-q"])
    
    # Add coverage if requested
    if args.coverage:
        base_cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    # Determine test path and markers - initialize variables to avoid unbound errors
    test_path: str
    markers: List[str]
    
    if args.type == "all":
        test_path = "tests/"
        markers = []
    elif args.type == "unit":
        test_path = "tests/unit/"
        markers = ["-m", "unit"]
    elif args.type == "integration": 
        test_path = "tests/integration/"
        markers = ["-m", "integration"]
    elif args.type == "core":
        test_path = "tests/"
        markers = ["-m", "core"]
    elif args.type == "plugins":
        test_path = "tests/"
        markers = ["-m", "plugins"]
    elif args.type == "demo":
        test_path = "tests/demo/"
        markers = ["-m", "demo"]
    else:
        # This should never happen due to choices constraint, but satisfies type checker
        test_path = "tests/"
        markers = []
    
    # Build final command
    cmd = base_cmd + [test_path] + markers
    
    print("🚀 PepeluGPT Test Runner")
    print("=" * 50)
    
    success = run_command(cmd, f"Running {args.type} tests")
    
    if args.coverage and success:
        print("📊 Coverage report generated in htmlcov/")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
