# =============================================================================
#  client.py
#  Client library for Colmi R12 ring to interact with the device over Bluetooth.
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# Inspired by
# - https://github.com/tahnok/colmi_r02_client/tree/main
# - https://github.com/Puxtril/colmi-docs/tree/main
# - https://github.com/CitizenOneX/colmi_r06_fbp/blob/main/lib/colmi_ring.dart
# - https://github.com/edgeimpulse/example-data-collection-colmi-r02
# =============================================================================
import logging
import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from types import TracebackType
import struct

# UUIDs for MAIN and RXTX services and characteristics
MAIN_SERVICE_UUID = "de5bf728-d711-4e47-af26-65e3012a5dc7"
MAIN_WRITE_CHARACTERISTIC_UUID = "de5bf72a-d711-4e47-af26-65e3012a5dc7"
MAIN_NOTIFY_CHARACTERISTIC_UUID = "de5bf729-d711-4e47-af26-65e3012a5dc7"
RXTX_SERVICE_UUID = "6e40fff0-b5a3-f393-e0a9-e50e24dcca9e"
RXTX_WRITE_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
RXTX_NOTIFY_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


def create_command(hex_string):
    bytes_array = [int(hex_string[i : i + 2], 16) for i in range(0, len(hex_string), 2)]
    while len(bytes_array) < 15:
        bytes_array.append(0)
    checksum = sum(bytes_array) & 0xFF
    bytes_array.append(checksum)
    return bytes(bytes_array)


# Other versions of this rings seems to use 12 bit format but looks like Colmi R12 uses 16 bit signed integers
def decode_accelerometer(packet: bytes):
    x, y, z = struct.unpack(">hhh", packet[2:8])
    return x, y, z


# Commands
CMD_BATTERY = create_command("03")
SET_UNITS_METRICS = create_command("0a0200")

# Ring will transmit data once per second after enabling raw sensor
CMD_ENABLE_RAW_SENSOR = create_command("a104")
# Disable raw sensor for my Colmi R12 is different from most documentation that claims this should be a102
CMD_DISABLE_RAW_SENSOR = create_command("a105")

logger = logging.getLogger(__name__)


class ColmiClient:
    def __init__(self, address: str):
        self.address = address
        self.bleak_client = BleakClient(self.address)
        self.battery_queue = asyncio.Queue()

        logger.info(f"Created client for {self.address}")

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

        await self.bleak_client.start_notify(
            MAIN_NOTIFY_CHARACTERISTIC_UUID, self.handle_notification
        )
        await self.bleak_client.start_notify(
            RXTX_NOTIFY_CHARACTERISTIC_UUID, self.handle_notification
        )
        await asyncio.sleep(2)  # Ensure notifications are set up

    async def disconnect(self):
        await self.bleak_client.disconnect()

    async def send_data_array(self, command, service_name):
        """Send data to RXTX or MAIN service's write characteristic."""
        try:
            if service_name == "MAIN":
                await self.bleak_client.write_gatt_char(
                    MAIN_WRITE_CHARACTERISTIC_UUID, command
                )
            elif service_name == "RXTX":
                await self.bleak_client.write_gatt_char(
                    RXTX_WRITE_CHARACTERISTIC_UUID, command
                )
        except Exception as e:
            print(f"Failed to send data to {service_name} service: {e}")

    def handle_notification(
        self, _: BleakGATTCharacteristic, packet: bytearray
    ) -> None:
        """Bleak callback that handles new packets from the ring."""
        packet_type = packet[0]
        packet_sub_type = packet[1]

        logger.info(f"Type: {packet_type} - {packet_sub_type}")
        logger.info(f"Packet {packet}")

        if packet_type == 0x03:
            battery_level = packet[1]
            self.battery_queue.put_nowait(battery_level)

        # get accelerometer values
        if packet_type == 0xA1 and packet_sub_type == 0x03:
            logger.info(f"Accelerometer packet: {packet}")
            self.accX, self.accY, self.accZ = decode_accelerometer(packet)

            logger.info(
                f"Accelerometer - X: {self.accX}, Y: {self.accY}, Z: {self.accZ}"
            )

    async def get_battery_level(self) -> int:
        """Get the battery level from the Colmi Ring."""
        await self.send_data_array(CMD_BATTERY, "RXTX")
        battery_level = await self.battery_queue.get()
        logger.info(f"Battery level: {battery_level}%")

        return battery_level

    async def start_streaming(self):
        """Start streaming raw sensor data from the Colmi Ring."""
        logger.info(f"Start Streaming Data")
        await self.send_data_array(SET_UNITS_METRICS, "RXTX")
        await self.send_data_array(CMD_ENABLE_RAW_SENSOR, "RXTX")

    async def stop_streaming(self):
        """Stop streaming raw sensor data from the Colmi Ring."""
        logger.info(f"Stop Streaming Data")
        await self.send_data_array(CMD_DISABLE_RAW_SENSOR, "RXTX")
