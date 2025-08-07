#!/usr/bin/env python3
"""
Enhanced logging configuration for PepeluGPT.
Provides comprehensive logging with file rotation, structured output, and audit trails.
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class SecurityAuditFormatter(logging.Formatter):
    """Custom formatter for security audit logs with structured data."""

    def format(self, record: logging.LogRecord) -> str:
        # Base formatting
        timestamp = datetime.fromtimestamp(record.created).isoformat()

        # Create structured log entry
        log_entry: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "user_query"):
            log_entry["user_query"] = getattr(record, "user_query")
        if hasattr(record, "response_time"):
            log_entry["response_time_ms"] = getattr(record, "response_time")
        if hasattr(record, "error_code"):
            log_entry["error_code"] = getattr(record, "error_code")
        if hasattr(record, "session_id"):
            log_entry["session_id"] = getattr(record, "session_id")

        return json.dumps(log_entry, ensure_ascii=False)


class ColoredConsoleFormatter(logging.Formatter):
    """Console formatter with colors and emojis for better readability."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }

    EMOJIS = {
        "DEBUG": "🔍",
        "INFO": "🔵",
        "WARNING": "🟡",
        "ERROR": "🔴",
        "CRITICAL": "💥",
    }

    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        # Add color and emoji
        level_color = self.COLORS.get(record.levelname, "")
        emoji = self.EMOJIS.get(record.levelname, "")

        # Format message
        message = super().format(record)

        return f"{level_color}{emoji} {message}{self.RESET}"


