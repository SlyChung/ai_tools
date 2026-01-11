"""
Configuration for the library.
"""

import os
import json
from typing import Dict, Any, Optional, List
#from library.logger import logger

# src/library/config.py
from pathlib import Path

from utilities.decorators import version

PROJECT_ROOT = Path.cwd()

@version("1.0.0")
class Config:
    """
    Manages Configuration for the library.
    """
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(PROJECT_ROOT, config_file)
        self.config = self.load_json()
        
    def load_json(self) -> Dict[str, Any]:
        """
        Loads the configuration from the config file.
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
        
    def get(self, path: str, default = None, cast_type = None) -> Any:
        """
        Get a value from the configuration.

        Supports dot-path access.
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
        """
        Set a value in the configuration.
        """
    
    # deprecated
    def is_user_whitelisted(self, user_id: int) -> bool:
        """
        Check if a user is whitelisted.
        """
        return user_id in self.get("access_control.whitelisted_users", [])
    
    # deprecated
    def is_user_admin(self, user_id: int) -> bool:
        """
        Check if a user is an admin.
        """
        return user_id in self.get("access_control.admin_users", [])