from datetime import datetime
import math
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from PathPlan import PathPlan

from Config import OFFSETX, OFFSETY, OFFSETZ,INDICE_LENGTH,SAVE_IMAGE,SHOW_ANIMATION_BUILDING,READ_FLYING_DATA 
from Config import TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION
from OctoTree import OctoTree
from MapUtil import get_classified_node_coor_list, get_classified_node_list, get_threshold_node_list

class Visualizer:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(7,7))
        self.path_planner = PathPlan()
    
    def visualize(self):
        """
        Visualize the occupied/free points
        """
        if READ_FLYING_DATA:
            occu_node_coor_list, free_node_coor_list = self.read_flying_data()
            self.export_flying_data()
        else:
            occu_node_coor_list, free_node_coor_list = self.import_known_node()
        self.show(occu_node_coor_list, free_node_coor_list, self.fig)
        print("length - occu_node_coor_list: ", len(occu_node_coor_list))
        print("length - free_node_coor_list: ", len(free_node_coor_list))

    def plan_path(self, start_point=(0,0,8), end_point=(20,-20,8)):
        path: list = self.path_planner.planning(start_point, end_point)
        print(path)
        return path

    def visual_path(self,path):
        self.path_planner.draw_static_graph(path)

    def export_rrt_path(self):
        rrt_path = self.plan_path()
        value = datetime.today()
        date_value = datetime.strftime(value,'%H:%M:%S')
        label = ('rrt_path', date_value,len(rrt_path))
        tempcsv = pd.DataFrame(columns=label, data=rrt_path)
        tempcsv.to_csv('rrt_path.csv', encoding='gbk')
        return rrt_path
        
    def import_known_node(self):
        occu_node_coor_list = []
        free_node_coor_list = []
        # TODO: read csv
        
        occu_nodes=pd.read_csv('occu_node_coor_list.csv', index_col=0)
        occu_node_coor_list = occu_nodes.values.tolist()

        free_nodes=pd.read_csv('free_node_coor_list.csv', index_col=0)
        free_node_coor_list= free_nodes.values.tolist()
        return occu_node_coor_list, free_node_coor_list

    def import_flying_data(self):
        start_points_list = []
        end_points_list = []
        
        start_points=pd.read_csv('start_points.csv', index_col=0)
        start_points_list = start_points.values.tolist()

        end_points=pd.read_csv('end_points.csv', index_col=0)
        end_points_list= end_points.values.tolist()
        return start_points_list, end_points_list

    def read_flying_data(self):
        # start_time = time.time()
        sheet_start_points,sheet_end_points = self.import_flying_data()
        self.octotree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
        for index in range(len(sheet_end_points)):
            self.octotree.ray_casting(tuple(sheet_start_points[index]), tuple(sheet_end_points[index]))
        leaf_node_list = self.octotree.get_leaf_node_list()
        threshold_node_list: list = get_threshold_node_list(leaf_node_list)
        occu_node_list, free_node_list = get_classified_node_list(threshold_node_list)
        occu_node_coor_list, free_node_coor_list = get_classified_node_coor_list(occu_node_list, free_node_list)
        # end_time = time.time()
        # print('Running time: %s s' % ((end_time - start_time)))
        return occu_node_coor_list, free_node_coor_list
    
    def export_flying_data(self):
        occu_node_coor_list, free_node_coor_list = self.read_flying_data()
        value = datetime.today()
        date_value = datetime.strftime(value,'%H:%M:%S')

        label_occu = ('occu_node_coor_list', date_value,len(occu_node_coor_list))
        occu_node_tempcsv = pd.DataFrame(columns=label_occu, data=occu_node_coor_list)
        occu_node_tempcsv.to_csv('occu_node_coor_list.csv', encoding='gbk')

        label_free = ('free_node_coor_list', date_value,len(free_node_coor_list))
        free_node_tempcsv = pd.DataFrame(columns=label_free, data=free_node_coor_list)
        free_node_tempcsv.to_csv('free_node_coor_list.csv', encoding='gbk')

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
 

def main():
    visualizer = Visualizer()
    visualizer.visualize()
    loop_counter = 0
    
    if SHOW_ANIMATION_BUILDING:
        plt.ion()
        while True: 
            visualizer.visualize()
            loop_counter += 1
            print("Refresh " + str(loop_counter) + " times...")
            plt.pause(0.1)
        plt.ioff()
    else: 
        plt.show()
    if SAVE_IMAGE:
        plt.savefig('./map.jpg', dpi=1200)
    rrt_path = visualizer.export_rrt_path()
    visualizer.visual_path(rrt_path)

if __name__ == "__main__":
    main()
