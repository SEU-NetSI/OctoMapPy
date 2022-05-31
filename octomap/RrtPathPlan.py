import random
from datetime import datetime
import math
import copy
from matplotlib import pyplot as plt
import numpy as np

import pandas as pd

from MapUtil import import_known_free_node, import_known_occu_node
from Config import GOAL_SAMPLE_RATE, EXPAND_STEP, OFFSETX, OFFSETY, OFFSETZ,SHOW_ANIMATION_RRT,INDICE_LENGTH

class Node:
    def __init__(self, value_x, value_y, value_z):
        self.value_x = value_x
        self.value_y = value_y
        self.value_z = value_z
        self.parent = None

class RrtPathPlan:
    def __init__(self):
        self.node_list = []

    def random_node(self):
        """
        Randomly pick from free_nodes and return
        """
        free_node_coor_list = import_known_free_node()
        node = random.sample(free_node_coor_list, 1)[0]
        return node

    def collision_check(self, new_node):
        occu_node_coor_list = import_known_occu_node()
        a = 1
        size = 1  # The space occupied by the obstacle
        for (obstacle_x, obstacle_y, obstacle_z) in occu_node_coor_list:
            dx = obstacle_x - new_node.value_x
            dy = obstacle_y - new_node.value_y
            dz = obstacle_z - new_node.value_z
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            if d <= size:
                a = 0  # collision
        return a  # safe
    
    def planning(self, start_point, end_point):
        """
        Path planning
        """
        self.start = Node(start_point[0], start_point[1], start_point[2])
        self.end = Node(end_point[0], end_point[1], end_point[2])
        self.node_list = [self.start]

        while True:
            if random.random() > GOAL_SAMPLE_RATE:
                random_new_node = self.random_node()
            else:
                random_new_node = [self.end.value_x, self.end.value_y, self.end.value_z]

            # Find nearest node
            min_index = self.get_nearest_list_index(self.node_list, random_new_node)
            
            # expand tree
            nearest_node = self.node_list[min_index]

            # grow a step along the direction of a random point at the nearest node
            path_len = math.sqrt((random_new_node[2] - nearest_node.value_z) ** 2 +
                                 (random_new_node[1] - nearest_node.value_y) ** 2 +
                                 (random_new_node[0] - nearest_node.value_x) ** 2)

            path_x_angle = (random_new_node[0] - nearest_node.value_x) / path_len
            path_y_angle = (random_new_node[1] - nearest_node.value_y) / path_len
            path_z_angle = (random_new_node[2] - nearest_node.value_z) / path_len

            new_node = copy.deepcopy(nearest_node)
            new_node.value_x += EXPAND_STEP * path_x_angle
            new_node.value_y += EXPAND_STEP * path_y_angle
            new_node.value_z += EXPAND_STEP * path_z_angle
            new_node.parent = min_index

            if not self.collision_check(new_node):
                # print("Wrong parameter,unable to plan path!!!")
                continue

            self.node_list.append(new_node)

            # Exit the loop when the target distance from the new_node is less than the step size
            d = math.sqrt((new_node.value_x - self.end.value_x) **2 + 
                          (new_node.value_y - self.end.value_y) **2 + 
                          (new_node.value_z - self.end.value_z) **2)
            if d <= EXPAND_STEP:
                break
            if SHOW_ANIMATION_RRT:
                self.draw_dynamic_graph(random_new_node)

        path = [(self.end.value_x, self.end.value_y, self.end.value_z)]
        last_index = len(self.node_list) - 1
        while self.node_list[last_index].parent is not None:
            node = self.node_list[last_index]
            path.append((int(node.value_x), int(node.value_y),int(node.value_z)))
            last_index = node.parent
        path.append((self.start.value_x, self.start.value_y, self.start.value_z))
        path.reverse()
        return path

    @staticmethod
    def get_nearest_list_index(node_list, random_new_node):
        """
        get the nearest node
        """
        list = [(node.value_x - random_new_node[0]) ** 2 + 
                (node.value_y - random_new_node[1]) ** 2 + 
                (node.value_z - random_new_node[2]) ** 2 for node in node_list]
        min_index = list.index(min(list))
        return min_index

    def draw_dynamic_graph(self, random_new_node=None):
        """
        Draw animation in process
        """
        plt.clf()
        ax = plt.gca(projection='3d')
        # Randomly generated points represented by green triangles
        if random_new_node is not None:
            ax.plot(random_new_node[0]+OFFSETX, 
                    random_new_node[1]+OFFSETY, 
                    random_new_node[2]+OFFSETZ, "^g")

        # rrt tree represented by a green line
        for node in self.node_list:
            if node.parent is not None:
                ax.plot([node.value_x+OFFSETX, self.node_list[node.parent].value_x+OFFSETX],
                        [node.value_y+OFFSETY, self.node_list[node.parent].value_y+OFFSETY], 
                        [node.value_z+OFFSETZ, self.node_list[node.parent].value_z+OFFSETZ], "-g")
        
        # Obstacle points represented by black squares              
        # occu_node_coor_list = import_known_occu_node()
        # for (obstacle_x, obstacle_y, obstacle_z) in occu_node_coor_list:
        #     ax.plot(obstacle_x+OFFSETX, obstacle_y+OFFSETY, obstacle_z+OFFSETZ, "sk", ms=10)
    
        # start_point is red, end_point is blue
        ax.plot(self.start.value_x+OFFSETX, self.start.value_y+OFFSETY, self.start.value_z+OFFSETZ, "^r")
        ax.plot(self.end.value_x+OFFSETX, self.end.value_y+OFFSETY, self.end.value_z+OFFSETZ, "^b")
        """
        set x, y, z axis limits
        """
        ax.set_xlim(0, INDICE_LENGTH)
        ax.set_ylim(0, INDICE_LENGTH)
        ax.set_zlim(0, INDICE_LENGTH)
        plt.grid(True)
        plt.pause(0.01)
    
    def plan_path(self, start_point=(15,-15,9), end_point=(-15,15,9)):
        path: list = self.planning(start_point, end_point)
        return path

    def export_rrt_path(self):
        rrt_path = self.plan_path()
        value = datetime.today()
        date_value = datetime.strftime(value,'%H:%M:%S')
        label = ('rrt_path', date_value,len(rrt_path))
        tempcsv = pd.DataFrame(columns=label, data=rrt_path)
        tempcsv.to_csv('rrt_path.csv', encoding='gbk')
        return rrt_path