"""
MemoryChunk is a parent class that represents a chunk of memory.

It is a base class for all memory chunk objects.
"""

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

    def delete(self) -> None:
        """
        Delete the chunk from the working memory
        """
        pass

    def close(self) -> None:
        """
        Close the chunk
        """
        pass

    def envelope(self) -> Dict[str, Any]:
        """
        Get the chunk as a dictionary
        """
        pass
        