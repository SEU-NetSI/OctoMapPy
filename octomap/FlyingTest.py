import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander

from Config import URI, LOGGER, WHETHER_FLY, OBSTACLE_HEIGHT, TAKEOFF_HEIGHT, SIDE_LENGTH,FLIGHT_SPEED

class FlyingTest:
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
                    
                    flying_height = TAKEOFF_HEIGHT
                    up_times_total = (OBSTACLE_HEIGHT - TAKEOFF_HEIGHT) * 10
                    up_times_real = 0
                    while up_times_real <= up_times_total:
                        pc.set_default_height(flying_height)
                        pc.go_to(0, 0)
                        pc.go_to(0, -SIDE_LENGTH)
                        pc.go_to(SIDE_LENGTH, -SIDE_LENGTH)   
                        pc.go_to(SIDE_LENGTH, 0)
                        pc.go_to(0, 0)
                        print(pc.get_position())
                        flying_height += 0.1
                        up_times_real += 1
                    print('done')
                    

    def connected(self, URI):
        LOGGER.info('Connected with {}'.format(URI))

    def disconnected(self, URI):
        LOGGER.info('Disconnected with {}'.format(URI))

def main():
    flyingTest = FlyingTest()
    flyingTest.start()

if __name__=="__main__":
    main()