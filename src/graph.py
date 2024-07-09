"""
This script reads the weight data from the esp32 through serial communication and plots it in real-time using matplotlib.
Author: Sami Kaab
Date: 2024-07-08
"""
import serial.tools.list_ports
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# pip install matplotlib pyserial

# Serial port configuration
baud_rate = 115200
maxWeight = 50
minWeight = -50
state = ""

def find_serial_port():
    """Find the serial port that the ESP32 is connected to.

    Returns:
        str: The serial port name, or None if the device is
    """
    global state
    state = "Looking for device"
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "CP210x USB" in desc:
            return port
    return None

serial_port = find_serial_port()
print(f"Serial port: {serial_port}")
if serial_port is None:
    state = "Device not found"
else:
    try:
        # Initialize serial connection
        ser = serial.Serial(serial_port, baud_rate)
        state = "Connected to device"
    except serial.SerialException:
        state = "Failed to connect to device"
# Create a figure and axis for the plot
fig, ax = plt.subplots()
bar = ax.bar([0], [0])

def update(frame):
    """Update the plot with the latest weight data.

    Args:
        frame (int): The frame number
    """
    global maxWeight, minWeight, state
    try:
        ax.set_title(state)
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        weight = float(line)
        # Update the min and max weight values
        maxWeight = max(maxWeight, weight)
        minWeight = min(minWeight, weight)
        
        # Update the bar graph
        bar[0].set_height(weight)
        ax.set_ylim(minWeight, maxWeight)
        # dont show axis ticks
        # ax.set_yticks([])
        ax.set_xticks([])
    except:
        pass

ani = animation.FuncAnimation(fig, update, interval=0.1)  # Update every second
plt.show()

# Close serial connection on exit
ser.close()
