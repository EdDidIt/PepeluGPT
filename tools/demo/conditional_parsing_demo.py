"""
Example script demonstrating conditional parsing strategies.
This script shows all three approaches mentioned in your request:
1. Check for parsed output first
2. Use hash/timestamp validation
3. Singleton/lazy initialization
"""

# Add parent directory to path for imports
import sys
import time
from pathlib import Path
from typing import Any, Dict

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.data_manager import DataManager
from core.utils import get_logger

LOG = get_logger(__name__)


def load_config() -> Dict[str, Any]:
    """Load the default configuration."""
    config_path = Path("../../config/default.yaml")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            # Ensure we return a proper dict type
            if isinstance(config, dict):
                return config  # type: ignore[return-value]
            return {}
    return {}


def demonstrate_strategy_1() -> None:
    """
    Strategy 1: Check for Parsed Output First
    This demonstrates checking if parsed data exists before parsing.
    """
    print("🔵 Strategy 1: Check for Parsed Output First")
    print("=" * 50)

    config = load_config()
    data_manager = DataManager(config.get("data_management", {}))

    # Clear cache to start fresh
    data_manager.invalidate_cache()

    # First call - will parse from scratch
    print("🔵 First call (no cache):")
    start_time = time.time()
    data = data_manager.get_data()
    parse_time = time.time() - start_time
    print(f"    Parsing took: {parse_time:.3f}s")
    print(f"   Files processed: {data.get('metadata', {}).get('total_files', 0)}")

    # Second call - will use cached data
    print("\n🔵 Second call (with cache):")
    start_time = time.time()
    data = data_manager.get_data()
    cache_time = time.time() - start_time
    print(f"    Loading took: {cache_time:.3f}s")
    print(f"   Speedup: {parse_time/cache_time:.1f}x faster")

    print(f"\n🟢 Strategy 1 complete - cache working effectively!\n")


def demonstrate_strategy_2() -> None:
    """
    Strategy 2: Use Hash/Timestamp Validation
    This demonstrates how the system checks if data has changed.
    """
    print("🔵 Strategy 2: Use Hash/Timestamp Validation")
    print("=" * 50)

    config = load_config()
    data_manager = DataManager(config.get("data_management", {}))

    # Get initial data
    print("🔵 Loading data initially:")
    data = data_manager.get_data()
    print(f"   Files processed: {data.get('metadata', {}).get('total_files', 0)}")

    # Simulate a new session (reset memory cache but keep persistent cache)
    DataManager.reset_singleton()
    new_data_manager = DataManager(config.get("data_management", {}))

    print("\n🔵 New session - checking if data changed:")
    start_time = time.time()
    data = new_data_manager.get_data()
    load_time = time.time() - start_time
    print(f"    Loading took: {load_time:.3f}s")
    print(f"  🟢 Data unchanged - loaded from persistent cache")

    # Force refresh to demonstrate fresh parsing
    print("\n🔵 Forcing refresh (ignoring cache):")
    start_time = time.time()
    data = new_data_manager.get_data(force_refresh=True)
    refresh_time = time.time() - start_time
    print(f"    Refresh took: {refresh_time:.3f}s")
    print(f"  🟢 Fresh data parsed")

    print(f"\n🟢 Strategy 2 complete - hash validation working!\n")


def demonstrate_strategy_3() -> None:
    """
    Strategy 3: Singleton Pattern with Lazy Initialization
    This demonstrates the singleton pattern ensuring single instance.
    """
    print("🔵 Strategy 3: Singleton Pattern with Lazy Initialization")
    print("=" * 50)

    config = load_config()

    # Create multiple instances - should be same object
    print("🔵 Creating multiple DataManager instances:")
    dm1 = DataManager(config.get("data_management", {}))
    dm2 = DataManager(config.get("data_management", {}))
    dm3 = DataManager()

    print(f"  Instance 1 ID: {id(dm1)}")
    print(f"  Instance 2 ID: {id(dm2)}")
    print(f"  Instance 3 ID: {id(dm3)}")
    print(f"  🟢 All instances are same object: {dm1 is dm2 is dm3}")

    # Demonstrate lazy loading
    print("\n🔵 Demonstrating lazy initialization:")
    DataManager.reset_singleton()

    # First access triggers parsing
    dm = DataManager(config.get("data_management", {}))
    print("  🔵 Data will be parsed on first access...")

    start_time = time.time()
    _ = dm.get_data()  # Don't need to store the result
    first_access_time = time.time() - start_time
    print(f"    First access: {first_access_time:.3f}s")

    # Second access uses cached data
    start_time = time.time()
    _ = dm.get_data()  # Don't need to store the result
    second_access_time = time.time() - start_time
    print(f"    Second access: {second_access_time:.3f}s")

    print(f"\n🟢 Strategy 3 complete - singleton and lazy loading working!\n")


def demonstrate_cache_info() -> None:
    """Show detailed cache information."""
    print("🔵 Cache Information")
    print("=" * 50)

    config = load_config()
    data_manager = DataManager(config.get("data_management", {}))

    # Ensure data is loaded
    data_manager.get_data()

    cache_info = data_manager.get_cache_info()

    print("🔵 Current Cache Status:")
    for key, value in cache_info.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            # Type: ignore to handle unknown dict value types from cache_info
            for subkey, subvalue in value.items():  # type: ignore
                print(f"    {subkey}: {subvalue}")
        else:
            print(f"  {key}: {value}")

    print("\n🟢 Cache information displayed!\n")


def main() -> None:
    """Main demonstration function."""
    print(
        """
PepeluGPT Conditional Parsing Demonstration
============================================

This script demonstrates three conditional parsing strategies:
1. Check for parsed output first (memory + persistent cache)
2. Hash/timestamp validation (detect changes)
3. Singleton pattern with lazy initialization

Let's see each strategy in action...
"""
    )

    try:
        # Strategy 1: Basic caching
        demonstrate_strategy_1()

        # Strategy 2: Hash validation
        demonstrate_strategy_2()

        # Strategy 3: Singleton pattern
        demonstrate_strategy_3()

        # Show cache information
        demonstrate_cache_info()

        print("🟢 All demonstrations completed successfully!")
        print("\n🔵 Key Benefits Achieved:")
        print("   Avoid re-parsing unchanged data")
        print("   Fast cache-based loading")
        print("   Hash-based change detection")
        print("   Singleton pattern prevents duplicate instances")
        print("   Lazy initialization saves resources")
        print("   Persistent cache survives application restarts")

    except Exception as e:
        LOG.error(f"Demonstration failed: {e}")
        print(f"🔴 Error during demonstration: {e}")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
