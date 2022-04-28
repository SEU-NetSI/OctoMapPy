import random
import math
import copy

import pandas as pd
from Config import GOAL_SAMPLE_RATE, EXPAND_STEP

class Node:
    def __init__(self, value_x, value_y, value_z):
        self.value_x = value_x
        self.value_y = value_y
        self.value_z = value_z
        self.parent = None

class PathPlan:
    def __init__(self):
        self.node_list = []

    def import_known_free_node(self):
        free_node_coor_list = []
        filename="point_list.xls"
        free_nodes=pd.read_excel( filename, sheet_name="free_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        free_node_coor_list= list(map(tuple,free_nodes.values))
        return free_node_coor_list

    def import_known_occu_node(self):
        occu_node_coor_list = []
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
            dx = obstacle_x - new_node.value_x
            dy = obstacle_y - new_node.value_y
            dz = obstacle_z - new_node.value_z
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            if d <= size:
                a = 0  # collision
        return a  # safe

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
    
    def planning(self, start_point, end_point):
        """
        Path planning
        """
        self.start = Node(start_point[0], start_point[1], start_point[2])
        self.end = Node(end_point[0], end_point[1], end_point[2])
        self.node_list.append(self.start)

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
                continue

            self.node_list.append(new_node)

            # Exit the loop when the target distance from the new_node is less than the step size
            d = math.sqrt((new_node.value_x - self.end.value_x) **2 + 
                          (new_node.value_y - self.end.value_y) **2 + 
                          (new_node.value_z - self.end.value_z) **2)
            if d <= EXPAND_STEP:
                break
            # if show_animation:
            #     self.draw_graph(rnd)

        path = [(self.end.value_x, self.end.value_y, self.end.value_z)]
        last_index = len(self.node_list) - 1
        while self.node_list[last_index].parent is not None:
            node = self.node_list[last_index]
            path.append((node.value_x, node.value_y,node.value_z))
            last_index = node.parent
        path.append((self.start.value_x, self.start.value_y, self.start.value_z))

        return path
    
    def draw_graph(self, rnd=None):
        """
        Draw Graph
        """
        plt.clf()
        # fig = plt.figure()
        ax = plt.gca(projection='3d')

        if rnd is not None:
            ax.plot(rnd[0], rnd[1], rnd[2], "^g")
        for node in self.node_list:
            if node.parent is not None:
                ax.plot([node.x, self.node_list[node.parent].x], [
                    node.y, self.node_list[node.parent].y], [node.z, self.node_list[node.parent].z], "-g")

        for (ox, oy, oz, size) in self.obstacleList:
            ax.plot(ox, oy, oz, "sk", ms=10 * size)

        ax.plot(self.start.x, self.start.y, self.start.z, "^r")
        ax.plot(self.end.x, self.end.y, self.end.z, "^b")
        # plt.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand])
        ax.set_xlim(self.min_rand, self.max_rand)
        ax.set_ylim(self.min_rand, self.max_rand)
        ax.set_zlim(self.min_rand, self.max_rand)
        plt.grid(True)
        plt.pause(0.01)
