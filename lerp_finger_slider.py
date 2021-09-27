import numpy as np
import bone
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

RESET_SCALE = False
a0 = 1.0

if __name__ == "__main__":
	# Get something to plot initially
	pose = bone.lerp_pose(0.2)
	points = bone.build_hand(pose, True)
	print("Built hand", points.shape)

	# Plot Setup
	fig = plt.figure("Finger Plots",figsize=(10, 10), dpi=100)
	ax = fig.add_subplot(111, projection='3d')
	plt.subplots_adjust(left=0.25, bottom=0.40)
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	# Slider setup
	ax.margins(x=0)
	axcolor = 'lightgoldenrodyellow'
	axamp = plt.axes([0.25, 0.30, 0.65, 0.03], facecolor=axcolor)
	ax_thumb = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
	ax_index = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
	ax_middle = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
	ax_ring = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
	ax_pinky = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
	# Add the sliders
	samp = Slider(axamp, 'Amp', 0.1, 1.5, valinit=a0)
	sthumb = Slider(ax_thumb, 'Thumb', 0.1, 1.5, valinit=a0)
	sindex = Slider(ax_index, 'Index', 0.1, 1.5, valinit=a0)
	smiddle = Slider(ax_middle, 'Middle', 0.1, 1.5, valinit=a0)
	sring = Slider(ax_ring, 'Ring', 0.1, 1.5, valinit=a0)
	spinky = Slider(ax_pinky, 'Pinky', 0.1, 1.5, valinit=a0)


	# Plot the Points
	x = points[:,0]
	y = points[:,1]
	z = points[:,2]
	ax.scatter(x,y,z)

	def update(val):
		ax.clear()
		ax.set_xlabel('X [mm]')
		ax.set_ylabel('Y [mm]')
		ax.set_zlabel('Z [mm]')
		
		if (RESET_SCALE == True):
			ax.set_xlim3d([-0.05, 0.1])
			ax.set_ylim3d([-0.1, 0.1])
			ax.set_zlim3d([0, 0.2])

		# Read the sliders
		amp = samp.val

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
		thumb_pose = bone.lerp_pose(sthumb.val, thumb_pose_o, thumb_pose_c)
		index_pose = bone.lerp_pose(sindex.val, index_pose_o, index_pose_c)
		middle_pose = bone.lerp_pose(smiddle.val, middle_pose_o, middle_pose_c)
		ring_pose = bone.lerp_pose(sring.val, ring_pose_o, ring_pose_c)
		pinky_pose = bone.lerp_pose(spinky.val, pinky_pose_o, pinky_pose_c)

		# Put the hand back together
		hand = [wrist, thumb_pose, index_pose, middle_pose, ring_pose, pinky_pose]
		# Conbine them into one model
		pose = np.concatenate(hand)

		points = bone.build_hand(pose, True)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	def update_curl(val):
		ax.clear()
		ax.set_xlabel('X [mm]')
		ax.set_ylabel('Y [mm]')
		ax.set_zlabel('Z [mm]')
		
		if (RESET_SCALE == True):
			ax.set_xlim3d([-0.05, 0.1])
			ax.set_ylim3d([-0.1, 0.1])
			ax.set_zlim3d([0, 0.2])

		# Read the slider
		amp = samp.val

		pose = bone.lerp_pose(amp)
		points = bone.build_hand(pose, True)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	samp.on_changed(update_curl)
	sthumb.on_changed(update)
	sindex.on_changed(update)
	smiddle.on_changed(update)
	sring.on_changed(update)
	spinky.on_changed(update)


	def reset(event):
		samp.reset()

	def colorfunc(label):
		l.set_color(label)
		fig.canvas.draw_idle()

	plt.show()