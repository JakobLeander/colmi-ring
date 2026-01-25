# =============================================================================
#  client.py
#  Client library for Colmi Ring to interact with the device over Bluetooth.
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# Inspired by
# - https://github.com/tahnok/colmi_r02_client/tree/main
# - https://github.com/Puxtril/colmi-docs/tree/main
# =============================================================================
import logging
import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from types import TracebackType

SERVICE_ID = "6E40FFF0-B5A3-F393-E0A9-E50E24DCCA9E"
REQUEST_ID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
RESPONSE_ID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Command codes
CMD_BATTERY = 3

COMMANDS = []
COMMANDS.append(int(CMD_BATTERY))


logger = logging.getLogger(__name__)


class ColmiClient:
    def __init__(self, address: str):
        self.address = address
        self.bleak_client = BleakClient(self.address)
        logger.info(f"Created client for {self.address}")
        self.queues: dict[int, asyncio.Queue] = {
            cmd: asyncio.Queue() for cmd in COMMANDS
        }

    async def __aenter__(self) -> "ColmiClient":
        logger.info(f"Connecting to {self.address}")
        await self.connect()
        logger.info("Connected!")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        logger.info("Disconnecting")
        if exc_val is not None:
            logger.error("had an error")
        await self.disconnect()

    async def connect(self):
        await self.bleak_client.connect(timeout=30.0)

        uart_service = self.bleak_client.services.get_service(SERVICE_ID)
        assert uart_service
        rx_char = uart_service.get_characteristic(REQUEST_ID)
        assert rx_char
        self.rx_char = rx_char

        await self.bleak_client.start_notify(RESPONSE_ID, self._handle_tx)

    async def disconnect(self):
        await self.bleak_client.disconnect()

    def _handle_tx(self, _: BleakGATTCharacteristic, packet: bytearray) -> None:
        """Bleak callback that handles new packets from the ring."""

        logger.info(f"Received packet {packet}")
        packet_type = packet[0]

        logger.info(f"Packet Type {packet_type}")

        if packet_type in COMMANDS:
            logger.info(f"write packet to queue")
            self.queues[packet_type].put_nowait(packet)

    async def send_packet(self, packet: bytearray) -> None:
        logger.debug(f"Sending packet: {packet}")
        await self.bleak_client.write_gatt_char(self.rx_char, packet, response=False)

    async def get_battery_level(self) -> int:
        """Get the battery level from the Colmi Ring."""
        packet = self.create_packet(CMD_BATTERY)
        await self.send_packet(packet)
        result_packet = await self.queues[CMD_BATTERY].get()
        logger.debug(f"packet from queue: {result_packet}")
        battery_level = result_packet[1]
        logger.info(f"Battery level: {battery_level}%")

        return battery_level

    @staticmethod
    def create_packet(command: int) -> bytearray:
        """Create a packet to send to the Colmi Ring."""
        packet = bytearray(16)
        packet[0] = command

        # Calculate checksum. Add all bytes modulo 255
        packet[-1] = sum(packet) & 255

        return packet
