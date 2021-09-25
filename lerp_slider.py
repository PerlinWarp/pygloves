import numpy as np
import bone
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

a0 = 1.0

if __name__ == "__main__":
	pose = bone.lerp_pose(0.2)
	points = bone.build_hand(pose, True)

	# Plot Setup
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	plt.subplots_adjust(left=0.25, bottom=0.25)
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	# Slider setup
	ax.margins(x=0)
	axcolor = 'lightgoldenrodyellow'
	axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
	samp = Slider(axamp, 'Amp', 0.1, 1.5, valinit=a0)

	# Plot the Points
	x = points[:,0]
	y = points[:,1]
	z = points[:,2]
	ax.scatter(x,y,z)

	def update(val):
		ax.clear()
		# Read the slider
		amp = samp.val

		pose = bone.lerp_pose(amp)
		points = bone.build_hand(pose, True)
		# Plot the Points
		bone.plot_steam_hand(points, "Lerped Pose", ax)

		fig.canvas.draw_idle()

	samp.on_changed(update)

	def reset(event):
		samp.reset()

	def colorfunc(label):
		l.set_color(label)
		fig.canvas.draw_idle()

	plt.show()