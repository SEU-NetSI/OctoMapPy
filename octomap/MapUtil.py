import math
from datetime import datetime

import numpy as np
import pandas as pd
import xlwt
from cflib.crazyflie.log import LogConfig

from Config import SENSOR_TH, WIDTH, FREE_LOGODDS, LOGGER, OCCUPANY_LOGODDS, TREE_RESOLUTION


"""
OctoMap
"""
def determine_threshold(point: tuple):
    temp = list(point)
    temp[0] = np.clip(temp[0], a_min=-WIDTH / 2, a_max=WIDTH / 2)
    temp[1] = np.clip(temp[1], a_min=-WIDTH / 2, a_max=WIDTH / 2)
    temp[2] = np.clip(temp[2], a_min=-WIDTH / 2, a_max=WIDTH / 2)
    res = tuple(temp)
    return res

def rot(roll, pitch, yaw, origin, point):
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
    return determine_threshold(tmp4)

def rotate_and_create_points(measurement, start_point):
    end_points = []
    roll = measurement['roll']
    pitch = -measurement['pitch']
    yaw = measurement['yaw']

    if (measurement['front'] < SENSOR_TH):
        front = [start_point[0] + measurement['front'], start_point[1], start_point[2]]
        end_points.append(rot(roll, pitch, yaw, start_point, front))
    
    if (measurement['back'] < SENSOR_TH):
        back = [start_point[0] - measurement['back'], start_point[1], start_point[2]]
        end_points.append(rot(roll, pitch, yaw, start_point, back))
    
    if (measurement['left'] < SENSOR_TH):
        left = [start_point[0], start_point[1] + measurement['left'], start_point[2]]
        end_points.append(rot(roll, pitch, yaw, start_point, left))

    if (measurement['right'] < SENSOR_TH):
        right = [start_point[0], start_point[1] - measurement['right'] , start_point[2]]
        end_points.append(rot(roll, pitch, yaw, start_point, right))

    return end_points

def get_end_point(start_point: list, measurement: dict):
    end_points = rotate_and_create_points(measurement, start_point)
    return end_points

def get_log_config():
    lmap = LogConfig(name='Mapping', period_in_ms=100)
    
    lmap.add_variable('stateEstimateZ.x')
    lmap.add_variable('stateEstimateZ.y')
    lmap.add_variable('stateEstimateZ.z')
    
    lmap.add_variable('range.front')
    lmap.add_variable('range.back')
    lmap.add_variable('range.left')
    lmap.add_variable('range.right')

    lmap.add_variable('stabilizer.roll')
    lmap.add_variable('stabilizer.pitch')
    lmap.add_variable('stabilizer.yaw')
    
    return lmap

def parse_log_data(data):
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
        'left': data['range.left'] / 10,
        'right': data['range.right']  / 10
    }
    start_point = [
        int(measurement['x']),
        int(measurement['y']),
        int(measurement['z'])
    ]
    return measurement, start_point


