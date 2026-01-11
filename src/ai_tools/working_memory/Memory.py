"""
Abstract base class for AI agent working memory.

This module defines the Memory class, which serves as the foundation for
managing an agent's working memory. Memory stores a collection of "chunks"
(notes, tasks, etc.) that form part of the agent's context.

The memory system is designed to:
- Store and manage memory chunks the agent is working on
- Provide a standardized interface for chunk operations
- Output memory state as dictionaries for system prompt injection

Subclasses should implement chunk-specific loading and management logic.
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
    """Abstract base class for agent working memory.

    Memory manages a collection of MemoryChunk objects, providing common
    operations for opening, closing, and interacting with chunks.

    Subclasses (WorkingMemory, etc.) extend this with domain-specific
    chunk types and loading logic.

    Attributes:
        id: Unique identifier for this memory instance.
        chunks: Dictionary mapping chunk IDs to MemoryChunk objects.
    """

    def __init__(self):
        """Initialize a new Memory instance with a unique ID."""
        self.id = str(uuid.uuid4())
        self.chunks = {}

    def load(self, self_id: str) -> None:
        """Load an existing memory from persistent storage.

        Args:
            self_id: The ID of the memory instance to load.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass

    def open_memory_chunk(self, chunk_name: str, chunk_type: str) -> None:
        """Open and add a new memory chunk.

        Args:
            chunk_name: Name/identifier for the chunk.
            chunk_type: Type of chunk to create.

        Note:
            Not yet implemented. Subclasses should override with
            chunk-type-specific logic.
        """
        pass

    @version("1.0.0")
    def close_memory_chunk(self, chunk_id: str) -> Dict[str, Any]:
        """Close and remove a memory chunk.

        Args:
            chunk_id: ID of the chunk to close.

        Returns:
            Dictionary with status, data, and message fields.
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

    @version("1.0.0")
    def envelope(self) -> Dict[str, Any]:
        """Get the entire memory state as a dictionary.

        Iterates through all chunks and collects their envelope representations
        for injection into an agent's system prompt.

        Returns:
            Dictionary mapping chunk IDs to their envelope dictionaries.
        """
        memory_envelope = {}
        for chunk in self.chunks:
            memory_envelope[chunk.id] = self.chunks[chunk].envelope()

        return memory_envelope

    @version("1.0.0")
    def execute_tool(self, chunk_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool operation on a specific chunk.

        Args:
            chunk_id: ID of the chunk to operate on.
            args: Dictionary of arguments to pass to the chunk's tool.

        Returns:
            Dictionary with status, data, and message from the tool execution.
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
        """Refresh all memory chunks from their sources.

        Reloads chunk data from persistent storage to ensure the
        in-memory state is current.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass


