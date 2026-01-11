"""
NoteV3 memory chunk for markdown note management.

NoteV3 is the current (MVP) implementation of a note memory chunk. It provides
basic read/write operations for markdown notes, with planned support for
tree-structured element manipulation.

Architecture:
    - Notes are stored as markdown files on disk
    - In-memory representation is raw markdown string (note_md)
    - Future: Tree structure for element-level operations

Tools available:
    - read_note: Return the note content
    - write_note: Update the note content
"""

from typing import Dict, Any

from ai_tools.working_memory.memoryChunk import MemoryChunk
from ai_tools.utilities.logger import Logger
from ai_tools.general_tools import file_management as fm
from ai_tools.utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")


class NoteV3(MemoryChunk):
    """Memory chunk for managing a single markdown note.

    Provides MVP functionality for loading, saving, and manipulating
    markdown notes. Future versions will support tree-structured
    element manipulation.

    Attributes:
        note_id: Unique identifier for this note (also chunk_id).
        note_md: Raw markdown content of the note.
        note_location: Tuple of (file_path, file_name) after loading.
        tools: Dictionary mapping tool names to methods.

    Available Tools:
        read_note: Returns the current note content.
        write_note: Updates the note content in memory.
    """

    def __init__(self, note_id: str):
        """Initialize a NoteV3 instance and load from disk.

        Args:
            note_id: Identifier for the note (used to find the file).
        """
        super().__init__(note_id)
        self.note_id = note_id
        # self.note = Element(element_id=note_id) # Use a section object to store the note
        self.note_md = ""
        self.tools = {
            "read_note": self.read_note,
            "write_note": self.write_note
        }
        self.load() # Load the note from the file system
        # self.note_tree = {}

    # ----- MemoryChunk Methods -----

    @version("1.0.0")
    def load(self) -> Dict[str, Any]:
        """Load the note from disk into memory.

        Finds the note file using find_file() and reads its content
        into the note_md attribute.

        Returns:
            Dictionary with status, data (note details), and message.
        """
        # Find the note in the file system given the note id
        try:
            self.note_location = fm.find_file(self.note_id) # find_file returns a list with file_path and file_name
        except Exception as e:
            error_logger.log_error(f"NoteV3.load: Error finding note: {e}")
            return {
                "status": False,
                "data": {
                    "note_id": self.note_id,
                    "error": str(e)
                },
                "message": f"Error finding note: {e}"
            }

        # Load the raw note from the file system into the class memory
        try:
            self.note_md = fm.read_file(self.note_location[0], self.note_location[1])
        except Exception as e:
            error_logger.log_error(f"NoteV3.load: Error reading note: {e}")
            return {
                "status": False,
                "data": {
                    "note_id": self.note_id,
                    "note_path": self.note_location[0],
                    "note_name": self.note_location[1],
                    "error": str(e)
                },
                "message": f"Error reading note: {e}"
            }

        # Parse the raw note into a tree structure in the class memory
        # try:
        #     self.note_tree = self.parse_note(raw_note) # TODO: this is a placeholder
        # except Exception as e:
        #     error_logger.log_error(f"NoteV3.load: Error parsing note: {e}")
        #     return False

        # Return Confirmation Payload
        return {
            "status": True,
            "data": {
                "note_id": self.note_id,
                "note_path": self.note_location[0],
                "note_name": self.note_location[1],
                "note_content": self.note_md,
            },
            "message": f"Note {self.note_id} loaded successfully"
        }
    
    @version("1.0.0")
    def save(self) -> Dict[str, Any]:
        """Save the note from memory to disk.

        Writes the current note_md content to the file at note_location.

        Returns:
            Dictionary with status, data (note details, file_size), and message.
        """

        # Save the note to the file system
        try:
            fm.write_file(self.note_location[0], self.note_location[1], self.note_md)
        except Exception as e:
            error_logger.log_error(f"NoteV3.save: Error saving note: {e}")
            return {
                "status": False,
                "data": {
                    "note_id": self.note_id,
                    "note_path": self.note_location[0],
                    "note_name": self.note_location[1],
                    "error": str(e)
                },
                "message": f"Error saving note: {e}"
            }
        return {
            "status": True,
            "data": {
                "note_id": self.note_id,
                "note_path": self.note_location[0],
                "note_name": self.note_location[1],
                "file_size": fm.file_size(self.note_location[0], self.note_location[1])
            },
            "message": f"Note {self.note_id} saved successfully"
        }


    @version("1.0.0")
    def execute_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool operation on this note.

        Args:
            args: Dictionary with 'tool' key specifying the tool name,
                plus any tool-specific arguments.

        Returns:
            Dictionary with status, data, and message from the tool.

        Available tools:
            read_note: No additional args required.
            write_note: Requires 'content' arg with new note text.
        """

        # Receive the tool and arguments as a dictionary

        try:
            # Pop the tool from the arguments dictionary and store it in a variable
            tool = args.pop("tool")

            # Check if the tool is valid
            if tool not in self.tools:
                return {
                    "status": False,
                    "data": {
                        "note_id": self.note_id,
                        "tool": tool,
                        "error": f"Tool {tool} not found"
                    },
                    "message": f"Tool {tool} not found"
                }
            elif tool == "read_note":
                # Check if the arguments are valid
                if args == {}:
                    # Execute the tool with the arguments
                    return self.read_note()
                else:
                    return {
                        "status": False,
                        "data": {
                            "note_id": self.note_id,
                            "error": "Invalid arguments provided"
                        },
                        "message": "Invalid arguments provided"
                    }
            elif tool == "write_note":
                # Check if the arguments are valid
                if "content" not in args:
                    return {
                        "status": False,
                        "data": {
                            "note_id": self.note_id,
                            "error": "Invalid arguments provided"
                        },
                        "message": "Invalid arguments provided"
                    }
                else:
                    # Execute the tool with the arguments
                    return self.write_note(args["content"])
            else:
                return {
                    "status": False,
                    "data": {
                        "note_id": self.note_id,
                        "tool": tool,
                        "error": f"Tool {tool} not found"
                    },
                    "message": f"Tool {tool} not found"
                }
        except Exception as e:
            error_logger.log_error(f"NoteV3.execute_tool: Error executing tool: {e}")
            return {
                "status": False,
                "data": {
                    "note_id": self.note_id,
                    "tool": tool,
                    "error": str(e)
                },
                "message": f"Error executing tool: {e}"
            }

    # MVP Version
    @version("1.0.0")
    def envelope(self) -> Dict[str, Any]:
        """
        Get the note as a dictionary
        """

        return {
            "note_id": self.note_id,
            "note_content": self.note_md
        }

    # ----- Note Methods -----

    @version("1.0.0")
    def build_note(self, args: Dict[str, Any]) -> None:
        """
        Build the note
        """

        # Build the note in Markdown format from the tree structure

        # Return Confirmation

        return True

    @version("1.0.0")
    def parse_note(self, args: Dict[str, Any]) -> None:
        """
        Parse the note
        """

        # Pull the raw note in Markdown format from class memory

        # Parse the note into a tree structure

        # Return Confirmation

        return True

    # ----- Tools -----

    @version("1.0.0")
    def add_element(self, args: Dict[str, Any]) -> None:
        """
        Add an element to the note
        """

        # Receive the element and arguments

        # Check if the element is valid

        # Check if the arguments are valid

        # Add the element to the note
    
    @version("1.0.0")
    def edit_element(self, args: Dict[str, Any]) -> None:
        """
        Edit an element in the note
        """

        # Receive the element and arguments

        # Check if the element is valid

        # Check if the arguments are valid

        # Edit the element in the note

        # Return Confirmation

        return True
    
    @version("1.0.0")
    def delete_element(self, args: Dict[str, Any]) -> None:
        """
        Delete an element from the note
        """

        # Receive the element id

        # Check if the element is valid

        # Delete the element from the note

        # Return Confirmation

        return True
    
    #----- MVP Tools -----

    @version("1.0.0")
    def read_note(self) -> Dict[str, Any]:
        """Return the current note content from memory.

        Returns:
            Dictionary with status=True, data containing note_id and
            note_content, and success message.
        """

        # Return the note in Markdown format from the class memory
        return {
            "status": True,
            "data": {
                "note_id": self.note_id,
                "note_content": self.note_md
            },
            "message": f"Note {self.note_id} read successfully"
        }
        
    
    @version("1.0.0")
    def write_note(self, note_content: str) -> Dict[str, Any]:
        """Update the note content in memory.

        Note: This updates the in-memory content only. Call save()
        to persist changes to disk.

        Args:
            note_content: New markdown content for the note.

        Returns:
            Dictionary with status=True, data containing note_id and
            updated note_content, and success message.
        """
        
        # Write the note in Markdown format to the class memory
        self.note_md = note_content

        # Return Confirmation
        return {
            "status": True,
            "data": {
                "note_id": self.note_id,
                "note_content": self.note_md
            },
            "message": f"Note {self.note_id} written successfully"
        }

    # ----- Error Classes -----

    @version("1.0.0")
    class ElementNotFoundError(Exception):
        """
        Error raised when an element is not found in the note
        """
        pass
    
    @version("1.0.0")
    class NoteToolError(Exception):
        """
        Error raised when a tool is not found in the note
        """
        pass
    
    @version("1.0.0")
    class NoteToolArgumentError(Exception):
        """
        Error raised when a tool argument is not found in the note
        """
        pass
    