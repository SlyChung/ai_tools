from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")

class EmbeddingError(Exception):
    """
    Exception raised for errors in the embedding tool.
    """
    pass
