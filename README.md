# OctoMap in Python
OctoMap is an efficient probabilistic 3D mapping framework based on Octrees. This is a python-based implementation of the [OctoMap](http://octomap.github.io/) described in: 

```
Hornung, Armin, et al. "OctoMap: An efficient probabilistic 3D mapping framework based on octrees." Autonomous robots 34.3 (2013): 189-206.
```

In this repository, we provide a basic implementation of OctoMap, a visualization tool and a path plan algorithm (RRT) working with OctoMap.

# Config
TREE_CENTER：Indicates an area that can be represented by an octree centered on this point. When the insertion point exceeds this area, the error "Point is not contained in node." will be prompted

SENSOR_TH：The distance measurement of the VL53L1X series laser sensor used by the Multi-ranger deck in this project is accurate within 400cm. This value is determined by the configuration of the selected sensor

WIDTH： The width of the experimental scene, determined by the area supported by the light-house in this project. When the insertion point is larger than this range, the point is shrunk to the boundary of the experimental scene

Offset： Place Crazyflie at the center point of the light-house area, and get the coordinates of the corresponding point. When doing visualization processing, you need to add an offset to convert all of them to points in the first quadrant 
(the initialization values of the visualization coordinate voxels are all positive values)

URI: Change the URI variable to your Crazyflie configuration.

# Install
`pip install` will be provided soon.