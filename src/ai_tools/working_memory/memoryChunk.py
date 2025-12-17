"""
MemoryChunk is a parent class that represents a chunk of memory.

It is a base class for all memory chunk objects.
"""

from typing import Dict, Any, Optional

from ai_tools.utilities.decorators import version
from utilities.logger import Logger

error_logger = Logger("error")

@version("1.0.0")
class MemoryChunk:
    def __init__(self, chunk_id: str):
        self.chunk_id = chunk_id

    def load(self) -> dict:
        """
        Get the chunk id
        """
        pass

    def save(self) -> None:
        """
        Save the chunk to the working memory
        """
        pass

    def envelope(self) -> Dict[str, Any]:
        """
        Get the chunk as a dictionary
        """
        pass

    def execute_tool(self, args: Dict[str, Any]) -> None:
        """
        Execute a tool on the chunk
        """
        pass


    # Finished, no need to override
    @version("1.0.0")
    def refresh(self) -> None:
        """
        Refresh the chunk
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