"""Luxafor Device Discovery"""
from __future__ import annotations

from luxafor_base.model import LuxaforDevice, LuxaforConnectionMethod

import luxafor_usb
import luxafor_ble

async def discover(
    scan_type: list[LuxaforConnectionMethod]|LuxaforConnectionMethod|None = None
) -> list[LuxaforDevice]:
    """Discover all devices connected"""
    if scan_type is None:
        scan_type = [LuxaforConnectionMethod.USB, LuxaforConnectionMethod.BLE]

    devices: list[LuxaforDevice] = []

    try:
        iter(scan_type)
    except TypeError:
        if scan_type == LuxaforConnectionMethod.BLE:
            devices.extend(await luxafor_ble.discover())
        elif scan_type == LuxaforConnectionMethod.USB:
            devices.extend(await luxafor_usb.discover())
        else:
            raise ValueError("Invalid scan type")
    else: 
        for method in scan_type:
            devices.extend(await discover(method))

    return devices
