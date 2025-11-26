"""
This module is a wrapper for the note module.
It provides a higher level interface for the note module.

Needs:
- [ ] Context support for use with LLMs
"""

from working_memory.note import Note
from utilities.logger import Logger

def load_note(note_id: str) -> dict:
    """
    Load a note from a file
    """
    note = Note(find_note(note_id))
    return note.envelope()

def save_note(note_id: str) -> None:
    """
    Save a note to a file
    """

    note = find_note(note_dict["note_id"])

    pass

def find_note(note_id: str) -> dict:
    """
    Find a note by id in the database
    returns note file path and name
    """
    pass

def create_note(file_path: str, file_name: str) -> dict:
    """
    Create a new note

    """
    pass

def delete_note(note: dict) -> None:
    """
    Delete a note
    """
    pass

def add_section(note: dict, title: str, content: str, parent_id: int = None) -> None:
    """
    Add a section to a note
    """
    pass

def delete_section(note: dict, section_id: int) -> None:
    """
    Delete a section from a note
    """
    pass

def