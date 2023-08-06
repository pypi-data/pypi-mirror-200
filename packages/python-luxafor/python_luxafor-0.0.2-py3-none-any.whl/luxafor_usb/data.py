"""Luxafor USB data.

Classes representing data and command formats for flag.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from .const import LuxaforCommand

logger = logging.getLogger(__name__)


@dataclass
class FlagState:
    """Represents a dot device's state."""

    last_command: LuxaforCommand | None
    """Last command sent to the device."""

    color: tuple[int, int, int]
    """Last color set on the device."""

    def __init__(self):  # type: ignore[annotation-unchecked]
        """Create a new FlagState entity."""
        self.last_command = None
        self.color = (0, 0, 0)

    def set_led(
        self,
        color: tuple[int, int, int],
    ) -> None:
        """Set the color of the LEDs.

        Args:
            color (tuple[int, int, int]): Color to set in Red, Green, Blue ints
        """
        self.color = color
        self.last_command = LuxaforCommand.COLOR
        logger.debug(
            "Color: %s   Command: %s",
            self.color,
            self.last_command,
        )
