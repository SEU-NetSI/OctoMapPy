import math
import matplotlib.pyplot as plt
import numpy as np

from Config import OCCUPANY_LOGODDS, FREE_LOGODDS, TREE_MAX_DEPTH, TREE_RESOLUTION
from OctoNode import OctoNode


class Visualization:
    def __init__(self) -> None:
        pass

    def visualize(self, root: OctoNode):
        """
        Visualize the occupied/free points
        """
        leaf_node_list: list = self.get_leaf_node_list(root)
        print("leaf_node_list: ", len(leaf_node_list))

        threshold_node_list: list = self.get_threshold_node_list(leaf_node_list)
        print("threshold_node_list: ", len(threshold_node_list))

        occu_node_list, free_node_list = self.get_classified_node_list(threshold_node_list)
        print("occu_node_list: ", len(occu_node_list), "; free_node_list: ", len(free_node_list))

        occu_node_coor_list, free_node_coor_list = self.get_classified_node_coor_list(occu_node_list, free_node_list)
        print("occu_node_coor_list: ", len(occu_node_coor_list), "; free_node_coor_list: ", len(free_node_coor_list))
        print(occu_node_coor_list)
        print(free_node_coor_list)

        self.show(occu_node_coor_list, free_node_coor_list)

    def get_leaf_node_list(self, root: OctoNode):
        """
        Return leaf nodes for tree traversal
        """
        if not root:
            return []

        leaf_nodes = []
        queue = [root]
        while queue:
            """
            Store the list of child nodes of the current layer
            """
            childNodes = []
            for node in queue:
                if node.is_leaf():
                    leaf_nodes.append(node)
                if node.has_children():
                    childNodes.extend(node.get_children())
            """
            Update the queue to the node of the next layer and continue to traverse 
            """
            queue = childNodes

        
        return leaf_nodes

    @staticmethod
    def get_threshold_node_list(leaf_node_list):
        """
        Store leaf nodes with deterministic probability
        """
        threshold_node_list = []
        for node in leaf_node_list:
            print(node.get_log_odds())
            if node.get_log_odds() == OCCUPANY_LOGODDS or node.get_log_odds() == FREE_LOGODDS:
                threshold_node_list.append(node)
        return threshold_node_list
    
    @staticmethod
    def get_classified_node_list(threshold_node_list):
        """
        Separate occupied and free points 
        """
        occu_node_list: list = []
        free_node_list: list = []

        for node in threshold_node_list:
            if node.get_log_odds() == OCCUPANY_LOGODDS:
                occu_node_list.append(node)
            if node.get_log_odds() == FREE_LOGODDS:
                free_node_list.append(node)
        
        return occu_node_list, free_node_list

    @staticmethod
    def get_classified_node_coor_list(occu_node_list, free_node_list):
        """
        Use list to store the corresponding coordinates 
        """        
        occu_node_coor_list = []
        free_node_coor_list = []

        for node in occu_node_list:
            node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), int(node.get_origin()[1] / TREE_RESOLUTION), int(node.get_origin()[2] / TREE_RESOLUTION))
            occu_node_coor_list.append(node_coor)
        for node in free_node_list:
            node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), int(node.get_origin()[1] / TREE_RESOLUTION), int(node.get_origin()[2] / TREE_RESOLUTION))
            free_node_coor_list.append(node_coor)

        return occu_node_coor_list, free_node_coor_list
    
    @staticmethod
    def show(occu_node_coor_list, free_node_coor_list):
        """
        Draw a 3D occupancy grid 
        """
        indice_length = int(math.pow(2, TREE_MAX_DEPTH))
        x, y, z = np.indices((indice_length, indice_length, indice_length))
        ax = plt.figure().add_subplot(projection='3d')
        
        for i in range(len(occu_node_coor_list)):
            occu_voxel = (x >= occu_node_coor_list[i][0]) & (x < occu_node_coor_list[i][0] + 1) & (y >= occu_node_coor_list[i][1]) & (y < occu_node_coor_list[i][1] + 1) & (z >= occu_node_coor_list[i][2]) & (z < occu_node_coor_list[i][2] + 1)
            colors = np.empty(occu_voxel.shape, dtype=object)
            colors[occu_voxel] = 'red'
            ax.voxels(occu_voxel, facecolors=colors, edgecolor='k')


        for i in range(len(free_node_coor_list)):
            free_voxel = (x >= free_node_coor_list[i][0]) & (x < free_node_coor_list[i][0] + 1) & (y >= free_node_coor_list[i][1]) & (y < free_node_coor_list[i][1] + 1) & (z >= free_node_coor_list[i][2]) & (z < free_node_coor_list[i][2] + 1)
            colors = np.empty(free_voxel.shape, dtype=object)
            colors[free_voxel] = 'green'
            ax.voxels(free_voxel, facecolors=colors, edgecolor='k')

        plt.show()


if __name__ == "__main__":
    Visualization().test()
