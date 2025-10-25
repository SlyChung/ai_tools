"""
Specialized tools for working with the library database.
"""

import os, hashlib, json
from pathlib import Path

from sources.base_source import Source
from models import Registry, Element
from ai_tools.db_session import SessionLocal
from utilities.logger import Logger

database_logger = Logger("database")
error_logger = Logger("error")

def add_to_registry(source: Source):
    """
    Add a source to the registry.
    """
    # --- 1. Check if the source is already in the registry ---
    # --- 2. If not, add it to the registry ---

    database_logger.log_debug(f"db_library.add_to_registry: Adding {source.file_path.name} to the registry")

    entry = source.get_registry_entry()
    
    with SessionLocal() as session:
        doc = Registry(
            **entry,
        )
        session.add(doc)
        session.flush()
        session.commit()
    
    return

def add_to_elements(source: Source):
    """
    Add a source to the elements.
    """

    database_logger.log_debug(f"db_library.add_to_elements: Adding {source.file_path.name} elements")

    entry = source.get_elements_entry()

    with SessionLocal() as session:
        for e in entry:
            element = Element(
                **e,
            )
            session.add(element)
        session.commit()
    return

def add_to_pages(source: Source):
    """
    Add a source to the pages.
    """

    database_logger.log_debug(f"db_library.add_to_pages: Adding {source.file_path.name} pages")

    return

def add_to_chunks(source: Source):
    """
    Add a source to the chunks.
    """

    database_logger.log_debug(f"db_library.add_to_chunks: Adding {source.file_path.name} chunks")

    return

def add_to_embeddings(source: Source):
    """
    Add a source to the embeddings.
    """

    database_logger.log_debug(f"db_library.add_to_embeddings: Adding {source.file_path.name} embeddings")

    return
