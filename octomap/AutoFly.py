
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
import pandas as pd

from Config import TREE_RESOLUTION, URI, LOGGER, TAKEOFF_HEIGHT, FLIGHT_SPEED

class AutoFly:
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
    
    def import_rrt_path(self):
        rrt_path_list = []     
        rrt_path=pd.read_csv('rrt_path.csv', index_col=0)
        rrt_path_list = rrt_path.values.tolist()
        return rrt_path_list

    def fly_path(self):
        fly_path = []
        RRT_path = self.import_rrt_path()
        fly_path_temp = RRT_path[::5]
        for data in fly_path_temp:
            fly_path.append((data[0] * TREE_RESOLUTION / 100,
                             data[1] * TREE_RESOLUTION / 100,
                             data[2] * TREE_RESOLUTION / 100))
        return fly_path

    def connect(self, URI):
        self.cf.open_link(URI)
        LOGGER.info('We are now connected to {}'.format(URI))
        fly_path = self.fly_path()
        with SyncCrazyflie(URI, cf=self.cf) as scf:
            print("ready to fly")
            with PositionHlCommander(crazyflie=scf, 
                                    x=0.0, y=0.0, z=0.0,
                                    default_height=TAKEOFF_HEIGHT,
                                    default_velocity=FLIGHT_SPEED,
                                    controller=PositionHlCommander.CONTROLLER_PID) as pc:
                for data in fly_path:
                    pc.go_to(data[0],data[1],data[2])
                print('done')
                    

    def connected(self, URI):
        LOGGER.info('Connected with {}'.format(URI))

    def disconnected(self, URI):
        LOGGER.info('Disconnected with {}'.format(URI))

def main():
    flying = AutoFly()
    flying.start()

if __name__=="__main__":
    main()