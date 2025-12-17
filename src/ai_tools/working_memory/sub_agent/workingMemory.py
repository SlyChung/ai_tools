"""
TaskMemory is a class that manages the task memory of the sub-agent..

Contracted Fields:
- plan_id: str


"""

from typing import Dict, Any, Optional
import uuid

from ai_tools.working_memory.Memory import Memory

class WorkingMemory(Memory):
    def __init__(self):
        super().__init__()

    
    # ----- MemoryChunk Methods -----
    """
    For each chunk type, we need to implement the following methods:
    - load_chunk
    - save_chunk
    - delete_chunk
    - close_chunk
    - refresh_chunk


    """
    
    # ----- Important Methods -----
    def envelope(self) -> Dict[str, Any]:
        """
        Get the task memory as a dictionary
        """
        return super().envelope()
    
    # ----- Interactive Methods -----
    def execute_tool(self, chunk_id: str, args: Dict[str, Any]) -> None:
        """
        Execute a tool on a chunk
        """
        super().execute_tool(chunk_id, args)
    