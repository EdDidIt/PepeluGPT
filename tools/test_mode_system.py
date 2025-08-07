#!/usr/bin/env python3
"""
PepeluGPT Mode Switching System Test Suite

Tests all mode switching functionality, role management, and enhanced features.

Usage:
    python tools/test_mode_system.py --all
    python tools/test_mode_system.py --mode-switching
    python tools/test_mode_system.py --role-management
    python tools/test_mode_system.py --suggestions
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_command(command: List[str], capture_output: bool = True) -> Dict[str, Any]:
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }


def test_mode_switcher() -> List[Dict[str, Any]]:
    """Test basic mode switching functionality."""
    print("🔵 Testing Mode Switcher...")

    tests: List[Dict[str, Any]] = [
        {
            "name": "Get current status",
            "command": ["python", "tools/mode_switcher.py", "--status"],
            "expected_keywords": ["Current Mode", "Configuration Files"],
        },
        {
            "name": "Switch to adaptive mode",
            "command": ["python", "tools/mode_switcher.py", "--mode", "adaptive"],
            "expected_keywords": ["Mode switched to: adaptive"],
        },
        {
            "name": "Switch to classic mode",
            "command": ["python", "tools/mode_switcher.py", "--mode", "classic"],
            "expected_keywords": ["Mode switched to: classic"],
        },
    ]

    results: List[Dict[str, Any]] = []
    for test in tests:
        print(f"  Testing: {test['name']}")
        result = run_command(test["command"])  # type: ignore

        success = result["success"]
        if success and "expected_keywords" in test:
            success = any(
                keyword in result["stdout"] for keyword in test["expected_keywords"]  # type: ignore
            )

        results.append(
            {
                "name": test["name"],
                "success": success,
                "output": (
                    result["stdout"][:200] + "..."
                    if len(result["stdout"]) > 200
                    else result["stdout"]
                ),
            }
        )

        print(f"    {'✅' if success else '❌'} {test['name']}")
        if not success:
            print(f"    Error: {result.get('stderr', 'Unknown error')}")

    return results


def test_role_manager() -> List[Dict[str, Any]]:
    """Test role management functionality."""
    print("\n🔵 Testing Role Manager...")

    tests: List[Dict[str, Any]] = [
        {
            "name": "List available roles",
            "command": ["python", "tools/role_manager.py", "--list-roles"],
            "expected_keywords": ["Available Roles"],
        },
        {
            "name": "Get current role",
            "command": ["python", "tools/role_manager.py", "--get-role"],
            "expected_keywords": ["Current Role"],
        },
        {
            "name": "Set role to analyst",
            "command": ["python", "tools/role_manager.py", "--set-role", "analyst"],
            "expected_keywords": ["Role set to: analyst"],
        },
    ]

    results: List[Dict[str, Any]] = []
    for test in tests:
        print(f"  Testing: {test['name']}")
        result = run_command(test["command"])  # type: ignore

        success = result["success"]
        if success and "expected_keywords" in test:
            success = any(
                keyword in result["stdout"] for keyword in test["expected_keywords"]  # type: ignore
            )

        results.append(
            {
                "name": test["name"],
                "success": success,
                "output": (
                    result["stdout"][:200] + "..."
                    if len(result["stdout"]) > 200
                    else result["stdout"]
                ),
            }
        )

        print(f"    {'✅' if success else '❌'} {test['name']}")
        if not success:
            print(f"    Error: {result.get('stderr', 'Unknown error')}")

    return results


def test_mode_suggestions() -> List[Dict[str, Any]]:
    """Test mode suggestion functionality."""
    print("\n🔵 Testing Mode Suggestions...")

    try:
        from tools.mode_suggester import suggest_mode_for_query

        test_queries: List[Dict[str, Any]] = [
            {
                "query": "Explain the concept of threat intelligence",
                "expected_mode": "adaptive",
                "reason": "Exploratory question",
            },
            {
                "query": "Show me the exact steps for NIST compliance",
                "expected_mode": "classic",
                "reason": "Procedural request",
            },
            {
                "query": "What are the requirements for RMF implementation?",
                "expected_mode": "classic",
                "reason": "Specific requirements",
            },
            {
                "query": "Help me understand emerging cybersecurity trends",
                "expected_mode": "adaptive",
                "reason": "Research and exploration",
            },
        ]

        results: List[Dict[str, Any]] = []
        for test in test_queries:
            suggestion = suggest_mode_for_query(test["query"], "classic")
            suggested_mode = suggestion.get("suggested_mode")
            confidence = suggestion.get("confidence", 0)

            success = suggested_mode == test["expected_mode"] and confidence > 0.5

            results.append(
                {
                    "name": f"Suggest mode for: {test['query'][:50]}...",
                    "success": success,
                    "expected": test["expected_mode"],
                    "actual": suggested_mode,
                    "confidence": confidence,
                }
            )

            print(f"  {'✅' if success else '❌'} Query: {test['query'][:50]}...")
            print(
                f"    Expected: {test['expected_mode']}, Got: {suggested_mode} (confidence: {confidence:.2f})"
            )

        return results

    except Exception as e:
        print(f"  ❌ Mode suggestion test failed: {e}")
        return [{"name": "Mode Suggestions", "success": False, "error": str(e)}]


def test_config_files() -> List[Dict[str, Any]]:
    """Test configuration file integrity."""
    print("\n🔵 Testing Configuration Files...")

    config_files = [
        "config/default.yaml",
        "config/adaptive.yaml",
        "config/classic.yaml",
        "config/user_roles.yaml",
    ]

    results: List[Dict[str, Any]] = []
    for config_file in config_files:
        config_path = Path(__file__).parent.parent / config_file

        if config_path.exists():
            try:
                import yaml

                with open(config_path, "r") as f:
                    yaml.safe_load(f)

                results.append(
                    {"name": f"Load {config_file}", "success": True, "exists": True}
                )
                print(f"  ✅ {config_file} - Valid YAML")

            except Exception as e:
                results.append(
                    {
                        "name": f"Load {config_file}",
                        "success": False,
                        "exists": True,
                        "error": str(e),
                    }
                )
                print(f"  ❌ {config_file} - Invalid YAML: {e}")
        else:
            results.append(
                {"name": f"Check {config_file}", "success": False, "exists": False}
            )
            print(f"  ⚠️  {config_file} - File not found")

    return results


def test_integration() -> List[Dict[str, Any]]:
    """Test integration between components."""
    print("\n🔵 Testing Integration...")

    tests: List[Dict[str, Any]] = []

    # Test mode switcher with role integration
    try:
        from tools.mode_switcher import ModeManager
        from tools.role_manager import RoleManager

        mode_manager = ModeManager()
        role_manager = RoleManager()

        current_mode = mode_manager.get_current_mode()
        current_role = role_manager.get_current_role()
        default_mode = role_manager.get_default_mode_for_role()

        tests.append(
            {
                "name": "Mode-Role Integration",
                "success": True,
                "current_mode": current_mode,
                "current_role": current_role,
                "default_mode": default_mode,
            }
        )

        print(f"  ✅ Mode-Role Integration")
        print(f"    Current Mode: {current_mode}")
        print(f"    Current Role: {current_role}")
        print(f"    Role Default: {default_mode}")

    except Exception as e:
        tests.append(
            {"name": "Mode-Role Integration", "success": False, "error": str(e)}
        )
        print(f"  ❌ Mode-Role Integration: {e}")

    return tests


def generate_report(all_results: Dict[str, List[Dict[str, Any]]]) -> None:
    """Generate a test report."""
    print("\n📊 Test Report")
    print("=" * 50)

    total_tests = 0
    passed_tests = 0

    for category, results in all_results.items():
        category_passed = sum(1 for r in results if r.get("success", False))
        category_total = len(results)

        total_tests += category_total
        passed_tests += category_passed

        print(f"\n{category}:")
        print(f"  Passed: {category_passed}/{category_total}")

        for result in results:
            status = "✅" if result.get("success", False) else "❌"
            print(f"  {status} {result['name']}")

    print(f"\n🎯 Overall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {total_tests - passed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Mode switching system is working correctly.")
    else:
        print(
            f"\n⚠️  {total_tests - passed_tests} tests failed. Check the details above."
        )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Test PepeluGPT Mode Switching System")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument(
        "--mode-switching", action="store_true", help="Test mode switching"
    )
    parser.add_argument(
        "--role-management", action="store_true", help="Test role management"
    )
    parser.add_argument(
        "--suggestions", action="store_true", help="Test mode suggestions"
    )
    parser.add_argument(
        "--config", action="store_true", help="Test configuration files"
    )
    parser.add_argument("--integration", action="store_true", help="Test integration")

    args = parser.parse_args()

    if not any(
        [
            args.all,
            args.mode_switching,
            args.role_management,
            args.suggestions,
            args.config,
            args.integration,
        ]
    ):
        args.all = True

    print("🔵 PepeluGPT Mode Switching System Test Suite")
    print("=" * 50)

    all_results: Dict[str, List[Dict[str, Any]]] = {}

    if args.all or args.mode_switching:
        all_results["Mode Switching"] = test_mode_switcher()

    if args.all or args.role_management:
        all_results["Role Management"] = test_role_manager()

    if args.all or args.suggestions:
        all_results["Mode Suggestions"] = test_mode_suggestions()

    if args.all or args.config:
        all_results["Configuration Files"] = test_config_files()

    if args.all or args.integration:
        all_results["Integration"] = test_integration()

    generate_report(all_results)


if __name__ == "__main__":
    main()
