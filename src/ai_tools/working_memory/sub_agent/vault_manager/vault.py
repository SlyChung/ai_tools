"""
Vault is a class that represents a vault.

It is a child class of MemoryChunk.

A vault is a file structure that contains notes.
"""

from working_memory.memoryChunk import MemoryChunk

class Vault(MemoryChunk):
    def __init__(self, vault_id: str):
        super().__init__(vault_id)
        self.vault_data = {}