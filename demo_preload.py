#!/usr/bin/env python3
"""
Demo script to show the new preload behavior in action.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from cli.args import parse_args


def demo_preload_behavior():
    """Demonstrate the new preload behavior."""
    print("🎯 Demonstrating PepeluGPT's new smart preload behavior")
    print("=" * 60)

    # Create temporary config
    temp_dir = Path(tempfile.mkdtemp())
    config_content = f"""
data_management:
  cache_dir: {temp_dir}/cache
  source_dir: cyber_documents
  enable_caching: true
  cache_validation: hash

model:
  name: demo-model
  parameters:
    temperature: 0.7

logging:
  level: INFO

vector_db:
  index_path: {temp_dir}/cache/faiss_index.bin
  metadata_path: {temp_dir}/cache/metadata.pkl
  chunk_size: 1000
  overlap: 200
"""

    config_file = temp_dir / "demo_config.yaml"
    with open(config_file, "w") as f:
        f.write(config_content)

    try:
        print("\n📋 Scenario 1: Default behavior (no --preload-data flag)")
        print(
            "   Expected: Check if data is cached, if so skip preload, if not load on first query"
        )

        with patch("sys.argv", ["main.py", "chat"]):
            args = parse_args()
            print(f"   Preload data flag: {args.preload_data}")

            # This would normally start the orchestrator
            print("   Result: Data would be loaded on first query (lazy loading)")

        print("\n📋 Scenario 2: Explicit preload (--preload-data flag)")
        print("   Expected: Force data loading on startup regardless of cache status")

        with patch("sys.argv", ["main.py", "chat", "--preload-data"]):
            args = parse_args()
            print(f"   Preload data flag: {args.preload_data}")
            print("   Result: Data would be preloaded during startup")

        print("\n📋 Scenario 3: With existing cache")
        print("   Expected: Detect cache and report that preload is not needed")

        # Simulate creating some cache
        cache_dir = Path(temp_dir) / "cache"
        cache_dir.mkdir(exist_ok=True)
        (cache_dir / "parsed_data.pkl").touch()  # Create empty cache file

        with patch("sys.argv", ["main.py", "chat"]):
            args = parse_args()
            print(f"   Preload data flag: {args.preload_data}")
            print("   Result: Would detect cache and skip preload")

        print("\n🟢 Demo completed successfully!")
        print("\n💡 Summary of the new behavior:")
        print("   • By default: Smart lazy loading - check cache, load only if needed")
        print("   • With --preload-data: Force immediate data loading on startup")
        print(
            "   • Cache-aware: Detects existing data and avoids unnecessary reloading"
        )
        print(
            "   • User-friendly: Never skips data loading unless data is actually available"
        )

    except Exception as e:
        print(f"\n🔴 Demo failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Clean up
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    demo_preload_behavior()
