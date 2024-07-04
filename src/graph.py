import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Serial port configuration
serial_port = 'COM18'
baud_rate = 115200

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)

# Create a figure and axis for the plot
fig, ax = plt.subplots()
bar = ax.bar([0], [0])

def update(frame):
    try:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        print(line)
        weight = float(line)
        
        # Update the bar graph
        bar[0].set_height(weight)
        ax.set_ylim(0, 5000)
        # dont show axis ticks
        ax.set_yticks([])
        ax.set_xticks([])
    except:
        pass

ani = animation.FuncAnimation(fig, update, interval=0.1)  # Update every second
plt.show()

# Close serial connection on exit
ser.close()