"""
OctoTree
"""
def bresenham3D(startPoint, endPoint):
    """
    Use bresenham algorithm to return points on the ray's path
    """
    path = []

    startPoint = [int(startPoint[0]), int(startPoint[1]), int(startPoint[2])]
    endPoint = [int(endPoint[0]), int(endPoint[1]), int(endPoint[2])]
    endpoint_origin = [int(endPoint[0] / TREE_RESOLUTION) * TREE_RESOLUTION, 
                        int(endPoint[1] / TREE_RESOLUTION) * TREE_RESOLUTION, 
                        int(endPoint[2] / TREE_RESOLUTION) * TREE_RESOLUTION]

    steepXY = (np.abs(endPoint[1] - startPoint[1]) > np.abs(endPoint[0] - startPoint[0]))
    if steepXY:
        startPoint[0], startPoint[1] = startPoint[1], startPoint[0]
        endPoint[0], endPoint[1] = endPoint[1], endPoint[0]

    steepXZ = (np.abs(endPoint[2] - startPoint[2]) > np.abs(endPoint[0] - startPoint[0]))
    if steepXZ:
        startPoint[0], startPoint[2] = startPoint[2], startPoint[0]
        endPoint[0], endPoint[2] = endPoint[2], endPoint[0]

    delta = [np.abs(endPoint[0] - startPoint[0]), np.abs(endPoint[1] - startPoint[1]),
                np.abs(endPoint[2] - startPoint[2])]

    errorXY = delta[0] / 2
    errorXZ = delta[0] / 2

    step = [
        -TREE_RESOLUTION if startPoint[0] > endPoint[0] else TREE_RESOLUTION,
        -TREE_RESOLUTION if startPoint[1] > endPoint[1] else TREE_RESOLUTION,
        -TREE_RESOLUTION if startPoint[2] > endPoint[2] else TREE_RESOLUTION
    ]

    y = startPoint[1]
    z = startPoint[2]

    for x in range(startPoint[0], endPoint[0], step[0]):
        point = [x, y, z]
        if steepXZ:
            point[0], point[2] = point[2], point[0]
        if steepXY:
            point[0], point[1] = point[1], point[0]
            
        errorXY -= delta[1]
        errorXZ -= delta[2]
        if errorXY < 0:
            y += step[1]
            errorXY += delta[0]
        if errorXZ < 0:
            z += step[2]
            errorXZ += delta[0]

        if (point != endpoint_origin):
            path.append(point)
    return path

def export_known_voxel(leaf_node_list):
    LOGGER.info("leaf_node_list: {}".format(len(leaf_node_list)))
    threshold_node_list: list = get_threshold_node_list(leaf_node_list)
    LOGGER.info("threshold_node_list: {}".format(len(threshold_node_list)))
    occu_node_list, free_node_list = get_classified_node_list(threshold_node_list)
    occu_node_coor_list, free_node_coor_list = get_classified_node_coor_list(occu_node_list, free_node_list)
    LOGGER.info("length of occu_node_coor_list: {}".format(len(occu_node_coor_list)))
    LOGGER.info("length of free_node_coor_list: {}".format(len(free_node_coor_list)))   

    # Output points to csv 
    value = datetime.today()
    date_value = datetime.strftime(value,'%H:%M:%S')

    label_occu = ('occu_node_coor_list', date_value,len(occu_node_coor_list))
    occu_node_tempcsv = pd.DataFrame(columns=label_occu, data=occu_node_coor_list)
    occu_node_tempcsv.to_csv('occu_node_coor_list.csv', encoding='gbk')

    label_free = ('free_node_coor_list', date_value,len(free_node_coor_list))
    free_node_tempcsv = pd.DataFrame(columns=label_free, data=free_node_coor_list)
    free_node_tempcsv.to_csv('free_node_coor_list.csv', encoding='gbk')
    

def get_threshold_node_list(leaf_node_list):
    """
    Store leaf nodes with deterministic probability
    """
    threshold_node_list = []
    for node in leaf_node_list:
        if node.get_log_odds() == OCCUPANY_LOGODDS or node.get_log_odds() == FREE_LOGODDS:
            threshold_node_list.append(node)
    return threshold_node_list

def get_classified_node_list(threshold_node_list):
    """
    Separate occupied and free points 
    """
    occu_node_list: list = []
    free_node_list: list = []

    for node in threshold_node_list:
        if node.get_log_odds() == OCCUPANY_LOGODDS:
            occu_node_list.append(node)
        if node.get_log_odds() == FREE_LOGODDS:
            free_node_list.append(node)
    
    return occu_node_list, free_node_list

def get_classified_node_coor_list(occu_node_list, free_node_list):
    """
    Use list to store the corresponding coordinates 
    """        
    occu_node_coor_list = []
    free_node_coor_list = []

    for node in occu_node_list:
        node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), 
                    int(node.get_origin()[1] / TREE_RESOLUTION), 
                    int(node.get_origin()[2] / TREE_RESOLUTION))
        occu_node_coor_list.append(node_coor)
    for node in free_node_list:
        node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), 
                    int(node.get_origin()[1] / TREE_RESOLUTION), 
                    int(node.get_origin()[2] / TREE_RESOLUTION))
        free_node_coor_list.append(node_coor)

    return occu_node_coor_list, free_node_coor_list
