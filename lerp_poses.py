import numpy as np
import bone

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
	open_pose = bone.right_pose
	closed_pose = bone.right_fist_pose
	print("Open Pose Shape", open_pose.shape)
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
		print("Coors:",c, type(c))
		print("Quat:",q)

		new_row = np.array([c,q])
		new_pose.append(new_row)

	new_pose = np.array(new_pose)
	print("Shape ", new_pose.shape)
	return new_pose

if __name__ == "__main__":
	pose = lerp_pose(0.2)
	points = bone.build_hand(pose, True)
	bone.plot_steam_hand(points, "Lerped Pose")

	for i in [x * 0.1 for x in range(0, 10)]:
		pose = lerp_pose(i)
		points = bone.build_hand(pose, True)
		bone.plot_steam_hand(points, "Lerped Pose "+str(i))
