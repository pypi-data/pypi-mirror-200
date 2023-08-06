"""Classes representing data and command formats for dot
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, NamedTuple

import logging

logger = logging.getLogger(__name__)

from .const import (
    LuxaforCommand,
    LuxaforLED,
    LuxaforPattern,
    LuxaforWavePattern,
    LUXAFOR_DONT_CARE,
    PushEvent
)

@dataclass
class DotLED:
    red: int
    green: int
    blue: int

    @classmethod
    def __eq__(self, other) -> bool:
        return (
            self.red == other.red and
            self.green == other.green and
            self.blue == other.blue
        )

    @classmethod
    def set_rgb(
        self,
        color: tuple[int,int,int],
    ) -> None:
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]


class DotState:
    def __init__(self):
        self.last_command: LuxaforCommand | None = None
        self.last_event: PushEvent | None = None
        self.color: tuple[int,int,int] = [0,0,0]

    def set_led(
        self,
        color: tuple[int, int, int],
    ) -> None:
        self.color = color
        self.last_command = LuxaforCommand.COLOR
        self.last_event = None
        logger.debug("Color: %s   Command: %s    Event: %s", self.color, self.last_command, self.last_event)

