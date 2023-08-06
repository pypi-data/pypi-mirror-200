"""Luxafor Device Discovery.

Provides unified discovery method for BLE and USB devices.
"""
from __future__ import annotations

import luxafor_ble
import luxafor_usb
from luxafor_base.model import LuxaforConnectionMethod, LuxaforDevice


async def discover(
    scan_type: list[LuxaforConnectionMethod] | LuxaforConnectionMethod | None = None,
) -> list[LuxaforDevice]:
    """Discover all devices connected."""
    if scan_type is None:
        scan_type = [LuxaforConnectionMethod.USB, LuxaforConnectionMethod.BLE]

    devices: list[LuxaforDevice] = []

    try:
        iter(scan_type)  # type: ignore[arg-type]
    except TypeError:
        if scan_type == LuxaforConnectionMethod.BLE:
            devices.extend(await luxafor_ble.discover())
        elif scan_type == LuxaforConnectionMethod.USB:
            devices.extend(await luxafor_usb.discover())
        else:
            raise ValueError("Invalid scan type")  # pylint: disable=raise-missing-from
    else:
        for method in scan_type:  # type: ignore[union-attr]
            devices.extend(await discover(method))

    return devices
