import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time

from Config import OCCUPANY_LOGODDS, FREE_LOGODDS, TREE_MAX_DEPTH, TREE_RESOLUTION, Offset_x, Offset_y, Offset_z
from OctoNode import OctoNode


class Visualizer:
    fig = plt.figure(figsize=(15,15))
    def __init__(self) -> None:
        pass

    def visualize(self):
        """
        Visualize the occupied/free points
        """
        occu_node_coor_list, free_node_coor_list = self.import_known_node()
        self.show(occu_node_coor_list, free_node_coor_list, self.fig)
        print("occu_node_coor_list:", occu_node_coor_list)
        # print("free_node_coor_list", free_node_coor_list)

    def import_known_node(self):
        occu_node_coor_list = []
        free_node_coor_list = []
        # TODO: read csv
        filename="\\point_list.xls"
        occu_nodes=pd.read_excel(os.path.dirname(os.getcwd()) + filename, sheet_name="occu_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        occu_node_coor_list = list(map(tuple,occu_nodes.values))
        free_nodes=pd.read_excel(os.path.dirname(os.getcwd()) + filename, sheet_name="free_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        free_node_coor_list= list(map(tuple,free_nodes.values))
        return occu_node_coor_list, free_node_coor_list


    @staticmethod
    def show(occu_node_coor_list, free_node_coor_list, fig):
        """
        Draw a 3D occupancy grid 
        """
        plt.clf()
        ax = fig.add_subplot(projection='3d')
        indice_length = int(math.pow(2, TREE_MAX_DEPTH))    
        # x,y,z determined by the number of grids in that direction
        x, y, z = np.indices((indice_length, indice_length, indice_length))

        
        # ax.set_xlim(-indice_length, indice_length)
        # ax.set_ylim(-indice_length, indice_length)
        # ax.set_zlim(-indice_length, indice_length)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        """
        Two ways to draw:
        voxel:Better display but very slow
        Scatter:The speed is fast but the observation effect is not ideal
        """

        for i in range(len(free_node_coor_list)):
            free_voxel = (x >= free_node_coor_list[i][0] + Offset_x) & (x < free_node_coor_list[i][0] + 1 + Offset_x) \
                        & (y >= free_node_coor_list[i][1] + Offset_y) & (y < free_node_coor_list[i][1] + 1 + Offset_y) \
                        & (z >= free_node_coor_list[i][2] + Offset_z) & (z < free_node_coor_list[i][2] + 1 + Offset_z)
            colors = np.empty(free_voxel.shape, dtype=object)
            colors[free_voxel] = 'green'
            ax.voxels(free_voxel, facecolors=colors, edgecolor='k')

            # ax.scatter3D(free_node_coor_list[i][0], free_node_coor_list[i][1], free_node_coor_list[i][2], marker = 's',
            #           c='g', s =70)

        for i in range(len(occu_node_coor_list)):
            occu_voxel = (x >= occu_node_coor_list[i][0] + Offset_x) & (x < occu_node_coor_list[i][0] + 1 + Offset_x) \
                         & (y >= occu_node_coor_list[i][1] + Offset_y) & (y < occu_node_coor_list[i][1] + 1 + Offset_y) \
                         & (z >= occu_node_coor_list[i][2] + Offset_z) & (z < occu_node_coor_list[i][2] + 1 + Offset_z)
            colors = np.empty(occu_voxel.shape, dtype=object)
            colors[occu_voxel] = 'red'
            ax.voxels(occu_voxel, facecolors=colors, edgecolor='k')

            # ax.scatter3D(occu_node_coor_list[i][0], occu_node_coor_list[i][1], occu_node_coor_list[i][2], marker='s',
            #              c='r', s=70)

        # plt.show()
        # plt.savefig('./map.jpg', dpi=1200)


def main():
    visualizer = Visualizer()
    loop_counter = 0
    plt.ion()
    # TODO: while loop
    # while True:
    #     visualizer.visualize()
    #     time.sleep(5)
    while loop_counter < 5:
        visualizer.visualize()
        loop_counter += 1
        print("已插入一组数据")
        time.sleep(3)
        plt.pause(0.2)
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
