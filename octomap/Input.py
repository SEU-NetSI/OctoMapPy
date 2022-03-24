import logging
import math
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie

from cflib.crazyflie.log import LogConfig
import numpy as np

from octomap.Config import PLOT_SENSOR_DOWN, SENSOR_TH, URI

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

class Input:
    def __init__(self) -> None:
        self.main()

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
        self.get_end_point(measurement)
        # self.canvas.set_measurement(measurement)

    def rot(self, roll, pitch, yaw, origin, point):
        cosr = math.cos(math.radians(roll))
        cosp = math.cos(math.radians(pitch))
        cosy = math.cos(math.radians(yaw))

        sinr = math.sin(math.radians(roll))
        sinp = math.sin(math.radians(pitch))
        siny = math.sin(math.radians(yaw))

        roty = np.array([[cosy, -siny, 0],
                         [siny, cosy, 0],
                         [0, 0,    1]])

        rotp = np.array([[cosp, 0, sinp],
                         [0, 1, 0],
                         [-sinp, 0, cosp]])

        rotr = np.array([[1, 0,   0],
                         [0, cosr, -sinr],
                         [0, sinr,  cosr]])

        rotFirst = np.dot(rotr, rotp)

        rot = np.array(np.dot(rotFirst, roty))

        tmp = np.subtract(point, origin)
        tmp2 = np.dot(rot, tmp)
        return np.add(tmp2, origin)

    def rotate_and_create_points(self, m, start_point):
        data = []
        roll = m['roll']
        pitch = -m['pitch']
        yaw = m['yaw']

        # if (m['up'] < SENSOR_TH):
        #     up = [start_point[0], start_point[1], start_point[2] + m['up'] / 1000.0]
        #     data.append(self.rot(roll, pitch, yaw, start_point, up))

        # if (m['down'] < SENSOR_TH and PLOT_SENSOR_DOWN):
        #     down = [start_point[0], start_point[1], start_point[2] - m['down'] / 1000.0]
        #     data.append(self.rot(roll, pitch, yaw, start_point, down))

        # if (m['left'] < SENSOR_TH):
        #     left = [start_point[0], start_point[1] + m['left'] / 1000.0, start_point[2]]
        #     data.append(self.rot(roll, pitch, yaw, start_point, left))

        # if (m['right'] < SENSOR_TH):
        #     right = [start_point[0], start_point[1] - m['right'] / 1000.0, start_point[2]]
        #     data.append(self.rot(roll, pitch, yaw, start_point, right))

        if (m['front'] < SENSOR_TH):
            front = [start_point[0] + m['front'] / 1000.0, start_point[1], start_point[2]]
            data.append(self.rot(roll, pitch, yaw, start_point, front))

        # if (m['back'] < SENSOR_TH):
        #     back = [start_point[0] - m['back'] / 1000.0, start_point[1], start_point[2]]
        #     data.append(self.rot(roll, pitch, yaw, start_point, back))

        return data
                     
    def get_end_point(self, measurement: dict):
        start_point = [
            measurement['stateEstimate.x'],
            measurement['stateEstimate.y'],
            measurement['stateEstimate.z']
        ]

        data = self.rotate_and_create_points(measurement, start_point)
        return data

        # TODO: 1->6
        # for i in range(1):
        #     if (i < len(data)):
        #         self.lines[i].set_data(np.array([start_point, data[i]]))
        #     else:
        #         self.lines[i].set_data(np.array([start_point, start_point]))        