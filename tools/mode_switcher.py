#!/usr/bin/env python3
"""
PepeluGPT Mode Switcher Utility

Seamlessly switch between adaptive and classic modes with config management,
runtime commands, and session persistence.

Usage:
    python tools/mode_switcher.py --mode adaptive
    python tools/mode_switcher.py --mode classic
    python tools/mode_switcher.py --status
    python tools/mode_switcher.py --interactive
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils import get_logger

LOG = get_logger(__name__)


class ModeManager:
    """Manages switching between adaptive and classic modes."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"
        self.mode_state_file = self.base_dir / ".mode_state"

        # Default configurations for each mode
        self.mode_configs = {
            "classic": "config/classic.yaml",
            "adaptive": "config/adaptive.yaml",
        }

        # Legacy support mapping (with deprecation warnings)
        self.legacy_mode_mapping = {"deterministic": "classic", "learning": "adaptive"}

        # Backup directory for config safety
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def get_current_mode(self) -> str:
        """Get the currently active mode."""
        try:
            if self.mode_state_file.exists():
                with open(self.mode_state_file, "r") as f:
                    state = yaml.safe_load(f)
                    mode = state.get("mode", "classic")
                    # Handle legacy mode names
                    if mode in self.legacy_mode_mapping:
                        return self.legacy_mode_mapping[mode]
                    return mode

            # Check config file to determine mode
            default_config = self.config_dir / "default.yaml"
            if default_config.exists():
                with open(default_config, "r") as f:
                    config = yaml.safe_load(f)
                    learning_enabled = config.get("learning", {}).get("enabled", False)
                    return "adaptive" if learning_enabled else "classic"

        except Exception as e:
            LOG.warning(f"Could not determine current mode: {e}")

        return "classic"  # Default fallback

    def set_mode(self, mode: str, config_path: Optional[str] = None) -> bool:
        """
        Switch to specified mode.

        Args:
            mode: 'adaptive' or 'classic' (legacy: 'learning' or 'deterministic')
            config_path: Optional custom config path

        Returns:
            True if successful, False otherwise
        """
        # Handle legacy mode names with deprecation warning
        original_mode = mode
        if mode in self.legacy_mode_mapping:
            LOG.warning(
                f"[Deprecation] Mode '{mode}' is deprecated. Use '{self.legacy_mode_mapping[mode]}' instead."
            )
            mode = self.legacy_mode_mapping[mode]

        if mode not in ["adaptive", "classic"]:
            LOG.error(f"Invalid mode: {original_mode}. Must be 'adaptive' or 'classic'")
            return False

        try:
            # Create backup of current state
            self._create_backup()

            # Use provided config or default for mode
            source_config = config_path or self.mode_configs[mode]
            source_path = self.base_dir / source_config

            if not source_path.exists():
                LOG.error(f"Config file not found: {source_path}")
                return False

            # Update mode state file
            state = {
                "mode": mode,
                "timestamp": datetime.now().isoformat(),
                "config_source": str(source_config),
                "previous_mode": self.get_current_mode(),
            }

            with open(self.mode_state_file, "w") as f:
                yaml.dump(state, f, default_flow_style=False)

            # Update default config if switching modes
            if mode == "adaptive":
                self._enable_adaptive_mode(source_path)
            else:
                self._enable_classic_mode(source_path)

            LOG.info(f"Successfully switched to {mode} mode")
            return True

        except Exception as e:
            LOG.error(f"Failed to switch to {mode} mode: {e}")
            return False

    def _enable_adaptive_mode(self, source_config: Path):
        """Enable adaptive mode configuration."""
        # Copy adaptive config to active position if needed
        target_config = self.config_dir / "active_config.yaml"
        shutil.copy2(source_config, target_config)

        # Ensure learning is enabled in default.yaml
        default_config = self.config_dir / "default.yaml"
        if default_config.exists():
            with open(default_config, "r") as f:
                config = yaml.safe_load(f)

            # Enable learning
            if "learning" not in config:
                config["learning"] = {}
            config["learning"]["enabled"] = True

            with open(default_config, "w") as f:
                yaml.dump(config, f, default_flow_style=False)

    def _enable_classic_mode(self, source_config: Path):
        """Enable classic mode configuration."""
        # Update default config to disable learning
        default_config = self.config_dir / "default.yaml"
        if default_config.exists():
            with open(default_config, "r") as f:
                config = yaml.safe_load(f)

            # Disable learning
            if "learning" not in config:
                config["learning"] = {}
            config["learning"]["enabled"] = False

            with open(default_config, "w") as f:
                yaml.dump(config, f, default_flow_style=False)

    def _create_backup(self):
        """Create backup of current configuration."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = self.backup_dir / f"backup_{timestamp}"
        backup_subdir.mkdir(exist_ok=True)

        # Backup all config files
        for config_file in self.config_dir.glob("*.yaml"):
            if config_file.is_file():
                backup_file = backup_subdir / config_file.name
                shutil.copy2(config_file, backup_file)

        # Backup mode state if exists
        if self.mode_state_file.exists():
            shutil.copy2(self.mode_state_file, backup_subdir / ".mode_state")

    def get_mode_status(self) -> Dict[str, Any]:
        """Get detailed status of current mode configuration."""
        current_mode = self.get_current_mode()

        status: Dict[str, Any] = {
            "current_mode": current_mode,
            "timestamp": datetime.now().isoformat(),
            "configs_available": {},
            "mode_state_exists": self.mode_state_file.exists(),
        }

        # Check available configurations
        for mode, config_path in self.mode_configs.items():
            full_path = self.base_dir / config_path
            status["configs_available"][mode] = {
                "path": str(config_path),
                "exists": full_path.exists(),
                "readable": full_path.exists() and os.access(full_path, os.R_OK),
            }

        # Add mode state info if available
        if self.mode_state_file.exists():
            try:
                with open(self.mode_state_file, "r") as f:
                    mode_state = yaml.safe_load(f)
                    status["mode_state"] = mode_state
            except Exception as e:
                status["mode_state_error"] = str(e)

        return status

    def interactive_mode(self):
        """Start interactive mode selection with role awareness."""
        print("\n🎯 PepeluGPT Mode Switcher")
        print("=" * 40)

        # Show role information if available
        try:
            from tools.role_manager import RoleManager

            role_manager = RoleManager()
            current_role = role_manager.get_current_role()
            default_mode = role_manager.get_default_mode_for_role()
            # Map legacy default mode to new names
            if default_mode in self.legacy_mode_mapping:
                default_mode = self.legacy_mode_mapping[default_mode]
            print(f"👤 Current Role: {current_role.upper()}")
            print(f"🎯 Role Default Mode: {default_mode.upper()}")
            print()
        except Exception:
            LOG.debug("Role manager not available")

        status = self.get_mode_status()
        current_mode = status["current_mode"]

        print(f"Current Mode: {current_mode.upper()}")
        print(f"Available Modes:")

        modes_info = {
            "classic": {
                "description": "Rule-based, predictable, fast responses",
                "benefits": "Auditable, consistent, no ML overhead",
                "trade_offs": "No adaptation, manual updates required",
                "best_for": "SOC analysts, compliance officers, production",
            },
            "adaptive": {
                "description": "AI-enhanced, personalized, improves with feedback",
                "benefits": "Gets smarter over time, contextual responses",
                "trade_offs": "Requires feedback, less predictable",
                "best_for": "Researchers, trainees, exploration",
            },
        }

        for i, (mode, info) in enumerate(modes_info.items(), 1):
            marker = "→" if mode == current_mode else " "
            print(f"{marker} {i}. {mode.upper()}")
            print(f"   {info['description']}")
            print(f"   ✓ {info['benefits']}")
            print(f"   ⚠ {info['trade_offs']}")
            print(f"   👥 Best for: {info['best_for']}")
            print()

        while True:
            try:
                choice = (
                    input(
                        "Select mode (1-2), 'r' for roles, 's' for status, 'q' to quit: "
                    )
                    .strip()
                    .lower()
                )

                if choice == "q":
                    break
                elif choice == "r":
                    self._show_role_options()
                    continue
                elif choice == "s":
                    self.print_detailed_status(status)
                    continue
                elif choice in ["1", "2"]:
                    mode_list = list(modes_info.keys())
                    selected_mode = mode_list[int(choice) - 1]

                    if selected_mode == current_mode:
                        print(f"Already in {selected_mode} mode!")
                        continue

                    # Check role compatibility
                    try:
                        from tools.role_manager import RoleManager

                        role_manager = RoleManager()
                        role_default = role_manager.get_default_mode_for_role()
                        # Map legacy role default to new names
                        if role_default in self.legacy_mode_mapping:
                            role_default = self.legacy_mode_mapping[role_default]
                        if selected_mode != role_default:
                            print(
                                f"⚠️  Note: Your role ({role_manager.get_current_role()}) typically uses {role_default} mode."
                            )
                            print(
                                f"    You can still switch to {selected_mode} mode if needed."
                            )
                    except Exception:
                        pass

                    confirm = (
                        input(f"Switch to {selected_mode} mode? (y/N): ")
                        .strip()
                        .lower()
                    )
                    if confirm == "y":
                        if self.set_mode(selected_mode):
                            print(f"✅ Successfully switched to {selected_mode} mode")
                            print("🔄 Restart PepeluGPT to apply changes")
                        else:
                            print("❌ Failed to switch mode")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 'r', 's', or 'q'")

            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                break

    def _show_role_options(self):
        """Show role management options."""
        try:
            from tools.role_manager import RoleManager

            role_manager = RoleManager()

            print("\n👥 Role Management:")
            print("-" * 30)
            role_manager.print_role_status()

            print("Role Commands:")
            print(
                "  • Use 'python tools/role_manager.py --set-role <role>' to change role"
            )
            print(
                "  • Use 'python tools/role_manager.py --list-roles' to see all roles"
            )
            print()

        except Exception as e:
            print(f"Role management not available: {e}")
            print("Install role management features to use this functionality.")
            print()

    def print_detailed_status(self, status: Dict[str, Any]):
        """Print detailed status information."""
        print("\n📊 Detailed Status")
        print("-" * 30)
        print(f"Current Mode: {status['current_mode']}")
        print(f"Timestamp: {status['timestamp']}")
        print(f"Mode State File: {'✓' if status['mode_state_exists'] else '✗'}")

        print("\nConfiguration Files:")
        for mode, config_info in status["configs_available"].items():
            exists = "✓" if config_info["exists"] else "✗"
            readable = "✓" if config_info["readable"] else "✗"
            print(
                f"  {mode}: {exists} exists, {readable} readable - {config_info['path']}"
            )

        if "mode_state" in status:
            print("\nMode State Details:")
            state = status["mode_state"]
            print(f"  Last Switch: {state.get('timestamp', 'Unknown')}")
            print(f"  Previous Mode: {state.get('previous_mode', 'Unknown')}")
            print(f"  Config Source: {state.get('config_source', 'Unknown')}")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="PepeluGPT Mode Switcher - Switch between adaptive and classic modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode adaptive                    # Switch to adaptive mode
  %(prog)s --mode classic                     # Switch to classic mode  
  %(prog)s --status                           # Show current mode status
  %(prog)s --interactive                      # Interactive mode selection
  %(prog)s --mode adaptive --config custom.yaml  # Use custom config
  
Legacy Support (deprecated):
  %(prog)s --mode learning                    # Use --mode adaptive instead
  %(prog)s --mode deterministic               # Use --mode classic instead
        """,
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=["adaptive", "classic", "learning", "deterministic"],
        help="Mode to switch to (learning/deterministic are deprecated, use adaptive/classic)",
    )

    parser.add_argument(
        "--config", "-c", help="Custom config file path (relative to project root)"
    )

    parser.add_argument(
        "--status", "-s", action="store_true", help="Show current mode status"
    )

    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode selection"
    )

    parser.add_argument("--base-dir", help="Base directory of PepeluGPT project")

    args = parser.parse_args()

    # Initialize mode manager
    manager = ModeManager(args.base_dir)

    try:
        if args.interactive:
            manager.interactive_mode()
        elif args.status:
            status = manager.get_mode_status()
            manager.print_detailed_status(status)
        elif args.mode:
            success = manager.set_mode(args.mode, args.config)
            if success:
                # Map to current mode name for display
                display_mode = manager.legacy_mode_mapping.get(args.mode, args.mode)
                print(f"✅ Mode switched to: {display_mode}")
                print("🔄 Restart PepeluGPT to apply changes")

                # Show quick usage reminder
                if display_mode == "adaptive":
                    print("\n💡 Adaptive Mode Tips:")
                    print("  • Rate responses: 'rate 1-5'")
                    print("  • Provide corrections: 'correct: better answer'")
                    print("  • Use 'session' to see history")
                else:
                    print("\n⚡ Classic Mode:")
                    print("  • Fast, consistent responses")
                    print("  • Rule-based processing")
                    print("  • No feedback collection")
            else:
                print(f"❌ Failed to switch to {args.mode} mode")
                sys.exit(1)
        else:
            # No specific action, show current status
            current_mode = manager.get_current_mode()
            print(f"Current mode: {current_mode}")
            print("Use --help for more options")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
