"""
MemoryChunk for the Notepad

Used to store information, tasks, and as scap paper for the Agent.
"""

from ai_tools.working_memory.memoryChunk import MemoryChunk

class Notepad(MemoryChunk):
    def __init__(self, notepad_id: str):
        super().__init__(notepad_id)

    # ----- MemoryChunk Methods -----

    def load(self) -> None:
        """
        Load the notepad from the file system
        """
        pass
    
    def save(self) -> None:
        """
        Save the notepad to the file system
        """
        pass
    
    def delete(self) -> None:
        """
        Delete the notepad from the file system
        """
        pass

    def close(self) -> None:
        """
        Close the notepad
        """
        pass
    
    def refresh(self) -> None:
        """
        Refresh the notepad
        """
        pass
    
    def execute_tool(self, args: Dict[str, Any]) -> None:
        """
        Execute a tool on the notepad
        """
        pass

    def envelope(self) -> Dict[str, Any]:
        """
        Get the notepad as a dictionary
        """
        pass
    
    # ----- Notepad Methods -----

    # ----- Tools -----

    def add_note(self, note_id: str) -> None:
        """
        Add a note to the notepad
        """
        pass
    
    def delete_note(self, note_id: str) -> None:
        """
        Delete a note from the notepad
        """
        pass
    
    def edit_note(self, note_id: str) -> None:
        """
        Edit a note in the notepad
        """

    def toggle_note_status(self, note_id: str) -> None:
        """
        Toggle the status of a note in the notepad
        """
        pass