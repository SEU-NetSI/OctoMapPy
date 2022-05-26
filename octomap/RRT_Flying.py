import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander

from Config import URI, LOGGER, WHETHER_FLY, TAKEOFF_HEIGHT, FLIGHT_SPEED

class RRT_Flying:
    def __init__(self):
        pass

    def start(self):
        cflib.crtp.init_drivers()
        self.cf = Crazyflie(ro_cache=None, rw_cache='cache')
        
        # Connect callbacks from the Crazyflie API
        self.cf.connected.add_callback(self.connected)
        self.cf.disconnected.add_callback(self.disconnected)

        # Connect to the Crazyflie
        self.connect(URI)
        # self.cf.open_link(URI)
    
    def connect(self, URI):
        self.cf.open_link(URI)
        LOGGER.info('We are now connected to {}'.format(URI))
        with SyncCrazyflie(URI, cf=self.cf) as scf:
            if WHETHER_FLY:
                print("ready to fly")
                with PositionHlCommander(crazyflie=scf, 
                                        x=0.0, y=0.0, z=0.0,
                                        default_height=TAKEOFF_HEIGHT,
                                        default_velocity=FLIGHT_SPEED,
                                        controller=PositionHlCommander.CONTROLLER_PID) as pc:
                    
                    print('done')
                    

    def connected(self, URI):
        LOGGER.info('Connected with {}'.format(URI))

    def disconnected(self, URI):
        LOGGER.info('Disconnected with {}'.format(URI))

def main():
    flying = RRT_Flying()
    flying.start()

if __name__=="__main__":
    main()