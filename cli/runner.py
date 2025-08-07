#!/usr/bin/env python3
"""
CLI runner for PepeluGPT - handles mode resolution, config loading, and orchestrator launch.
"""

import argparse
import sys
from typing import Any, Dict

from cli.utils import display_banner, interactive_mode_selection
from core.logging_config import log_error, setup_enhanced_logging
from core.orchestrator import Orchestrator


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        import yaml

        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"🔴 Failed to load config from {config_path}: {e}")
        return {}


def resolve_mode(args: argparse.Namespace) -> str:
    """Resolve the mode to use - either from args or interactive selection."""
    # Check if mode is set (only available for chat command)
    mode = getattr(args, "mode", None)
    if mode:
        print(f"� Mode override: {mode}")
        return mode

    # Interactive mode selection
    return interactive_mode_selection()


def setup_mode_and_config(
    args: argparse.Namespace, selected_mode: str
) -> tuple[str, str]:
    """Setup mode and return internal mode name and config path."""
    # Convert user-friendly names to internal mode names
    mode_mapping = {"adaptive": "adaptive", "classic": "classic"}
    internal_mode = mode_mapping.get(selected_mode, selected_mode)

    # Use mode switcher to properly set the mode
    try:
        from tools.mode_switcher import ModeManager

        mode_manager = ModeManager()
        current_mode = mode_manager.get_current_mode()

        if current_mode != internal_mode:
            print(f"� Switching to {selected_mode} mode...")
            if mode_manager.set_mode(internal_mode):
                # Update config path to use the mode-specific config
                config_path = mode_manager.mode_configs[internal_mode]
            else:
                print(f"🟡 Could not switch mode, using current: {current_mode}")
                internal_mode = current_mode
                config_path = mode_manager.mode_configs[current_mode]
        else:
            # Use the appropriate config for current mode
            config_path = mode_manager.mode_configs[internal_mode]

    except Exception as e:
        print(f"⚠️ Mode switching not available: {e}")
        # Fallback to config file selection
        fallback_configs = {
            "adaptive": "config/adaptive.yaml",
            "classic": "config/classic.yaml",
        }
        config_path = fallback_configs.get(selected_mode, args.config) or args.config

    return internal_mode, config_path


def run_cli(args: argparse.Namespace):
    """Main CLI runner function with subcommand support."""
    # Handle subcommands
    if args.command == "status":
        from cli.commands import handle_status_command

        handle_status_command(args)
        return
    elif args.command == "config":
        from cli.commands import handle_config_command

        handle_config_command(args)
        return
    elif args.command == "audit":
        from cli.audit import handle_audit_command

        if args.audit_action == "run" or args.audit_action is None:
            # Check if framework-specific audit requested
            if hasattr(args, "framework") and args.framework:
                from cli.plugins import handle_framework_audit_command

                handle_framework_audit_command(args)
            else:
                # Default to 'run' if no audit action specified
                handle_audit_command(args)
        elif args.audit_action == "history":
            from cli.audit_history import handle_audit_history_command

            handle_audit_history_command(args)
        elif args.audit_action == "trends":
            from cli.audit_history import handle_audit_trends_command

            handle_audit_trends_command(args)
        else:
            print(f"❌ Unknown audit action: {args.audit_action}")
            return 1
        return
    elif args.command == "plugins":
        from cli.plugins import handle_plugins_command

        handle_plugins_command(args)
        return
    elif args.command == "chat":
        # Continue with the chat functionality below
        pass
    else:
        print(f"❌ Unknown command: {args.command}")
        sys.exit(1)

    # Chat command logic (original main functionality)
    try:
        display_banner()
        print("🔵 Initializing PepeluGPT...")

        # Resolve mode
        selected_mode = resolve_mode(args)
        
        # Show processing message after mode selection
        print("Processing...")
        
        _internal_mode, config_path = setup_mode_and_config(args, selected_mode)

        # Load configuration
        config = load_config(config_path)

        # Setup enhanced logging system
        setup_enhanced_logging(config, debug=args.debug)

        # Launch orchestrator
        orchestrator = Orchestrator(config_path=config_path, args=args)
        orchestrator.run()

    except Exception as e:
        log_error(e, "cli_runner", "STARTUP_001")
        print(
            f"🔴 Chat Not Ready\n🔵 Contact the development team to enable full functionality.\n� Be sure to include the following error code: {str(e)}"
        )
        sys.exit(1)
