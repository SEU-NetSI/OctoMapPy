"""
This script shows the basic use of the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

The MotionCommander uses velocity setpoints.

Change the URI variable to your Crazyflie configuration.
"""
from codecs import lookup_error
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        with MotionCommander(scf,0.1) as mc:
            # mc.circle_right(0.2, velocity=0.1, angle_degrees=360)

            height=30   # Obstacle height  cm
            max_counter = height/10 
            loop_counter=0
            while loop_counter < max_counter:
                time.sleep(1)
                # m m/s
                mc.right(0.5,velocity=0.1)
                # degree
                mc.turn_left(90)
                mc.right(0.5,velocity=0.1)
                
                mc.turn_left(90)
                mc.right(0.5,velocity=0.1)
                
                mc.turn_left(90)
                mc.right(0.5,velocity=0.1)
                mc.turn_left(90)
                
                mc.up(0.1)
                loop_counter+=1
            
            print("Done")
            mc.stop()

            
