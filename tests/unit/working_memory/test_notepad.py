"""
Tests for Notepad class in src/ai_tools/working_memory/notepad.py

Stub component - skeleton only.
"""

import pytest
import json


class TestNotepadInit:
    """Tests for Notepad initialization."""

    @pytest.mark.mvp
    def test_init_with_notepad_id(self, temp_dir, sample_config_dict, monkeypatch):
        """Test Notepad initialization."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.working_memory.notepad import Notepad

        notepad = Notepad("notepad_123")
        assert notepad.chunk_id == "notepad_123"


class TestNotepadMemoryChunkMethods:
    """Tests for Notepad MemoryChunk methods (all stubs)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.load() is not implemented - method body is pass")
    def test_load(self):
        """Test loading notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.save() is not implemented - method body is pass")
    def test_save(self):
        """Test saving notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.delete() is not implemented - method body is pass")
    def test_delete(self):
        """Test deleting notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.close() is not implemented - method body is pass")
    def test_close(self):
        """Test closing notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.refresh() is not implemented - method body is pass")
    def test_refresh(self):
        """Test refreshing notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.execute_tool() is not implemented - method body is pass")
    def test_execute_tool(self):
        """Test executing tool on notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.envelope() is not implemented - method body is pass")
    def test_envelope(self):
        """Test getting notepad envelope."""
        pass


class TestNotepadToolMethods:
    """Tests for Notepad tool methods (all stubs)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.add_note() is not implemented - method body is pass")
    def test_add_note(self):
        """Test adding note to notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.delete_note() is not implemented - method body is pass")
    def test_delete_note(self):
        """Test deleting note from notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.edit_note() is not implemented - method body is empty")
    def test_edit_note(self):
        """Test editing note in notepad."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Notepad.toggle_note_status() is not implemented - method body is pass")
    def test_toggle_note_status(self):
        """Test toggling note status."""
        pass
