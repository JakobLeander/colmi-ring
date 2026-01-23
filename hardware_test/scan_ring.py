# =============================================================================
#  scan_ring.py
#  Test scanniing for Colmi Rings
#  Copyright (c) 2026 Jakob Leander
#  Licensed under the MIT License.
# =============================================================================
#!/usr/bin/env python

import sys
import asyncio

sys.path.append("..")
from colmi_ring.client import Client


async def main():
    client = Client()
    await client.scan()


asyncio.run(main())
