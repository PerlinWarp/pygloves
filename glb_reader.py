# glb reader
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as plt3d

import bone

def read_jsonglb(file_path):
	with open(file_path) as f:
	 	# Remove the binary data from the start and end of glb first
	 	data = json.load(f)

	decoded = []
	for i in data['nodes']:
		c = i['translation']
		x, y, z = c
		c = [x, y, z, 1]

		q = i['rotation']
		x, y, z, w = q
		q = w, x, y, z

		decoded.append(np.array([c,q]))

	decoded = np.array(decoded)
	# OpenGloves Skips the first root node
	decoded = decoded[1:,:,:]
	return decoded

def plot_glb(file_path, title="GlbPlot"):
	decoded = read_jsonglb(file_path)
	print("Glb shape: ", decoded.shape)
	print("Expected Shape:", "(31,2,4)")
	np.save('decoded', decoded)

	# 0th element should be root
	# 1st element should be wrist
	print("Root: ", decoded[0, :, :])
	print("Wrist: ", decoded[1, :, :])

	print(decoded.shape)
	points = bone.build_hand(decoded, True)
	# Plot the points
	# Plot setup
	fig = plt.figure(title)
	ax = fig.add_subplot(111, projection='3d')
	bone.plot_steam_hand(points, "Lerped Pose", ax=ax)

if __name__ == "__main__":
	file_path_skeleton = 'assets/vr_glove_right_skeleton.json'
	# json from danwillm glb
	file_path_dwm = 'assets/glb.json'

	plot_glb(file_path_skeleton, "vr_glove_right_skeletonon")
	plot_glb(file_path_dwm, "danwillm")
	plot_glb('assets/vr_glove_left_model.json','vr_glove_left_model')