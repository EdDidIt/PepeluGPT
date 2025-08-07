#!/usr/bin/env python3
"""
Command handlers for PepeluGPT CLI subcommands.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from cli.utils import get_mode_display_name


def handle_status_command(args: argparse.Namespace) -> None:
    """Handle the status subcommand."""
    from cli.runner import load_config

    try:
        # Get current mode information
        try:
            from tools.mode_switcher import ModeManager

            mode_manager = ModeManager()
            current_mode = mode_manager.get_current_mode()
            config_path = mode_manager.mode_configs.get(current_mode, args.config)
            mode_available = True
        except Exception:
            current_mode = "unknown"
            config_path = args.config
            mode_available = False

        # Load configuration
        config = load_config(config_path or args.config)

        # Prepare status information
        status_info: Dict[str, Any] = {
            "mode": {
                "current": current_mode,
                "display_name": get_mode_display_name(current_mode),
                "mode_switching_available": mode_available,
            },
            "configuration": {
                "config_file": config_path or args.config,
                "config_exists": os.path.exists(config_path or args.config),
                "config_valid": bool(config),
                "debug_enabled": args.debug,
            },
            "system": {
                "python_version": sys.version.split()[0],
                "working_directory": os.getcwd(),
                "pepchat_available": True,  # Assuming always available
            },
        }

        # Add config details if available
        if config:
            status_info["configuration"]["loaded_sections"] = list(config.keys())

        if args.json:
            print(json.dumps(status_info, indent=2))
        else:
            # Human-readable format
            print("🔍 PepeluGPT System Status")
            print("=" * 40)

            # Mode information
            mode_display = status_info["mode"]["display_name"]
            mode_status = "✅" if mode_available else "⚠️"
            print(f"\n🎯 Mode: {mode_status} {mode_display}")
            if not mode_available:
                print("   ⚠️  Mode switching unavailable")

            # Configuration
            config_status = (
                "✅" if status_info["configuration"]["config_valid"] else "❌"
            )
            print(f"\n📁 Configuration: {config_status}")
            print(f"   File: {config_path}")
            print(
                f"   Exists: {'✅' if status_info['configuration']['config_exists'] else '❌'}"
            )
            print(
                f"   Valid: {'✅' if status_info['configuration']['config_valid'] else '❌'}"
            )

            if config:
                sections = ", ".join(status_info["configuration"]["loaded_sections"])
                print(f"   Sections: {sections}")

            # System
            print(f"\n🖥️  System:")
            print(f"   Python: {status_info['system']['python_version']}")
            print(f"   Working Dir: {status_info['system']['working_directory']}")
            print(f"   Debug: {'✅ Enabled' if args.debug else '❌ Disabled'}")

            print(f"\n🚀 Ready to launch PepeluGPT!")

    except Exception as e:
        if args.json:
            error_info = {"error": str(e), "status": "failed"}
            print(json.dumps(error_info, indent=2))
        else:
            print(f"❌ Error getting status: {e}")
        sys.exit(1)


def handle_config_command(args: argparse.Namespace) -> None:
    """Handle the config subcommand and its actions."""
    if args.config_action == "validate":
        handle_config_validate(args)
    elif args.config_action == "show":
        handle_config_show(args)
    elif args.config_action == "list":
        handle_config_list(args)
    else:
        print("❌ No config action specified. Use 'validate', 'show', or 'list'.")
        sys.exit(1)


def handle_config_validate(args: argparse.Namespace) -> None:
    """Validate the configuration file."""
    from cli.runner import load_config

    print(f"🔍 Validating configuration: {args.config}")

    # Check if file exists
    if not os.path.exists(args.config):
        print(f"❌ Configuration file not found: {args.config}")
        sys.exit(1)

    # Try to load config
    config = load_config(args.config)
    if not config:
        print(f"❌ Configuration file is invalid or empty: {args.config}")
        sys.exit(1)

    # Basic validation checks
    validation_results: list[str] = []

    # Check for required sections (customize based on your app needs)
    required_sections = ["logging", "mode"]  # Adjust as needed
    for section in required_sections:
        if section in config:
            validation_results.append(f"✅ Section '{section}' found")
        else:
            validation_results.append(f"⚠️  Section '{section}' missing")

    # Display results
    print("\n📋 Validation Results:")
    for result in validation_results:
        print(f"   {result}")

    # Check for unknown keys (optional warning)
    known_sections = set(
        required_sections + ["database", "api", "features"]
    )  # Expand as needed
    unknown_sections = set(config.keys()) - known_sections
    if unknown_sections:
        print(f"\n💡 Unknown sections found: {', '.join(unknown_sections)}")
        print("   These may be custom configurations.")

    print(f"\n✅ Configuration validation complete!")


def handle_config_show(args: argparse.Namespace) -> None:
    """Show current configuration."""
    from cli.runner import load_config

    print(f"📋 Current Configuration: {args.config}")
    print("=" * 50)

    config = load_config(args.config)
    if not config:
        print(f"❌ Could not load configuration from: {args.config}")
        sys.exit(1)

    # Pretty print the configuration
    print(json.dumps(config, indent=2))


def handle_config_list(args: argparse.Namespace) -> None:
    """List available configuration files."""
    config_dir = Path("config")

    print("📁 Available Configuration Files:")
    print("=" * 40)

    if not config_dir.exists():
        print("❌ Config directory not found")
        return

    # Find all YAML files in config directory
    config_files = list(config_dir.glob("*.yaml")) + list(config_dir.glob("*.yml"))

    if not config_files:
        print("❌ No configuration files found in config/")
        return

    for config_file in sorted(config_files):
        # Get file size and modification time
        stat = config_file.stat()
        size = stat.st_size
        mtime = stat.st_mtime

        # Format size
        if size < 1024:
            size_str = f"{size}B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f}KB"
        else:
            size_str = f"{size/(1024*1024):.1f}MB"

        # Format time
        import datetime

        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")

        # Check if it's the current config
        current_marker = "📍" if str(config_file) == args.config else "📄"

        print(f"   {current_marker} {config_file.name}")
        print(f"      Size: {size_str}, Modified: {mtime_str}")

        # Try to get a brief description if possible
        try:
            from cli.runner import load_config

            config_data = load_config(str(config_file))
            if config_data and "description" in config_data:
                print(f"      Description: {config_data['description']}")
        except:
            pass  # Ignore errors when trying to read description

        print()  # Empty line between files
