import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

right_pose = np.array([
	# Position{HmdVector4_t} (x,y,z,1) , Quaternion{HmdQuaternionf_t} (w,x,y,z)
	# https://github.com/ValveSoftware/openvr/issues/505
	[[0.000000, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]], # 0 - Root Node, Dan Skipped the Ref:Root
	[[0.034038, 0.036503, 0.164722, 1.000000], [-0.055147, -0.078608, 0.920279, -0.379296]], # 2 - Wrist
	[[0.012083, 0.028070, 0.025050, 1.000000], [0.567418, -0.464112, 0.623374, -0.272106]], # Thumb Meta
	[[-0.040406, -0.000000, 0.000000, 1.000000], [0.994838, 0.082939, 0.019454, 0.055130]],
	[[-0.032517, -0.000000, -0.000000, 1.000000], [0.974793, -0.003213, 0.021867, -0.222015]],
	[[-0.030464, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[-0.000632, 0.026866, 0.015002, 1.000000], [0.421979, -0.644251, 0.422133, 0.478202]], # Index Meta
	[[-0.074204, 0.005002, -0.000234, 1.000000], [0.995332, 0.007007, -0.039124, 0.087949]],
	[[-0.043930, 0.000000, 0.000000, 1.000000], [0.997891, 0.045808, 0.002142, -0.045943]],
	[[-0.028695, -0.000000, -0.000000, 1.000000], [0.999649, 0.001850, -0.022782, -0.013409]],
	[[-0.022821, -0.000000, 0.000000, 1.000000], [1.000000, -0.000000, 0.000000, -0.000000]],
	[[-0.002177, 0.007120, 0.016319, 1.000000], [0.541276, -0.546723, 0.460749, 0.442520]], # Middle Meta
	[[-0.070953, -0.000779, -0.000997, 1.000000], [0.980294, -0.167261, -0.078959, 0.069368]],
	[[-0.043108, -0.000000, -0.000000, 1.000000], [0.997947, 0.018493, 0.013192, 0.059886]],
	[[-0.033266, -0.000000, -0.000000, 1.000000], [0.997394, -0.003328, -0.028225, -0.066315]],
	[[-0.025892, 0.000000, -0.000000, 1.000000], [0.999195, -0.000000, 0.000000, 0.040126]],
	[[-0.000513, -0.006545, 0.016348, 1.000000], [0.550143, -0.516692, 0.429888, 0.495548]], # Ring Meta
	[[-0.065876, -0.001786, -0.000693, 1.000000], [0.990420, -0.058696, -0.101820, 0.072495]],
	[[-0.040697, -0.000000, -0.000000, 1.000000], [0.999545, -0.002240, 0.000004, 0.030081]],
	[[-0.028747, 0.000000, 0.000000, 1.000000], [0.999102, -0.000721, -0.012693, 0.040420]],
	[[-0.022430, 0.000000, -0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]], 
	[[0.002478, -0.018981, 0.015214, 1.000000], [0.523940, -0.526918, 0.326740, 0.584025]], # Pinky Meta
	[[-0.062878, -0.002844, -0.000332, 1.000000], [0.986609, -0.059615, -0.135163, 0.069132]],
	[[-0.030220, -0.000000, -0.000000, 1.000000], [0.994317, 0.001896, -0.000132, 0.106446]],
	[[-0.018187, -0.000000, -0.000000, 1.000000], [0.995931, -0.002010, -0.052079, -0.073526]],
	[[-0.018018, -0.000000, 0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	# https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton#auxiliary-bones
	[[0.006059, 0.056285, 0.060064, 1.000000], [0.737238, 0.202745, -0.594267, -0.249441]], # thumb aux
	[[0.040416, -0.043018, 0.019345, 1.000000], [-0.290331, 0.623527, 0.663809, 0.293734]], # index aux
	[[0.039354, -0.075674, 0.047048, 1.000000], [-0.187047, 0.678062, 0.659285, 0.265683]], # middle aux
	[[0.038340, -0.090987, 0.082579, 1.000000], [-0.183037, 0.736793, 0.634757, 0.143936]], # ring aux
	[[0.031806, -0.087214, 0.121015, 1.000000], [-0.003659, 0.758407, 0.639342, 0.126678]], # pinky aux
])

thumb_pose = right_pose[2:6, :, :]

def q_conjugate(q):
	w, x, y, z = q
	return [w, -x, -y, -z]

def q_mult(q1, q2):
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2
	w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
	x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
	y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
	z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
	return np.array([w, x, y, z])

def qv_mult(q1, v1):
	# Rotates a vector by a quaternion
	x1, y1, z1 = v1
	q2 = (0.0, x1, y1, z1)
	print("q2",q2)
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def build_pose(pose, rotate=False, parent_row=None):
	# Set Starting point, wrist
	quad = np.array([1.000000, -0.000000, -0.000000, 0.000000])
	point = np.array([0.000000, 0.000000, 0.000000])
	if (parent_row is not None):
		quad = parent_row[1,:].copy()
		point = parent_row[0,:3].copy()
	points = [point.copy()]

	for row in pose:

		c = np.array(row[0,:3])
		q = np.array(row[1,:])
		print("Point", point)
		print("Coors:",c, type(c))
		print("Quat:",q)
		if (rotate):
			# Multiply the quaternions
			quad = q_mult(q,  quad)
			# Rotate the point
			rp = qv_mult(quad, c)
		else:
			rp = c
		# Get the global point
		point += rp

		# Add the new point to points
		points.append(point.copy())

	return points

def build_hand(pose, rotate=False):
	# Splitting up each parent
	wrist = pose[1, :, :]
	print("wrist", wrist)
	thumb_pose = pose[2:6, :, :]
	index_pose = pose[6:11, :,:]
	middle_pose = pose[11:16, :,:]
	ring_pose = pose[16:21, :, :]
	pinky_pose = pose[21:26, :, :]
	
	# Building all the children
	thumb = build_pose(thumb_pose, rotate, wrist)
	index = build_pose(index_pose, rotate, wrist)
	middle = build_pose(middle_pose, rotate, wrist)
	ring = build_pose(ring_pose, rotate, wrist)
	pinky = build_pose(pinky_pose, rotate, wrist)
	fingers = [[wrist[0, :3]], thumb, index, middle, ring, pinky]

	# Conbine them into one model
	points = np.concatenate(fingers)

	return points


def plot_points(points):
	# Plot the Points
	x = points[:,0]
	y = points[:,1]
	z = points[:,2]
	# Plot setup
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	ax.scatter(x,y,z)
	plt.show()


def plot_steam_hand(points):
	# Plot setup
	fig = plt.figure("Steam Hand")
	ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	hand_points = points
	xs = hand_points[:,0]
	ys = hand_points[:,1]
	zs = hand_points[:,2]
	print("Global", hand_points.shape)
	# Plot the Points that make up the hand
	ax.scatter(xs,ys,zs)

	# Draw lines between them
	# Seperate the fingers
	c = hand_points

	# Draw the thumb
	for n in [1,2,3]:
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color="lime")
		ax.add_line(l)
	# Index
	for n in range(5,9):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='firebrick')
		ax.add_line(l)
	# Middle
	for n in range(10,14):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='purple')
		ax.add_line(l)
	# Ring Finger
	for n in range(15,19):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='blue')
		ax.add_line(l)
	# Pinky finger
	for n in range(20,24):
		l = plt3d.art3d.Line3D([c[n,0], c[n+1,0]], [c[n,1], c[n+1,1]], [c[n,2], c[n+1,2]], color='pink')
		ax.add_line(l)
	
	# Draw lines to connect the metacarpals
	for i in range(4):
		ms = [2, 6,11,16,21]
		l = plt3d.art3d.Line3D([c[ms[i],0], c[ms[i+1],0]], [c[ms[i],1], c[ms[i+1],1]], [c[ms[i],2], c[ms[i+1],2]], color="aqua")
		ax.add_line(l)
	# Draw lines to connect the hand
	for i in range(4):
		ms = [1, 5,10,15,20]
		l = plt3d.art3d.Line3D([c[ms[i],0], c[ms[i+1],0]], [c[ms[i],1], c[ms[i+1],1]], [c[ms[i],2], c[ms[i+1],2]], color="aqua")
		ax.add_line(l)
	# Connect the bottom of the hand together
	l = plt3d.art3d.Line3D([c[1,0], c[20,0]], [c[1,1], c[20,1]], [c[1,2], c[20,2]], color="aqua")
	ax.add_line(l)
	l = plt3d.art3d.Line3D([c[1,0], c[0,0]], [c[1,1], c[0,1]], [c[1,2], c[0,2]], color="aqua")
	ax.add_line(l)
	l = plt3d.art3d.Line3D([c[0,0], c[20,0]], [c[0,1], c[20,1]], [c[0,2], c[20,2]], color="aqua")
	ax.add_line(l)


	plt.show()


if __name__ == "__main__":
	points = build_hand(right_pose, False)
	print("Points Shape",points.shape)
	print(points)
	plot_points(points)
	plot_steam_hand(points)

	points = build_hand(right_pose, True)
	print("Points Shape",points.shape)
	print(points)
	plot_points(points)
	plot_steam_hand(points)

