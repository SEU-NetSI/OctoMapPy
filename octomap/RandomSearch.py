import random
import math
import copy

import pandas as pd
from OctoTree import OctoTree
from Config import GoalSampleRate,Expand_Step

class RandomSearch:
    def __init__(self):
        self.nodeList = [(0,0,0)]
        self.end = (10,10,10)
        pass

    def import_known_free_node(self):
        occu_node_coor_list = []
        free_node_coor_list = []
        # TODO: read csv
        filename="point_list.xls"
        free_nodes=pd.read_excel( filename, sheet_name="free_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        free_node_coor_list= list(map(tuple,free_nodes.values))
        return free_node_coor_list

    def import_known_occu_node(self):
        occu_node_coor_list = []
        # TODO: read csv
        filename="point_list.xls"
        occu_nodes=pd.read_excel( filename, sheet_name="occu_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        occu_node_coor_list = list(map(tuple,occu_nodes.values))
        return occu_node_coor_list

    def random_node(self):
        """
        Randomly pick from free_nodes and return
        """
        free_node_coor_list = self.import_known_free_node()
        node = random.sample(free_node_coor_list, 1)[0]
        return node

    def collision_check(self,new_node):
        occu_node_coor_list = self.import_known_occu_node()
        a = 1
        size = 1  # The space occupied by the obstacle
        for (obstacle_x, obstacle_y, obstacle_z) in occu_node_coor_list:
            dx = obstacle_x - new_node.x
            dy = obstacle_y - new_node.y
            dz = obstacle_z - new_node.z
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            if d <= size:
                a = 0  # collision
        return a  # safe

    @staticmethod
    def get_nearest_list_index(node_list, random_new_node):
        """
        
        """
        list = [(node.x - random_new_node[0]) ** 2 + 
                (node.y - random_new_node[1]) ** 2 + 
                (node.y - random_new_node[1]) ** 2 for node in node_list]
        min_index = list.index(min(list))
        return min_index

    def plan(self, octotree: OctoTree):
        point_list = []
        return point_list
    
    def planning(self):
        """
        Path planning
        """
        while True:
            if random.random() > GoalSampleRate:
                random_new_node = self.random_node()
            else:
                random_new_node = [self.end[0], self.end[1], self.end[2]]

            # Find nearest node
            min_index = self.get_nearest_list_index(self.nodeList, random_new_node)
            
            # expand tree
            nearest_node = self.nodeList[min_index]

            # 
            path_len = math.sqrt((random_new_node[2] - nearest_node[2]) ** 2 +
                                 (random_new_node[1] - nearest_node[1]) ** 2 +
                                 (random_new_node[0] - nearest_node[0]) ** 2)
            path_x_angle = (random_new_node[0] - nearest_node[0]) / path_len
            path_y_angle = (random_new_node[1] - nearest_node[1]) / path_len
            path_z_angle = (random_new_node[2] - nearest_node[2]) / path_len
            new_node = copy.deepcopy(nearest_node)
            new_node[0] += Expand_Step * path_x_angle
            new_node[1] += Expand_Step * path_y_angle
            new_node[2] += Expand_Step * path_z_angle
            new_node.parent = min_index

            if not self.collision_check(new_node):
                continue

            self.nodeList.append(new_node)

            # check goal
            d = math.sqrt((new_node[0] - self.end[0]) **2 + 
                          (new_node[1] - self.end[1]) **2 + 
                          (new_node[2] - self.end[2]) **2)
            if d <= Expand_Step:
                break
            # if show_animation:
            #     self.draw_graph(rnd)

        path = [[self.end.x, self.end.y, self.end.z]]
        last_index = len(self.nodeList) - 1
        while self.nodeList[last_index].parent is not None:
            node = self.nodeList[last_index]
            path.append([node.x, node.y,node.z])
            last_index = node.parent
        path.append([self.start.x, self.start.y, self.start.z])

        return path