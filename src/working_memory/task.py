"""
Task is a class that represents a task.

It is a child class of MemoryChunk.

A task is a single unit of work that the agent is working on.
"""

from working_memory.memoryChunk import MemoryChunk

class Task(MemoryChunk):
    def __init__(self, task_id: str):
        super().__init__(task_id)