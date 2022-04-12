import logging
import math

# STEP
HIT_LOGODDS=0.85
HIT_PROBABILITY=0.7
MISS_LOGODDS=-0.4
MISS_PROBABILITY=0.4
# THRESHOLD
OCCUPANY_LOGODDS=3.5
OCCUPANY_PROBABILITY=0.97
FREE_LOGODDS=-2
FREE_PROBABILITY=0.12
# DEFAULT
DEFAULT_PROBABILITY=0.5
DEFAULT_LOGODDS=0
# OCTOTREE
TREE_RESOLUTION=4
TREE_MAX_DEPTH=6

# TREE_CENTER=(math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2)
# TODO: The setting of the midpoint changes the output
TREE_CENTER=(50, 50 , 50)     

# Crazyflie
URI='radio://0/80/2M/E7E7E7E7E7'
SENSOR_TH=400
PLOT_SENSOR_DOWN=False
# Visualization
Offset_x = (math.pow(2, TREE_MAX_DEPTH) * TREE_RESOLUTION) / (2 *TREE_RESOLUTION)
Offset_y = (math.pow(2, TREE_MAX_DEPTH) * TREE_RESOLUTION) / (2 *TREE_RESOLUTION)
Offset_z = (10 / TREE_RESOLUTION)
# Only output errors from the logging framework
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()