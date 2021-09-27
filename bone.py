import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

'''
https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton
https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
Example glb from OpenGloves, originally from steamvr/drivers/indexcontroller
Steam's OpenVR Uses (w,z,y,z) for Quaternions as defined in HmdQuaternionf_t

0 RootNode, 
1 REF:Root, 
2 REF:wrist_r, # All metacarpal positons are relative to this. 
3 REF:finger_thumb_0_r, 
4 REF:finger_thumb_1_r,
5 REF:finger_thumb_2_r,
6 REF:finger_thumb_r_end,
7 REF:finger_index_meta_r - -0.000632452196441591, 0.0268661547452211, 0.01500194799155
8 REF:finger_index_0_r
9 REF:finger_index_1_r
10 REF:finger_index_2_r
11 REF:finger_index_r_end
12 REF:finger_middle_meta_r  -0.00217731343582273, 0.00711954385042191, 0.0163187384605408
13 REF:finger_middle_0_r
14 REF:finger_middle_1_r
15 REF:finger_middle_2_r
16 REF:finger_middle_r_end
17 REF:finger_ring_meta_r -0.000513435574248433, -0.00654512271285057, 0.0163476932793856
18 REF:finger_ring_0_r
19 REF:finger_ring_1_r
20 REF:finger_ring_2_r
21 REF:finger_ring_r_end
22 REF:finger_pinky_meta_r 0.00247815088368952, -0.0189813692122698, 0.0152135835960507
23 REF:finger_pinky_0_r
24 REF:finger_pinky_1_r
25 REF:finger_pinky_2_r
26 REF:finger_pinky_r_end
27 REF:finger_thumb_r_aux -0.00605911063030362, 0.0562852211296558, -0.0600638426840305
28 REF:finger_index_r_aux
29 REF:finger_middle_r_aux
30 REF:finger_ring_r_aux
31 REF:finger_pinky_r_aux
'''

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

