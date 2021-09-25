# glb reader
import json
import numpy as np

with open('assets/glb.json') as f:
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
print(decoded)
np.save('decoded', decoded)

# Try Plotting
import bone

# Ignore the AUX
decoded = decoded[1:27, :, :]

print(decoded.shape)
points = bone.build_hand(decoded, True)
bone.plot_steam_hand(points, "Lerped Pose")