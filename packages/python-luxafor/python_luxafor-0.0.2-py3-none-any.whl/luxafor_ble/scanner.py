"""Scanner.

Scanning tools to find dots.
"""
from __future__ import annotations

import asyncio
import logging

from bleak import BleakScanner

from .const import IS_LINUX, LUXAFOR_BLUETOOTH_NAMES, DotCharacteristic

if False:  # pylint: disable=using-constant-test
    from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData

logger = logging.getLogger(__name__)


def build_scanner_kwargs(
    adapter: str | None = None,
) -> dict[str, Any]:
    """Build the Scanner configuration dictionary.

    Args:
        adapter (str | None, optional): Adapter to use. Defaults to None.

    Raises:
        ValueError: The adapter option is only valid for the Linux BlueZ Backend.

    Returns:
        dict[str, Any]: Scanner configuration
    """
    if adapter and IS_LINUX is not True:
        raise ValueError(
            "The adapter option is only valid for the Linux BlueZ Backend.",
        )
    return {"adapter": adapter} if adapter else {}


async def discover_dots(
    mac: str | None = None,
    adapter: str | None = None,  # pylint: disable=unused-argument
    wait: int = 5,
) -> list[BLEDevice]:
    """Discover Dots available via BLE.

    Args:
        mac (str | None, optional): MAC address to look for. Defaults to None.
        adapter (str | None, optional): Adapter to use. Defaults to None.
        wait (int, optional): Time in seconds to scan. Defaults to 5.

    Returns:
        list[BLEDevice]: Available devices.
    """
    scanner_kwargs = build_scanner_kwargs()
    async with BleakScanner(
        service_uuids=[str(DotCharacteristic.SERVICE)], **scanner_kwargs
    ) as scanner:
        await asyncio.sleep(wait)
        if mac:
            mac = mac.lower()
            return [d for d in scanner.discovered_devices if d.address.lower() == mac]
        return scanner.discovered_devices


def build_find_filter(
    mac: str | None = None,
) -> Callable:
    """Build filtering.

    Args:
        mac (str | None, optional): MAC address to look for. Defaults to None.

    Returns:
        Callable: Filter method.
    """
    known_names = [n.lower() for n in LUXAFOR_BLUETOOTH_NAMES]

    def dot_filter(
        device: BLEDevice,
        advertisement: AdvertisementData,  # pylint: disable=unused-argument
    ) -> bool:
        if mac is not None and device.address.lower() != mac:
            return False
        return device.name.lower()[:7] in known_names if device.name else False

    return dot_filter


async def find_dot(
    mac: str | None = None,
    adapter: str | None = None,
) -> BLEDevice | None:
    """Find a dot.

    Args:
        mac (str | None, optional): MAC address to look for. Defaults to None.
        adapter (str | None, optional): Adapter to use. Defaults to None.

    Returns:
        BLEDevice | None: BLE device that was found.
    """
    if mac is not None:
        mac = mac.lower()
    scanner_kwargs = build_scanner_kwargs(adapter)
    return await BleakScanner.find_device_by_filter(
        build_find_filter(mac),
        **scanner_kwargs,
    )
