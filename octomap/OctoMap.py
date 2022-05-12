from datetime import datetime
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
import pandas as pd
import xlwt

from Config import URI, LOGGER, TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION, WHETHER_FLY, OBSTACLE_HEIGHT, TAKEOFF_HEIGHT
from Config import SIDE_LENGTH,FLIGHT_SPEED, SAVE_FLYING_DATA
from OctoTree import OctoTree
from PathPlan import PathPlan
from MapUtil import get_log_config, parse_log_data, get_end_point


class OctoMap:
    def __init__(self):
        self.octotree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
        self.path_planner = PathPlan()
        self.counter = 0
        self.start_points_data = []
        self.end_points_data = []
        LOGGER.info("OctoTree has been build, the coordinate range is from {} to {}".
        format(-TREE_RESOLUTION * math.pow(2, TREE_MAX_DEPTH) / 2, TREE_RESOLUTION * math.pow(2, TREE_MAX_DEPTH) / 2))
        
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
            try:
                lmap = get_log_config()
                self.cf.log.add_config(lmap)
                lmap.data_received_cb.add_callback(self.update_map)
                lmap.start()
                LOGGER.info("Log has been configured.")
            except KeyError as e:
                LOGGER.error('Could not start log configuration,''{} not found in TOC'.format(str(e)))
            except AttributeError:
                LOGGER.error('Could not add Measurement log config, bad configuration.')
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

    def export_flying_data(self,start_points,end_points):
        value = datetime.today()
        date_value = datetime.strftime(value,'%H:%M:%S')

        label_start_points = ('start_points', date_value,len(start_points))
        start_points_tempcsv = pd.DataFrame(columns=label_start_points, data=start_points)
        start_points_tempcsv.to_csv('start_points.csv', encoding='gbk')

        label_end_points = ('end_points', date_value,len(end_points))
        end_points_tempcsv = pd.DataFrame(columns=label_end_points, data=end_points)
        end_points_tempcsv.to_csv('end_points.csv', encoding='gbk')
       


    def update_map(self, timestamp, data, logconf):
        
        # start_time = time.time()
        measurement, start_point = parse_log_data(data)
        for i in range(4):
            self.start_points_data.append(tuple(start_point))
        end_points = get_end_point(start_point, measurement)
        self.end_points_data.extend(end_points)
        if SAVE_FLYING_DATA:
            self.export_flying_data(self.start_points_data,self.end_points_data)
        for end_point in end_points:
            self.octotree.ray_casting(tuple(start_point), tuple(end_point))

        # export nodes each 100 times ranging
        self.counter += 1
        # TODO: new a thread to export
        if self.counter % 100 == 0:
            self.octotree.export_known_voxel()
        
        # end_time = time.time()
        # print('Running time: %s s' % ((end_time - start_time)))
    
    #TODO: Random Search Path Planning
    def plan_path(self, start_point=(0, 0, 0), end_point=(10, 10, 10)):
        path: list = self.path_planner.planning(start_point, end_point)
        return path
