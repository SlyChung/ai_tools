"""
Tests for the Logger class in src/ai_tools/utilities/logger.py

Production-ready component - all tests should pass.
"""

import pytest
import logging
import json
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestLoggerInit:
    """Tests for Logger initialization."""

    @pytest.mark.production
    def test_logger_init_creates_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Logger creates a logging.Logger on init."""
        # Setup config and logs directory
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        assert logger.logger is not None
        assert isinstance(logger.logger, logging.Logger)

    @pytest.mark.production
    def test_logger_init_sets_logger_type(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Logger sets the logger_type attribute."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger
        logger = Logger("error")

        assert logger.logger_type == "error"

    @pytest.mark.production
    def test_logger_init_sets_correct_level(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Logger sets the correct log level from config."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger
        logger = Logger("error")

        assert logger.logger.level == logging.ERROR

    @pytest.mark.production
    def test_logger_init_creates_file_handler(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Logger creates a file handler on init."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        assert logger.logger.hasHandlers()

    @pytest.mark.production
    def test_logger_init_with_vault_log(self, temp_dir, sample_config_dict, monkeypatch):
        """Test Logger initialization with vault_log parameter."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()
        vaults_dir = logs_dir / "vaults"
        vaults_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger
        logger = Logger("vault", vault_log="my_vault")

        assert logger.vault_log == "my_vault"
        assert "my_vault.log" in logger.log_path


class TestLoggerMethods:
    """Tests for Logger logging methods using mocks (appropriate for library unit tests)."""

    @pytest.mark.production
    def test_log_info_calls_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_info calls the underlying logger.info method."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        # Mock the underlying logger
        logger.logger = MagicMock()
        logger.log_info("Test info message")

        logger.logger.info.assert_called_once_with("Test info message")

    @pytest.mark.production
    def test_log_error_calls_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_error calls the underlying logger.error method."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("error")

        logger.logger = MagicMock()
        logger.log_error("Test error message")

        logger.logger.error.assert_called_once_with("Test error message")

    @pytest.mark.production
    def test_log_debug_calls_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_debug calls the underlying logger.debug method."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("technical")

        logger.logger = MagicMock()
        logger.log_debug("Test debug message")

        logger.logger.debug.assert_called_once_with("Test debug message")

    @pytest.mark.production
    def test_log_warning_calls_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_warning calls the underlying logger.warning method."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        logger.logger = MagicMock()
        logger.log_warning("Test warning message")

        logger.logger.warning.assert_called_once_with("Test warning message")

    @pytest.mark.production
    def test_log_critical_calls_logger(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_critical calls the underlying logger.critical method."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        logger.logger = MagicMock()
        logger.log_critical("Test critical message")

        logger.logger.critical.assert_called_once_with("Test critical message")

    @pytest.mark.production
    def test_log_user_action_includes_prefix(self, temp_dir, sample_config_dict, monkeypatch):
        """Test log_user_action includes [USER ACTION] prefix."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        logger = Logger("app")

        logger.logger = MagicMock()
        logger.log_user_action("User clicked button")

        logger.logger.info.assert_called_once_with("[USER ACTION] User clicked button")


class TestLoggerVersion:
    """Tests for Logger version decorator."""

    @pytest.mark.production
    def test_logger_has_version(self):
        """Test that Logger class has version attribute."""
        from ai_tools.utilities.logger import Logger
        assert hasattr(Logger, "__version__")
        assert Logger.__version__ == "1.0.0"


class TestLoggerConfiguration:
    """Tests for Logger configuration handling."""

    @pytest.mark.production
    def test_logger_avoids_duplicate_handlers(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Logger doesn't add duplicate handlers."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.utilities.logger import Logger

        # Create logger twice with same name
        logger1 = Logger("app")
        initial_handler_count = len(logger1.logger.handlers)

        logger2 = Logger("app")
        final_handler_count = len(logger2.logger.handlers)

        # Handler count should not increase
        assert final_handler_count == initial_handler_count
