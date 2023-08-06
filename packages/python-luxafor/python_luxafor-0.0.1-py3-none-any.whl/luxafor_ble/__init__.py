"""Python Luxafor BLE module"""

__all__ = ('LuxaforDot','discover',)

__author__ = """Matt Lizzie"""
__email__ = 'matt@lizzie.pro'
__version__ = '0.0.1'

from luxafor_base import LuxaforDevice
from .scanner import discover_dots
from .dot import LuxaforDot

async def discover() -> list[LuxaforDevice]:
    """Discover all available devices

    Returns:
        list[LuxaforDevice]: List of discovered devices
    """
    return await discover_dots()

