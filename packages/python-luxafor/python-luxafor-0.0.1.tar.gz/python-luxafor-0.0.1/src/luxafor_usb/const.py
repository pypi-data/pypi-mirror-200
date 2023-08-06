"""UUIDs and other constants for communicating with Luxafor USB devices"""
from __future__ import annotations

import platform
import re
from enum import Enum, IntEnum
from functools import cached_property
from typing import Literal
from uuid import UUID

#Placeholder value to fill in blank values
LUXAFOR_DONT_CARE = 0x00

VENDOR_ID = 0x04d8
PRODUCT_ID = 0xf372

class LuxaforLED(IntEnum):
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
    COLOR = 0x01
    FADE = 0x02
    STROBE = 0x03
    WAVE = 0x04
    PATTERN = 0x06


class LuxaforWavePattern(IntEnum):
    PATTERN_1 = 1
    PATTERN_2 = 2
    PATTERN_3 = 3
    PATTERN_4 = 4
    PATTERN_5 = 5

class LuxaforPattern(IntEnum):
    PATTERN_POLICE = 5
    PATTERN_RAINBOW = 8
    PATTERN_STOPLIGHT = 1

    PATTERN_RANDOM1 = 2
    PATTERN_RANDOM2 = 3
    PATTERN_RANDOM3 = 4
    PATTERN_RANDOM4 = 6
    PATTERN_RANDOM5 = 7