# =============================================================================
#  simple_read_battery.py
#  Simplest code to request data from the ring
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python

import sys
import asyncio
import logging
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your Colmi Ring's Bluetooth address

# Id of ring bluetooth service and characteristics
RXTX_WRITE_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
RXTX_NOTIFY_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

CMD_BATTERY = b"\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03"


def handle_notification(_: BleakGATTCharacteristic, packet: bytearray) -> None:
    """Bleak callback that handles new packets from the ring."""
    print(f"Received packet: {packet}")
    packet_type = packet[0]

    # if packet is about battery level
    if packet_type == 0x03:
        battery_level = packet[1]
        print(f"Battery level: {battery_level}%")


async def main():
    async with BleakClient(RING_ADDRESS, timeout=30) as client:
        # Setup callback for notifications
        await client.start_notify(RXTX_NOTIFY_CHARACTERISTIC_UUID, handle_notification)
        await asyncio.sleep(1)

        # Send command to request battery level
        print("Requesting battery level...")
        await client.write_gatt_char(RXTX_WRITE_CHARACTERISTIC_UUID, CMD_BATTERY)

        # Wait to receive notification
        await asyncio.sleep(5)


asyncio.run(main())
