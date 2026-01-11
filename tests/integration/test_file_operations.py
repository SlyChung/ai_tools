"""
Integration tests for file operations.

These tests verify end-to-end file operation workflows.
"""

import pytest
import json


class TestFileOperationsWorkflow:
    """Integration tests for complete file operation workflows."""

    @pytest.mark.integration
    @pytest.mark.production
    def test_create_write_read_delete_workflow(self, temp_dir, sample_config_dict, monkeypatch):
        """Test complete file lifecycle: create -> write -> read -> delete."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Step 1: Create directory
        dir_result = fm.create_directory("test_workflow")
        assert dir_result["status"] is True
        assert (temp_dir / "test_workflow").exists()

        # Step 2: Create file
        file_result = fm.create_file("test_workflow", "test.txt")
        assert file_result["status"] is True
        assert (temp_dir / "test_workflow" / "test.txt").exists()

        # Step 3: Write content
        fm.write_file("test_workflow", "test.txt", "Hello, Integration Test!")

        # Step 4: Read content
        content = fm.read_file("test_workflow", "test.txt")
        assert content == "Hello, Integration Test!"

        # Step 5: Delete file
        delete_result = fm.delete_file("test_workflow", "test.txt")
        assert delete_result["status"] is True
        assert not (temp_dir / "test_workflow" / "test.txt").exists()

    @pytest.mark.integration
    @pytest.mark.production
    def test_append_workflow(self, temp_dir, sample_config_dict, monkeypatch):
        """Test file append workflow."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Create initial file
        fm.create_file("", "append_test.txt")
        fm.write_file("", "append_test.txt", "Line 1")

        # Append multiple times
        fm.append_file("", "append_test.txt", "\nLine 2")
        fm.append_file("", "append_test.txt", "\nLine 3")

        # Verify final content
        content = fm.read_file("", "append_test.txt")
        assert "Line 1" in content
        assert "Line 2" in content
        assert "Line 3" in content

    @pytest.mark.integration
    @pytest.mark.production
    def test_directory_listing_workflow(self, temp_dir, sample_config_dict, monkeypatch):
        """Test directory listing workflow."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Create test structure
        fm.create_directory("list_test")
        fm.create_directory("list_test/subdir1")
        fm.create_directory("list_test/subdir2")
        fm.create_file("list_test", "file1.txt")
        fm.create_file("list_test", "file2.md")

        # List files
        files_result = fm.list_files("list_test")
        assert files_result["status"] is True
        files = files_result["data"]["files"]
        assert "file1.txt" in files
        assert "file2.md" in files
        assert "subdir1" in files
        assert "subdir2" in files

        # List subdirectories only
        dirs_result = fm.list_direct_subdirectories("list_test")
        assert dirs_result["status"] is True
        dirs = dirs_result["data"]["directories"]
        assert "subdir1" in dirs
        assert "subdir2" in dirs
        assert "file1.txt" not in dirs
        assert "file2.md" not in dirs

    @pytest.mark.integration
    @pytest.mark.production
    def test_file_exists_workflow(self, temp_dir, sample_config_dict, monkeypatch):
        """Test file existence check workflow."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Check file doesn't exist initially
        result1 = fm.file_exists("", "existence_test.txt")
        assert result1["status"] is True
        assert result1["data"]["file_exists"] is False

        # Create file
        fm.create_file("", "existence_test.txt")

        # Check file exists now
        result2 = fm.file_exists("", "existence_test.txt")
        assert result2["status"] is True
        assert result2["data"]["file_exists"] is True

        # Delete file
        fm.delete_file("", "existence_test.txt")

        # Check file doesn't exist anymore
        result3 = fm.file_exists("", "existence_test.txt")
        assert result3["status"] is True
        assert result3["data"]["file_exists"] is False

    @pytest.mark.integration
    @pytest.mark.production
    def test_rename_workflow(self, temp_dir, sample_config_dict, monkeypatch):
        """Test file rename workflow."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Create file with content
        fm.create_file("", "original.txt")
        fm.write_file("", "original.txt", "Important content")

        # Rename file
        result = fm.rename_file("", "original.txt", "renamed.txt")
        assert result["status"] is True

        # Verify old name doesn't exist
        old_exists = fm.file_exists("", "original.txt")
        assert old_exists["data"]["file_exists"] is False

        # Verify new name exists with same content
        new_exists = fm.file_exists("", "renamed.txt")
        assert new_exists["data"]["file_exists"] is True

        content = fm.read_file("", "renamed.txt")
        assert content == "Important content"


class TestLoggerIntegration:
    """Integration tests for logger functionality."""

    @pytest.mark.integration
    @pytest.mark.production
    def test_logger_configures_correctly(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that logger configures itself from config file."""
        # Setup
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.logger import Logger
        import logging

        # Create logger
        app_logger = Logger("app")

        # Verify logger is configured correctly
        assert app_logger.logger_type == "app"
        assert app_logger.logger.level == logging.INFO
        assert "logs/app.log" in app_logger.log_path

        # Verify logging methods work (using mock)
        from unittest.mock import MagicMock
        app_logger.logger = MagicMock()

        app_logger.log_info("Test message 1")
        app_logger.log_warning("Test warning")
        app_logger.log_error("Test error")

        app_logger.logger.info.assert_called_with("Test message 1")
        app_logger.logger.warning.assert_called_with("Test warning")
        app_logger.logger.error.assert_called_with("Test error")


class TestConfigIntegration:
    """Integration tests for config with file system."""

    @pytest.mark.integration
    @pytest.mark.production
    def test_config_loads_from_file(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that config loads correctly from JSON file."""
        # Write config file
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config

        config = Config("config.json")

        # Verify config loaded correctly
        assert config.get("logging.log_format.app.level") == "INFO"
        assert config.get("logging.log_format.error.level") == "ERROR"

    @pytest.mark.integration
    @pytest.mark.production
    def test_config_creates_default_when_missing(self, temp_dir, monkeypatch):
        """Test that config creates default file when missing."""
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config

        # Config file shouldn't exist
        config_path = temp_dir / "new_config.json"
        assert not config_path.exists()

        # Load config - should create default
        config = Config("new_config.json")

        # File should now exist
        assert config_path.exists()

        # Should have default structure
        assert "vault" in config.config
