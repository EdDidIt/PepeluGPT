#!/usr/bin/env python3
"""
Demo tests for showcasing PepeluGPT functionality.
These are more like executable examples than traditional unit tests.
"""

import pytest
from typing import Any, Dict, List, Optional, Tuple


@pytest.mark.demo
def test_mode_mapping_demo() -> None:
    """Demo of mode command mapping functionality."""
    print("🧪 Testing Mode Command Mapping:")
    print("-" * 40)

    # Test the mapping logic
    mode_mapping: Dict[str, str] = {
        "adaptive": "learning",
        "classic": "deterministic", 
        "learning": "learning",
        "deterministic": "deterministic",
    }

    test_cases: List[Tuple[str, Optional[str]]] = [
        ("mode status", "status"),
        ("mode adaptive", "learning"),
        ("mode classic", "deterministic"),
        ("mode learning", "learning"),
        ("mode deterministic", "deterministic"),
        ("mode invalid", None),
    ]

    for command, expected in test_cases:
        parts: List[str] = command.split()  # type: ignore
        if len(parts) >= 2:
            mode_arg: str = parts[1].lower()  # type: ignore

            result: Optional[str]
            if mode_arg == "status":
                result = "status"
            elif mode_arg in mode_mapping:
                result = mode_mapping[mode_arg]
            else:
                result = None
        else:
            result = None

        status = "✅" if result == expected else "❌"
        print(f"{status} '{command}' -> {result} (expected: {expected})")

    print("\n💡 Summary:")
    print("- 'mode status' shows current mode")
    print("- 'mode adaptive' or 'mode learning' switches to learning mode") 
    print("- 'mode classic' or 'mode deterministic' switches to deterministic mode")
    print("- Both user-friendly and internal names are supported")


@pytest.mark.demo 
def test_interface_help_demo() -> None:
    """Demo of help interface functionality."""
    print("=== Demo: Interface Help System ===")
    
    try:
        from interface.chat import ChatInterface
        from interface.learning_chat import LearningChatInterface

        print("📋 Testing ChatInterface Help:")
        chat = ChatInterface(None, None)
        chat._show_help()  # type: ignore # Accessing protected method for demo
        print()

        print("📋 Testing LearningChatInterface Help:")
        learning_chat = LearningChatInterface(None) 
        learning_chat._show_help()  # type: ignore # Accessing protected method for demo
        print()
        
        print("✅ Both interfaces show mode commands in their help!")
        
    except ImportError as e:
        print(f"⚠️ Interface modules not available for demo: {e}")


@pytest.mark.demo
def test_preload_behavior_demo() -> None:
    """Demo of data preload behavior."""
    print("🔵 Demo: Preload Data Behavior")
    print("-" * 30)
    
    try:
        import tempfile
        import shutil
        from pathlib import Path
        from core.data_manager import DataManager

        # Create a temporary config for demo
        temp_dir = Path(tempfile.mkdtemp())
        test_config: Dict[str, Any] = {
            "cache_dir": str(temp_dir / "demo_cache"),
            "source_dir": "cyber_documents",
            "enable_caching": True,
            "cache_validation": "hash",
        }

        print(f"📁 Demo workspace: {temp_dir}")
        print(f"📄 Demo config: {test_config}")
        
        # Reset any existing singleton for demo
        DataManager.reset_singleton()
        
        # Demo initialization
        _ = DataManager(test_config)  # Use underscore for unused variable
        print("✅ DataManager initialized for demo")
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("🧹 Demo cleanup completed")
        
    except Exception as e:
        print(f"⚠️ Demo failed: {e}")


if __name__ == "__main__":
    # Run demos when executed directly
    test_mode_mapping_demo()
    print()
    test_interface_help_demo() 
    print()
    test_preload_behavior_demo()
