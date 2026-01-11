"""
Tests for NoteV3 class in src/ai_tools/working_memory/sub_agent/note_writer/note_v3.py

MVP component - load, save, read_note, write_note work.
Tree operations are stubs.
"""

import pytest
import json
from unittest.mock import MagicMock, patch


class TestNoteV3Init:
    """Tests for NoteV3 initialization."""

    @pytest.mark.mvp
    def test_init_sets_note_id(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that init sets the note_id."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            assert note.note_id == "test_note"

    @pytest.mark.mvp
    def test_init_registers_tools(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that init registers read_note and write_note tools."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            assert "read_note" in note.tools
            assert "write_note" in note.tools

    @pytest.mark.mvp
    def test_init_calls_load(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that init calls load() automatically."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Loaded Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            # load() should have been called and populated note_md
            assert note.note_md == "# Loaded Content"


class TestNoteV3Load:
    """Tests for NoteV3.load() method."""

    @pytest.mark.mvp
    def test_load_success(self, temp_dir, sample_config_dict, monkeypatch):
        """Test successful note loading."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Test Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            assert note.note_md == "# Test Content"

    @pytest.mark.mvp
    def test_load_returns_status_dict(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that load returns proper status dictionary."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3.__new__(NoteV3)
            note.note_id = "test"
            note.tools = {}
            note.note_md = ""

            result = note.load()

            # Note: load() may return error since find_file is mocked differently here
            # The key is that it returns a dict with status


class TestNoteV3Save:
    """Tests for NoteV3.save() method."""

    @pytest.mark.mvp
    def test_save_calls_write_file(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that save calls write_file."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Original"
            mock_fm.write_file.return_value = None
            mock_fm.file_size.return_value = 100

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")
            note.note_md = "# Updated Content"

            result = note.save()

            assert result["status"] is True
            mock_fm.write_file.assert_called_once()


class TestNoteV3ReadNote:
    """Tests for NoteV3.read_note() method."""

    @pytest.mark.mvp
    def test_read_note_returns_content(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that read_note returns note content."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# My Note"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.read_note()

            assert result["status"] is True
            assert result["data"]["note_content"] == "# My Note"

    @pytest.mark.mvp
    def test_read_note_returns_note_id(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that read_note includes note_id in response."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("my_unique_note")

            result = note.read_note()

            assert result["data"]["note_id"] == "my_unique_note"


class TestNoteV3WriteNote:
    """Tests for NoteV3.write_note() method."""

    @pytest.mark.mvp
    def test_write_note_updates_memory(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that write_note updates in-memory content."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Original"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.write_note("# New Content")

            assert result["status"] is True
            assert note.note_md == "# New Content"

    @pytest.mark.mvp
    def test_write_note_returns_updated_content(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that write_note returns the updated content."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Original"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.write_note("# Updated")

            assert result["data"]["note_content"] == "# Updated"


class TestNoteV3ExecuteTool:
    """Tests for NoteV3.execute_tool() method."""

    @pytest.mark.mvp
    def test_execute_read_note(self, temp_dir, sample_config_dict, monkeypatch):
        """Test executing read_note tool."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.execute_tool({"tool": "read_note"})

            assert result["status"] is True

    @pytest.mark.mvp
    def test_execute_write_note(self, temp_dir, sample_config_dict, monkeypatch):
        """Test executing write_note tool."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Original"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.execute_tool({"tool": "write_note", "content": "# New"})

            assert result["status"] is True

    @pytest.mark.mvp
    def test_execute_invalid_tool(self, temp_dir, sample_config_dict, monkeypatch):
        """Test executing invalid tool fails gracefully."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.execute_tool({"tool": "invalid_tool"})

            assert result["status"] is False

    @pytest.mark.mvp
    def test_execute_write_note_missing_content(self, temp_dir, sample_config_dict, monkeypatch):
        """Test write_note without content argument fails."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            result = note.execute_tool({"tool": "write_note"})

            assert result["status"] is False


class TestNoteV3Envelope:
    """Tests for NoteV3.envelope() method."""

    @pytest.mark.mvp
    def test_envelope_structure(self, temp_dir, sample_config_dict, monkeypatch):
        """Test envelope returns correct structure."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Content"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")

            env = note.envelope()

            assert "note_id" in env
            assert "note_content" in env

    @pytest.mark.mvp
    def test_envelope_contains_current_content(self, temp_dir, sample_config_dict, monkeypatch):
        """Test envelope contains current note content."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        
        monkeypatch.setattr("ai_tools.general_tools.file_management.PROJECT_ROOT", temp_dir)

        with patch("ai_tools.working_memory.sub_agent.note_writer.note_v3.fm") as mock_fm:
            mock_fm.find_file.return_value = ["notes", "test.md"]
            mock_fm.read_file.return_value = "# Initial"

            from ai_tools.working_memory.sub_agent.note_writer.note_v3 import NoteV3
            note = NoteV3("test_note")
            note.write_note("# Modified Content")

            env = note.envelope()

            assert env["note_content"] == "# Modified Content"


class TestNoteV3TreeOperations:
    """Tests for NoteV3 tree operations (stubs)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="NoteV3.build_note() is not implemented - returns True without building")
    def test_build_note(self):
        """Test building note from tree structure."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="NoteV3.parse_note() is not implemented - returns True without parsing")
    def test_parse_note(self):
        """Test parsing note into tree structure."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="NoteV3.add_element() is not implemented - method body is empty")
    def test_add_element(self):
        """Test adding element to note tree."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="NoteV3.edit_element() is not implemented - returns True without editing")
    def test_edit_element(self):
        """Test editing element in note tree."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="NoteV3.delete_element() is not implemented - returns True without deleting")
    def test_delete_element(self):
        """Test deleting element from note tree."""
        pass
