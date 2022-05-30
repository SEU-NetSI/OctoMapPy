import random
import math
import copy
from matplotlib import pyplot as plt
import numpy as np

import pandas as pd
from Config import GOAL_SAMPLE_RATE, EXPAND_STEP, OFFSETX, OFFSETY, OFFSETZ,SHOW_ANIMATION_RRT,INDICE_LENGTH, TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION
from MapUtil import get_classified_node_coor_list, get_classified_node_list, get_threshold_node_list
from OctoTree import OctoTree

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

        free_nodes=pd.read_csv('free_node_coor_list13.0.csv', index_col=0)
        free_node_coor_list= free_nodes.values.tolist()
        return free_node_coor_list

    def import_known_occu_node(self):
        occu_node_coor_list = []
        occu_nodes=pd.read_csv('occu_node_coor_list13.0.csv', index_col=0)
        occu_node_coor_list = occu_nodes.values.tolist()
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
    
    def draw_dynamic_graph(self, random_new_node=None):
        """
        Draw animation in process
        """
        plt.clf()
        ax = plt.gca(projection='3d')
        """
        Randomly generated points represented by green triangles
        """
        if random_new_node is not None:
            ax.plot(random_new_node[0]+OFFSETX, 
                    random_new_node[1]+OFFSETY, 
                    random_new_node[2]+OFFSETZ, "^g")
        """
        rrt tree represented by a green line
        """
        for node in self.node_list:
            if node.parent is not None:
                ax.plot([node.value_x+OFFSETX, self.node_list[node.parent].value_x+OFFSETX],
                        [node.value_y+OFFSETY, self.node_list[node.parent].value_y+OFFSETY], 
                        [node.value_z+OFFSETZ, self.node_list[node.parent].value_z+OFFSETZ], "-g")
        """
        Obstacle points represented by black squares
        """                
        # occu_node_coor_list = self.import_known_occu_node()
        # for (obstacle_x, obstacle_y, obstacle_z) in occu_node_coor_list:
        #     ax.plot(obstacle_x+OFFSETX, obstacle_y+OFFSETY, obstacle_z+OFFSETZ, "sk", ms=10)
        """
        start_point is red, end_point is blue
        """
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

    def draw_static_graph(self, path):
        """
        Draw the final graph
        """
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        # for node in self.node_list:
        #     if node.parent is not None:
        #         ax.plot([node.value_x+OFFSETX, self.node_list[node.parent].value_x+OFFSETX],
        #                 [node.value_y+OFFSETY, self.node_list[node.parent].value_y+OFFSETY], 
        #                 [node.value_z+OFFSETZ, self.node_list[node.parent].value_z+OFFSETZ], "-g")

        occu_node_coor_list = self.import_known_occu_node()
        x, y, z = np.indices((INDICE_LENGTH, INDICE_LENGTH, INDICE_LENGTH))
        voxel_container = None
        for i in range(len(occu_node_coor_list)):
            occu_voxel = (x >= occu_node_coor_list[i][0] + OFFSETX) & (x < occu_node_coor_list[i][0] + 1 + OFFSETX) \
                         & (y >= occu_node_coor_list[i][1] + OFFSETY) & (y < occu_node_coor_list[i][1] + 1 + OFFSETY) \
                         & (z >= occu_node_coor_list[i][2] + OFFSETZ) & (z < occu_node_coor_list[i][2] + 1 + OFFSETZ)
            if voxel_container is not None:
                voxel_container = np.logical_or(voxel_container, occu_voxel)
            else:
                voxel_container = occu_voxel
        if voxel_container is not None:
            colors = np.empty(voxel_container.shape, dtype=object)
            colors[voxel_container] = 'black'
            ax.voxels(voxel_container, facecolors=colors, edgecolor='k')

        ax.set_xlim(0, INDICE_LENGTH)
        ax.set_ylim(0, INDICE_LENGTH)
        ax.set_zlim(0, INDICE_LENGTH)
        """
        Generated path indicated by red lines
        """
        ax.plot([data[0]+OFFSETX for data in path],
                [data[1]+OFFSETY for data in path], 
                [data[2]+OFFSETZ for data in path], '-r')
        ax.plot(self.start.value_x+OFFSETX, self.start.value_y+OFFSETY, self.start.value_z+OFFSETZ, "^r")
        ax.plot(self.end.value_x+OFFSETX, self.end.value_y+OFFSETY, self.end.value_z+OFFSETZ, "^b")
        plt.grid(True)
        plt.show()