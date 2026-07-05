import importlib.metadata

from .exceptions import VarEngineError

# This explicitly tells the user that only these items are meant for the public. Prevents them from using importlib.metadata.version(...)
__all__ = ["__version__", "VarEngineError"]

try:
    # library that provides access to the metadata of an install distribution package
    __version__ = importlib.metadata.version("var-engine")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
