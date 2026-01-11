"""
Task memory chunk representing a single unit of work.

A Task is a MemoryChunk subclass that represents a discrete piece of work
an agent is currently working on or has completed.
"""

from working_memory.memoryChunk import MemoryChunk


class Task(MemoryChunk):
    """A memory chunk representing a task or work item.

    Inherits from MemoryChunk and will provide task-specific
    functionality like status tracking, deadlines, and dependencies.

    Attributes:
        chunk_id: Inherited from MemoryChunk, serves as task_id.

    Note:
        This is a minimal implementation. Task-specific methods
        (load, save, envelope, execute_tool) not yet implemented.
    """

    def __init__(self, task_id: str):
        """Initialize a Task with a unique ID.

        Args:
            task_id: Unique identifier for this task.
        """
        super().__init__(task_id)