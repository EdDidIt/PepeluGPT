"""
CLI commands for data management operations.
Demonstrates conditional parsing strategies and cache management.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.data_manager import DataManager
from core.utils import get_logger

LOG = get_logger(__name__)


def load_config(config_path: str = "../../config/default.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        # Handle both relative and absolute paths
        if not Path(config_path).is_absolute():
            # If running from admin directory, adjust path
            config_path = str(Path(__file__).parent / config_path)

        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        LOG.error(f"🔴 Error loading config: {e}")
        return {}


def cmd_status(args: argparse.Namespace) -> None:
    """Show data manager status and cache information."""
    config = load_config(args.config)
    data_manager = DataManager(config.get("data_management", {}))

    print("🔵 Data Manager Status")
    print("=" * 50)

    cache_info = data_manager.get_cache_info()
    for key, value in cache_info.items():
        if isinstance(value, dict):
            print(f"{key}:")
            # Type: ignore to handle unknown dict value types from cache_info
            for subkey, subvalue in value.items():  # type: ignore
                print(f"  {subkey}: {subvalue}")
        else:
            print(f"{key}: {value}")


def cmd_parse(args: argparse.Namespace) -> None:
    """Parse data with conditional strategy."""
    config = load_config(args.config)
    data_manager = DataManager(config.get("data_management", {}))

    print("🟡 Starting conditional parsing...")

    # Parse data (will use cache if available)
    data = data_manager.get_data(force_refresh=args.force)

    print(f"🟢 Parsing complete!")
    print(f"🔵 Total files processed: {data.get('metadata', {}).get('total_files', 0)}")
    print(f"🔵 Parsed at: {data.get('metadata', {}).get('parsed_at', 'Unknown')}")

    if args.verbose:
        print("\n🔵 File Details:")
        for filename, file_data in data.get("files", {}).items():
            status = "🟢" if file_data.get("content") else "🔴"
            size = file_data.get("size", 0)
            print(f"  {status} {filename} ({size} bytes)")


def cmd_clear(args: argparse.Namespace) -> None:
    """Clear all cached data."""
    config = load_config(args.config)
    data_manager = DataManager(config.get("data_management", {}))

    print("🔵 Clearing cache...")
    data_manager.invalidate_cache()
    print("🟢 Cache cleared successfully!")


def cmd_benchmark(args: argparse.Namespace) -> None:
    """Benchmark parsing performance with and without cache."""
    import time

    config = load_config(args.config)
    data_manager = DataManager(config.get("data_management", {}))

    print("🔵 Running benchmark...")

    # First run - no cache
    data_manager.invalidate_cache()
    start_time = time.time()
    _ = data_manager.get_data()
    first_run_time = time.time() - start_time

    # Second run - with cache
    start_time = time.time()
    _ = data_manager.get_data()
    second_run_time = time.time() - start_time

    # Third run - force refresh
    start_time = time.time()
    _ = data_manager.get_data(force_refresh=True)
    refresh_time = time.time() - start_time

    print("\n🔵 Benchmark Results:")
    print(f"  First run (no cache):  {first_run_time:.3f}s")
    print(f"  Second run (cached):   {second_run_time:.3f}s")
    print(f"  Forced refresh:        {refresh_time:.3f}s")
    print(f"  Cache speedup:         {first_run_time/second_run_time:.1f}x")


def cmd_export(args: argparse.Namespace) -> None:
    """Export parsed data to JSON file."""
    config = load_config(args.config)
    data_manager = DataManager(config.get("data_management", {}))

    print("🔵 Exporting parsed data...")
    data = data_manager.get_data()

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"🟢 Data exported to: {output_path}")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="PepeluGPT Data Management CLI")
    parser.add_argument(
        "--config",
        "-c",
        default="../../config/default.yaml",
        help="Configuration file path",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show cache status")

    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Parse data with caching")
    parse_parser.add_argument(
        "--force", "-f", action="store_true", help="Force refresh (ignore cache)"
    )
    parse_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed file information"
    )

    # Clear command
    subparsers.add_parser("clear", help="Clear cache")

    # Benchmark command
    subparsers.add_parser(
        "benchmark", help="Run performance benchmark"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export parsed data")
    export_parser.add_argument(
        "--output", "-o", default="parsed_data.json", help="Output file path"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Setup logging
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Execute command
    try:
        if args.command == "status":
            cmd_status(args)
        elif args.command == "parse":
            cmd_parse(args)
        elif args.command == "clear":
            cmd_clear(args)
        elif args.command == "benchmark":
            cmd_benchmark(args)
        elif args.command == "export":
            cmd_export(args)
    except Exception as e:
        print(f"🔴 Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
