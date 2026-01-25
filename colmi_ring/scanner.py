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

logger = logging.getLogger(__name__)


class Scanner:
    async def scan(self):
        """Scan for available Colmi Rings. Need to scan for 10 seconds to ensure it finds it."""
        found_devices = 0
        devices = await BleakScanner.discover(timeout=10.0)

        for d in devices:
            if d.name is not None and d.name.startswith("COLMI"):
                found_devices += 1
                print(f"{d.name} - {d.address}")

        if found_devices == 0:
            print(
                "No Colmi ring found. Make sure ring is not connected to another device."
            )
