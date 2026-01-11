"""
Configurable logging system for the ai_tools package.

This module provides a Logger class that wraps Python's logging module,
configured via config.json. Supports multiple logger types (app, error,
api, vault, technical, database) with separate output files and formats.

Example:
    from ai_tools.utilities.logger import Logger

    error_logger = Logger("error")
    error_logger.log_error("Something went wrong")

    technical_logger = Logger("technical")
    technical_logger.log_debug("Debug information")
"""

import logging
import json
from pathlib import Path

from ai_tools.utilities import config as config_module
from ai_tools.utilities.config import Config
from ai_tools.utilities.decorators import version


@version("1.0.0")
class Logger:
    """Configurable logger that reads settings from config.json.

    Supports six logger types configured in config.json:
    - app: General application logging
    - error: Error-only logging
    - api: API interaction logging
    - vault: Vault operation logging
    - technical: Debug/technical logging
    - database: Database operation logging

    Each logger type can have its own log level, file path, format,
    and optional console output configured in config.json.

    Attributes:
        logger_type: The type of logger (e.g., "error", "technical").
        vault_log: Optional vault-specific log file name.
        config: Configuration instance for reading settings.
        logger: The underlying Python logging.Logger instance.
        log_path: Path to the log file.
    """

    def __init__(self, logger_type: str, vault_log: str = None, config=Config):
        """Initialize a Logger instance.

        Args:
            logger_type: Type of logger to create. Must match a key in
                config.json under logging.log_format (e.g., "error", "technical").
            vault_log: Optional vault name for vault-specific logging.
                If provided, logs go to logs/vaults/{vault_log}.log.
            config: Configuration class to use. Defaults to Config.
        """
        self.logger_type = logger_type
        self.vault_log = vault_log
        self.config = config()
        self.logger = logging.getLogger(logger_type)
        self._configure_logger()

    def _configure_logger(self):
        # Get PROJECT_ROOT at runtime to allow for patching in tests
        project_root = config_module.PROJECT_ROOT

        # Get the log path
        if self.vault_log:
            self.log_path = str(Path(project_root, f"logs/vaults/{self.vault_log}.log"))
        else:
            self.log_path = str(Path(project_root, self.config.get(f"logging.log_format.{self.logger_type}.file")))

        # Get the log level
        level_str = self.config.get(f"logging.log_format.{self.logger_type}.level", default="INFO")
        log_level = getattr(logging, level_str.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Avoid duplicate handlers if already configured
        if self.logger.hasHandlers():
            return
        
        # Get the log format
        log_format = self.config.get(f"logging.log_format.{self.logger_type}.format", default="%(asctime)s - %(levelname)s - %(message)s")
        formatter = logging.Formatter(log_format)

        # File handler
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler (optional)
        if self.config.get(f"logging.log_format.{self.logger_type}.console", default=False, cast_type=bool):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    # --------- Logging methods ---------

    def log_debug(self, message: str) -> None:
        """Log a debug-level message.

        Args:
            message: The message to log.
        """
        self.logger.debug(message)

    def log_info(self, message: str) -> None:
        """Log an info-level message.

        Args:
            message: The message to log.
        """
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning-level message.

        Args:
            message: The message to log.
        """
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error-level message.

        Args:
            message: The message to log.
        """
        self.logger.error(message)

    def log_critical(self, message: str) -> None:
        """Log a critical-level message.

        Args:
            message: The message to log.
        """
        self.logger.critical(message)

    def log_user_action(self, message: str) -> None:
        """Log a user action at info level with [USER ACTION] prefix.

        Args:
            message: The user action to log.
        """
        self.logger.info(f"[USER ACTION] {message}")

    
        
