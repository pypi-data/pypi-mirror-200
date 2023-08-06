"""Python Luxafor integration constants"""
from __future__ import annotations

from enum import IntEnum

class LuxaforDeviceType(IntEnum):
    """Device types for Luxafor"""
    FLAG = 0
    DONGLE = 1
    DOT = 2

class LuxaforConnectionMethod(IntEnum):
    """Connection methods for Luxafor"""
    USB = 0
    BLE = 1
