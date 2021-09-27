import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import bone

# Use device manager to find the Arduino's serial port.
COM_PORT = "COM9"
RESET_SCALE = False

# Open Serial Port
ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port
print("Listening on "+COM_PORT)

# Plot Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')


def decode_serial(s):
	if s == b'':
		print(s)
		return [0,0,0,0,0]
	else:
		# Decode the byte string to list of ints
		s = s.decode().rstrip().split('&')
		# Get rid of all other data than fingers
		s = s[0:5]
		# Cast to ints
		s = [int(f) for f in s]
		return s

def on_close(event):
	print("Closed Figure")
	ser.close()
	quit()

def animate(i):
	# Read from serial
	read = ser.readline()
	fingers = decode_serial(read)

	# Turn finger values into Lerp Vals
	val = fingers[0] / 1000
	print("Finger val", val)

	# Plot
	ax.clear()
	ax.set_xlabel('X [mm]')
	ax.set_ylabel('Y [mm]')
	ax.set_zlabel('Z [mm]')

	pose = bone.lerp_pose(val)
	points = bone.build_hand(pose, True)
	# Plot the Points
	bone.plot_steam_hand(points, "Lerped Pose", ax)

if __name__ == "__main__":
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)