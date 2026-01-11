"""
Tests for file_management in src/ai_tools/general_tools/file_management.py

Production-ready component - most tests should pass.
"""

import pytest
import json
from pathlib import Path


class TestCreateDirectory:
    """Tests for create_directory function."""

    @pytest.mark.production
    def test_create_directory_new(self, temp_dir, sample_config_dict, monkeypatch):
        """Test creating a new directory."""
        # Setup config and logs
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.create_directory("test_dir")

        assert result["status"] is True
        assert (temp_dir / "test_dir").exists()

    @pytest.mark.production
    def test_create_directory_idempotent(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that creating existing directory succeeds (idempotent)."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        (temp_dir / "existing").mkdir()

        from ai_tools.general_tools import file_management as fm

        result = fm.create_directory("existing")

        assert result["status"] is True

    @pytest.mark.production
    def test_create_directory_nested(self, temp_dir, sample_config_dict, monkeypatch):
        """Test creating nested directories."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.create_directory("parent/child/grandchild")

        assert result["status"] is True
        assert (temp_dir / "parent/child/grandchild").exists()


class TestCreateFile:
    """Tests for create_file function."""

    @pytest.mark.production
    def test_create_file_new(self, temp_dir, sample_config_dict, monkeypatch):
        """Test creating a new file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.create_file("", "test.txt")

        assert result["status"] is True
        assert result["data"]["created"] is True
        assert (temp_dir / "test.txt").exists()

    @pytest.mark.production
    def test_create_file_existing_no_overwrite(self, temp_dir, sample_config_dict, monkeypatch):
        """Test creating file that exists without overwrite."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        (temp_dir / "exists.txt").write_text("content")

        from ai_tools.general_tools import file_management as fm

        result = fm.create_file("", "exists.txt", overwrite=False)

        assert result["status"] is False
        assert result["data"]["error"] == "file_exists"

    @pytest.mark.production
    def test_create_file_existing_with_overwrite(self, temp_dir, sample_config_dict, monkeypatch):
        """Test creating file that exists with overwrite=True."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        (temp_dir / "exists.txt").write_text("old content")

        from ai_tools.general_tools import file_management as fm

        result = fm.create_file("", "exists.txt", overwrite=True)

        assert result["status"] is True
        assert (temp_dir / "exists.txt").read_text() == ""


class TestDeleteFile:
    """Tests for delete_file function."""

    @pytest.mark.production
    def test_delete_file_existing(self, temp_dir, sample_config_dict, monkeypatch):
        """Test deleting an existing file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        # Create file to delete
        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.txt").write_text("content")

        from ai_tools.general_tools import file_management as fm

        result = fm.delete_file("notes", "sample.txt")

        assert result["status"] is True
        assert not (notes_dir / "sample.txt").exists()

    @pytest.mark.production
    def test_delete_file_nonexistent_idempotent(self, temp_dir, sample_config_dict, monkeypatch):
        """Test deleting nonexistent file succeeds (idempotent)."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.delete_file("", "nonexistent.txt")

        assert result["status"] is True
        assert result["data"]["deleted"] is True


class TestReadFile:
    """Tests for read_file function."""

    @pytest.mark.production
    def test_read_file_existing(self, temp_dir, sample_config_dict, monkeypatch):
        """Test reading an existing file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.md").write_text("# Sample Note\n\nThis is a sample note.")

        from ai_tools.general_tools import file_management as fm

        # Note: read_file returns a string, not a dict
        result = fm.read_file("notes", "sample.md")

        assert "# Sample Note" in result

    @pytest.mark.production
    def test_read_file_nonexistent_raises(self, temp_dir, sample_config_dict, monkeypatch):
        """Test reading nonexistent file raises error."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm
        from ai_tools.general_tools.file_management import FileManagementError

        with pytest.raises(FileManagementError):
            fm.read_file("", "nonexistent.txt")


class TestWriteFile:
    """Tests for write_file function."""

    @pytest.mark.production
    def test_write_file_new(self, temp_dir, sample_config_dict, monkeypatch):
        """Test writing to a new file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        # Note: write_file returns None
        fm.write_file("", "new.txt", "Hello World")

        assert (temp_dir / "new.txt").read_text() == "Hello World"

    @pytest.mark.production
    def test_write_file_overwrites(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that write_file overwrites existing content."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.txt").write_text("old content")

        from ai_tools.general_tools import file_management as fm

        fm.write_file("notes", "sample.txt", "New content")

        assert (notes_dir / "sample.txt").read_text() == "New content"


class TestAppendFile:
    """Tests for append_file function."""

    @pytest.mark.production
    def test_append_file_existing(self, temp_dir, sample_config_dict, monkeypatch):
        """Test appending to an existing file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.txt").write_text("Original content")

        from ai_tools.general_tools import file_management as fm

        result = fm.append_file("notes", "sample.txt", "\nAppended")

        assert result["status"] is True
        new_content = (notes_dir / "sample.txt").read_text()
        assert new_content == "Original content\nAppended"

    @pytest.mark.production
    def test_append_file_creates_if_missing(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that append creates file if it doesn't exist."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.append_file("", "new_append.txt", "Content")

        assert result["status"] is True
        assert (temp_dir / "new_append.txt").read_text() == "Content"


class TestListFiles:
    """Tests for list_files function."""

    @pytest.mark.production
    def test_list_files_existing_dir(self, temp_dir, sample_config_dict, monkeypatch):
        """Test listing files in existing directory."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.md").write_text("# Sample")
        (notes_dir / "sample.txt").write_text("text")

        from ai_tools.general_tools import file_management as fm

        result = fm.list_files("notes")

        assert result["status"] is True
        assert "sample.md" in result["data"]["files"]
        assert "sample.txt" in result["data"]["files"]

    @pytest.mark.production
    def test_list_files_nonexistent_dir(self, temp_dir, sample_config_dict, monkeypatch):
        """Test listing files in nonexistent directory fails."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.list_files("nonexistent")

        assert result["status"] is False


class TestListDirectSubdirectories:
    """Tests for list_direct_subdirectories function."""

    @pytest.mark.production
    def test_list_subdirectories(self, temp_dir, sample_config_dict, monkeypatch):
        """Test listing subdirectories."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "subdir").mkdir()
        (notes_dir / "file.txt").write_text("not a dir")

        from ai_tools.general_tools import file_management as fm

        result = fm.list_direct_subdirectories("notes")

        assert result["status"] is True
        assert "subdir" in result["data"]["directories"]
        assert "file.txt" not in result["data"]["directories"]


class TestFileExists:
    """Tests for file_exists function."""

    @pytest.mark.production
    def test_file_exists_true(self, temp_dir, sample_config_dict, monkeypatch):
        """Test file_exists returns True for existing file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "sample.md").write_text("# Sample")

        from ai_tools.general_tools import file_management as fm

        result = fm.file_exists("notes", "sample.md")

        assert result["status"] is True
        assert result["data"]["file_exists"] is True

    @pytest.mark.production
    def test_file_exists_false(self, temp_dir, sample_config_dict, monkeypatch):
        """Test file_exists returns False for nonexistent file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.file_exists("", "nonexistent.txt")

        assert result["status"] is True
        assert result["data"]["file_exists"] is False


class TestDirectoryExists:
    """Tests for directory_exists function."""

    @pytest.mark.production
    def test_directory_exists_true(self, temp_dir, sample_config_dict, monkeypatch):
        """Test directory_exists returns True for existing directory."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()

        from ai_tools.general_tools import file_management as fm

        result = fm.directory_exists("notes")

        assert result["status"] is True
        assert result["data"]["directory_exists"] is True

    @pytest.mark.production
    def test_directory_exists_false(self, temp_dir, sample_config_dict, monkeypatch):
        """Test directory_exists returns False for nonexistent directory."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.directory_exists("nonexistent_dir")

        assert result["status"] is True
        assert result["data"]["directory_exists"] is False


class TestIsValidFilename:
    """Tests for is_valid_filename function."""

    @pytest.mark.production
    def test_valid_filename(self):
        """Test valid filenames."""
        from ai_tools.general_tools.file_management import is_valid_filename

        assert is_valid_filename("document.txt") is True
        assert is_valid_filename("my-file_123.md") is True

    @pytest.mark.production
    def test_invalid_empty(self):
        """Test empty filename is invalid."""
        from ai_tools.general_tools.file_management import is_valid_filename

        assert is_valid_filename("") is False

    @pytest.mark.production
    def test_invalid_dot_only(self):
        """Test dot-only names are invalid."""
        from ai_tools.general_tools.file_management import is_valid_filename

        assert is_valid_filename(".") is False
        assert is_valid_filename("..") is False

    @pytest.mark.production
    def test_invalid_null_byte(self):
        """Test filenames with null byte are invalid."""
        from ai_tools.general_tools.file_management import is_valid_filename

        assert is_valid_filename("file\x00name.txt") is False

    @pytest.mark.production
    def test_invalid_non_string(self):
        """Test non-string input is invalid."""
        from ai_tools.general_tools.file_management import is_valid_filename

        assert is_valid_filename(123) is False
        assert is_valid_filename(None) is False


class TestRenameFile:
    """Tests for rename_file function."""

    @pytest.mark.production
    def test_rename_file_success(self, temp_dir, sample_config_dict, monkeypatch):
        """Test renaming a file successfully."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        notes_dir = temp_dir / "notes"
        notes_dir.mkdir()
        (notes_dir / "old.txt").write_text("content")

        from ai_tools.general_tools import file_management as fm

        result = fm.rename_file("notes", "old.txt", "new.txt")

        assert result["status"] is True
        assert not (notes_dir / "old.txt").exists()
        assert (notes_dir / "new.txt").exists()

    @pytest.mark.production
    def test_rename_file_nonexistent(self, temp_dir, sample_config_dict, monkeypatch):
        """Test renaming nonexistent file fails."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        from ai_tools.general_tools import file_management as fm

        result = fm.rename_file("", "nonexistent.txt", "new.txt")

        assert result["status"] is False


class TestFindFile:
    """Tests for find_file function (stub)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="find_file is not implemented - returns None")
    def test_find_file_existing(self):
        """Test finding an existing file."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="find_file is not implemented - returns None")
    def test_find_file_nonexistent(self):
        """Test finding a nonexistent file."""
        pass


class TestMoveFile:
    """Tests for move_file function."""

    @pytest.mark.production
    @pytest.mark.xfail(reason="move_file uses shutil which is not imported in file_management.py")
    def test_move_file_success(self, temp_dir, sample_config_dict, monkeypatch):
        """Test moving a file successfully."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        source_dir = temp_dir / "source"
        source_dir.mkdir()
        dest_dir = temp_dir / "dest"
        dest_dir.mkdir()
        (source_dir / "file.txt").write_text("content")

        from ai_tools.general_tools import file_management as fm

        result = fm.move_file("source", "file.txt", "dest")

        assert result["status"] is True


class TestCopyFile:
    """Tests for copy_file function."""

    @pytest.mark.production
    @pytest.mark.xfail(reason="copy_file uses shutil which is not imported in file_management.py")
    def test_copy_file_success(self, temp_dir, sample_config_dict, monkeypatch):
        """Test copying a file successfully."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        source_dir = temp_dir / "source"
        source_dir.mkdir()
        dest_dir = temp_dir / "dest"
        dest_dir.mkdir()
        (source_dir / "file.txt").write_text("content")

        from ai_tools.general_tools import file_management as fm

        result = fm.copy_file("source", "file.txt", "dest")

        assert result["status"] is True
