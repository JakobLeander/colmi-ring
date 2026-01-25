# =============================================================================
#  get_battery.py
#  Test getting battery level from Colmi Ring
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python

import sys
import asyncio
import logging

sys.path.append("..")
from colmi_ring.colmi_client import ColmiClient

logging.basicConfig(
    filename="get_battery.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your Colmi Ring's Bluetooth address


async def main():
    client = ColmiClient(RING_ADDRESS)
    async with client:
        battery_level = await client.get_battery_level()
        print(f"Battery level: {battery_level}%")


asyncio.run(main())
