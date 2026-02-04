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


async def main():
    """Scan for bluetooth devices. Need to scan for up to 30 seconds to ensure it finds ring."""
    devices = await BleakScanner.discover(timeout=30.0)

    for d in devices:
        print(f"{d.name} - {d.address}")


asyncio.run(main())
