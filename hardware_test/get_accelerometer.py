# =============================================================================
#  get_accelerometer.py
#  Test getting accelerometer data from Colmi Ring
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
    filename="get_accelerometer.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your Colmi Ring's Bluetooth address


async def main():
    client = ColmiClient(RING_ADDRESS)
    async with client:
        await client.start_streaming()
        for i in range(20):
            await asyncio.sleep(1)
            print(client.accX, client.accY, client.accZ)
        await client.stop_streaming()


asyncio.run(main())
