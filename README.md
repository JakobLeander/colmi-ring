# Colmi Ring Client

A Python client library for interacting with Colmi Ring R12 over Bluetooth Low Energy (BLE).

Main focus for me is getting accelerometer data. You can find other libraries referenced below to extract fitness data.

## Overview

This project provides a client library to communicate with Colmi R12 Ring fitness tracker and collect sensor data via Bluetooth Low Energy (BLE). It enables you to connect to the ring, retrieve battery levels, and stream raw sensor from accelerometer

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
│   ├── scanner.py              # Device scanning utilities
│   └── __pycache__/
├── hardware_test/              # Hardware testing examples
│   ├── get_battery.py          # Get battery level example
│   ├── get_accelerometer.py    # Accelerometer data example
│   └── scan_ring.py            # Device scanning example
├── LICENSE                     # MIT License
├── README.md                   # This file
└── requirements.txt            # Python dependencies
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
- Bytes 2-3: Y-axis (12-bit signed)
- Bytes 4-5: Z-axis (12-bit signed)
- Bytes 6-7: X-axis (12-bit signed)

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