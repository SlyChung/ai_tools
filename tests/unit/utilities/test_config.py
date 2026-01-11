"""
Tests for the Config class in src/ai_tools/utilities/config.py

Production-ready component - all tests should pass.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch


class TestConfigInit:
    """Tests for Config initialization."""

    @pytest.mark.production
    def test_init_with_existing_config(self, temp_dir, sample_config_dict, monkeypatch):
        """Test Config initialization with existing config file."""
        # Create config file
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))

        # Patch PROJECT_ROOT
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        assert config.config == sample_config_dict

    @pytest.mark.production
    def test_init_creates_default_config_when_missing(self, temp_dir, monkeypatch):
        """Test Config creates default config when file doesn't exist."""
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        # Default config should be created
        assert (temp_dir / "config.json").exists()
        # Check for expected default keys
        assert "vault" in config.config

    @pytest.mark.production
    def test_init_stores_config_file_path(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Config stores the correct config file path."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        assert config.config_file == temp_dir / "config.json"


class TestConfigGet:
    """Tests for Config.get() method."""

    @pytest.mark.production
    def test_get_simple_path(self, temp_dir, sample_config_dict, monkeypatch):
        """Test getting a value with a simple dot path."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("logging.log_format.app.level")
        assert result == "INFO"

    @pytest.mark.production
    def test_get_nested_path(self, temp_dir, sample_config_dict, monkeypatch):
        """Test getting a deeply nested value."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("logging.log_format.technical.format")
        assert "%(module)s" in result

    @pytest.mark.production
    def test_get_invalid_path_returns_default(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that invalid path returns default value."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("invalid.path.here", default="fallback")
        assert result == "fallback"

    @pytest.mark.production
    def test_get_returns_none_for_missing_without_default(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that missing path without default returns None."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("nonexistent.path")
        assert result is None

    @pytest.mark.production
    def test_get_with_type_casting_bool(self, temp_dir, sample_config_dict, monkeypatch):
        """Test type casting with cast_type=bool."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("logging.log_format.app.console", cast_type=bool)
        assert result is False
        assert isinstance(result, bool)

    @pytest.mark.production
    def test_get_with_type_casting_str(self, temp_dir, sample_config_dict, monkeypatch):
        """Test type casting with cast_type=str."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("logging.log_format.app.level", cast_type=str)
        assert result == "INFO"
        assert isinstance(result, str)

    @pytest.mark.production
    def test_get_top_level_key(self, temp_dir, sample_config_dict, monkeypatch):
        """Test getting a top-level key."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        result = config.get("logging")
        assert isinstance(result, dict)
        assert "log_format" in result


class TestConfigSet:
    """Tests for Config.set() method (stub)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="Config.set() is not implemented - method body is empty")
    def test_set_simple_value(self):
        """Test setting a simple configuration value."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Config.set() is not implemented - method body is empty")
    def test_set_nested_value(self):
        """Test setting a nested configuration value."""
        pass


class TestConfigVersion:
    """Tests for Config version decorator."""

    @pytest.mark.production
    def test_config_has_version(self):
        """Test that Config class has version attribute."""
        from ai_tools.utilities.config import Config
        assert hasattr(Config, "__version__")
        assert Config.__version__ == "1.0.0"


class TestConfigLoadJson:
    """Tests for Config.load_json() method."""

    @pytest.mark.production
    def test_load_json_reads_valid_file(self, temp_dir, sample_config_dict, monkeypatch):
        """Test load_json reads a valid JSON file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        # load_json is called in __init__, verify the result
        assert config.config == sample_config_dict

    @pytest.mark.production
    def test_load_json_creates_file_when_missing(self, temp_dir, monkeypatch):
        """Test load_json creates config file when missing."""
        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)

        # Verify file doesn't exist
        assert not (temp_dir / "config.json").exists()

        from ai_tools.utilities.config import Config
        config = Config("config.json")

        # File should now exist
        assert (temp_dir / "config.json").exists()
