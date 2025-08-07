"""
Chat Interface with Learning Feedback
Enhanced chat interface that collects user feedback for the learning system.
"""

from typing import Any, Dict, List

from core.utils import get_logger

LOG = get_logger(__name__)


class LearningChatInterface:
    """Enhanced chat interface with feedback collection."""

    def __init__(self, learning_engine: Any) -> None:
        self.learning_engine = learning_engine
        self.last_query: str | None = None
        self.last_response: str | None = None
        self.last_context: Any | None = None

    def start(self) -> None:
        """Start the interactive chat session with learning feedback."""
        # Get mode indicator for display
        _mode_indicator = "🧠 [Learning Mode]"
        try:
            from tools.mode_switcher import ModeManager

            manager = ModeManager()
            current_mode = manager.get_current_mode()
            if current_mode == "learning":
                _mode_indicator = "🧠 [Learning Mode]"
            else:
                _mode_indicator = "⚡ [Deterministic Mode]"
        except Exception:
            pass

        print(f"🟢 Tomato is ready. Type 'help' for commands or 'exit' to quit.")
        print(
            "After each response, you can rate it with 'rate 1-5' or provide feedback with 'correct: better answer'"
        )
        print("-" * 50)

        try:
            while True:
                query = input("\n[You] ").strip()

                if not query:
                    continue

                if query.lower() in ["quit", "exit", "q"]:
                    break
                elif query.lower() == "help":
                    self._show_help()
                    continue
                elif query.startswith("rate "):
                    self._handle_rating(query)
                    continue
                elif query.startswith("correct:"):
                    self._handle_correction(query)
                    continue
                elif query.lower() == "session":
                    self._show_session_history()
                    continue
                elif self._handle_mode_command(query):
                    continue

                # Process the query
                try:
                    response: str
                    context: Any
                    response, context = self.learning_engine.process_query(query)

                    # Store for feedback
                    self.last_query = query
                    self.last_response = response
                    self.last_context = context

                    # Display response
                    print(f"\n[Pepelu] {response}")

                    # Show confidence and source info
                    if context:
                        confidence: float = getattr(context, 'confidence', 0.0)
                        sources: List[str] = getattr(context, 'sources', [])
                        print(
                            f"\n[Confidence: {confidence:.2f} | Source: {', '.join(sources)}]"
                        )
                        print(
                            "Rate this response: 'rate 1-5' or provide correction: 'correct: your better answer'"
                        )

                except Exception as e:
                    LOG.error(f"Error processing query: {e}")
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            pass

        print("\n👋 Goodbye!")

    def _show_help(self):
        """Display help information."""
        help_text = """
Available commands:
- help: Show this help message
- quit/exit/q: Exit the chat
- mode learning/adaptive: Switch to adaptive/learning mode
- mode deterministic/classic: Switch to rule-based mode
- mode status: Show current mode status
- rate 1-5: Rate the last response (1=poor, 5=excellent)
- correct: [your better answer]: Provide a correction for the last response
- session: Show conversation history for this session

Learning Features:
- Your ratings help improve future responses
- Corrections are used to enhance the knowledge base
- High-rated responses become training examples
        """
        print(help_text)

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

            print(f"\n📊 Current Mode Status:")
            print(f"  Configuration Mode: {current_mode.upper()}")
            print(f"  Active Engine: Learning Engine")
            print(f"  Learning Interface: ✓ Active")
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
                    print("  - Learning interface already active")
                    print(
                        "  - Continue providing feedback with ratings and corrections"
                    )
                else:  # deterministic
                    print("  - Learning interface will continue in current session")
                    print("  - Restart to switch to rule-based interface")

            else:
                print(f"❌ Failed to switch to {target_mode} mode")

        except Exception as e:
            LOG.error(f"Error switching mode: {e}")
            print(f"Error switching mode: {e}")

    def _handle_rating(self, command: str):
        """Handle user rating input."""
        if not self.last_response:
            print("No response to rate. Ask a question first.")
            return

        try:
            rating_part = command.split("rate ")[1].strip()
            rating = int(rating_part)

            if rating < 1 or rating > 5:
                print("Rating must be between 1 and 5.")
                return

            # Collect feedback
            self.learning_engine.collect_feedback(
                query=self.last_query, response=self.last_response, rating=rating
            )

            # Provide feedback
            rating_emoji = {1: "😞", 2: "😐", 3: "🙂", 4: "😊", 5: "🤩"}
            print(f"Thanks! Rated {rating}/5 {rating_emoji.get(rating, '')}")

            if rating <= 2:
                print(
                    "Sorry it wasn't helpful. Consider providing a correction with 'correct: better answer'"
                )
            elif rating >= 4:
                print("Great! This response will help improve future answers.")

        except (ValueError, IndexError):
            print("Invalid rating format. Use 'rate 1-5'")

    def _handle_correction(self, command: str):
        """Handle user correction input."""
        if not self.last_response:
            print("No response to correct. Ask a question first.")
            return

        try:
            correction = command.split("correct:", 1)[1].strip()

            if not correction:
                print("Please provide your correction after 'correct:'")
                return

            # Collect feedback with correction
            self.learning_engine.collect_feedback(
                query=self.last_query,
                response=self.last_response,
                rating=1,  # Implicit low rating for corrected responses
                correction=correction,
            )

            print("✅ Thanks! Your correction will help improve future responses.")

        except IndexError:
            print("Invalid correction format. Use 'correct: your better answer'")

    def _show_session_history(self) -> None:
        """Display current session conversation history."""
        history: List[Dict[str, Any]] = self.learning_engine.get_session_context()

        if not history:
            print("No conversation history in this session.")
            return

        print("\n=== Session History ===")
        for i, entry in enumerate(history, 1):
            response_text: str = entry['response']
            print(f"\n{i}. Q: {entry['query']}")
            print(
                f"   A: {response_text[:100]}{'...' if len(response_text) > 100 else ''}"
            )
            print(f"   Time: {entry['timestamp']}")
        print("=" * 23)


# Legacy interface for backward compatibility
class ChatInterface:
    """Legacy chat interface - redirects to learning interface."""

    def __init__(self, orchestrator: Any) -> None:
        self.orchestrator = orchestrator

        # Check if orchestrator has learning engine
        if hasattr(orchestrator, "learning_engine"):
            self.learning_interface = LearningChatInterface(
                orchestrator.learning_engine
            )
        else:
            self.learning_interface = None
            LOG.warning(
                "Orchestrator doesn't have learning engine, using basic interface"
            )

    def start(self):
        """Start the chat interface."""
        if self.learning_interface:
            self.learning_interface.start()
        else:
            self._basic_start()

    def _basic_start(self) -> None:
        """Fallback basic chat interface."""
        print("🟢 Tomato is ready")
        print("Type 'quit' to exit")
        print("-" * 30)

        try:
            while True:
                query = input("\n> ").strip()

                if not query:
                    continue

                if query.lower() in ["quit", "exit", "q"]:
                    break

                try:
                    response: str = self.orchestrator.engine.process_query(query)
                    print(f"\n{response}")
                except Exception as e:
                    LOG.error(f"Error processing query: {e}")
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            pass

        print("\n👋 Goodbye!")
