"""
This script reads the weight from the esp32 through Bluetooth communication and plots it in real-time using matplotlib.
Author: Sami Kaab
Date: 2024-07-09
"""
import asyncio
import struct
from bleak import BleakClient, BleakScanner, BleakError
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# pip install matplotlib pyserial bleak 


# Bluetooth setup
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
global_weight = 0  # Global variable to hold the latest weight value
maxWeight = 50
minWeight = -50
state = ""

async def read_weight(device_address):
    global global_weight, state
    try:
        state = "Trying to connect to ESP32_BT_Scale"
        async with BleakClient(device_address, timeout=30.0) as client:
            connected = client.is_connected
            if connected:
                state = "Connected to ESP32_BT_Scale"
                print("Connected to ESP32!")
                while True:
                    try:
                        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
                        weight = struct.unpack('f', value)[0]
                        global_weight = weight  # Update the global variable
                    except Exception as e:
                        print(f"Failed to read characteristic: {e}")
                        state = "Failed to read"
                        return
                    await asyncio.sleep(0.05)
            else:
                print("Failed to connect.")
                state = "Failed to connect to ESP32_BT_Scale"
    except Exception as e:
        print(f"Unexpected error: {e}")
        state = "Unexpected error"

async def discover_and_run():
    global state
    while True:
        state = "Looking for ESP32_BT_Scale"
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == "ESP32_BT_Scale":
                address = device.address
                await read_weight(address)
                
        await asyncio.sleep(5)

def start_bleak_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(discover_and_run())

# Start the Bluetooth reading in a separate thread
threading.Thread(target=start_bleak_loop, daemon=True).start()

# Graph setup
fig, ax = plt.subplots()
bar = ax.bar([0], [0])

def update(frame):
    global global_weight, maxWeight, minWeight, state
    maxWeight = max(maxWeight, global_weight)  # Update the max weight
    minWeight = min(minWeight, global_weight)  # Update the min weight
    weight = global_weight  # Use the global variable
    bar[0].set_height(weight)
    ax.set_ylim(minWeight, maxWeight)
    ax.set_xticks([])
    # set title as the state
    ax.set_title(state)

ani = animation.FuncAnimation(fig, update, interval=100)  # Update every 100 milliseconds
plt.show()