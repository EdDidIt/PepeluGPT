#!/usr/bin/env python3
"""
Basic test cases for the refactored CLI components.
This demonstrates how the modular structure enables better testing.
"""

import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from cli.args import parse_args
from cli.utils import get_mode_display_name, interactive_mode_selection


class TestCLIArgs(unittest.TestCase):
    """Test argument parsing functionality."""

    def test_default_args(self):
        """Test default argument values."""
        with patch("sys.argv", ["main.py"]):
            args = parse_args()
            self.assertEqual(args.config, "config/default.yaml")
            self.assertFalse(args.debug)
            self.assertFalse(args.preload_data)
            self.assertIsNone(args.mode)

    def test_mode_override(self):
        """Test mode override functionality."""
        with patch("sys.argv", ["main.py", "chat", "--mode", "adaptive"]):
            args = parse_args()
            self.assertEqual(args.mode, "adaptive")

    def test_preload_data_flag(self):
        """Test preload data flag functionality."""
        # Test default (no flag)
        with patch("sys.argv", ["main.py", "chat"]):
            args = parse_args()
            self.assertFalse(args.preload_data)

        # Test with --preload-data flag
        with patch("sys.argv", ["main.py", "chat", "--preload-data"]):
            args = parse_args()
            self.assertTrue(args.preload_data)

    def test_debug_flag(self):
        """Test debug flag parsing."""
        with patch("sys.argv", ["main.py", "--debug"]):
            args = parse_args()
            self.assertTrue(args.debug)


class TestCLIUtils(unittest.TestCase):
    """Test CLI utility functions."""

    def test_mode_display_names(self):
        """Test mode display name generation."""
        self.assertEqual(get_mode_display_name("adaptive"), "🧠 Adaptive")
        self.assertEqual(get_mode_display_name("classic"), "🛡️ Classic")
        self.assertEqual(get_mode_display_name("learning"), "🧠 Adaptive")  # legacy
        self.assertEqual(get_mode_display_name("deterministic"), "🛡️ Classic")  # legacy
        self.assertEqual(get_mode_display_name("other"), "� Other")

    @patch("builtins.input", side_effect=["adaptive"])
    def test_interactive_mode_selection_adaptive(self, mock_input: MagicMock) -> None:
        """Test interactive mode selection for adaptive mode."""
        with patch("sys.stdout", new_callable=StringIO):
            result = interactive_mode_selection()
            self.assertEqual(result, "adaptive")

    @patch("builtins.input", side_effect=["classic"])
    def test_interactive_mode_selection_classic(self, mock_input: MagicMock) -> None:
        """Test interactive mode selection for classic mode."""
        with patch("sys.stdout", new_callable=StringIO):
            result = interactive_mode_selection()
            self.assertEqual(result, "classic")

    @patch("builtins.input", side_effect=["a"])
    def test_interactive_mode_selection_shorthand(self, mock_input: MagicMock) -> None:
        """Test interactive mode selection with shorthand input."""
        with patch("sys.stdout", new_callable=StringIO):
            result = interactive_mode_selection()
            self.assertEqual(result, "adaptive")


class TestCLIRunner(unittest.TestCase):
    """Test CLI runner functionality (mock-based tests)."""

    @patch("cli.runner.setup_enhanced_logging")
    @patch("cli.runner.Orchestrator")
    @patch("cli.runner.load_config")
    def test_run_cli_with_mode_override(
        self, mock_load_config: MagicMock, mock_orchestrator: MagicMock, mock_logging: MagicMock
    ) -> None:
        """Test CLI run with mode override."""
        from argparse import Namespace

        from cli.runner import run_cli

        # Mock configuration
        mock_load_config.return_value = {"test": "config"}
        mock_orch_instance = MagicMock()
        mock_orchestrator.return_value = mock_orch_instance

        # Create mock args
        args = Namespace(mode="adaptive", debug=False, config="config/test.yaml")

        # Mock mode manager to avoid actual mode switching
        with patch("cli.runner.ModeManager") as mock_mode_manager:
            mock_manager = MagicMock()
            mock_mode_manager.return_value = mock_manager
            mock_manager.get_current_mode.return_value = "adaptive"
            mock_manager.mode_configs = {"adaptive": "config/adaptive.yaml"}

            # Capture output
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_cli(args)

            # Verify orchestrator was called
            mock_orchestrator.assert_called_once()
            mock_orch_instance.run.assert_called_once()

            # Verify output contains expected messages
            output = mock_stdout.getvalue()
            self.assertIn("🧠 Adaptive mode enabled", output)


if __name__ == "__main__":
    unittest.main()
