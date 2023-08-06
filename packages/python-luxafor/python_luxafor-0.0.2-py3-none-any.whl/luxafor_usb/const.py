"""Luxafor USB constants.

UUIDs and other constants for communicating with Luxafor USB devices.
"""
from __future__ import annotations

from enum import IntEnum

# Placeholder value to fill in blank values
LUXAFOR_DONT_CARE = 0x00

VENDOR_ID = 0x04D8
PRODUCT_ID = 0xF372


class LuxaforLED(IntEnum):
    """LEDs on the device."""

    FRONT1 = 1
    FRONT2 = 2
    FRONT3 = 3
    FRONT_ALL = 65
    BACK1 = 4
    BACK2 = 5
    BACK3 = 6
    BACK_ALL = 66
    ALL = 255


class LuxaforCommand(IntEnum):
    """Acceptable commands for the device."""

    COLOR = 0x01
    FADE = 0x02
    STROBE = 0x03
    WAVE = 0x04
    PATTERN = 0x06


class LuxaforWavePattern(IntEnum):
    """Available wave patterns for the device."""

    PATTERN_1 = 1
    PATTERN_2 = 2
    PATTERN_3 = 3
    PATTERN_4 = 4
    PATTERN_5 = 5


class LuxaforPattern(IntEnum):
    """Available patterns for the device."""

    PATTERN_POLICE = 5
    PATTERN_RAINBOW = 8
    PATTERN_STOPLIGHT = 1

    PATTERN_RANDOM1 = 2
    PATTERN_RANDOM2 = 3
    PATTERN_RANDOM3 = 4
    PATTERN_RANDOM4 = 6
    PATTERN_RANDOM5 = 7
