"""
Tests for Task class in src/ai_tools/working_memory/task.py

Stub component - skeleton only.
"""

import pytest
import json


class TestTaskInit:
    """Tests for Task initialization."""

    @pytest.mark.mvp
    def test_init_with_task_id(self, temp_dir, sample_config_dict, monkeypatch):
        """Test Task initialization with task_id."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.working_memory.task import Task

        task = Task("task_123")

        # This should pass since __init__ does call super()
        assert task.chunk_id == "task_123"


class TestTaskMethods:
    """Tests for Task methods (all stubs - inherited from MemoryChunk)."""

    @pytest.mark.stub
    @pytest.mark.skip(reason="Task inherits from MemoryChunk - load() is a stub")
    def test_load(self):
        """Test loading task from storage."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Task inherits from MemoryChunk - save() is a stub")
    def test_save(self):
        """Test saving task to storage."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Task inherits from MemoryChunk - envelope() is a stub")
    def test_envelope(self):
        """Test getting task envelope."""
        pass

    @pytest.mark.stub
    @pytest.mark.skip(reason="Task inherits from MemoryChunk - execute_tool() is a stub")
    def test_execute_tool(self):
        """Test executing tool on task."""
        pass


class TestTaskRefresh:
    """Tests for Task.refresh() method (inherited from MemoryChunk)."""

    @pytest.mark.mvp
    def test_refresh_inherited(self, temp_dir, sample_config_dict, monkeypatch):
        """Test that Task inherits working refresh() from MemoryChunk."""
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(sample_config_dict))
        logs_dir = temp_dir / "logs"
        logs_dir.mkdir()

        monkeypatch.setattr("ai_tools.utilities.config.PROJECT_ROOT", temp_dir)
        

        from ai_tools.working_memory.task import Task

        task = Task("task_123")

        # refresh() is inherited and should work (calls stub load())
        result = task.refresh()

        # Should return success since load() stub doesn't raise
        assert result["status"] is True
        assert result["data"]["chunk_id"] == "task_123"
