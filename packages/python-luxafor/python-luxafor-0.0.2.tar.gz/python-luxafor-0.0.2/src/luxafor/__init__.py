"""Top level package for Python Luxafor Integration.

Provides unified discovery for BLE and USB devices.
"""

from .discovery import discover

__all__ = ("discover",)

__version__ = "0.0.2"