right_pose2 = np.array([
	# Position{HmdVector4_t} (x,y,z,1) , Quaternion{HmdQuaternionf_t} (w,x,y,z)
	# https://github.com/ValveSoftware/openvr/issues/505
	[[0.000000, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]], # 0 - Root Node, Dan Skipped the Ref:Root
	[[0.034038, 0.036503, 0.164722, 1.000000], [-0.055147, -0.078608, 0.920279, -0.379296]], # 2 - Wrist
	[[0.012083, 0.028070, 0.025050, 1.000000], [0.567418, -0.464112, 0.623374, -0.272106]], # Thumb Meta
	[[-0.040406, -0.000000, 0.000000, 1.000000], [0.994838, 0.082939, 0.019454, 0.055130]],
	[[-0.032517, -0.000000, -0.000000, 1.000000], [0.974793, -0.003213, 0.021867, -0.222015]],
	[[-0.030464, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[-0.000632, 0.026866, 0.015002, 1.000000], [-0.421979, 0.644251, -0.422133, -0.478202]], # Index Meta MODIFIED
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

right_fist_pose = np.array([
	[[0.000000, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[0.034038, 0.036503, 0.164722, 1.000000], [-0.055147, -0.078608, 0.920279, -0.379296]], # 2 - Wrist
	[[0.016305, 0.027529, 0.017800, 1.000000], [0.483332, -0.225703, 0.836342, -0.126413]], # Thumb meta
	[[-0.040406, -0.000000, 0.000000, 1.000000], [0.894335, -0.013302, -0.082902, 0.439448]],
	[[-0.032517, -0.000000, -0.000000, 1.000000], [0.842428, 0.000655, 0.001244, 0.538807]],
	[[-0.030464, 0.000000, 0.000000, 1.000000], [1.000000, -0.000000, -0.000000, 0.000000]],
	[[-0.003802, 0.021514, 0.012803, 1.000000], [0.395174, -0.617314, 0.449185, 0.510874]],
	[[-0.074204, 0.005002, -0.000234, 1.000000], [0.737291, -0.032006, -0.115013, 0.664944]],
	[[-0.043287, 0.000000, 0.000000, 1.000000], [0.611381, 0.003287, 0.003823, 0.791321]],
	[[-0.028275, -0.000000, -0.000000, 1.000000], [0.745388, -0.000684, -0.000945, 0.666629]],
	[[-0.022821, -0.000000, 0.000000, 1.000000], [1.000000, -0.000000, 0.000000, -0.000000]],
	[[-0.005787, 0.006806, 0.016534, 1.000000], [0.522315, -0.514203, 0.483700, 0.478348]],
	[[-0.070953, -0.000779, -0.000997, 1.000000], [0.723653, -0.097901, 0.048546, 0.681458]],
	[[-0.043108, -0.000000, -0.000000, 1.000000], [0.637464, -0.002366, -0.002831, 0.770472]],
	[[-0.033266, -0.000000, -0.000000, 1.000000], [0.658008, 0.002610, 0.003196, 0.753000]],
	[[-0.025892, 0.000000, -0.000000, 1.000000], [0.999195, -0.000000, 0.000000, 0.040126]],
	[[-0.004123, -0.006858, 0.016563, 1.000000], [0.523374, -0.489609, 0.463997, 0.520644]],
	[[-0.065876, -0.001786, -0.000693, 1.000000], [0.759970, -0.055609, 0.011571, 0.647471]],
	[[-0.040331, -0.000000, -0.000000, 1.000000], [0.664315, 0.001595, 0.001967, 0.747449]],
	[[-0.028489, 0.000000, 0.000000, 1.000000], [0.626957, -0.002784, -0.003234, 0.779042]],
	[[-0.022430, 0.000000, -0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	[[-0.001131, -0.019295, 0.015429, 1.000000], [0.477833, -0.479766, 0.379935, 0.630198]],
	[[-0.062878, -0.002844, -0.000332, 1.000000], [0.827001, 0.034282, 0.003440, 0.561144]],
	[[-0.029874, -0.000000, -0.000000, 1.000000], [0.702185, -0.006716, -0.009289, 0.711903]],
	[[-0.017979, -0.000000, -0.000000, 1.000000], [0.676853, 0.007956, 0.009917, 0.736009]],
	[[-0.018018, -0.000000, 0.000000, 1.000000], [1.000000, 0.000000, 0.000000, 0.000000]],
	[[-0.019716, 0.002802, 0.093937, 1.000000], [0.377286, -0.540831, -0.150446, 0.736562]],
	[[-0.000171, 0.016473, 0.096515, 1.000000], [-0.006456, 0.022747, 0.932927, 0.359287]],
	[[-0.000448, 0.001536, 0.116543, 1.000000], [-0.039357, 0.105143, 0.928833, 0.353079]],
	[[-0.003949, -0.014869, 0.130608, 1.000000], [-0.055071, 0.068695, 0.944016, 0.317933]],
	[[-0.003263, -0.034685, 0.139926, 1.000000], [0.019690, -0.100741, 0.957331, 0.270149]],
])


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
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def build_pose(pose, rotate=False, parent_row=None):
	'''
	Expects to be fed an array of nodes where
	each node has one parent and one child.
	Build hand splits up the hand then feeds it to this
	functon. e.g. just the thumb. 
	'''

	if (parent_row is not None):
		quad = parent_row[1,:].copy()
		point = parent_row[0,:3].copy()
	else:
		# Set Starting point, root
		#quad = np.array([1.000000, -0.000000, -0.000000, 0.000000])
		#point = np.array([0.000000, 0.000000, 0.000000])
		# Set Starting point, wrist
		quad = np.array([-0.055147, -0.078608, 0.920279, -0.379296])
		point = np.array([0.034038, 0.036503, 0.164722, 1.000000])
	points = []

	for row in pose:

		c = np.array(row[0,:3])
		q = np.array(row[1,:])
		# Change quaternion representation between glb and SteamVR
		w, x, y, z = q
		q = np.array([-w, -x, -y, -z])

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
	'''
	The hand is defined relatively using a series of nodes,
	Each node has a parent leading back to the wrist,
	in order to plot the hand, the global positions need to 
	be calculated. Each position and rotation w.r.t the parents. 
	Think of the turtle / logo programming enviroment.

	Input is expected to follow the format listed above

	'''

	thumb_start = 2
	index_start = 6
	middle_start = 11
	ring_start = 16
	pinky_start = 21

	# Splitting up each parent
	root = pose[0, :, :]
	wrist = pose[1, :, :]
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
	hand = [[wrist[0, :3]], thumb, index, middle, ring, pinky]

	# Conbine them into one model
	points = np.concatenate(hand)

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

def draw_line(p, a, ax, color="blue", b=None):
	if (b == None): b = a + 1
	l = plt3d.art3d.Line3D(
	 [p[a,0], p[b,0]],
	 [p[a,1], p[b,1]],
	 [p[a,2], p[b,2]], color=color)
	ax.add_line(l)

def plot_steam_hand(points, title="Steam Hand", ax=None):
	if (ax == None):
		# Plot setup
		fig = plt.figure(title)
		ax = fig.add_subplot(111, projection='3d', xlim=(-0.2, 0.2), ylim=(-0.2, 0.2), zlim=(0, 0.4))
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_zlabel('Z [m]')

	hand_points = points
	xs = hand_points[:,0]
	ys = hand_points[:,1]
	zs = hand_points[:,2]
	# Plot the Points that make up the hand
	ax.scatter(xs,ys,zs)

	# Draw lines between them
	# Seperate the fingers
	c = hand_points

	# Draw the thumb
	for n in [2,3]:
		draw_line(c, n, ax, "lime")
	# Index
	for n in range(5,9):
		draw_line(c, n, ax, "firebrick")
	# Middle
	for n in range(10,14):
		draw_line(c, n, ax, "purple")
	# Ring Finger
	for n in range(15,19):
		draw_line(c, n, ax, "blue")
	# Pinky finger
	for n in range(20,24):
		draw_line(c, n, ax, "pink")
	
	# Draw lines to connect the metacarpals
	for i in range(4):
		ms = [1, 5, 10, 15, 20]
		l = plt3d.art3d.Line3D([c[ms[i],0], c[ms[i+1],0]], [c[ms[i],1], c[ms[i+1],1]], [c[ms[i],2], c[ms[i+1],2]], color="aqua")
		ax.add_line(l)
	# Draw lines to connect the hand
	# Connect the Thumb Metacarpal to the base of the index
	draw_line(c, 1, ax, "aqua", 2)
	draw_line(c, 2, ax, "aqua", 5)
	# Palm to pinky base
	draw_line(c, 1, ax, "aqua", 20)

	plt.show()

def lerp(a, b, f):
	return a + f * (b - a)

def lerp_quat(q1, q2, f):
	# Returns a lerped quat between q1 and q2
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2

	w = lerp(w1,w2,f)
	x = lerp(x1,x2,f)
	y = lerp(y1,y2,f)
	z = lerp(z1,z2,f)
	return [w, x, y, z]

def lerp_pos(p1, p2, f):
	# Returns a lerped position between q1 and q2
	# Is this function needed?
	x1, y1, z1, w = p1
	x2, y2, z2, w = p2
	x = lerp(x1,x2,f)
	y = lerp(y1,y2,f)
	z = lerp(z1,z2,f)
	return [x, y, z, 1.0]

def lerp_pose(amount):
	'''Amount should be between 0 and 1'''
	open_pose = right_pose
	closed_pose = right_fist_pose

	# Make a placeholder new pose
	new_pose = []

	for i in range(0,31):
		open_row = open_pose[i]
		open_c = open_row[0, :]
		open_q = open_row[1, :]

		closed_row = closed_pose[i]
		closed_c = closed_row[0, :]
		closed_q = closed_row[1, :]

		c = lerp_pos(open_c, closed_c, amount)
		q = lerp_quat(open_q, closed_q, amount)

		new_row = np.array([c,q])
		new_pose.append(new_row)

	new_pose = np.array(new_pose)
	return new_pose

if __name__ == "__main__":
	print("Open Pose Shape: ", right_pose.shape)

	points = build_hand(right_pose, False)
	print("Points Shape",points.shape)
	print(points)
	#plot_points(points)
	plot_steam_hand(points, "Right Pose without Rotation")

	points = build_hand(right_fist_pose, False)
	print("Points Shape",points.shape)
	print(points)
	plot_steam_hand(points, "Fist Pose without Rotation")

	points = build_hand(right_pose, True)
	print("Points Shape",points.shape)
	print(points)
	#plot_points(points)
	plot_steam_hand(points, "Right pose with Rotation")

	points = build_hand(right_pose2, True)
	print("Points Shape",points.shape)
	print(points)
	#plot_points(points)
	plot_steam_hand(points, "Right pose2 with Rotation")

	points = build_hand(right_fist_pose, True)
	print("Points Shape",points.shape)
	print(points)
	plot_steam_hand(points, "Fist Pose with Rotation")

	pose = lerp_pose(0.5)
	points = build_hand(pose, True)
	plot_steam_hand(points, "Lerped Pose")