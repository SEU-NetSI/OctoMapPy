import logging
import math

# STEP
HIT_LOGODDS=0.85
HIT_PROBABILITY=0.7    
MISS_LOGODDS=-0.4
MISS_PROBABILITY=0.4   # The probability value of each update when the occupied/free state is observed

# THRESHOLD
OCCUPANY_LOGODDS=3.5
OCCUPANY_PROBABILITY=0.97
FREE_LOGODDS=-2
FREE_PROBABILITY=0.12  # When the node probability is greater than or less than the threshold, 
                       # it indicates the occupied/free state
 
# DEFAULT
DEFAULT_PROBABILITY=0.5
DEFAULT_LOGODDS=0       # initial probability value

# OCTOTREE
TREE_RESOLUTION=4       # Spatial resolution:the smaller the value, the higher the spatial resolution
TREE_MAX_DEPTH=5        # When the resolution is determined, the larger the value, the larger the space that can be represented

# TREE_CENTER=(math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2,
#             math.pow(2 , TREE_MAX_DEPTH) * TREE_RESOLUTION / 2)
# TODO: The setting of the midpoint changes the output
TREE_CENTER=(50, 50 , 50)     # regional center point

# Crazyflie
URI='radio://0/80/2M/E7E7E7E7E7'  # URI to the Crazyflie to connect to
SENSOR_TH=400  # Sensor ranging threshold
PLOT_SENSOR_DOWN=False

# SPACE
WIDTH=256     # The width of the experimental scene

# Visualization
# Visualize point offsets
# Offset half the width of the experimental area so that all coordinate points are turned to positive values
# Offset_x = WIDTH / (2 *TREE_RESOLUTION) 
# Offset_y = WIDTH / (2 *TREE_RESOLUTION)
# Offset_z = 0
Offset_x = 0
Offset_y = 0
Offset_z = 0  

# Only output errors from the logging framework
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
