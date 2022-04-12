import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Config import OCCUPANY_LOGODDS, FREE_LOGODDS, TREE_MAX_DEPTH, TREE_RESOLUTION, Offset_x, Offset_y, Offset_z
from OctoNode import OctoNode


class Visualization:
    def __init__(self) -> None:
        pass

    def visualize(self, root: OctoNode):
        """
        Visualize the occupied/free points
        """
        occu_node_coor_list, free_node_coor_list = self.import_known_node()
        self.show(occu_node_coor_list, free_node_coor_list)

    def import_known_node():
        occu_node_coor_list = [], free_node_coor_list = []
        # TODO: read csv
        filename="point_list.xls"
        occu_nodes=pd.read_excel(filename,sheet_name="occu_node_coor_list",usecols=(0,1,2),skiprows=0)
        occu_node_coor_list = list(map(tuple,occu_nodes.values))
        free_nodes=pd.read_excel(filename,sheet_name="free_node_coor_list",usecols=(0,1,2),skiprows=0)
        free_node_coor_list= list(map(tuple,free_nodes.values))
        return occu_node_coor_list, free_node_coor_list


    @staticmethod
    def show(occu_node_coor_list, free_node_coor_list):
        """
        Draw a 3D occupancy grid 
        """
        indice_length = int(math.pow(2, TREE_MAX_DEPTH))    
        # x,y,z determined by the number of grids in that direction
        x, y, z = np.indices((indice_length, indice_length, indice_length))

        ax = plt.figure(figsize=(20,20)).add_subplot(projection='3d')
        # ax.set_xlim(-indice_length, indice_length)
        # ax.set_ylim(-indice_length, indice_length)
        # ax.set_zlim(-indice_length, indice_length)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        for i in range(len(occu_node_coor_list)):
            occu_voxel = (x >= occu_node_coor_list[i][0] + Offset_x) & (x < occu_node_coor_list[i][0] + 1 + Offset_x) \
                        & (y >= occu_node_coor_list[i][1] + Offset_y) & (y < occu_node_coor_list[i][1] + 1 + Offset_y) \
                        & (z >= occu_node_coor_list[i][2] + Offset_z) & (z < occu_node_coor_list[i][2] + 1 + Offset_z)
            colors = np.empty(occu_voxel.shape, dtype=object)
            colors[occu_voxel] = 'red'
            ax.voxels(occu_voxel, facecolors=colors, edgecolor='k')
            
            # ax.scatter3D(occu_node_coor_list[i][0], occu_node_coor_list[i][1], occu_node_coor_list[i][2], marker='s',
            #              c='r', s=70)

        for i in range(len(free_node_coor_list)):
            free_voxel = (x >= free_node_coor_list[i][0] + Offset_x) & (x < free_node_coor_list[i][0] + 1 + Offset_x) \
                        & (y >= free_node_coor_list[i][1] + Offset_y) & (y < free_node_coor_list[i][1] + 1 + Offset_y) \
                        & (z >= free_node_coor_list[i][2] + Offset_z) & (z < free_node_coor_list[i][2] + 1 + Offset_z)
            colors = np.empty(free_voxel.shape, dtype=object)
            colors[free_voxel] = 'green'
            ax.voxels(free_voxel, facecolors=colors, edgecolor='k')

            #  ax.scatter3D(free_node_coor_list[i][0], free_node_coor_list[i][1], free_node_coor_list[i][2], marker = 's',
            #               c='g', s =70)


        plt.show()
        # plt.savefig('./map.jpg', dpi=1200)


if __name__ == "__main__":
    Visualization().test()
