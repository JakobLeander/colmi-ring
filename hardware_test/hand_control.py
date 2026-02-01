# =============================================================================
#  Handcontrol.py
#  Test getting hand-gesture
#  Start with open hand palm up
#  Close hand to make a fist
#  Ring will only transmit position every second
#  Y axis is 1550 when first is closed and 0 when open
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python

import sys
import asyncio
import logging
import keyboard

sys.path.append("..")
from colmi_ring.colmi_client import ColmiClient

logging.basicConfig(
    filename="hand_control.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your Colmi Ring's Bluetooth address


async def main():
    print("Press SPACE to stop streaming")
    client = ColmiClient(RING_ADDRESS)
    async with client:
        await client.start_streaming()
        while True:
            await asyncio.sleep(0.5)

            x_abs = abs(client.accX)
            if x_abs > 8192:
                x_abs = 8192  # Clamp to max value

            fist_closed = x_abs / 81.92  # Scale to 0-100%
            print(
                f"How closed is fist: {fist_closed:6.2f}%, X:{client.accX}, Y:{client.accY}, Z:{client.accZ}"
            )

            if keyboard.is_pressed(" "):  # Check if space key is pressed
                print("Space key pressed - stopping streaming")
                await client.stop_streaming()
                break


asyncio.run(main())
