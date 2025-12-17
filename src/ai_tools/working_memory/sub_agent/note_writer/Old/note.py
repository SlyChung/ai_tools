from dataclasses import dataclass, replace
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
import yaml

import ai_tools.file_management as fm
from utilities.logger import Logger

"""
Note class
"""

error_logger = Logger("error")
technical_logger = Logger("technical")

class Section:
    """
    Section class
    """
    def __init__(self, 
                 title: str, 
                 content: str, 
                 children: Optional[List["Section"]] = None, 
                 parent: Optional["Section"] = None, 
                 note: Optional["Note"] = None, 
                 section_id: int = None):
        
        self.section_id = section_id
        self.title = title
        self.content = content
        self.children = children
        self.parent = parent
        self.note = note

    def add_child(self, child: "Section") -> None:
        """
        Add a child section to the current section
        """
        if self.children is None:
            self.children = []
        self.children.append(child)

    def read_content(self) -> str:
        """
        Read the content from the section
        """
        return self.content
    
    def write_content(self, content: str) -> None:
        """
        Write the content to the section
        """
        self.content = content

    def envelope(self) -> Dict[str, Any]:
        """
        Get the section as a dictionary
        """
        return {
            "section_id": self.section_id,
            "title": self.title if self.title else None,
            "content": self.content if self.content else None,
            "children": [child.envelope() for child in self.children] if self.children else None,
            "parent": self.parent.envelope() if self.parent else None,
            "note": self.note.envelope() if self.note else None,
            "section_id": self.section_id if self.section_id else None,
        }
    def get_section_id(self) -> int:
        """
        Get the section id
        """
        return self.section_id

class Note:
    """
    Note class
    """

    # TODO: Add handling for new note creation
    def __init__(self, file_name: str, file_path: str, vault: str):
        self.file_name = file_name
        self.file_path = file_path
        self.vault = vault
        self.raw_content = fm.read_file(file_path, file_name)
        self.sections = []
        self.section_tree = self.build_section_tree()

    def read_metadata(self) -> None:
        """
        Read the metadata from the note frontmatter
        """

        FRONTMATTER_RE = re.compile(
            r'^\ufeff?---\s*\n(.*?)\n---\s*\n?',  # BOM-safe
            re.DOTALL | re.MULTILINE
        )

        m = FRONTMATTER_RE.match(self.raw_content)
        if m:
            raw_metadata = m.group(1)
            self.body = self.raw_content[m.end():]
        
        if not raw_metadata is None:
            self.metadata = yaml.safe_load(raw_metadata) or {}
    
    def write_metadata(self, metadata: dict) -> None:
        """
        Write the metadata to the note content
        """
        self.metadata = yaml.dump(metadata)

    def get_metadata(self) -> dict:
        """
        Get the metadata from the note
        """
        return self.metadata
    
    def parse_sections(self) -> List["Section"]:
        """
        Parse the sections from the note content
        """
        pass

    # TODO: Add handling for new section creation, and tracking of section ids
    # TODO: Add handling for new section creation, and tracking of section ids
    def add_section(self, title: str, content: str, parent_id: int = None) -> None:
        """
        Add a section to the note
        """
        if parent_id:
            parent = self.get_section(parent_id)
            if parent:
                parent.add_child(Section(
                    title=title,
                    content=content,
                    section_id=self.create_section_id(),
                    parent=parent
                ))
        else:
            self.sections.append(Section(
                title=title,
                content=content,
                section_id=self.create_section_id()
            ))

    # Bro IDK on this one
    def delete_section(self, section_id: str) -> bool:
        """
        Delete a section by id
        """
        for section in self.sections:
            if section.section_id == section_id:
                parent = getattr(section, "parent", None)
                if parent is None:
                    # Nothing to detach from
                    return False
                try:
                    parent.children.remove(section)
                except ValueError:
                    # Child list didn't contain it; tree is inconsistent
                    return False
                # Break the back-reference to keep the tree consistent
                section.parent = None
                # Optional: also remove from the registry if that's the intent
                self.sections.remove(section)
                return True
        return False  # not found

    def write_section(self, section_id: int, content: str) -> None:
        """
        Write the content to a section by id
        """
        self.sections[section_id].write_content(content)
        
    def get_section(self, section_id: int) -> Dict[str, Any]:
        """
        Get a section by id as a dictionary
        """
        for section in self.sections:
            if section.section_id == section_id:
                return section.envelope()
        return None