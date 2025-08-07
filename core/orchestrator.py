"""
Orchestrator ties together config loading, the engine, and the chat interface.
Enhanced with learning capabilities for adaptive improvement.
"""

import yaml
from typing import Any

from core.data_manager import DataManager
from core.engine import Engine
from core.logging_config import log_error, log_system_event
from core.utils import get_logger
from interface.chat import ChatInterface

# Learning engine import with fallback
try:
    from core.learning_engine import LearningEngine

    learning_available = True
except ImportError:
    learning_available = False
    LearningEngine = None  # type: ignore

LOG = get_logger(__name__)


class Orchestrator:
    def __init__(self, config_path: str, args: Any = None):
        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)

            # Initialize data manager with conditional parsing
            self.data_manager = DataManager(self.config.get("data_management", {}))

            # Handle data preloading based on args
            if args and hasattr(args, "preload_data") and args.preload_data:
                # Force preload data on startup
                LOG.info("🔵 Preloading data on startup as requested...")
                self.data_manager.get_data()
                LOG.info("🟢 Data preloaded successfully")
            elif self.data_manager.is_data_available():
                LOG.info("🔵 Data cache available - no need to preload")
            else:
                LOG.info("🔵 Data will be loaded on first query")

            # Check if learning mode is enabled
            learning_enabled = self.config.get("learning", {}).get("enabled", False)

            if learning_enabled and learning_available:
                # Initialize learning engine
                self.learning_engine = LearningEngine(self.config, self.data_manager)  # type: ignore
                self.engine = self.learning_engine  # Use learning engine as primary
                LOG.info("Learning engine initialized - adaptive mode enabled")
            else:
                # Initialize standard engine
                self.engine = Engine(self.config, self.data_manager)
                self.learning_engine = None
                if learning_enabled:
                    LOG.warning(
                        "Learning requested but dependencies not available - using standard engine"
                    )

            # Initialize UI with learning support
            self.ui = ChatInterface(self)

            LOG.info("Orchestrator initialized successfully")
            log_system_event(
                "orchestrator_initialized",
                {
                    "config_path": config_path,
                    "data_management": self.config.get("data_management", {}),
                    "model": self.config.get("model", {}),
                },
            )
        except Exception as e:
            LOG.error(f"Failed to initialize Orchestrator: {e}")
            log_error(e, "orchestrator_init", "ORCH_001")
            raise

    def run(self):
        try:
            LOG.info("Starting orchestrator run phase")
            log_system_event("orchestrator_run_started")

            # Start the UI (data will be loaded on first query)
            LOG.info("Starting UI interface")
            log_system_event("ui_start")
            self.ui.start()

        except Exception as e:
            LOG.error(f"Error during orchestrator run: {e}")
            log_error(e, "orchestrator_run", "ORCH_002")
            raise
