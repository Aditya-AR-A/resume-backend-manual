"""
Custom logger module for enhanced logging functionality.

This module provides the `CLogger` class, a custom logging formatter that adds
date and time information to each log entry, and supports colored log messages
for improved readability. Logs are written to both:
- A complete log file (all logs across runs).
- A session log file (only current session).

Usage:
    from logger import get_logger
    logger = get_logger("my_app")

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
"""

import logging
import os
from datetime import datetime

class CLogger(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self._datefmt = "%Y-%m-%d %H:%M:%S"
        self.colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "gray": "\033[90m",
            "orange": "\033[38;5;208m",
            "reset": "\033[0m",
        }
        self._style = logging.LogRecord

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._fmt

        # If the user provides a custom color via `extra`
        color = getattr(record, "color", None)
        if color and color in self.colors:
            log_fmt = f"{self.colors[color]}{log_fmt}{self.colors['reset']}"
        else:
            # Fallback: color based on log level
            if record.levelname == "DEBUG":
                log_fmt = self.colors["cyan"] + log_fmt + self.colors["reset"]
            elif record.levelname == "INFO":
                log_fmt = self.colors["green"] + log_fmt + self.colors["reset"]
            elif record.levelname == "WARNING":
                log_fmt = self.colors["yellow"] + log_fmt + self.colors["reset"]
            elif record.levelname == "ERROR":
                log_fmt = self.colors["red"] + log_fmt + self.colors["reset"]
            elif record.levelname == "CRITICAL":
                log_fmt = self.colors["magenta"] + log_fmt + self.colors["reset"]

        # Temporarily swap fmt so logging.Formatter can process it
        original_fmt = self._fmt
        self._fmt = log_fmt
        formatted = super().format(record)
        self._fmt = original_fmt

        return formatted



def get_logger(name: str = None,
               log_dir: str = "logs",
               complete_log: str = "complete.log",
               session_prefix: str = "session") -> logging.Logger:
    """Create a logger with file handlers (complete + session) and console output."""
    if name is None:
        name = datetime.now().strftime('%Y%m%d_%H%M%S')  # Default to date-time string
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    


    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Formatter (color for console, plain for files)
    console_formatter = CLogger("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                       "%Y-%m-%d %H:%M:%S")

    # Console handler (with colors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Complete log file handler
    complete_handler = logging.FileHandler(os.path.join(log_dir, complete_log))
    complete_handler.setLevel(logging.DEBUG)
    complete_handler.setFormatter(file_formatter)
    logger.addHandler(complete_handler)

    # Session log file handler
    session_file = os.path.join(
        log_dir,
        f"{session_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    session_handler = logging.FileHandler(session_file)
    session_handler.setLevel(logging.DEBUG)
    session_handler.setFormatter(file_formatter)
    logger.addHandler(session_handler)

    return logger
