# Colmi Ring Client

A Python client library for interacting with Colmi Ring R12 over Bluetooth Low Energy (BLE).

Main focus for me is getting accelerometer data, but the library also supports basic battery and device management. Alongside the client, the repository contains utility scripts for scanning and simple hardware tests, making it easier to explore data from the ring. You can find other libraries referenced below to extract fitness data.

## Overview

This project provides a Python client library to communicate with Colmi R12 (and compatible R02/R06) ring fitness tracker and collect sensor data via Bluetooth Low Energy (BLE). In addition to the core `ColmiClient` class, the repo includes a standalone scanner tool (`colmi_ring/scanner.py`) and a handful of example scripts under `hardware_test/` for quick experiments. The library lets you connect to the ring, retrieve battery levels, stream raw accelerometer data, and manage the BLE connection lifecycle.

## Features

- **Battery Management**: Query battery level from the Colmi Ring
- **Raw Sensor Streaming**: Enable/disable continuous streaming of sensor data
- **Accelerometer Data**: Extract X, Y, Z axis acceleration values with proper two's complement handling
- **Async/Await Support**: Full async implementation using `bleak` and `asyncio`
- **Proper Device Lifecycle**: Context manager support for clean connection handling

## Requirements

- Python 3.7+
- `bleak` - Bluetooth Low Energy library for Python

## Installation

You can install the library directly from this repository or use it as a dependency in your own project.

```bash
# clone the repo
git clone https://github.com/yourusername/colmi-ring.git
cd colmi-ring

# install into your active environment
pip install -r requirements.txt
```

The code requires Python 3.7+ and depends on `bleak` for BLE communication (version pinned in `requirements.txt`).

## Usage

Before trying to connect you may want to scan for the MAC address of your ring. A simple scanner is provided:

```bash
python -m colmi_ring.scanner
```

or

```bash
python colmi_ring/scanner.py
```

It will perform a 30‑second BLE scan and print any discovered devices (the ring typically appears with a name like ``Colmi`` or ``R12``).

Once you have the address you can use the client as shown below.

### Getting Battery Level

```python
import asyncio
from colmi_ring.colmi_client import ColmiClient

async def main():
    RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your ring's address
    client = ColmiClient(RING_ADDRESS)
    
    async with client:
        battery_level = await client.get_battery_level()
        print(f"Battery level: {battery_level}%")

asyncio.run(main())
```

### Streaming Raw Sensor Data

```python
import asyncio
from colmi_ring.colmi_client import ColmiClient

async def main():
    RING_ADDRESS = "32:31:47:36:08:07"  # Replace with your ring's address
    client = ColmiClient(RING_ADDRESS)
    
    async with client:
        await client.start_streaming()
        await asyncio.sleep(5)  # Stream for 5 seconds
        await client.stop_streaming()

asyncio.run(main())
```

## Project Structure

```
colmi-ring/
├── colmi_ring/
│   ├── __init__.py
│   ├── colmi_client.py        # Main ColmiClient class
│   ├── scanner.py             # Device scanning utility
├── hardware_test/             # Example scripts for quick testing
│   ├── get_battery.py         # Battery level example
│   ├── get_accelerometer.py   # Accelerometer data example
│   └── scan_ring.py           # Scanning example (duplicate of scanner.py)
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Bluetooth Service Details

### MAIN Service
- **Service UUID**: `DE5BF728-D711-4E47-AF26-65E3012A5DC7`
- **Write Characteristic**: `DE5BF72A-D711-4E47-AF26-65E3012A5DC7`
- **Notify Characteristic**: `DE5BF729-D711-4E47-AF26-65E3012A5DC7`

### RXTX Service
- **Service UUID**: `6E40FFF0-B5A3-F393-E0A9-E50E24DCCA9E`
- **Write Characteristic**: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- **Notify Characteristic**: `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`

## Commands

- **Battery**: `0x03`
- **Set Units (Metrics)**: `0x0A 0x02 0x00`
- **Enable Raw Sensor**: `0xA1 0x04` (sends 1 packet per second)
- **Disable Raw Sensor**: `0xA1 0x05`

## Data Format

The ring transmits sensor data in the following formats:

### Accelerometer Data (0xA1 0x03)
- Bytes 2-3: X-axis (16-bit little Endian)
- Bytes 4-5: Y-axis (16-bit little Endian)
- Bytes 6-7: Z-axis (16-bit little Endian)

### Battery Data (0x03)
- Byte 1: Battery percentage (0-100)

## Important Notes

- Device address format: `XX:XX:XX:XX:XX:XX` (MAC address)
- The ring cannot be paired to other devices or it cannot be discovered
- Raw sensor streaming sends approximately 1 packet per second
- Always use the `async with` context manager for proper connection lifecycle management

## References

This project is inspired by:
- [colmi_r02_client](https://github.com/tahnok/colmi_r02_client)
- [colmi-docs](https://github.com/Puxtril/colmi-docs)
- [CitizenOneX/colmi_r06_fbp](https://github.com/CitizenOneX/colmi_r06_fbp/blob/main/lib/colmi_ring.dart)
- [Edge Impulse Colmi R02 Example](https://github.com/edgeimpulse/example-data-collection-colmi-r02)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Jakob Leander