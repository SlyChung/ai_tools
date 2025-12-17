"""
This module is the structure for the note in the working memory.
It is a wrapper for the MemoryChunk class.
"""

from typing import Dict, Any

from ai_tools import file_management as fm

from ai_tools.working_memory.memoryChunk import MemoryChunk
from ai_tools.working_memory.element import Element
from ai_tools.utilities.logger import Logger


error_logger = Logger("error")
technical_logger = Logger("technical")

class Note(MemoryChunk):
    def __init__(self, note_id: str):
        super().__init__(note_id)
        self.note = Element(element_id=note_id) # Use a section object to store the note
        self.note_data = {}

    # -----
    # MemoryChunk methods
    # -----

    def load(self) -> str:
        """
        Load the note to the working memory from the file system

        Search a database for the note name and location
        Load the note from the file system
        Save the note location and name to the object instance
        Parse the note
        Return the status, parsed note, and message
        """

        try:
            # TODO: Add a database search for the note name and location
            self.note_data = { #fm.find_file(self.note_id)
                "note_id": self.note_id,
                "note_location": self.note_location,
                "note_name": self.note_name
            }

            if self.note_location and self.note_name:
                self.raw_file = fm.read_file(self.note_location, self.note_name)
                self.parse_note()
            else:
                raise FileNotFoundError(f"Note {self.note_id} not found")
            
            
        except Exception as e:
            error_logger.error(f"Note: Error loading note {self.note_id} to the working memory: {e}")
            return "Failed to load note"

    def save(self) -> None:
        """
        Save the note from the working memory to the file system

        Save the note to the file system
        Return the status, note id, and message
        """
        pass
    
    def delete(self) -> None:
        """
        Delete the note from the working memory and the file system

        Delete the note from the file system
        Return the status, note id, and message
        """
        pass
    
    def close(self) -> None:
        """
        Close the note from the working memory
        """
        pass

    def refresh(self) -> None:
        """
        Refresh the note from the system directory
        """
        pass
    
    def execute_tool(self, args: dict) -> None:
        """
        Execute a tool on the note
        """

        tool = args["tool"]
        args.pop("tool")

        element_id = args["element_id"]
        if element_id:
            args.pop("element_id")

        if tool == "edit_element":
            self.edit_element(element_id, args)
        elif tool == "insert_element":
            self.insert_element(element_id, args)
        elif tool == "delete_element":
            self.delete_element(element_id)
        else:
            raise NoteToolError(f"Tool {tool} not found in the note")

        pass
    
    # -----
    # Note methods
    # -----

    def build_note(self, note_id: str) -> str:
        """
        Build a note from the working memory
        """
        pass

    def get_note(self, note_id: str) -> str:
        """
        Get a note from the working memory
        """
        pass

    def parse_note(self) -> None:
        """
        Parse a note from the working memory

        Takes in a raw Markdown file and parses it into a section object
        Returns the section object

        Sections are divided by Markdown headers (e.g. #, ##, ###, etc.)
        The first section is the note title
        The remaining sections are the note content
        The note content is stored in the section object
        The note title is stored in the section object
        The note id is stored in the section object
        The note location is stored in the section object

        parsing must also take into account the note frontmatter (e.g. ---)
        """
        pass

    # -----
    # Element methods
    # -----

    def delete_element(self, section_id: str) -> None:
        """
        Delete a section from the note
        """
        pass

    def get_element(self, section_id: str) -> str:
        """
        Get a section from the note
        """
        pass

    def edit_element(self, element_id: str, args: dict) -> None:
        """
        Edit an element in the note
        """
        pass

    def insert_element(self, element_id: str, args: dict) -> None:
        """
        Insert an element into the note
        """
        pass

# ----- Error classes ----- #

class ElementNotFoundError(Exception):
    """
    Error raised when an element is not found in the note
    """
    pass

class NoteToolError(Exception):
    """
    Error raised when a tool is not found in the note
    """
    pass

    
class NoteToolArgumentError(Exception):
    """
    Error raised when a tool argument is not found in the note
    """
    pass

    
