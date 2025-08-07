#!/usr/bin/env python3
"""
Argument parsing for PepeluGPT CLI with subcommands.
"""

import argparse


def parse_args():
    """Parse command line arguments for PepeluGPT CLI with subcommands."""
    parser = argparse.ArgumentParser(
        description="PepeluGPT - Your Cybersecurity AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s chat --mode adaptive          # Launch interactive chat
  %(prog)s status                        # Show system status
  %(prog)s config validate               # Validate configuration
  %(prog)s --debug chat                  # Launch with debug logging
        """,
    )

    # Global arguments
    parser.add_argument(
        "--config",
        "-c",
        default="config/default.yaml",
        help="Path to configuration YAML",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--version", "-v", action="version", version="PepeluGPT 1.1.0")

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", metavar="COMMAND"
    )

    # Chat subcommand (default behavior)
    chat_parser = subparsers.add_parser(
        "chat",
        help="Launch interactive chat session (default)",
        description="Start an interactive Q&A session with PepeluGPT",
    )
    chat_parser.add_argument(
        "--preload-data",
        action="store_true",
        help="Force data loading on startup (data loads automatically on first query if not cached)",
    )
    chat_parser.add_argument(
        "--mode",
        choices=["adaptive", "classic"],
        help="Force specific mode: adaptive (exploratory) or classic (stable)",
    )

    # Status subcommand
    status_parser = subparsers.add_parser(
        "status",
        help="Show system status and configuration",
        description="Display current mode, configuration, and system health",
    )
    status_parser.add_argument(
        "--json", action="store_true", help="Output status in JSON format"
    )

    # Config subcommand
    config_parser = subparsers.add_parser(
        "config",
        help="Configuration management",
        description="Validate, edit, or manage configuration files",
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_action", help="Configuration actions"
    )

    # Config validate
    config_subparsers.add_parser(
        "validate",
        help="Validate configuration file",
        description="Check configuration file for errors and completeness",
    )

    # Config show
    config_subparsers.add_parser(
        "show",
        help="Display current configuration",
        description="Show the current configuration settings",
    )

    # Config list
    config_subparsers.add_parser(
        "list",
        help="List available configuration files",
        description="Show all available configuration files",
    )

    # Audit subcommand
    audit_parser = subparsers.add_parser(
        "audit",
        help="Security and compliance auditing",
        description="Run security audits and compliance checks",
    )
    audit_subparsers = audit_parser.add_subparsers(
        dest="audit_action", help="Audit actions", metavar="ACTION"
    )

    # Audit run command
    run_parser = audit_subparsers.add_parser(
        "run",
        help="Run security audit",
        description="Execute security and compliance audits",
    )
    run_parser.add_argument(
        "--type",
        choices=["security", "config", "dependencies", "documents", "all"],
        default="all",
        help="Type of audit to perform",
    )
    run_parser.add_argument(
        "--output",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format for audit results",
    )
    run_parser.add_argument(
        "--severity",
        choices=["low", "medium", "high", "critical"],
        help="Filter results by minimum severity level",
    )
    run_parser.add_argument("--save", metavar="FILE", help="Save audit report to file")
    run_parser.add_argument(
        "--framework", help="Specific framework(s) to run (comma-separated)"
    )
    run_parser.add_argument(
        "--control", help="Specific control(s) to run (comma-separated)"
    )

    # Audit history commands (Phase 4 preview)
    history_parser = audit_subparsers.add_parser(
        "history",
        help="View audit history",
        description="Display historical audit reports",
    )
    history_parser.add_argument(
        "--limit", type=int, default=10, help="Number of reports to show"
    )
    history_parser.add_argument("--type", help="Filter by audit type")

    trend_parser = audit_subparsers.add_parser(
        "trends", help="View audit trends", description="Analyze audit trends over time"
    )
    trend_parser.add_argument("--days", type=int, default=30, help="Days to analyze")
    trend_parser.add_argument("--type", help="Filter by audit type")

    # Plugins subcommand (Phase 5)
    plugins_parser = subparsers.add_parser(
        "plugins",
        help="Plugin management",
        description="Manage audit plugins and frameworks",
    )
    plugins_subparsers = plugins_parser.add_subparsers(
        dest="plugin_action", help="Plugin actions", metavar="ACTION"
    )

    # Plugin list command
    plugins_subparsers.add_parser(
        "list",
        help="List installed plugins",
        description="Display all registered audit plugins",
    )

    # Plugin install command
    install_parser = plugins_subparsers.add_parser(
        "install", help="Install a plugin", description="Register a new audit plugin"
    )
    install_parser.add_argument("plugin_path", help="Path to the plugin file")
    install_parser.add_argument(
        "--category",
        choices=["core", "custom", "community"],
        default="custom",
        help="Plugin category",
    )

    # Plugin enable command
    enable_parser = plugins_subparsers.add_parser(
        "enable", help="Enable a plugin", description="Enable a disabled plugin"
    )
    enable_parser.add_argument("framework", help="Framework name to enable")

    # Plugin disable command
    disable_parser = plugins_subparsers.add_parser(
        "disable", help="Disable a plugin", description="Disable an active plugin"
    )
    disable_parser.add_argument("framework", help="Framework name to disable")

    # Plugin validate command
    plugins_subparsers.add_parser(
        "validate", help="Validate plugins", description="Check all plugins for errors"
    )

    # Set default command to 'chat' if no subcommand is provided
    args = parser.parse_args()
    if args.command is None:
        args.command = "chat"
        # Set default chat arguments when no subcommand specified
        if not hasattr(args, "preload_data"):
            args.preload_data = False
        if not hasattr(args, "mode"):
            args.mode = None

    return args
