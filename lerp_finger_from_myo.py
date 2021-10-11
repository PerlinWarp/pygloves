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
fig = plt.figure("Finger plots from Myo")
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

def emg_to_fingers(emg):
	'''
	Take in 8 channel array for emg
	return 5 array, 1 number for each finger
	'''
	# Create a mapping between channel and finger
	thumb_val = emg[2]
	index_val = emg[4]
	middle_val = emg[6]
	ring_val = emg[7]
	pinky_val = emg[0]
	# Scale the values assuming emg mode is preprocessing 
	thumb_val = thumb_val / 1024
	index_val = index_val / 1024
	middle_val = middle_val / 1024
	ring_val = ring_val / 1024
	pinky_val = pinky_val / 1024

	fingers = [thumb_val, index_val, middle_val, ring_val, pinky_val]
	return fingers

def animate(i):
	fingers = [0,0,0,0,0]
	emgs = [0,0,0,0,0,0,0,0]
	while not(q.empty()):
		emgs = list(q.get())

	# Plot
	ax.clear()
	ax.set_xlabel('X [mm]')
	ax.set_ylabel('Y [mm]')
	ax.set_zlabel('Z [mm]')
	if (RESET_SCALE == True):
		ax.set_xlim3d([-0.05, 0.1])
		ax.set_ylim3d([-0.1, 0.1])
		ax.set_zlim3d([0, 0.2])

	# Convert emg to finger lerp values:
	fingers = emg_to_fingers(emgs)
	# Lerp the right hand
	points = bone.lerp_fingers(fingers, bone.right_open_pose, bone.right_fist_pose)

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