# some code from ChatGPT to create a bluetooth keyboard.
# this is code for a central host (using the bleak python lib) to receive chars from the keyboard
# Doesn't work at all.   Needs some tweaking

import asyncio
from bleak import BleakClient, BleakScanner

# UUID of the characteristic you want to read from (this must match your peripheral's characteristic UUID)
# Replace with actual UUID
CHARACTERISTIC_UUID = "0000xxxx-0000-1000-8000-00805f9b34fb"

TARGET_DEVICE_NAME = "BLE-Peripheral"


async def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print(f"Received notification from {sender}: {data}")


async def run():
    # Scan for devices
    print("Scanning for devices...")
    devices = await BleakScanner.discover()

    # Find the target device by name
    target_device = None
    for device in devices:
        print(f"Found device: {device.name}, {device.address}")
        if device.name == TARGET_DEVICE_NAME:
            target_device = device
            break

    if not target_device:
        print(f"Device named '{TARGET_DEVICE_NAME}' not found.")
        return

    print(f"Connecting to {target_device.name} ({target_device.address})")

    # Connect to the peripheral
    async with BleakClient(target_device) as client:
        print(f"Connected to {target_device.name}")

        # Start receiving notifications
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        print("Waiting for notifications...")
        await asyncio.sleep(60)  # Keep the connection open for 60 seconds

        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Stopped notifications and disconnected.")

# Run the async loop
asyncio.run(run())
