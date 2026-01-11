"""
Shared pytest fixtures for ai_tools test suite.

This module provides:
- Temporary directories for file operations
- Mock config objects
- Test data factories
- Cleanup utilities
"""

import pytest
import tempfile
import shutil
import json
import sys
import logging
from pathlib import Path
from unittest.mock import MagicMock
from typing import Generator, Dict, Any

# Add both src and src/ai_tools to path for imports
# This handles both absolute imports (from ai_tools.utilities...)
# and relative imports (from utilities...) used in the source code
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root / "src"))
sys.path.insert(0, str(_project_root / "src" / "ai_tools"))


# --------------------------------------------------------------------------
# Temporary Directory Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test file operations.

    Yields:
        Path: Path to the temporary directory

    Automatically cleaned up after test completes.
    """
    temp_path = Path(tempfile.mkdtemp(prefix="ai_tools_test_"))
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_project_root(temp_dir: Path, monkeypatch) -> Path:
    """
    Create a temporary PROJECT_ROOT and patch the config module.

    This allows file_management functions to operate on a test directory
    instead of the real project root.

    Args:
        temp_dir: The temporary directory fixture
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Path: The patched PROJECT_ROOT path
    """
    # Patch PROJECT_ROOT in the config module
    monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
    # Also need to patch it in file_management since it imports at module level
    monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)
    return temp_dir


# --------------------------------------------------------------------------
# Config Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def sample_config_dict() -> Dict[str, Any]:
    """
    Provide a sample configuration dictionary for testing.

    Returns:
        Dict[str, Any]: A minimal valid configuration
    """
    return {
        "logging": {
            "log_format": {
                "app": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(levelname)s: %(message)s",
                    "file": "logs/app.log",
                    "console": False
                },
                "error": {
                    "level": "ERROR",
                    "format": "%(asctime)s - %(levelname)s: %(message)s",
                    "file": "logs/error.log",
                    "console": False
                },
                "api": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(levelname)s: %(message)s",
                    "file": "logs/api.log",
                    "console": False
                },
                "vault": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(levelname)s: %(message)s",
                    "file": "logs/vaults",
                    "console": False
                },
                "technical": {
                    "level": "DEBUG",
                    "format": "%(asctime)s - %(levelname)s - %(module)s.%(funcName)s: %(message)s",
                    "file": "logs/technical.log",
                    "console": False
                },
                "database": {
                    "level": "DEBUG",
                    "format": "%(asctime)s - %(levelname)s - %(module)s.%(funcName)s: %(message)s",
                    "file": "logs/database.log",
                    "console": False
                }
            }
        }
    }


@pytest.fixture
def temp_config_file(temp_dir: Path, sample_config_dict: Dict[str, Any]) -> Path:
    """
    Create a temporary config.json file.

    Args:
        temp_dir: Temporary directory fixture
        sample_config_dict: Sample configuration dictionary

    Returns:
        Path: Path to the temporary config file
    """
    config_path = temp_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(sample_config_dict, f)
    return config_path


@pytest.fixture
def mock_config(sample_config_dict: Dict[str, Any]):
    """
    Create a mock Config object without file I/O.

    Args:
        sample_config_dict: Sample configuration dictionary

    Returns:
        MagicMock: A mock Config object
    """
    mock = MagicMock()
    mock.config = sample_config_dict

    def mock_get(path: str, default=None, cast_type=None):
        keys = path.split(".")
        value = sample_config_dict
        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            return default
        if cast_type:
            try:
                value = cast_type(value)
            except (ValueError, TypeError):
                return default
        return value

    mock.get = mock_get
    return mock


# --------------------------------------------------------------------------
# Logger Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def temp_log_dir(temp_dir: Path) -> Path:
    """
    Create a temporary logs directory.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the logs directory
    """
    log_dir = temp_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    (log_dir / "vaults").mkdir(exist_ok=True)
    return log_dir


@pytest.fixture
def mock_logger():
    """
    Create a mock Logger that doesn't write to files.

    Returns:
        MagicMock: A mock Logger object
    """
    mock = MagicMock()
    mock.log_debug = MagicMock()
    mock.log_info = MagicMock()
    mock.log_warning = MagicMock()
    mock.log_error = MagicMock()
    mock.log_critical = MagicMock()
    mock.log_user_action = MagicMock()
    return mock


# --------------------------------------------------------------------------
# File Management Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def sample_file_structure(temp_project_root: Path) -> Dict[str, Path]:
    """
    Create a sample file structure for file management tests.

    Args:
        temp_project_root: Patched temporary PROJECT_ROOT

    Returns:
        Dict[str, Path]: Dictionary of created paths
    """
    # Create directories
    notes_dir = temp_project_root / "notes"
    notes_dir.mkdir()

    subdirs = temp_project_root / "notes" / "subdir"
    subdirs.mkdir()

    # Create sample files
    sample_md = notes_dir / "sample.md"
    sample_md.write_text("# Sample Note\n\nThis is a sample note.")

    sample_txt = notes_dir / "sample.txt"
    sample_txt.write_text("Plain text content")

    return {
        "root": temp_project_root,
        "notes_dir": notes_dir,
        "subdir": subdirs,
        "sample_md": sample_md,
        "sample_txt": sample_txt
    }


# --------------------------------------------------------------------------
# Memory/Chunk Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def sample_note_content() -> str:
    """
    Provide sample Markdown content for note tests.

    Returns:
        str: Sample Markdown content
    """
    return """# Test Note

## Section 1
Some content here.

## Section 2
More content here.

### Subsection 2.1
Detailed content.
"""


# --------------------------------------------------------------------------
# Tool Envelope Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def sample_tool_function():
    """
    Create a sample function for ToolEnvelope testing.

    Returns:
        Callable: A sample function with proper annotations
    """
    def sample_add(a: int, b: int, optional: str = "default") -> Dict[str, Any]:
        """Add two numbers together."""
        return {
            "status": True,
            "data": {"result": a + b},
            "message": "Addition successful"
        }

    sample_add.__version__ = "1.0.0"
    return sample_add


# --------------------------------------------------------------------------
# Autouse Fixtures for Test Isolation
# --------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_logging_handlers():
    """
    Reset logging handlers between tests to prevent handler accumulation.

    This runs automatically before AND after each test.
    """
    # Clean up handlers BEFORE test to ensure clean state
    for name in ["app", "error", "api", "vault", "technical", "database"]:
        logger = logging.getLogger(name)
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)

    yield

    # Clean up handlers AFTER test
    for name in ["app", "error", "api", "vault", "technical", "database"]:
        logger = logging.getLogger(name)
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
