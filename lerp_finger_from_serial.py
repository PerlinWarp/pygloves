import multiprocessing
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import bone

# Use device manager to find the Arduino's serial port.
COM_PORT = "COM9"
RESET_SCALE = False

q = multiprocessing.Queue()
# Plot Setup
fig = plt.figure("Serial Finger Plots")
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

# ------------ Serial Setup ---------------
def serial_worker(q):
	# Open Serial Port
	COM_PORT = "COM9"
	ser = serial.Serial(COM_PORT,'115200', timeout=1)  # open serial port
	print("Listening on "+COM_PORT)

	while True:
		try:
			# Read from serial
			read = ser.readline()
			fingers = decode_serial(read)
			# Add the decoded values to the queue
			q.put(fingers)
		except KeyboardInterrupt:
			print("Quitting thread...")
			ser.close()
			quit()

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

def animate(i):
	fingers = [0,0,0,0,0]
	while not(q.empty()):
		fingers = list(q.get())

	# Turn finger values into Lerp Vals
	thumb_val = fingers[0] / 1024
	index_val = fingers[1] / 1024
	middle_val = fingers[2] / 1024
	ring_val = fingers[3] / 1024
	pinky_val = fingers[4] / 1024
	print("Fingers", fingers)

	# Plot
	ax.clear()
	ax.set_xlabel('X [mm]')
	ax.set_ylabel('Y [mm]')
	ax.set_zlabel('Z [mm]')

	open_pose = bone.right_pose
	closed_pose = bone.right_fist_pose

	# Split up the hand
	wrist = open_pose[0:2, :, :]
	thumb_pose_o = open_pose[2:6, :, :]
	index_pose_o = open_pose[6:11, :,:]
	middle_pose_o = open_pose[11:16, :,:]
	ring_pose_o = open_pose[16:21, :, :]
	pinky_pose_o = open_pose[21:26, :, :]

	thumb_pose_c = closed_pose[2:6, :, :]
	index_pose_c = closed_pose[6:11, :,:]
	middle_pose_c = closed_pose[11:16, :,:]
	ring_pose_c = closed_pose[16:21, :, :]
	pinky_pose_c = closed_pose[21:26, :, :]
	# Lerp individual parts
	thumb_pose = bone.lerp_pose(thumb_val, thumb_pose_o, thumb_pose_c)
	index_pose = bone.lerp_pose(index_val, index_pose_o, index_pose_c)
	middle_pose = bone.lerp_pose(middle_val, middle_pose_o, middle_pose_c)
	ring_pose = bone.lerp_pose(ring_val, ring_pose_o, ring_pose_c)
	pinky_pose = bone.lerp_pose(pinky_val, pinky_pose_o, pinky_pose_c)

	# Put the hand back together
	hand = [wrist, thumb_pose, index_pose, middle_pose, ring_pose, pinky_pose]
	# Conbine them into one model
	pose = np.concatenate(hand)

	points = bone.build_hand(pose, True)
	# Plot the Points
	bone.plot_steam_hand(points, "Lerped Pose", ax)

if __name__ == "__main__":
	p = multiprocessing.Process(target=serial_worker, args=(q,), daemon=True)
	p.start()
	anim = animation.FuncAnimation(fig, animate, blit=False, interval=1)
	try:
		plt.show()
	except KeyboardInterrupt:
		quit()