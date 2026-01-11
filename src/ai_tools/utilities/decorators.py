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