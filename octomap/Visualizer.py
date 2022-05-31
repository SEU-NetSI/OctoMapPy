import matplotlib.pyplot as plt
import numpy as np

from RrtPathPlan import RrtPathPlan
from Config import OFFSETX, OFFSETY, OFFSETZ,INDICE_LENGTH, SAVE_IMAGE, SHOW_ANIMATION_BUILDING, REGENERATE_BEFORE_VISUALIZE, SHOW_RRT_EXPLORATION
from MapUtil import import_known_node, read_flying_data

class Visualizer:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(14, 6))
       
    def visualize(self):
        self.set_known_node_list()
        self.set_rrt_path()

        self.visualize_octomap()
        self.visualize_rrtpath()

        if SHOW_ANIMATION_BUILDING:
            loop_counter = 0
            plt.ion()
            while True:
                plt.clf()
                loop_counter += 1
                print("Refresh " + str(loop_counter) + " times...")
                plt.pause(0.1)
            plt.ioff()
        else:
            if SAVE_IMAGE:
                plt.savefig('./octomap-rrtpath.jpg', dpi=1200)
            else:
                plt.show()
    
    def set_known_node_list(self):
        if REGENERATE_BEFORE_VISUALIZE:
            self.occu_node_coor_list, self.free_node_coor_list = read_flying_data()
        else:
            self.occu_node_coor_list, self.free_node_coor_list = import_known_node()

        print("length - occu_node_coor_list: ", len(self.occu_node_coor_list))
        print("length - free_node_coor_list: ", len(self.free_node_coor_list))

    def set_rrt_path(self):
        self.path_planner = RrtPathPlan()
        self.rrt_path = self.path_planner.export_rrt_path()
        print("length - rrt_path: ", len(self.rrt_path))

    def visualize_octomap(self):
        """
        Draw a 3D occupancy grid 
        """
        ax = self.fig.add_subplot(121, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        x, y, z = np.indices((INDICE_LENGTH, INDICE_LENGTH, INDICE_LENGTH))

        # show the free voxels
        voxel_container = None
        for i in range(len(self.free_node_coor_list)):
            free_voxel = (x >= self.free_node_coor_list[i][0] + OFFSETX) & (x < self.free_node_coor_list[i][0] + 1 + OFFSETX) \
                        & (y >= self.free_node_coor_list[i][1] + OFFSETY) & (y < self.free_node_coor_list[i][1] + 1 + OFFSETY) \
                        & (z >= self.free_node_coor_list[i][2] + OFFSETZ) & (z < self.free_node_coor_list[i][2] + 1 + OFFSETZ)
            if voxel_container is not None:
                voxel_container = np.logical_or(voxel_container, free_voxel)
            else:
                voxel_container = free_voxel

        if voxel_container is not None:
            ax.voxels(voxel_container, facecolors='#b7eb8f0f', edgecolor='#b7eb8f17')

        # show the occupied voxels
        voxel_container = None
        for i in range(len(self.occu_node_coor_list)):
            occu_voxel = (x >= self.occu_node_coor_list[i][0] + OFFSETX) & (x < self.occu_node_coor_list[i][0] + 1 + OFFSETX) \
                         & (y >= self.occu_node_coor_list[i][1] + OFFSETY) & (y < self.occu_node_coor_list[i][1] + 1 + OFFSETY) \
                         & (z >= self.occu_node_coor_list[i][2] + OFFSETZ) & (z < self.occu_node_coor_list[i][2] + 1 + OFFSETZ)
            if voxel_container is not None:
                voxel_container = np.logical_or(voxel_container, occu_voxel)
            else:
                voxel_container = occu_voxel

        if voxel_container is not None:
            ax.voxels(voxel_container, facecolors='#a8071a', edgecolor='#000000')

    def visualize_rrtpath(self):
        """
        Draw the RRT planning graph
        """
        ax = self.fig.add_subplot(122, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # show the green exploration path
        if SHOW_RRT_EXPLORATION:
            for node in self.path_planner.node_list:
                if node.parent is not None:
                    ax.plot([node.value_x+OFFSETX, self.path_planner.node_list[node.parent].value_x+OFFSETX],
                            [node.value_y+OFFSETY, self.path_planner.node_list[node.parent].value_y+OFFSETY], 
                            [node.value_z+OFFSETZ, self.path_planner.node_list[node.parent].value_z+OFFSETZ], "-g")

        # show the occupied nodes
        x, y, z = np.indices((INDICE_LENGTH, INDICE_LENGTH, INDICE_LENGTH))
        voxel_container = None
        for i in range(len(self.occu_node_coor_list)):
            occu_voxel = (x >= self.occu_node_coor_list[i][0] + OFFSETX) & (x < self.occu_node_coor_list[i][0] + 1 + OFFSETX) \
                         & (y >= self.occu_node_coor_list[i][1] + OFFSETY) & (y < self.occu_node_coor_list[i][1] + 1 + OFFSETY) \
                         & (z >= self.occu_node_coor_list[i][2] + OFFSETZ) & (z < self.occu_node_coor_list[i][2] + 1 + OFFSETZ)
            if voxel_container is not None:
                voxel_container = np.logical_or(voxel_container, occu_voxel)
            else:
                voxel_container = occu_voxel
        if voxel_container is not None:
            colors = np.empty(voxel_container.shape, dtype=object)
            colors[voxel_container] = 'black'
            ax.voxels(voxel_container, facecolors=colors, edgecolor='k')

        # show the red planning path
        ax.plot([data[0]+OFFSETX for data in self.rrt_path],
                [data[1]+OFFSETY for data in self.rrt_path], 
                [data[2]+OFFSETZ for data in self.rrt_path], '-r')

        # show the blue start point and cyan end point
        ax.plot(self.path_planner.start.value_x + OFFSETX, self.path_planner.start.value_y + OFFSETY, self.path_planner.start.value_z + OFFSETZ, "*b")
        ax.plot(self.path_planner.end.value_x + OFFSETX, self.path_planner.end.value_y + OFFSETY, self.path_planner.end.value_z + OFFSETZ, "*c")

def main():
    visualizer = Visualizer()
    visualizer.visualize()

if __name__ == "__main__":
    main()
