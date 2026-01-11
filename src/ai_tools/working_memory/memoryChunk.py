"""
Base class for all memory chunk types.

A MemoryChunk represents a discrete unit of working memory that an agent
can load, save, and operate on. Examples include notes, tasks, and plans.

Subclasses (Task, NoteV3, etc.) implement chunk-specific behavior while
inheriting the common interface defined here.
"""

from typing import Dict, Any, Optional

from ai_tools.utilities.decorators import version
from utilities.logger import Logger

error_logger = Logger("error")


@version("1.0.0")
class MemoryChunk:
    """Base class for memory chunks in the working memory system.

    Provides a common interface for all chunk types. Subclasses must
    implement load(), save(), envelope(), and execute_tool() methods.

    Attributes:
        chunk_id: Unique identifier for this chunk.
    """

    def __init__(self, chunk_id: str):
        """Initialize a MemoryChunk with a unique ID.

        Args:
            chunk_id: Unique identifier for this chunk.
        """
        self.chunk_id = chunk_id

    def load(self) -> Dict[str, Any]:
        """Load the chunk data from persistent storage.

        Returns:
            Dictionary with status, data, and message fields.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass

    def save(self) -> Dict[str, Any]:
        """Save the chunk data to persistent storage.

        Returns:
            Dictionary with status, data, and message fields.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass

    def envelope(self) -> Dict[str, Any]:
        """Get the chunk state as a dictionary for agent viewing.

        Returns:
            Dictionary representation of the chunk's current state.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass

    def execute_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool operation on this chunk.

        Args:
            args: Dictionary containing 'tool' key and tool-specific arguments.

        Returns:
            Dictionary with status, data, and message fields.

        Note:
            Not yet implemented. Subclasses should override.
        """
        pass

    @version("1.0.0")
    def refresh(self) -> Dict[str, Any]:
        """Reload the chunk from its source.

        Calls load() to refresh the chunk data from persistent storage.

        Returns:
            Dictionary with status, data, and message fields.
        """
        try:
            self.load()
            return {
                "status": True,
                "data": {
                    "chunk_id": self.chunk_id
                },
                "message": "Chunk refreshed successfully"
            }
        except Exception as e:
            error_logger.log_error(f"MemoryChunk.refresh: Error refreshing chunk: {e}")
            return {
                "status": False,
                "data": {
                    "chunk_id": self.chunk_id,
                    "error": str(e)
                },
                "message": f"Error refreshing chunk: {e}"
            }