"""Objects and methods related to connection to the dot"""
from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from enum import Enum
from time import time
from typing import Any, Callable, Literal

from bleak import BleakClient, BleakError
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from luxafor_base import *

from .const import (
    LuxaforCommand,
    LuxaforLED,
    PushEvent,
    DotCharacteristic,
    IS_LINUX,
    LUXAFOR_DONT_CARE,
)
from .data import DotState

logger = logging.getLogger(__name__)

DISCONNECT_DELAY = 120

class LuxaforDot(LuxaforDevice):
    """Handle actual dot connection and update states."""

    def __init__(
        self,
        ble_device: BLEDevice,
        include_extra: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize connection manager

        Args:
            ble_device (BLEDevice): _description_
            include_extra (bool, optional): _description_. Defaults to False.
        """

        self.device = ble_device
        self.serial_number = ble_device.address
        self._connect_lock = asyncio.Lock()
        self._operation_lock = asyncio.Lock()
        self._expected_disconnect = False
        self._latest_events: dict[int,float] = {}
        self._callbacks: dict[Callable[[DotState], None], Callable[[], None]] = {}
        self._client: BleakClient = None # type: ignore[assignment]
        self._client_kwargs: dict[str,str] = {}
        self.state = DotState()
        self.device_type = LuxaforDeviceType.DOT
        self.connection_method = LuxaforConnectionMethod.BLE

        logger.debug("New dot connection initialized")
        self.set_client_options(**kwargs)

    def set_device(
        self,
        ble_device: BLEDevice
    ) -> None:
        """
        Change BLE device

        Args:
            ble_device (BLEDevice): New BLEDevice to use
        """

        logger.debug("Set new device from %s to %s", self.device, ble_device)
        self.device = ble_device

    async def _ensure_connection(self) -> None:
        """
        Connect to Dot
        """

        if self._connect_lock.locked():
            logger.debug("Connection to %s already in progress. Waiting first", self.device.name)

        if self._client is not None and self._client.is_connected:
            return
        
        async with self._connect_lock:
            if self._client is not None and self._client.is_connected:
                return
            try:
                logger.debug("Establishing new connection to dot (ID: %s) to %s", id(self), self.device)
                client = await establish_connection(
                    client_class=BleakClient,
                    device=self.device,
                    name=f'{self.device.name} ({self.device.address})',
                    use_services_cache=True,
                    disconnected_callback=self._disconnect_callback, # type: ignore
                    ble_device_callback=lambda: self.device,
                )
                self._expected_disconnect = False
            except (asyncio.TimeoutError, BleakError) as error:
                logger.error ("%s: Failed to connect to the dot: %s", self.device, error)
                raise error

            try:
                await client.pair()
            except (BleakError, EOFError):
                pass
            except NotImplementedError:
                logger.warning('Pairing not implmented.')

            self._client = client
            await self.subscribe()
    async def _read(
        self,
        characteristic: DotCharacteristic,
    ) -> bytearray:
        """
        Helper to read characteristics

        Args:
            characteristic (DotCharacteristic): _description_

        Returns:
            bytearray: _description_
        """

        if self._operation_lock.locked():
            logger.debug("Operation already in progress, wiating for it to complete")
        async with self._operation_lock:
            data = await self._client.read_gatt_char(characteristic.uuid)
            logger.debug("Read attribute %s with value %s", characteristic, data)
            return data
    
    async def _write(
        self,
        characteristic: DotCharacteristic,
        data: bytearray,
    ) -> None:
        """_summary_

        Args:
            characteristic (DotCharacteristic): _description_
            data (bytearray): _description_
        """
        if self._operation_lock.locked():
            logger.debug("Operation in progress. Waiting for it to complete")
        async with self._operation_lock:
            await self._ensure_connection()
            try:
                await self._client.write_gatt_char(characteristic.uuid, data)
                logger.debug("Wrote '%s' to attribute '%s'", data, characteristic)
            except BleakError as error:
                logger.error("Failed to write '%s' to attribute '%s': %s", data, characteristic, error)
                raise
        
    async def disconnect(
        self,
        expected: bool = True
    ) -> None:
        """
        serw

        Args:
            expected (bool, optional): _description_. Defaults to true.
        """
        logger.debug("%s disconnect called" "Expected" if expected else "Unexpected")
        self._expected_disconnect = expected
        if self._client and self._client.is_connected:
            async with self._connect_lock:
                await self.unsubscribe()
                await self._client.disconnect()
            self._client = None
            self._expected_disconnect = False

    def _disconnect_callback(
        self,
        client: BleakClient
    ) -> None:
        """_summary_

        Args:
            client (BleakClient): _description_
        """
        if self._expected_disconnect:
            logger.debug("Disconnect callback called")
        else:
            logger.warning("Unexpectedly disconnected")

    def _fire_callbacks(self) -> None:
        """
        _summary_
        """
        logger.debug("Firing callbacks: %s", self._callbacks)
        for callback in self._callbacks:
            callback(self.data)

    def register_callback(
        self,
        callback: Callable[[DotState], None]
    ) -> Callable[[], None]:
        """_summary_

        Args:
            callback (Callable[[DotData], None]): _description_

        Returns:
            Callable[[], None]: _description_
        """
        if existing_unregister_callback := self._callbacks.get(callback):
            logger.debug("Callback %s already registered", callback)
            return existing_unregister_callback
        
        def unregister_callback() -> None:
            """_summary_
            """
            if callback in self._callbacks:
                del self._callbacks[callback]
            logger.debug("Unregistered callback %s", callback)
        
        self._callbacks[callback] = unregister_callback
        logger.debug("Registered callback %s", callback)
        return unregister_callback
        
    async def _notify_callback(
        self,
        characteristic: BleakGATTCharacteristic,
        data: bytearray
    ) -> None:
        """_summary_

        Args:
            characteristic (BleakGATTCharacteristic): _description_
            data (bytearray): _description_
        """
        event_id = data[0]
        now = time()
        if (last_time := self._latest_events.get(event_id)) and now - last_time < 5:
            return
        self._latest_events[event_id] = now

        logger.debug(f"Push event revceived from Dot ({event_id}) - Data: {' '.join(f'{i:02x}' for i in data)}")

        self.state.last_event = event_id
        await self._write_state()

    async def unsubscribe(self) -> None:
        """Unsubscribe from characteristic updates
        """
        logger.debug("Unsubscribe called")
        if not self._client:
            return
        with contextlib.suppress(BleakError):
            await self._client.stop_notify(DotCharacteristic.STATUS.uuid)

    async def subscribe(self) -> None:
        """Subscribe for characteristic updates
        """
        logger.info("Subscribing to updates")
        try:
            await self._client.start_notify(DotCharacteristic.STATUS.uuid, self._notify_callback)
        except Exception as e:
            logger.warning("Failed to subscribe to characteristic: %s", e)

    def set_client_options(
        self,
        **kwargs: str,
    ) -> None:
        """Update options to allow overrides
        """
        if kwargs.get("adapter") and IS_LINUX is False:
            raise ValueError("Adapter option only supported by Linux BlueZ backend.")
        self._client_kwargs = {**kwargs}

    @contextlib.asynccontextmanager
    async def connection(
        self,
        **kwargs: str,
    ) -> AsyncIterator[LuxaforDot]:
        """_summary_

        Returns:
            AsyncIterator[LuxaforDot]: _description_
        """
        self.set_client_options(**kwargs)
        await self._ensure_connection()
        yield self
        await self.disconnect()

    async def set_color(
        self,
        color: tuple[int,int,int]
    ) -> None:
        logger.debug("Set Color: %s", color)
        self.state.set_led(color)
        await self._write_state()

    def is_on(self) -> bool:
        return self.state.color != [0,0,0]

    async def _write_state(self) -> None:
        """Convert the state values into an obj and write them
        """
        command: list[int] = [0,0,0,0,0,0,0,0]

        if self.state.last_event == PushEvent.OKAY:
            return
        elif self.state.last_event == PushEvent.HELLO:
            #The light is idle, we should repeat the last static color
            command[0] = LuxaforCommand.COLOR
            command[1] = LuxaforLED.ALL
            command[2] = self.state.color[0]
            command[3] = self.state.color[1]
            command[4] = self.state.color[2]
            command[5] = LUXAFOR_DONT_CARE
            command[6] = LUXAFOR_DONT_CARE
            command[7] = LUXAFOR_DONT_CARE
        else:
            #The command wasn't accepted, we should retry the original command
            command[0] = self.state.last_command
            command[1] = LuxaforLED.ALL
            command[2] = self.state.color[0]
            command[3] = self.state.color[1]
            command[4] = self.state.color[2]
            command[5] = LUXAFOR_DONT_CARE
            command[6] = LUXAFOR_DONT_CARE
            command[7] = LUXAFOR_DONT_CARE

        await self._write(DotCharacteristic.LED_COMMAND, bytearray(command))


