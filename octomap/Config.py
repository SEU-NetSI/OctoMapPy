import logging
import math

"""
The probability change for each new observation.
The default value is from the '5.1 Evaluation - Sensor model for laser range data' of the OctoMap Paper.
"""
HIT_LOGODDS=0.85
HIT_PROBABILITY=0.7    
MISS_LOGODDS=-0.4
MISS_PROBABILITY=0.4

"""
The probability threshold for occupany and free.
If there is not threshold, the status change will be very hard and not in time. 
When the probability of the voxel is arrived at the threshold, it indicates the voxel has been set occupied/free status.
"""
OCCUPANY_LOGODDS=3.5
OCCUPANY_PROBABILITY=0.97
FREE_LOGODDS=-2
FREE_PROBABILITY=0.12

"""
Initial probability value.
"""
DEFAULT_PROBABILITY=0.5
DEFAULT_LOGODDS=0

"""
Shape of the OctoTree, a cube with the same width, length and the height.
TREE_RESOLUTION (cm): the size of each voxel.
TREE_MAX_DEPTH: the recursion of the tree.
So, the size of the OctoTree is TREE_RESOLUTION * 2^TREE_MAX_DEPTH.
"""
TREE_RESOLUTION=4
TREE_MAX_DEPTH=6
# TREE_CENTER=(math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2)
# TODO: The setting of the midpoint changes the output
TREE_CENTER=(0, 0, 0)     # regional center point

"""
Crazyflie and its laser sensor.
"""
URI='radio://0/80/2M/E7E7E7E7E7'
SENSOR_TH=400
PLOT_SENSOR_DOWN=False
WHETHER_FLY=True

"""
Visualization.
The coornidate under the OctoTree should be adjusted to the Matplotlib.
"""
# SPACE
WIDTH=TREE_RESOLUTION * math.pow(2, TREE_MAX_DEPTH)     # The width of the experimental scene
# Visualize point offsets
# Offset half the width of the experimental area so that all coordinate points are turned to positive values
Offset_x = math.pow(2, TREE_MAX_DEPTH) / 2
Offset_y = math.pow(2, TREE_MAX_DEPTH) / 2
Offset_z = math.pow(2, TREE_MAX_DEPTH) / 2
#Animation effect for RRT algorithm display
Show_Animation = True

#RRT Path Planning
GoalSampleRate = 0.05    # The probability of picking the target point
Expand_Step = 2          # step size per growth
Start_Point = (0, 0, 0)  # starting point
End_Point = (10, 10, 10) # end point

# Only output errors from the logging framework
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
