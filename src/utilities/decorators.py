"""
This module contains small functions to manage tools.
"""

import re
from functools import wraps

_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

def version(v: str):
    # Optional: enforce simple SemVer like "0.1.0"
    if not _SEMVER.match(v):
        raise ValueError(f"Invalid version '{v}'. Use MAJOR.MINOR.PATCH, e.g. 0.1.0")

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        wrapped.__version__ = v
        return wrapped
    return decorator