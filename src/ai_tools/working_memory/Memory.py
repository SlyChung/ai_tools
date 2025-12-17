"""
This module is the structure for the working memory of the AI.
It is a tree of notes, sections, and tasks.

The working memory will be a part of the system prompt of an agent.

What the working memory will do is:
- Store the tasks that the agent is working on
- Store the memory chunks that the agent is working on
- Output all memory chunks as a list of dictionaries

Memory Mandatory Methods:
- add_memory_chunk
- close_memory_chunk
- refresh_memory
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import os
import uuid

from general_tools import file_management as fm
from ai_tools.utilities.decorators import version
from working_memory.task import Task

from utilities.logger import Logger

error_logger = Logger("error")
technical_logger = Logger("technical")

@version("1.0.0")
class Memory:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.chunks = {}

    def load(self, self_id: str) -> None:
        """
        Load the memory from the file system
        To load in an existing memory, we need to pass in the memory id
        """
        pass

    def open_memory_chunk(self, chunk_name: str, chunk_type: str) -> None:
        """
        Add a chunk to the working memory
        """
        pass

    # Finished, no need to override
    @version("1.0.0")
    def close_memory_chunk(self, chunk_id: str) -> None:
        """
        Delete a chunk from the working memory
        """
        try:
            self.chunks[chunk_id].delete()
            return {
                "status": True,
                "data": {
                    "chunk_id": chunk_id
                },
                "message": "Memory chunk closed successfully"
            }
        except Exception as e:
            error_logger.log_error(f"WorkingMemory.close_memory_chunk: Error closing memory chunk: {e}")
            return {
                "status": False,
                "data": {
                    "chunk_id": chunk_id,
                    "error": str(e)
                },
                "message": f"Error closing memory chunk: {e}"
            }

    # Finished, no need to override
    @version("1.0.0")
    def envelope(self) -> Dict[str, Any]:
        """
        Get the working memory as a dictionary
        """
        memory_envelope = {}
        for chunk in self.chunks:
            memory_envelope[chunk.id] = self.chunks[chunk].envelope()

        return memory_envelope

    # Finished, no need to override
    @version("1.0.0")
    def execute_tool(self, chunk_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool on a chunk
        """
        try:
            return self.chunks[chunk_id].execute_tool(args)
        except Exception as e:
            error_logger.log_error(f"WorkingMemory.execute_tool: Error executing tool: {e}")
            return {
                "status": False,
                "data": {
                    "chunk_id": chunk_id,
                    "error": str(e)
                },
                "message": f"Error executing tool: {e}"
            }
            
    def refresh_memory(self) -> None:
        """
        Refresh the memory
        """
        pass


