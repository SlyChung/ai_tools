"""
Logger class

Important information:
- The logger is configured in the config.json file.
- Unsure what part of the code is responsible for creating the log files.

Note:
- This logger is a more updated version of the logger in Scribe_V3 - 9/2/25.
"""

import logging
import json
from pathlib import Path

from ai_tools.utilities import config as config_module
from ai_tools.utilities.config import Config
from ai_tools.utilities.decorators import version

@version("1.0.0")
class Logger:
    def __init__(self, logger_type: str, vault_log: str = None, config = Config):
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

    def log_debug(self, message: str):
        self.logger.debug(message)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)
    
    def log_critical(self, message: str):
        self.logger.critical(message)

    def log_user_action(self, message: str):
        self.logger.info(f"[USER ACTION] {message}")

    
        
