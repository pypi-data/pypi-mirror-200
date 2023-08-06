"""Python Luxafor BLE module.

Contains methods for discovering devices.
"""

__all__ = ("LuxaforDot", "discover")

__version__ = "0.0.2"

from luxafor_base import LuxaforDevice

from .dot import LuxaforDot
from .scanner import discover_dots


async def discover() -> list[LuxaforDevice]:
    """Discover all available devices.

    Returns:
        list[LuxaforDevice]: List of discovered devices
    """
    return await discover_dots()
