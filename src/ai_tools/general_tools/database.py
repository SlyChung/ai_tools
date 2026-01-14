"""
Database tools for AI agents.

Provides utilities for database operations including connections,
queries, and data management.
"""

from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")
database_logger = Logger("database")


class DatabaseError(Exception):
    """
    Exception raised for errors in the embedding tool.
    """
    pass
