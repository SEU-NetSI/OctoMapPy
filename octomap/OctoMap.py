from email.policy import default
import math
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
import numpy as np

from Config import SENSOR_TH, URI, LOGGER, WIDTH
from Config import TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION
from OctoTree import OctoTree



class OctoMap:
    def __init__(self):
        self.octotree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
        self.counter = 0
        
    def start(self):
        # Initialize the low-level drivers
        cflib.crtp.init_drivers()
        self.cf = Crazyflie(rw_cache='cache')
        self.cf.connected.add_callback(self.connected)
        self.cf.disconnected.add_callback(self.disconnected)

        # Connect to the Crazyflie
        self.connect(URI)
    
    def connect(self, URI):
        LOGGER.info('We are now connected to {}'.format(URI))


        # with SyncCrazyflie(URI, cf=self.cf) as scf:
            # Config the log content
        self.cf.open_link(URI)
        logconf = LogConfig(name='Mapping', period_in_ms=100)
        logconf.add_variable('stateEstimateZ.x')
        logconf.add_variable('stateEstimateZ.y')
        logconf.add_variable('stateEstimateZ.z')
        
        logconf.add_variable('range.front')
        logconf.add_variable('range.back')
        # logconf.add_variable('range.up')
        # logconf.add_variable('range.left')
        # logconf.add_variable('range.right')
        # logconf.add_variable('range.zrange')

        logconf.add_variable('stabilizer.roll')
        logconf.add_variable('stabilizer.pitch')
        logconf.add_variable('stabilizer.yaw')
        print('test')
        # try:
        self.cf.log.add_config(logconf)
        print('test1')
        logconf.data_received_cb.add_callback(self.mapping_data)
        logconf.start()
            
                # with MotionCommander(scf, 0.2) as mc:
                #     height = 20   # Obstacle height  cm
                #     max_counter = height / 10 
                #     loop_counter = 0
                #     while loop_counter < max_counter:
                #         time.sleep(1)
                #         # m m/s
                #         mc.right(0.5,velocity=0.1)
                #         # degree
                #         mc.turn_left(90)
                #         mc.right(0.5,velocity=0.1)
                        
                #         mc.turn_left(90)
                #         mc.right(0.5,velocity=0.1)
                        
                #         mc.turn_left(90)
                #         mc.right(0.5,velocity=0.1)
                #         mc.turn_left(90)
                        
                #         # mc.up(0.1)
                #         loop_counter+=1

        # except KeyError as e:
        #     LOGGER.info('Could not start log configuration,'
        #           '{} not found in TOC'.format(str(e)))
        # except AttributeError:
        #     LOGGER.info('Could not add Measurement log config, bad configuration.')
        # finally:
        #     print("test2")
    def connected(self, URI):
        LOGGER.info('Connected')

    def disconnected(self, URI):
        LOGGER.info('Disconnected')

    def get_octotree(self):
        return self.octotree

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
            'back': data['range.back'] / 10,
            # 'up': data['range.up'] / 10,
            # 'down': data['range.zrange'] / 10,
            # 'left': data['range.left'] / 10,
            # 'right': data['range.right']  / 10
        }
        start_point = [
            int(measurement['x']),
            int(measurement['y']),
            int(measurement['z'])
        ]
        LOGGER.info("measurement: {}".format(measurement))
        end_points = self.get_end_point(start_point, measurement)
        # LOGGER.info("end_points: {}".format(end_points))
        for end_point in end_points:
            self.octotree.ray_casting(tuple(start_point), tuple(end_point))

        # export nodes each 100 times ranging
        self.counter += 1
        # TODO: new a thread to export
        if self.counter % 100 == 0:
            self.octotree.export_known_node()

    def determine_threshold(self, point: tuple):
        """
        Determine whether it exceeds the scope of lighthouse and return the corresponding point
        """
        temp = list(point)
        temp[0] = np.clip(temp[0], a_min=-WIDTH / 2, a_max=WIDTH / 2)
        temp[1] = np.clip(temp[1], a_min=-WIDTH / 2, a_max=WIDTH / 2)
        temp[2] = np.clip(temp[2], a_min=-WIDTH / 2, a_max=WIDTH / 2)
        res = tuple(temp)
        return res


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
        tmp3 = np.around(np.add(tmp2, origin), decimals=1)
        tmp4 = tuple(tmp3.tolist())
        return self.determine_threshold(tmp4)

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
                     
    def get_end_point(self, start_point: list, measurement: dict):
        end_points = self.rotate_and_create_points(measurement, start_point)
        return end_points
