"""
Interactive chat interface with session management.
Enhanced with runtime mode switching capabilities.
"""

import sys
from typing import Any, Dict, Optional

from core.utils import get_logger

LOG = get_logger(__name__)


class ChatInterface:
    def __init__(
        self, orchestrator_or_engine: Any, config: Optional[Dict[str, Any]] = None
    ):
        """
        orchestrator_or_engine: Instance of Orchestrator or Engine for backward compatibility
        config: Configuration dict loaded by Orchestrator (optional for new learning interface)
        """
        # Handle both old (engine, config) and new (orchestrator) calling patterns
        if config is not None:
            # Old pattern: ChatInterface(engine, config)
            self.engine = orchestrator_or_engine
            self.config = config
            self.orchestrator = None
        else:
            # New pattern: ChatInterface(orchestrator)
            self.orchestrator = orchestrator_or_engine
            self.engine = orchestrator_or_engine.engine
            self.config = orchestrator_or_engine.config

        # Check if we have learning capabilities
        if (
            self.orchestrator
            and hasattr(self.orchestrator, "learning_engine")
            and self.orchestrator.learning_engine
        ):
            # Import and use learning interface
            try:
                from interface.learning_chat import LearningChatInterface

                self.learning_interface = LearningChatInterface(
                    self.orchestrator.learning_engine
                )
            except ImportError:
                LOG.warning("Learning interface not available, using basic chat")
                self.learning_interface = None
        else:
            self.learning_interface = None

    def _get_mode_indicator(self) -> str:
        """Get visual indicator for current mode."""
        try:
            from tools.mode_switcher import ModeManager

            manager = ModeManager()
            current_mode = manager.get_current_mode()

            if current_mode == "learning":
                return "🧠 [Learning Mode]"
            else:
                return "⚡ [Deterministic Mode]"
        except Exception:
            return ""

    def _handle_mode_command(self, command: str) -> bool:
        """
        Handle runtime mode switching commands.

        Args:
            command: The mode command (e.g., 'mode deterministic', 'mode learning')

        Returns:
            True if command was handled, False otherwise
        """
        if not command.startswith("mode "):
            return False

        try:
            parts = command.split()
            if len(parts) < 2:
                print("Usage: mode [learning|deterministic|adaptive|classic|status]")
                return True

            mode_arg = parts[1].lower()

            # Map user-friendly names to internal names
            mode_mapping = {
                "adaptive": "learning",
                "classic": "deterministic",
                "learning": "learning",
                "deterministic": "deterministic",
            }

            if mode_arg == "status":
                self._show_mode_status()
            elif mode_arg in mode_mapping:
                internal_mode = mode_mapping[mode_arg]
                self._switch_mode_runtime(internal_mode)
            else:
                print(
                    "Invalid mode. Use 'learning/adaptive', 'deterministic/classic', or 'status'"
                )

            return True

        except Exception as e:
            LOG.error(f"Error handling mode command: {e}")
            print(f"Error processing mode command: {e}")
            return True

    def _show_mode_status(self):
        """Show current mode status."""
        try:
            # Import here to avoid circular imports
            from tools.mode_switcher import ModeManager

            manager = ModeManager()
            current_mode = manager.get_current_mode()

            learning_active = self.learning_interface is not None
            engine_type = "Standard Engine"
            if (
                self.orchestrator
                and hasattr(self.orchestrator, "learning_engine")
                and self.orchestrator.learning_engine
            ):
                engine_type = "Learning Engine"

            print(f"\n📊 Current Mode Status:")
            print(f"  Configuration Mode: {current_mode.upper()}")
            print(f"  Active Engine: {engine_type}")
            print(
                f"  Learning Interface: {'✓ Active' if learning_active else '✗ Inactive'}"
            )
            print(f"  Runtime Commands: Available")
            print("\n💡 Commands:")
            print("  • mode learning      - Switch to adaptive mode")
            print("  • mode deterministic - Switch to rule-based mode")
            print("  • mode status        - Show this status")
            print("  • help               - Show all commands")

        except Exception as e:
            LOG.error(f"Error showing mode status: {e}")
            print(f"Could not determine mode status: {e}")

    def _switch_mode_runtime(self, target_mode: str):
        """
        Switch mode at runtime.

        Args:
            target_mode: 'learning' or 'deterministic'
        """
        try:
            # Import here to avoid circular imports
            from tools.mode_switcher import ModeManager

            manager = ModeManager()
            current_mode = manager.get_current_mode()

            if current_mode == target_mode:
                print(f"Already in {target_mode} mode!")
                return

            print(f"🔄 Switching from {current_mode} to {target_mode} mode...")

            if manager.set_mode(target_mode):
                print(f"✅ Configuration updated to {target_mode} mode")
                print("⚠️  Note: Full mode switch requires restart for all features")
                print("💡 For immediate effect in current session:")

                if target_mode == "learning":
                    if not self.learning_interface:
                        print("  - Learning interface will be available after restart")
                        print("  - Current session continues with standard interface")
                    else:
                        print("  - Learning interface already active")
                else:  # deterministic
                    if self.learning_interface:
                        print("  - Learning interface disabled for new queries")
                        self.learning_interface = None
                    print("  - Using rule-based processing")

            else:
                print(f"❌ Failed to switch to {target_mode} mode")

        except Exception as e:
            LOG.error(f"Error switching mode: {e}")
            print(f"Error switching mode: {e}")

    def _show_help(self):
        """Show available commands."""
        print("\n🆘 Available Commands:")
        print("  • help                       - Show this help")
        print("  • mode learning/adaptive     - Switch to adaptive/learning mode")
        print("  • mode deterministic/classic - Switch to rule-based mode")
        print("  • mode status               - Show current mode status")
        print("  • exit/quit                 - Exit PepeluGPT")

        if self.learning_interface:
            print("\n🧠 Learning Mode Commands:")
            print("  • rate 1-5           - Rate the last response")
            print("  • correct: [text]    - Provide correction for last response")
            print("  • session            - Show session history")

        print("\n💡 Pro Tips:")
        print("  • Mode changes persist across sessions")
        print("  • Restart for full feature activation")
        print("  • Learning mode improves with your feedback")
        print("")

    def start(self):
        """
        Begin REPL loop: read user input, get engine response, print to console.
        Uses learning interface if available for enhanced feedback collection.
        Enhanced with runtime mode switching support.
        """
        if self.learning_interface:
            # Use enhanced learning interface
            self.learning_interface.start()
        else:
            # Use basic interface with mode switching support
            mode_indicator = self._get_mode_indicator()
            print(f"🟢 Tomato is ready. Type 'help' for commands or 'exit' to quit.")
            print("⚪️ How may I help you today?")

            while True:
                try:
                    user_input = input("\n[You] ").strip()

                    if not user_input:
                        continue

                    # Handle special commands
                    if user_input.lower() in ("exit", "quit", "q"):
                        break
                    elif user_input.lower() == "help":
                        self._show_help()
                        continue
                    elif self._handle_mode_command(user_input):
                        continue

                    # Check for mode suggestions before processing
                    try:
                        from tools.mode_suggester import suggest_mode_for_query
                        from tools.mode_switcher import ModeManager

                        manager = ModeManager()
                        current_mode = manager.get_current_mode()
                        suggestion = suggest_mode_for_query(user_input, current_mode)

                        # Show suggestion if warranted
                        if suggestion["should_suggest"]:
                            try:
                                suggester = suggest_mode_for_query.__globals__[
                                    "ModeSuggester"
                                ]()
                                prompt = suggester.get_suggestion_prompt(suggestion)
                                if prompt:
                                    print(prompt)
                            except:
                                # Fallback suggestion display
                                suggested = suggestion["suggested_mode"]
                                emoji = "🧠" if suggested == "learning" else "⚡"
                                print(
                                    f"💡 Consider switching to {emoji} {suggested.upper()} mode for this query. Use 'mode {suggested}' to switch.\n"
                                )
                    except Exception as e:
                        LOG.debug(f"Mode suggestion failed: {e}")
                        # Continue without suggestions if module unavailable

                    # Process regular query
                    mode_indicator = "🧠" if self.learning_interface else "⚡"
                    answer = self.engine.process_query(user_input)
                    print(f"[Pepelu {mode_indicator}] {answer}")

                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    LOG.error(f"🔴 Chat error: {e}")
                    print(f"🔴 Error: {e}")
                    print("💡 Try 'help' for available commands")

        sys.exit(0)
