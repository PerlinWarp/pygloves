import multiprocessing
import re
from pyomyo import Myo, emg_mode
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import bone
import serial_utils as s

# Use device manager to find the Arduino's serial port.
COM_PORT = "COM9"
RESET_SCALE = True
LEGACY_DECODE = False # If false, will use alpha encodings

q = multiprocessing.Queue()
# Plot Setup
fig = plt.figure("Grip plots from Myo")
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

# ------------ Myo Setup ---------------
def emg_worker(q):
	m = Myo(mode=emg_mode.PREPROCESSED)
	m.connect()
	
	def add_to_queue(emg, movement):
		q.put(emg)

	m.add_emg_handler(add_to_queue)
	
	def print_battery(bat):
		print("Battery level:", bat)

	m.add_battery_handler(print_battery)

	 # Green logo and bar LEDs
	m.set_leds([0, 128, 0], [0, 128, 0])
	# Vibrate to know we connected okay
	m.vibrate(1)
	
	"""worker function"""
	while True:
		m.run()
	print("Worker Stopped")

def animate(i):
	fingers = [0,0,0,0,0]
	while not(q.empty()):
		fingers = list(q.get())

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
	p = multiprocessing.Process(target=emg_worker, args=(q,), daemon=True)
	p.start()
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
	try:
		plt.show()
	except KeyboardInterrupt:
		quit()