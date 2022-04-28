import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from Config import LOGGER, OFFSETX, OFFSETY, OFFSETZ,INDICE_LENGTH
from OctoNode import OctoNode


class Visualizer:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(7,7))

    def visualize(self):
        """
        Visualize the occupied/free points
        """
        occu_node_coor_list, free_node_coor_list = self.import_known_node()
        self.show(occu_node_coor_list, free_node_coor_list, self.fig)
        print("length - occu_node_coor_list: ", len(occu_node_coor_list))
        print("length - free_node_coor_list: ", len(free_node_coor_list))

    def import_known_node(self):
        occu_node_coor_list = []
        free_node_coor_list = []
        # TODO: read csv
        filename="point_list.xls"
        occu_nodes=pd.read_excel( filename, sheet_name="occu_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        
        occu_node_coor_list = list(map(tuple,occu_nodes.values))
        free_nodes=pd.read_excel( filename, sheet_name="free_node_coor_list",
                                 usecols=(0, 1, 2), skiprows=0)
        free_node_coor_list= list(map(tuple,free_nodes.values))
        return occu_node_coor_list, free_node_coor_list


    def show(self, occu_node_coor_list, free_node_coor_list, fig):
        """
        Draw a 3D occupancy grid 
        """
        plt.clf()
        ax = self.fig.add_subplot(projection='3d')   
        # x,y,z determined by the number of grids in that direction
        x, y, z = np.indices((INDICE_LENGTH, INDICE_LENGTH, INDICE_LENGTH))

        
        # ax.set_xlim(-indice_length, indice_length)
        # ax.set_ylim(-indice_length, indice_length)
        # ax.set_zlim(-indice_length, indice_length)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        """
        Two ways to draw:
        voxel: Better display but very slow
        scatter: The speed is fast but the observation effect is not ideal
        """
        # free space
        voxel_container = None
        for i in range(len(free_node_coor_list)):
            free_voxel = (x >= free_node_coor_list[i][0] + OFFSETX) & (x < free_node_coor_list[i][0] + 1 + OFFSETX) \
                        & (y >= free_node_coor_list[i][1] + OFFSETY) & (y < free_node_coor_list[i][1] + 1 + OFFSETY) \
                        & (z >= free_node_coor_list[i][2] + OFFSETZ) & (z < free_node_coor_list[i][2] + 1 + OFFSETZ)
            if voxel_container is not None:
                voxel_container = np.logical_or(voxel_container, free_voxel)
            else:
                voxel_container = free_voxel

        if voxel_container is not None:
            colors = np.empty(voxel_container.shape, dtype=object)
            colors[voxel_container] = 'green'
            ax.voxels(voxel_container, facecolors=colors, edgecolor='k')

        # occupied space
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
            colors[voxel_container] = 'red'
            ax.voxels(voxel_container, facecolors=colors, edgecolor='k')


        # plt.savefig('./map.jpg', dpi=1200)


def main():
    visualizer = Visualizer()
    visualizer.visualize()
    loop_counter = 0
    plt.ion()
    
    while True:
        visualizer.visualize()
        loop_counter += 1
        print("Refresh " + str(loop_counter) + " times...")
        plt.pause(0.1)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
