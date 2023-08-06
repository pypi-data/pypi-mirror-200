"""Luxafor Python base classes.

Provides generic classes and constants used by both BLE and USB devices.
"""
from __future__ import annotations

from .const import LuxaforConnectionMethod, LuxaforDeviceType
from .model import LuxaforDevice

__all__ = ("LuxaforDevice", "LuxaforDeviceType", "LuxaforConnectionMethod")


__version__ = "0.0.2"
