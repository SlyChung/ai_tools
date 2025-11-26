"""
This module is the structure for the working memory of the AI.
It is a tree of notes, sections, and tasks.

The working memory will be a part of the system prompt of an agent.

What the working memory will do is:
- Store the tasks that the agent is working on
- Store the memory chunks that the agent is working on
- Output all memory chunks as a list of dictionaries
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import os
import uuid

from general_tools import file_management as fm

from working_memory.memoryChunk import MemoryChunk
from working_memory.task import Task

# Scribe Specific
from working_memory.note import Note
from working_memory.vault import Vault

from utilities.logger import Logger

error_logger = Logger("error")
technical_logger = Logger("technical")

class WorkingMemory:
    def __init__(self):

        self.tasks = []
        self.memory_chunks = []
        self.chat_history = []

    def add_task(self, task_name: str, task_description: str) -> None:
        """
        Add a task to the working memory
        """
        task_id = str(uuid.uuid4())
        task = Task(task_id, task_name, task_description)

        self.tasks.append(task)

    def delete_task(self, task_id: str) -> None:
        """
        Delete a task from the working memory
        """
        for task in self.tasks:
            if task.chunk_id == task_id:
                self.tasks.remove(task)
                return # TODO: return a status message
        return # TODO: return a status message

    def get_tasks(self) -> List[Task]:
        """
        Get all tasks from the working memory
        """
        return self.tasks

    def add_memory_chunk(self, chunk_name: str, chunk_type: str) -> None:
        """
        Add a chunk to the working memory
        """
        chunk_id = str(uuid.uuid4())

        if chunk_type == "note":
            chunk = Note(chunk_id)
        elif chunk_type == "vault":
            chunk = Vault(chunk_id)
        else:
            raise ValueError(f"Invalid chunk type: {chunk_type}")

        self.chunks.append(chunk)

    def delete_memory_chunk(self, chunk_id: str) -> None:
        """
        Delete a chunk from the working memory
        """
        for chunk in self.chunks:
            if chunk.chunk_id == chunk_id:
                self.chunks.remove(chunk)
                return # TODO: return a status message
        return # TODO: return a status message

    # TODO: not implemented right
    def get_memory_chunks(self) -> List[str]:
        """
        Get all memory chunks from the working memory
        """
        return self.chunks
    
    def envelope(self) -> Dict[str, Any]:
        """
        Get the working memory as a dictionary
        """
        return {
            "tasks": [task.envelope() for task in self.tasks],
            "chunks": [chunk.envelope() for chunk in self.chunks]
        }


