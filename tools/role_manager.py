#!/usr/bin/env python3
"""
PepeluGPT Role Manager

Manages user roles and automatically selects appropriate modes based on
user context, role, and query patterns.

Usage:
    python tools/role_manager.py --set-role analyst
    python tools/role_manager.py --get-role
    python tools/role_manager.py --list-roles
    python tools/role_manager.py --auto-detect
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils import get_logger

LOG = get_logger(__name__)


class RoleManager:
    """Manages user roles and role-based mode preferences."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent
        self.roles_config_path = self.base_dir / "config" / "user_roles.yaml"
        self.user_state_file = self.base_dir / ".user_state"

        self.roles_config = self._load_roles_config()

    def _load_roles_config(self) -> Dict[str, Any]:
        """Load roles configuration from YAML file."""
        try:
            if self.roles_config_path.exists():
                with open(self.roles_config_path, "r") as f:
                    return yaml.safe_load(f)
            else:
                LOG.warning(f"Roles config not found: {self.roles_config_path}")
                return self._get_default_roles_config()
        except Exception as e:
            LOG.error(f"Failed to load roles config: {e}")
            return self._get_default_roles_config()

    def _get_default_roles_config(self) -> Dict[str, Any]:
        """Get default roles configuration if file is missing."""
        return {
            "roles": {
                "analyst": {
                    "default_mode": "classic",
                    "description": "SOC analyst requiring fast, consistent responses",
                },
                "researcher": {
                    "default_mode": "adaptive",
                    "description": "Security researcher exploring new concepts",
                },
                "admin": {
                    "default_mode": "mixed",
                    "description": "Admin with full control capabilities",
                },
            },
            "default_role": "analyst",
        }

    def get_current_role(self) -> str:
        """Get the currently active user role."""
        try:
            if self.user_state_file.exists():
                with open(self.user_state_file, "r") as f:
                    state = yaml.safe_load(f)
                    return state.get(
                        "role", self.roles_config.get("default_role", "analyst")
                    )
        except Exception as e:
            LOG.warning(f"Could not determine current role: {e}")

        return self.roles_config.get("default_role", "analyst")

    def set_role(self, role: str) -> bool:
        """Set the active user role."""
        if role not in self.get_available_roles():
            LOG.error(f"Invalid role: {role}")
            return False

        try:
            state = {
                "role": role,
                "timestamp": self._get_timestamp(),
                "previous_role": self.get_current_role(),
            }

            with open(self.user_state_file, "w") as f:
                yaml.dump(state, f, default_flow_style=False)

            LOG.info(f"Role set to: {role}")
            return True

        except Exception as e:
            LOG.error(f"Failed to set role: {e}")
            return False

    def get_available_roles(self) -> List[str]:
        """Get list of available roles."""
        return list(self.roles_config.get("roles", {}).keys())

    def get_role_info(self, role: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific role."""
        return self.roles_config.get("roles", {}).get(role)

    def get_default_mode_for_role(self, role: Optional[str] = None) -> str:
        """Get the default mode for a role."""
        if role is None:
            role = self.get_current_role()

        role_info = self.get_role_info(role)
        if role_info:
            return role_info.get("default_mode", "classic")

        return "classic"

    def should_suggest_mode_switch(
        self, query: str, current_mode: str, role: Optional[str] = None
    ) -> Optional[str]:
        """Check if a mode switch should be suggested based on role and query."""
        if role is None:
            role = self.get_current_role()

        role_info = self.get_role_info(role)
        if not role_info:
            return None

        # Get switching rules for this role
        switching_rules = self.roles_config.get("switching_rules", {}).get(role, {})

        # Check if role suggests adaptive mode
        if (
            switching_rules.get("suggest_learning", False)
            and current_mode != "adaptive"
        ):
            # Look for research-oriented keywords
            research_keywords = [
                "explore",
                "research",
                "analyze",
                "understand",
                "learn",
            ]
            if any(keyword in query.lower() for keyword in research_keywords):
                return "adaptive"

        # Check if role suggests classic mode
        if (
            switching_rules.get("suggest_deterministic", False)
            and current_mode != "classic"
        ):
            # Look for compliance/procedure keywords
            classic_keywords = switching_rules.get("auto_suggest_deterministic", [])
            if any(keyword in query.lower() for keyword in classic_keywords):
                return "classic"

        return None

    def auto_detect_role(self) -> Optional[str]:
        """Attempt to auto-detect role based on environment and context."""
        detection_config = self.roles_config.get("role_detection", {})

        # Check environment variables
        user_name = os.environ.get("USERNAME", "").lower()
        computer_name = os.environ.get("COMPUTERNAME", "").lower()
        domain = os.environ.get("USERDOMAIN", "").lower()

        # Simple role detection based on naming patterns
        for role, patterns in detection_config.items():
            # Check keywords in username/domain
            keywords = patterns.get("keywords", [])
            if any(
                keyword in user_name or keyword in computer_name or keyword in domain
                for keyword in keywords
            ):
                return role

            # Check domain patterns
            domains = patterns.get("domains", [])
            if any(domain_pattern in domain for domain_pattern in domains):
                return role

        return None

    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime

        return datetime.now().isoformat()

    def print_role_status(self):
        """Print current role status and information."""
        current_role = self.get_current_role()
        role_info = self.get_role_info(current_role)

        print(f"👤 Current Role: {current_role.upper()}")

        if role_info:
            print(f"� Description: {role_info.get('description', 'No description')}")
            print(
                f"🎯 Default Mode: {role_info.get('default_mode', 'classic').upper()}"
            )

            preferences = role_info.get("preferences", {})
            if preferences:
                print("🔵 Preferences:")
                for key, value in preferences.items():
                    print(f"   • {key}: {value}")

            access_levels = role_info.get("access_levels", [])
            if access_levels:
                print("� Access Levels:")
                for level in access_levels:
                    print(f"   • {level}")

        print()

        # Show switching behavior
        switching_rules = self.roles_config.get("switching_rules", {}).get(
            current_role, {}
        )
        if switching_rules:
            print("🔄 Mode Switching Behavior:")
            for rule, value in switching_rules.items():
                print(f"   • {rule}: {value}")

        print()

    def list_all_roles(self):
        """List all available roles with descriptions."""
        print("� Available Roles:")
        print("=" * 40)

        roles = self.roles_config.get("roles", {})
        for role_name, role_info in roles.items():
            print(f"� {role_name.upper()}")
            print(f"   Description: {role_info.get('description', 'No description')}")
            print(f"   Default Mode: {role_info.get('default_mode', 'classic')}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="PepeluGPT Role Manager - Manage user roles and mode preferences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --get-role                         # Show current role
  %(prog)s --set-role analyst                 # Set role to analyst
  %(prog)s --list-roles                       # List all available roles
  %(prog)s --auto-detect                      # Auto-detect role from environment
        """,
    )

    parser.add_argument(
        "--get-role",
        "-g",
        action="store_true",
        help="Show current role and preferences",
    )

    parser.add_argument("--set-role", "-s", help="Set the active user role")

    parser.add_argument(
        "--list-roles", "-l", action="store_true", help="List all available roles"
    )

    parser.add_argument(
        "--auto-detect",
        "-a",
        action="store_true",
        help="Auto-detect role from environment",
    )

    parser.add_argument("--base-dir", help="Base directory of PepeluGPT project")

    args = parser.parse_args()

    # Initialize role manager
    manager = RoleManager(args.base_dir)

    try:
        if args.list_roles:
            manager.list_all_roles()

        elif args.set_role:
            if manager.set_role(args.set_role):
                print(f"✅ Role set to: {args.set_role}")
                manager.print_role_status()
            else:
                print(f"❌ Failed to set role to: {args.set_role}")
                print("Available roles:", ", ".join(manager.get_available_roles()))
                sys.exit(1)

        elif args.auto_detect:
            detected_role = manager.auto_detect_role()
            if detected_role:
                print(f"🔍 Auto-detected role: {detected_role}")
                confirm = input(f"Set role to {detected_role}? (y/N): ").strip().lower()
                if confirm == "y":
                    if manager.set_role(detected_role):
                        print(f"✅ Role set to: {detected_role}")
                    else:
                        print("❌ Failed to set role")
            else:
                print("🔍 Could not auto-detect role from environment")
                print("Available roles:", ", ".join(manager.get_available_roles()))

        elif args.get_role or not any(
            [args.set_role, args.list_roles, args.auto_detect]
        ):
            manager.print_role_status()

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
