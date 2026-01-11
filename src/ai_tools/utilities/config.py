"""
Configuration management for the ai_tools library.

This module provides the Config class for loading and accessing configuration
values from config.json. Supports dot-path access for nested values and
optional type casting.

Attributes:
    PROJECT_ROOT: Path to the project root directory (current working directory).

Example:
    from ai_tools.utilities.config import Config

    config = Config()
    log_level = config.get("logging.log_format.error.level")
    console_enabled = config.get("logging.log_format.error.console", cast_type=bool)
"""

import os
import json
from typing import Dict, Any, Optional, List

from pathlib import Path

from utilities.decorators import version

PROJECT_ROOT = Path.cwd()


@version("1.0.0")
class Config:
    """Configuration manager that loads settings from config.json.

    Provides dot-path access to nested configuration values with optional
    type casting and default values.

    Attributes:
        config_file: Path to the configuration file.
        config: The loaded configuration dictionary.

    Example:
        config = Config()
        level = config.get("logging.log_format.error.level", default="INFO")
    """

    def __init__(self, config_file: str = "config.json"):
        """Initialize the Config instance.

        Args:
            config_file: Name of the configuration file relative to PROJECT_ROOT.
                Defaults to "config.json".
        """
        self.config_file = Path(PROJECT_ROOT, config_file)
        self.config = self.load_json()
        
    def load_json(self) -> Dict[str, Any]:
        """Load configuration from the JSON config file.

        If the config file doesn't exist, creates a default configuration
        and saves it.

        Returns:
            The configuration dictionary loaded from the file.

        Raises:
            Exception: If the file exists but cannot be read or parsed.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                #logger.log_app(f"Loaded configuration from {self.config_file}")
                return config
            else:
                config = self._create_default_config()
                self._save_config(config)
                #logger.log_app(f"Created new configuration at {self.config_file}")
                return config
        except Exception as e:
            #logger.log_error(f"Error loading configuration from {self.config_file}", e)
            raise

    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to the config file.

        Args:
            config: Configuration dictionary to save
        """
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    # deprecated
    def _create_default_config(self) -> Dict[str, Any]:
        """
        Create default configuration.

        Returns:
            Dict[str, Any]: Default configuration
        """
        return {
            "vault": {
                "default_template": "default.md",
                "folder_structure": {
                    "notes": [],
                    "templates": [],
                    "attachments": [],
                    "daily": []
                }
            },
            "access_control": {
                "whitelist_enabled": True,
                "whitelisted_users": [],
                "admin_users": []
            },
            "telegram": {
                "enabled": True,
                "welcome_message": (
                    "Welcome to Obsidian Vault Scribe! \n\n"
                    "I can help you manage your Obsidian vaults and process your notes.\n\n"
                    "Use /help to see available commands."
                ),
                "help_message": (
                    "📚 Available Commands:\n\n"
                    "/vault - Select or create a vault\n"
                    "/config - Update configuration\n"
                    "/vaults - List all vaults\n"
                    "/tree - View vault structure\n"
                    "/tag <file> <tag1> [tag2]... - Add tags to a file\n"
                    "/view <file> - View file contents\n"
                    "/help - Show this help message\n\n"
                    "Example tag usage:\n"
                    "/tag notes/meeting.md meeting important"
                ),
                "max_message_length": 4000,
                "allowed_file_types": [".md", ".txt", ".pdf"],
                "max_file_size_mb": 10
            },
            "summarization": {
                "enabled": True,
                "model": "gpt-3.5-turbo",
                "temperature": 0.3,
                "max_tokens": 1000,
                "min_summary_length": 50,
                "max_summary_length": 200,
                "default_tags": ["#note", "#processed"],
                "output_format": "markdown",
                "include_metadata": True,
                "metadata_fields": [
                    "title",
                    "summary",
                    "topics",
                    "tags",
                    "reading_time",
                    "word_count",
                    "created_at",
                    "updated_at"
                ],
                "processing_rules": {
                    "clean_whitespace": True,
                    "normalize_line_endings": True,
                    "remove_special_chars": True,
                    "preserve_links": True,
                    "preserve_code_blocks": True
                }
            }
        }
        
    def get(self, path: str, default=None, cast_type=None) -> Any:
        """Get a value from the configuration using dot-path notation.

        Args:
            path: Dot-separated path to the config value
                (e.g., "logging.log_format.error.level").
            default: Value to return if path doesn't exist. Defaults to None.
            cast_type: Optional type to cast the value to (e.g., bool, int).

        Returns:
            The configuration value, cast to cast_type if specified,
            or default if the path doesn't exist or casting fails.

        Example:
            config.get("logging.log_format.error.level")  # "ERROR"
            config.get("logging.log_format.error.console", cast_type=bool)  # False
        """
        keys = path.split(".")
        value = self.config

        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            #logger.log_error(f"Invalid path: {path}")
            return default
        
        if cast_type:
            try:
                value = cast_type(value)
            except (ValueError, TypeError):
                #logger.log_error(f"Invalid type: {cast_type}")
                return default

        return value
    
    def set(self, target: str, value: Any) -> None:
        """Set a value in the configuration using dot-path notation.

        Args:
            target: Dot-separated path to the config key to set.
            value: The value to set.

        Note:
            Not yet implemented.
        """
        pass

    # deprecated
    def is_user_whitelisted(self, user_id: int) -> bool:
        """Check if a user is whitelisted.

        Deprecated:
            This method is deprecated and may be removed in future versions.

        Args:
            user_id: The user ID to check.

        Returns:
            True if the user is in the whitelist, False otherwise.
        """
        return user_id in self.get("access_control.whitelisted_users", [])

    # deprecated
    def is_user_admin(self, user_id: int) -> bool:
        """Check if a user is an admin.

        Deprecated:
            This method is deprecated and may be removed in future versions.

        Args:
            user_id: The user ID to check.

        Returns:
            True if the user is in the admin list, False otherwise.
        """
        return user_id in self.get("access_control.admin_users", [])