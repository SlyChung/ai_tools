"""
Decorators for managing tool metadata and versioning.

This module provides decorators that can be applied to functions and classes
to attach version information and other metadata.
"""

import re
from functools import wraps

_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def version(v: str):
    """Attach a semantic version string to a function or class.

    This decorator adds a `__version__` attribute to the decorated object,
    allowing version tracking at the function or class level.

    Args:
        v: Version string in MAJOR.MINOR.PATCH format (e.g., "1.0.0").

    Returns:
        A decorator that attaches the version to the target object.

    Raises:
        ValueError: If the version string doesn't match MAJOR.MINOR.PATCH format.

    Example:
        @version("1.0.0")
        def my_function():
            pass

        print(my_function.__version__)  # "1.0.0"
    """
    if not _SEMVER.match(v):
        raise ValueError(f"Invalid version '{v}'. Use MAJOR.MINOR.PATCH, e.g. 0.1.0")

    def decorator(obj):
        # For classes, just add the version attribute directly
        if isinstance(obj, type):
            obj.__version__ = v
            return obj
        # For functions, wrap and add version
        @wraps(obj)
        def wrapped(*args, **kwargs):
            return obj(*args, **kwargs)
        wrapped.__version__ = v
        return wrapped
    return decorator