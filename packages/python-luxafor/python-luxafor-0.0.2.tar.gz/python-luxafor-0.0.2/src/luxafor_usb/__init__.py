"""Python Luxafor USB module.

Provides discovery of USB devices.
"""

__all__ = ("discover", "LuxaforFlag")


__version__ = "0.0.2"

from luxafor_base import LuxaforDevice

from .flag import LuxaforFlag, discover_flags


async def discover() -> list[LuxaforDevice]:
    """Discover all available devices.

    Returns:
        list[LuxaforDevice]: List of discovered devices.
    """
    return await discover_flags()  # type: ignore[return-value]
