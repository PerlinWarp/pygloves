# pygloves-utils  
  
It would be nice to see if LucidGloves work without having to start SteamVR.
This repo attempts to plot glb files in the same was as Steam, so that you can test out experimental designs, such as gloves with potentiometers per finger joint, without having to get it working with Steam, etc    
  
```
pip install numpy
pip install matplotlib

python lerp_slider.py
```

#### bone.py  
Attempts to plot the OpenGloves glb file.   
The glb file is hierarchical, so the end of the finger cannot just be plotted, it has to be calculated by considering the other points in the finger. Relative positions have to be built into global positons.
  
#### Useful links  
[glb/gltf2.0 refrence guide](https://www.khronos.org/files/gltf20-reference-guide.pdf)  
[OpenVR Hand Skeleton Docs](https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton)  
[3Blue1Brown, Visualizing quaternions](https://www.youtube.com/watch?v=d4EgbgTm0Bg)  
