"""Flag classes.

Objects and methods related to connecting to flags.
"""
from __future__ import annotations

import asyncio
import logging

import usb

from luxafor_base import LuxaforConnectionMethod, LuxaforDevice, LuxaforDeviceType

from .const import LUXAFOR_DONT_CARE, PRODUCT_ID, VENDOR_ID, LuxaforLED
from .data import FlagState

logger = logging.getLogger(__name__)


async def discover_flags(
    serial_number: str | list[str] | None = None,
) -> list[LuxaforFlag]:
    """Discover Flag devices.

    Args:
        serial_number (str | list[str] | None, optional): Serial number to
            look for. Defaults to None.

    Returns:
        list[LuxaforFlag]: Discovered flags.
    """
    logger.debug("Starting Flag discovery")
    try:
        iter(serial_number)  # type: ignore[arg-type]
    except TypeError:
        if serial_number is not None:
            serial_number = {serial_number}  # type: ignore[assignment]

    logger.debug("Serial Number parameter: %s", serial_number)

    devices = usb.core.find(
        find_all=True,
        idVendor=VENDOR_ID,
        idProduct=PRODUCT_ID,
    )

    flags: list[LuxaforFlag] = []
    for device in devices:
        flag = LuxaforFlag(device)
        await flag.get_serial_number()
        logger.debug("Found flag %s", flag.serial_number)
        if (serial_number is None) or (
            serial_number is not None
            and flag.serial_number in serial_number  # type: ignore[operator]
        ):
            flags.append(flag)
        else:
            logger.debug("Discarded flag %s", flag.serial_number)
    return flags


class LuxaforFlag(LuxaforDevice):  # pylint: disable=too-many-instance-attributes
    """Handle actual flag connection and updates."""

    def __init__(
        self,
        device: usb.core.Device,
    ) -> None:
        """Initialize connection manager.

        Args:
            device (str, optional): USB device to use. Defaults to None.
        """
        self.device = device
        self._operation_lock = asyncio.Lock()
        self.device_type = LuxaforDeviceType.FLAG
        self.connection_method = LuxaforConnectionMethod.USB
        self.serial_number = None
        self.firmware_version = None
        self.state = FlagState()
        self._is_setup = False

    async def _setup_device(self) -> None:
        """Initialize the device."""
        try:
            self.device.detach_kernel_driver(0)
        except Exception:  # pylint: disable=broad-exception-caught
            pass
        self.device.set_configuration()
        self._is_setup = True

        await self.get_serial_number()

    async def get_serial_number(self) -> str:
        """Populate the device's serial number and firmware version."""
        if self.serial_number is None or self.firmware_version is None:
            if not self._is_setup:
                await self._setup_device()
                return self.serial_number  # type: ignore[return-value]
            await self._write(bytearray([0x80, 0, 0, 0, 0, 0, 0, 0]))
            data = await self._read(8)
            while data[0] != 0x80:
                await self._write(bytearray([0x80, 0, 0, 0, 0, 0, 0, 0]))
                data = await self._read(8)
            self.serial_number = str((data[2] << 8) | data[3])
            self.firmware_version = data[1]  # type: ignore[assignment]
        return self.serial_number

    async def _write(
        self,
        data: bytearray,
    ) -> None:
        """Write the data to the device.

        Args:
            data (bytearray): Data to write.
        """
        if not self._is_setup:
            await self._setup_device()
        if self._operation_lock.locked():
            logger.debug("Operation in progress, waiting to write until it completes")
        async with self._operation_lock:
            self.device.write(1, data)
            logger.debug("Wrote to flag %s: %s", self.serial_number, data)

            # Borrowed experience indicates repeating the command helps to
            # handle an issue in the firmware.
            self.device.write(1, data)

    async def _read(
        self,
        bytecount: int,
    ) -> bytearray:
        """Read data from the device.

        Args:
            bytecount (int): Number of bytes to read.

        Returns:
            bytearray: Data from device.
        """
        if not self._is_setup:
            await self._setup_device()
        if self._operation_lock.locked():
            logger.debug("Operation in progress, waiting for it to complete")
        async with self._operation_lock:
            data = self.device.read(0x81, bytecount)
            logger.debug("Read data: %s", data)
            return data

    async def set_color(
        self,
        color: tuple[int, int, int],
    ) -> None:
        """Set the color of the LEDs.

        Args:
            color (tuple[int, int, int]): Color to set in Red, Green, Blue ints
        """
        logger.debug("Set color: %s", color)
        self.state.set_led(color)
        await self._write_state()

    def is_on(self) -> bool:
        """Get the status of the LEDs.

        Returns:
            bool: True if on
        """
        return self.state.color != (0, 0, 0)

    async def _write_state(self) -> None:
        """Write state values to the device."""
        command: list[int] = [0, 0, 0, 0, 0, 0, 0, 0]

        command[0] = self.state.last_command  # type: ignore[assignment]
        command[1] = LuxaforLED.FRONT_ALL  # type: ignore[assignment]
        command[2] = self.state.color[0]
        command[3] = self.state.color[1]
        command[4] = self.state.color[2]
        command[5] = LUXAFOR_DONT_CARE
        command[6] = LUXAFOR_DONT_CARE
        command[7] = LUXAFOR_DONT_CARE

        await self._write(bytearray(command))
