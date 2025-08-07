#!/usr/bin/env python3
"""
UI utilities for PepeluGPT CLI.
"""

BANNER = r"""
 ____   _____   ____   _____   _       _   _
|  _ \ | ____| |  _ \ | ____| | |     | | | |
| |_) ||  _|   | |_) ||  _|   | |     | | | |
|  __/ | |___  |  __/ | |___  | |___  | |_| |
|_|    |_____| |_|    |_____| |_____| |_____|
 
            YOUR CYBER SIDEKICK 

"""


def display_banner():
    """Display the PepeluGPT banner."""
    print("\033[1m" + BANNER + "\033[0m")


def interactive_mode_selection() -> str:
    """Interactive mode selection for user."""
    print("🔵 Choose your mode:")
    print("   🧠 Adaptive Mode (exploratory, feedback-driven)")
    print("   🛡️ Classic Mode (stable, production-ready)")
    print()

    while True:
        choice = input("Enter 'adaptive' or 'classic': ").strip().lower()
        if choice in ["adaptive", "classic"]:
            return choice
        elif choice in ["a", "adapt"]:
            return "adaptive"
        elif choice in ["c", "class"]:
            return "classic"
        else:
            print("🟡 Please enter 'adaptive' or 'classic'")


def get_mode_display_name(internal_mode: str) -> str:
    """Get display name for mode with emoji."""
    # Handle current modes
    if internal_mode == "adaptive":
        return "🧠 Adaptive"
    elif internal_mode == "classic":
        return "🛡️ Classic"
    # Handle legacy modes (for backward compatibility)
    elif internal_mode == "learning":
        return "🧠 Adaptive"
    elif internal_mode == "deterministic":
        return "🛡️ Classic"
    else:
        return f"🟡 {internal_mode.title()}"