class PepeluGPTLogger:
    """Enhanced logging manager for PepeluGPT."""

    def __init__(self, config: Dict[str, Any], debug: bool = False):
        self.config = config
        self.debug = debug
        self.logs_dir = "logs"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)

        # Setup logging
        self._setup_loggers()

    def _setup_loggers(self):
        """Configure all loggers with appropriate handlers."""

        # Clear any existing handlers
        logging.getLogger().handlers.clear()

        # Determine log level
        if self.debug:
            log_level = logging.DEBUG
            console_level = logging.DEBUG
        else:
            config_level = self.config.get("logging", {}).get("level", "INFO")
            log_level = getattr(logging, config_level.upper(), logging.INFO)
            console_level = logging.INFO

        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # 1. Console Handler - For real-time feedback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_formatter = ColoredConsoleFormatter("%(name)s: %(message)s")
        console_handler.setFormatter(console_formatter)

        # 2. Main Application Log - Rotating file with all activity
        main_log_path = os.path.join(self.logs_dir, "pepeluGPT.log")
        main_handler = logging.handlers.RotatingFileHandler(
            main_log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        main_handler.setLevel(logging.DEBUG)
        main_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s:%(lineno)-4d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        main_handler.setFormatter(main_formatter)

        # 3. Session Log - Current session only
        session_log_path = os.path.join(self.logs_dir, f"session_{self.session_id}.log")
        session_handler = logging.FileHandler(session_log_path, encoding="utf-8")
        session_handler.setLevel(logging.INFO)
        session_handler.setFormatter(main_formatter)

        # 4. Error Log - Errors and critical issues only
        error_log_path = os.path.join(self.logs_dir, "errors.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_path,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(main_formatter)

        # 5. Security Audit Log - Structured logging for security events
        audit_log_path = os.path.join(self.logs_dir, "security_audit.log")
        audit_handler = logging.handlers.RotatingFileHandler(
            audit_log_path,
            maxBytes=20 * 1024 * 1024,  # 20MB
            backupCount=10,
            encoding="utf-8",
        )
        audit_handler.setLevel(logging.INFO)
        audit_formatter = SecurityAuditFormatter()
        audit_handler.setFormatter(audit_formatter)

        # Add handlers to root logger
        root_logger.addHandler(console_handler)
        root_logger.addHandler(main_handler)
        root_logger.addHandler(session_handler)
        root_logger.addHandler(error_handler)

        # Create separate audit logger
        audit_logger = logging.getLogger("pepeluGPT.audit")
        audit_logger.addHandler(audit_handler)
        audit_logger.setLevel(logging.INFO)
        audit_logger.propagate = False  # Don't propagate to root logger

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger for a specific module."""
        return logging.getLogger(name)

    def get_audit_logger(self) -> logging.Logger:
        """Get the security audit logger."""
        return logging.getLogger("pepeluGPT.audit")

    def log_user_query(self, query: str, response_time: Optional[float] = None):
        """Log user queries for audit purposes."""
        audit_logger = self.get_audit_logger()
        extra: Dict[str, Any] = {"user_query": query, "session_id": self.session_id}
        if response_time:
            extra["response_time"] = response_time

        audit_logger.info("User query processed", extra=extra)

    def log_system_event(self, event: str, details: Optional[Dict[str, Any]] = None):
        """Log important system events."""
        audit_logger = self.get_audit_logger()
        extra: Dict[str, Any] = {"system_event": event, "session_id": self.session_id}
        if details:
            extra.update(details)

        audit_logger.info(f"System event: {event}", extra=extra)

    def log_error(
        self,
        error: Exception,
        context: Optional[str] = None,
        error_code: Optional[str] = None,
    ):
        """Log errors with context."""
        error_logger = logging.getLogger("pepeluGPT.error")
        extra = {
            "session_id": self.session_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        if context:
            extra["context"] = context
        if error_code:
            extra["error_code"] = error_code

        error_logger.error(f"Error occurred: {error}", extra=extra, exc_info=True)

        # Also log to audit
        audit_logger = self.get_audit_logger()
        audit_logger.error(
            f"Error in {context or 'unknown context'}: {error}", extra=extra
        )

    def log_startup_phase(
        self,
        phase: str,
        status: str = "started",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Log startup phases for debugging initialization issues."""
        startup_logger = logging.getLogger("pepeluGPT.startup")
        extra: Dict[str, Any] = {
            "startup_phase": phase,
            "status": status,
            "session_id": self.session_id,
        }
        if details:
            extra.update(details)

        startup_logger.info(f"Startup phase '{phase}' {status}", extra=extra)

        # Also log to audit for security monitoring
        audit_logger = self.get_audit_logger()
        audit_logger.info(f"Startup: {phase} {status}", extra=extra)


# Global logger instance
_logger_instance: Optional[PepeluGPTLogger] = None


def setup_enhanced_logging(
    config: Dict[str, Any], debug: bool = False
) -> PepeluGPTLogger:
    """Setup the enhanced logging system."""
    global _logger_instance
    _logger_instance = PepeluGPTLogger(config, debug)
    return _logger_instance


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance. Falls back to basic logger if enhanced logging not setup."""
    if _logger_instance:
        return _logger_instance.get_logger(name)
    else:
        # Fallback to basic logging
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("🔴 %(levelname)s %(name)s: %(message)s")
            )
            logger.addHandler(handler)
            logger.setLevel(logging.ERROR)
        return logger


def get_audit_logger() -> logging.Logger:
    """Get the audit logger."""
    if _logger_instance:
        return _logger_instance.get_audit_logger()
    return get_logger("audit")


def log_user_query(query: str, response_time: Optional[float] = None):
    """Convenience function to log user queries."""
    if _logger_instance:
        _logger_instance.log_user_query(query, response_time)


def log_system_event(event: str, details: Optional[Dict[str, Any]] = None):
    """Convenience function to log system events."""
    if _logger_instance:
        _logger_instance.log_system_event(event, details)


def log_error(
    error: Exception, context: Optional[str] = None, error_code: Optional[str] = None
):
    """Convenience function to log errors."""
    if _logger_instance:
        _logger_instance.log_error(error, context, error_code)


def log_startup_phase(
    phase: str, status: str = "started", details: Optional[Dict[str, Any]] = None
):
    """Convenience function to log startup phases."""
    if _logger_instance:
        _logger_instance.log_startup_phase(phase, status, details)
