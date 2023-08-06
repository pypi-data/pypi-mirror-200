"""Model files for Luxafor.

Provides a basic class to define shared characteristics of both BLE and USB
devices.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .const import LuxaforConnectionMethod, LuxaforDeviceType


class LuxaforDevice(ABC):
    """Base class for all Luxafor devices."""

    serial_number: str | None
    """
    The serial number of the device.

    USB devices will list serial number from the HID API
    BLE devices will list their Bluetooth address (MAC or UUID based on backend)
    """

    connection_method: LuxaforConnectionMethod | None
    """The connection method."""

    device_type: LuxaforDeviceType | None
    """The device type."""

    firmware_version: str | None
    """Firmware version of the device"""

    @abstractmethod
    async def set_color(
        self,
        color: tuple[int, int, int],
    ) -> None:
        """Set the color of the LEDs.

        Args:
            color (tuple[int, int, int]): Color to set in Red, Green, Blue ints
        """

    @abstractmethod
    def is_on(self) -> bool:
        """Get the status of the LEDs.

        Returns:
            bool: True if on
        """

    async def turn_off(self) -> None:
        """Turn off LEDs."""
        await self.set_color((0, 0, 0))

    async def turn_on(self) -> None:
        """Turn on LEDs."""
        await self.set_color((255, 255, 255))

    async def set_red(self) -> None:
        """Set LEDs red."""
        await self.set_color((255, 0, 0))

    async def set_green(self) -> None:
        """Set LEDs green."""
        await self.set_color((0, 255, 0))

    async def set_blue(self) -> None:
        """Set LEDs blue."""
        await self.set_color((0, 0, 255))

    async def set_yellow(self) -> None:
        """Set LEDs yellow."""
        await self.set_color((255, 255, 0))

    async def set_purple(self) -> None:
        """Set LEDs purple."""
        await self.set_color((255, 0, 255))
