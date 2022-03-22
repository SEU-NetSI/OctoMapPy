import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from pandas import DataFrame

from octomap.Config import URI

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

class Input:
    def __init__(self) -> None:
        self.main()
        pass

    def main(self):
        # Initialize the low-level drivers
        cflib.crtp.init_drivers()
        self.cf = Crazyflie(ro_cache=None, rw_cache='cache')

        # Connect callbacks from the Crazyflie API
        self.cf.connected.add_callback(self.connected)
        self.cf.disconnected.add_callback(self.disconnected)

        # Connect to the Crazyflie
        self.cf.open_link(URI)
    
    def connected(self, URI):
        print('We are now connected to {}'.format(URI))

        # The definition of the logconfig
        lmap = LogConfig(name='Mapping', period_in_ms=100)
        lmap.add_variable('stateEstimate.x')
        lmap.add_variable('stateEstimate.y')
        lmap.add_variable('stateEstimate.z')

        lmap.add_variable('range.front')
        lmap.add_variable('range.back')
        lmap.add_variable('range.up')
        lmap.add_variable('range.left')
        lmap.add_variable('range.right')
        lmap.add_variable('range.zrange')

        lmap.add_variable('stabilizer.roll')
        lmap.add_variable('stabilizer.pitch')
        lmap.add_variable('stabilizer.yaw')

        try:
            self.cf.log.add_config(lmap)
            lmap.data_received_cb.add_callback(self.mapping_data)
            lmap.start()
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add Measurement log config, bad configuration.')

    def mapping_data(self, timestamp, data, logconf):
        measurement = {
            'x': data['stateEstimate.x'],
            'y': data['stateEstimate.y'],
            'y': data['stateEstimate.z'],

            'roll': data['stabilizer.roll'],
            'pitch': data['stabilizer.pitch'],
            'yaw': data['stabilizer.yaw'],
            
            'front': data['range.front'],
            'back': data['range.back'],
            'up': data['range.up'],
            'down': data['range.zrange'],
            'left': data['range.left'],
            'right': data['range.right']
        }
        # self.canvas.set_measurement(measurement)

