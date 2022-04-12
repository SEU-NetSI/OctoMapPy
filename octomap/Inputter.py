import logging
import math
import xlwt
import pandas as pd

import cflib.crtp
from cflib.crazyflie import Crazyflie

from cflib.crazyflie.log import LogConfig
import numpy as np

from Config import PLOT_SENSOR_DOWN, SENSOR_TH, URI
from Config import TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION
from OctoTree import OctoTree

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

class Inputter:
    def __init__(self):
        self.start_point_list = []
        self.end_point_list = []
        self.main()

    def main(self):
        # Initialize the low-level drivers
        cflib.crtp.init_drivers()
        self.cf = Crazyflie(ro_cache=None, rw_cache='cache')

        # Connect callbacks from the Crazyflie API
        try:
            self.cf.connected.add_callback(self.connected)
        except:
            print ("Connect failed.")
        self.cf.disconnected.add_callback(self.disconnected)

        # Connect to the Crazyflie
        self.cf.open_link(URI)
        
    
    def after(self):
        myTree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
        for index in range(len(self.end_point_list)):
            myTree.ray_casting(self.start_point_list[index], self.end_point_list[index])
        myTree.visualize()
    
    def connected(self, URI):
        print('We are now connected to {}'.format(URI))

        # The definition of the logconfig
        lmap = LogConfig(name='Mapping', period_in_ms=100)
        
        lmap.add_variable('stateEstimateZ.x')
        lmap.add_variable('stateEstimateZ.y')
        lmap.add_variable('stateEstimateZ.z')
        
        # lmap.add_variable('range.front')
        # lmap.add_variable('range.back')
        lmap.add_variable('range.front')
        # lmap.add_variable('range.left')
        # lmap.add_variable('range.right')
        # lmap.add_variable('range.zrange')

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

    def disconnected(self, URI):
        print('Disconnected')
        print("start_point_list: ", self.start_point_list)
        print("end_point_list: ", self.end_point_list)

        # Output points to xls file
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_start = workbook.add_sheet('start_point_list')
        sheet_end = workbook.add_sheet('end_point_list')
        sheet_start.write(0,0,label = 'x')
        sheet_start.write(0,1,label = 'y')
        sheet_start.write(0,2,label = 'z')
        sheet_end.write(0,0,label = 'x')
        sheet_end.write(0,1,label = 'y')
        sheet_end.write(0,2,label = 'z')
        for i in range(len(self.start_point_list)):
            sheet_start.write(i+1,0,self.start_point_list[i][0])
            sheet_start.write(i+1,1,self.start_point_list[i][1])
            sheet_start.write(i+1,2,self.start_point_list[i][2])
        for i in range(len(self.end_point_list)):
            sheet_end.write(i + 1, 0, self.end_point_list[i][0])
            sheet_end.write(i + 1, 1, self.end_point_list[i][1])
            sheet_end.write(i + 1, 2, self.end_point_list[i][2])
        workbook.save("D:/github/myproject/octomap/point_list.xls")


        # fw_start = open("D:/github/myproject/octomap/start_point_list.txt", 'w') # parameter: filename  mode               
        # for line in self.start_point_list:
        #     fw_start.write(str(line)+'\n')
        # # fw.write(str(self.start_point_list)) 
        # fw_start.close()
        # fw_end = open("D:/github/myproject/octomap/end_point_list.txt", 'w') # parameter: filename  mode               
        # for line in  self.end_point_list:
        #     fw_end.write(str(line)+'\n')
        # # fw.write(str( self.end_point_list)) 
        # fw_end.close()

    def mapping_data(self, timestamp, data, logconf):
        measurement = {
            # cm
            'x': data['stateEstimateZ.x'] / 10,
            'y': data['stateEstimateZ.y'] / 10,
            'z': data['stateEstimateZ.z'] / 10,
            # ±90, ±90, ±180
            'roll': round(data['stabilizer.roll'], 2),
            'pitch': round(data['stabilizer.pitch'], 2),
            'yaw': round(data['stabilizer.yaw'], 2),
            # cm
            'front': data['range.front'] / 10,
            # 'back': data['range.back'] / 10,
            # 'up': data['range.up'] / 10,
            # 'down': data['range.zrange'] / 10,
            # 'left': data['range.left'] / 10,
            # 'right': data['range.right']  / 10
        }
        self.get_end_point(measurement)
        # self.canvas.set_measurement(measurement)

    def rot(self, roll, pitch, yaw, origin, point):
        """
        Calculate the real coordinates of the target using two points

        origin:Sensor location coordinates
        point:position coordinates return using sensor distance
        
        """
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
        res = np.around(np.add(tmp2, origin), decimals=1)
        return tuple(res.tolist())

    def rotate_and_create_points(self, measurement, start_point):
        end_points = []
        roll = measurement['roll']
        pitch = -measurement['pitch']
        yaw = measurement['yaw']

        # if (measurement['up'] < SENSOR_TH):
        #     up = [start_point[0], start_point[1], start_point[2] + measurement['up'] / 1000.0]
        #     end_points.append(self.rot(roll, pitch, yaw, start_point, up))

        # if (measurement['down'] < SENSOR_TH and PLOT_SENSOR_DOWN):
        #     down = [start_point[0], start_point[1], start_point[2] - measurement['down'] / 1000.0]
        #     end_points.append(self.rot(roll, pitch, yaw, start_point, down))

        # if (measurement['left'] < SENSOR_TH):
        #     left = [start_point[0], start_point[1] + measurement['left'] / 1000.0, start_point[2]]
        #     end_points.append(self.rot(roll, pitch, yaw, start_point, left))

        # if (measurement['right'] < SENSOR_TH):
        #     right = [start_point[0], start_point[1] - measurement['right'] / 1000.0, start_point[2]]
        #     end_points.append(self.rot(roll, pitch, yaw, start_point, right))

        if (measurement['front'] < SENSOR_TH):
            front = [start_point[0] + measurement['front'], start_point[1], start_point[2]]
            end_points.append(self.rot(roll, pitch, yaw, start_point, front))

        # if (measurement['back'] < SENSOR_TH):
        #     back = [start_point[0] - measurement['back'] / 1000.0, start_point[1], start_point[2]]
        #     end_points.append(self.rot(roll, pitch, yaw, start_point, back))

        return end_points
                     
    def get_end_point(self, measurement: dict):
        start_point = [
            int(measurement['x']),
            int(measurement['y']),
            int(measurement['z'])
        ]
        print("measurement: ", measurement)

        end_points = self.rotate_and_create_points(measurement, start_point)
        for end_point in end_points:
            print("end_point: ", end_point)
            self.end_point_list.append(end_point)
            self.start_point_list.append(tuple(start_point))

        if len(self.end_point_list) == 100:
            self.cf.close_link()

        # TODO: 1->6
        # for i in range(1):
        #     if (i < len(data)):
        #         self.lines[i].set_data(np.array([start_point, data[i]]))
        #     else:
        #         self.lines[i].set_data(np.array([start_point, start_point]))        
