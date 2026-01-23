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
from bleak import BleakScanner


SERVICE_ID = "6E40FFF0-B5A3-F393-E0A9-E50E24DCCA9E"
REQUEST_ID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
RESPONSE_ID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

logger = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.connected = False

    async def scan(self):
        """Scan for available Colmi Rings. Need to scan for 10 seconds to ensure it finds it."""
        found_devices = 0
        devices = await BleakScanner.discover(timeout=10.0)

        for d in devices:
            if d.name is not None and d.name.startswith("COLMI"):
                found_devices += 1
                print(f"{d.name} - {d.address}")

        if found_devices == 0:
            print("No Colmi ring found")
