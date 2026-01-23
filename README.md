# Colmi Ring Client

A Python client library for interacting with Colmi Ring devices over Bluetooth.

## Overview

This project provides a client library to communicate with Colmi Ring fitness trackers via Bluetooth Low Energy (BLE). It allows you to scan for devices, connect, and interact with the Colmi Ring hardware.

## Features

- Bluetooth device scanning for Colmi Ring devices
- BLE communication support
- Device discovery and connection management

## Requirements

- Python 3.7+
- bleak (Bluetooth Low Energy library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/colmi-ring.git
cd colmi-ring
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Scanning for Colmi Ring Devices

```python
import asyncio
from colmi_ring.client import Client

async def main():
    client = Client()
    await client.scan()

asyncio.run(main())
```

This will scan for Colmi Ring devices (takes approximately 10 seconds) and display their names and MAC addresses.

## Project Structure

```
colmi-ring/
├── colmi_ring/          # Main client library
│   ├── __init__.py
│   └── client.py        # BLE client implementation
├── hardware_test/       # Hardware testing utilities
│   └── scan_ring.py
├── LICENSE              # MIT License
└── requirements.txt     # Project dependencies
```

## Bluetooth Service Details

- **Service UUID**: `6E40FFF0-B5A3-F393-E0A9-E50E24DCCA9E`
- **Request Characteristic**: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- **Response Characteristic**: `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`

## References

This project is inspired by:
- [colmi_r02_client](https://github.com/tahnok/colmi_r02_client)
- [colmi-docs](https://github.com/Puxtril/colmi-docs)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Jakob Leander