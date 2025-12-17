"""
This module is the structure for the subsection in the note object.
It is a wrapper for the MemoryChunk class.
"""

import uuid

class Section:
    def __init__(self, title: str, content: str = "", section_id: str = None):
        self.section_id = section_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.subsections: list["Section"] = []

    def add_subsection(self, subsection: "Section"):
        if not isinstance(subsection, Section):
            raise TypeError("subsection must be a Section object")
        self.subsections.append(subsection)

    def remove_subsection(self, section_id: str):
        """Remove a subsection by its ID, recursively."""
        for i, s in enumerate(self.subsections):
            if s.section_id == section_id:
                del self.subsections[i]
                return True
            if s.remove_subsection(section_id):
                return True
        return False

    def find(self, section_id: str):
        """Find a section by ID, recursively."""
        if self.section_id == section_id:
            return self
        for s in self.subsections:
            found = s.find(section_id)
            if found:
                return found
        return None

    def to_dict(self):
        """Convert section (and children) to dict form."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "content": self.content,
            "subsections": [s.to_dict() for s in self.subsections],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Rebuild section tree from dict."""
        section = cls(
            title=data["title"],
            content=data.get("content", ""),
            section_id=data.get("section_id"),
        )
        for sub in data.get("subsections", []):
            section.add_subsection(cls.from_dict(sub))
        return section

    def __repr__(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.title} ({self.section_id[:8]})\n"
        for s in self.subsections:
            result += s.__repr__(level + 1)
        return result

        