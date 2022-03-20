import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils.multiranger import Multiranger

import OctoTree
from Config import TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH

URI = 'radio://0/80/2M'

def get_lidar_point():
    cflib.crtp.init_drivers(enable_debug_driver=False)

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        with Multiranger(scf) as multi_ranger:
            while True:
                item = {
                    "front": multi_ranger.front,
                    "back": multi_ranger.back,
                    "left": multi_ranger.left,
                    "right": multi_ranger.right,
                    "up": multi_ranger.up
                }

                time.sleep(1)


def main():
    octotree: OctoTree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
    get_lidar_point()


if __name__ == "__main__":
    main()
