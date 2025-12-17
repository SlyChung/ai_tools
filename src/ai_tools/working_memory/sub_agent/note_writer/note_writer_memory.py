"""
NoteWriterMemory is a class that manages the note writer memory of the sub-agent.


"""
from typing import Dict, Any

from ai_tools.working_memory.sub_agent.workingMemory import WorkingMemory
from note_v3 import NoteV3

class NoteWriterMemory(WorkingMemory):
    def __init__(self):
        super().__init__()
        

    # ----- NoteWriterMemory Methods -----

    def load_note(self, note_id: str) -> None:
        """
        Load the note from the file system
        """
        self.chunks[note_id] = NoteV3(note_id)

    def save_note(self, note_id: str) -> None:
        """
        Save the note to the file system
        """
        self.chunks[note_id].save()

    def close_note(self, note_id: str) -> None:
        """
        Close the note
        """
        self.close_memory_chunk(note_id)


    # ----- Important Methods -----

    def envelope(self) -> Dict[str, Any]:
        """
        Get the note writer memory as a dictionary
        """
        return super().envelope()
    
    def finish_payload(self) -> Dict[str, Any]:
        """
        Get the note writer memory as a dictionary
        """
        pass
    
    # ----- Interactive Methods -----
    
    def execute_tool(self, chunk_id: str, args: Dict[str, Any]) -> None:
        """
        Execute a tool on a chunk
        """
        return super().execute_tool(chunk_id, args)
    