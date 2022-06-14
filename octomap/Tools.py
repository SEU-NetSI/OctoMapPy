import numpy as np
import matplotlib.pyplot as plt
from Config import INDICE_LENGTH, OFFSETX, OFFSETY, OFFSETZ
from MapUtil import read_flying_data


class Tools:

    def __init__(self) -> None:
        pass

    def build_octomap_from_file(self):
        """
        Build an octomap from a file.
        """
        self.occu_node_coor_list, self.free_node_coor_list = read_flying_data()
        print("The number of occupied nodes: ", len(self.occu_node_coor_list))
        print("The number of free nodes: ", len(self.free_node_coor_list))

    def visualize_octomap(self):
        """
        Draw a 3D occupancy grid 
        """
        self.fig = plt.figure(figsize=(6, 6))
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

        plt.show()


if __name__ == "__main__":
    tools = Tools()
    tools.build_octomap_from_file()
    # tools.visualize_octomap()
