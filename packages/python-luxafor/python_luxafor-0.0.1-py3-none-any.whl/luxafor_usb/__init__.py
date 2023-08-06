"""Python Luxafor USB module"""

__all__ = ('discover','LuxaforFlag',)

__author__ = """Matt Lizzie"""
__email__ = 'matt@lizzie.pro'
__version__ = '0.0.1'

from luxafor_base import LuxaforDevice
from .flag import LuxaforFlag, discover_flags

async def discover() -> list[LuxaforDevice]:
    """Discover all available devices

    Returns:
        list[LuxaforDevice]: List of discovered devices
    """
    return await discover_flags()