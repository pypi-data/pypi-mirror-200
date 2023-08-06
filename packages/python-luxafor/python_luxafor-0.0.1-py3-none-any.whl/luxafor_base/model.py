"""Model files for Luxafor"""
from __future__ import annotations

from abc import ABC, abstractclassmethod

from .const import LuxaforDeviceType, LuxaforConnectionMethod

class LuxaforDevice(ABC):
    """Base class for all Luxafor devices."""

    serial_number: str 
    """
    The serial number of the device.

    USB devices will list serial number from the HID API
    BLE devices will list their Bluetooth address (MAC or UUID based on backend)
    """

    connection_method: LuxaforConnectionMethod
    """The connection method."""

    device_type: LuxaforDeviceType
    """The device type."""

    serial_number: str
    """Serial number of the device"""

    firmware_version: str
    """Firmware version of the device"""

    @abstractclassmethod
    async def set_color(
        self,
        color: tuple[int, int, int],
    ) -> None:
        """Set the color of all LEDs on the device."""
        pass

    @abstractclassmethod
    def is_on(self) -> bool:
        """Utility method to check if the device is on"""
        pass

    def is_off(self) -> bool:
        """Utility method to check if the device is off"""
        return not self.is_on()

    async def off(self) -> None:
        """Utility method to turn off LEDs"""
        await self.set_color([0,0,0])

    async def on(self) -> None:
        """Utility method to turn on LEDs"""
        await self.set_color([255,255,255])

    async def set_red(self) -> None:
        """Utility method to set LEDs red"""
        await self.set_color([255, 0, 0])

    async def set_green(self) -> None:
        """Utility method to set LEDs green"""
        await self.set_color([0,255,0])

    async def set_blue(self) -> None:
        """Utility method to set LEDs blue"""
        await self.set_color([0,0,255])

    async def set_yellow(self) -> None:
        """Utility method to set LEDs yellow"""
        await self.set_color([255,255,0])

    async def set_purple(self) -> None:
        """Utility method to set LEDs purple"""
        await self.set_color([255,0,255])