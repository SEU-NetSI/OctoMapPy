import matplotlib.pyplot as plt
import numpy as np

from octomap.Config import OCCUPANY_LOGODDS, FREE_LOGODDS
from octomap.OctoNode import OctoNode


class Visualization:
    def __init__(self) -> None:
        pass

    @staticmethod
    def display():
        x, y, z = np.indices((8, 8, 8))

        cube1 = (x < 3) & (y < 3) & (z < 3)
        print(cube1)
        cube2 = (x >= 5) & (y >= 5) & (z >= 5)
        link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

        voxelarray = cube1 | cube2 | link

        colors = np.empty(voxelarray.shape, dtype=object)
        colors[link] = 'red'
        colors[cube1] = 'blue'
        colors[cube2] = 'green'

        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        plt.show()

    @staticmethod
    def get_leaf_nodes(root: OctoNode):
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
    def req_leaf_node(leaf_nodes):
        """
        Store leaf nodes with deterministic probability
        """
        require_nodes = []
        for node in leaf_nodes:
            if node.get_log_odds() == OCCUPANY_LOGODDS or node.get_log_odds() == FREE_LOGODDS:
                require_nodes.append(node)
        return require_nodes

    @staticmethod
    def show(require_nodes):
        occu_origin_to_coordinate = []
        free_origin_to_coordinate = []
        for node in require_nodes:
            if require_nodes.get_log_odds() == OCCUPANY_LOGODDS:
                occu_origin_to_coordinate.append(node)
            if require_nodes.get_log_odds() == FREE_LOGODDS:
                free_origin_to_coordinate.append(node)
        x, y, z = np.indices((80, 80, 80))
        occu_node = np.ones((3, 3, 3))
        free_node = np.ones((3, 3, 3))
        for node in occu_origin_to_coordinate:
            occu_node[0].append(node.get_origin()[0]/5)
            occu_node[1].append(node.get_origin()[1]/5)
            occu_node[2].append(node.get_origin()[2]/5)
        for node in free_origin_to_coordinate:
            free_node[0].append(node.get_origin()[0]/5)
            free_node[0].append(node.get_origin()[1]/5)
            free_node[0].append(node.get_origin()[2]/5)
        for i in range(len(occu_node)):
            occu_node[i] = (x >= x[0]) & (x < x[0]+1) & (y >= x[1]) & (y < x[1]+1) & (z >= x[3]) & (z < x[3]+1)
        for i in range(len(free_node)):
            free_node[i] = (x >= x[0]) & (x < x[0]+1) & (y >= x[1]) & (y < x[1]+1) & (z >= x[3]) & (z < x[3]+1)
        voxel = occu_node | free_node
        colors = np.empty(voxel.shape, dtype=object)
        colors[occu_node] = 'red'
        colors[free_node] = 'green'
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxel, facecolors=colors, edgecolor='k')
        # occu_x = [x[0] for x in occu_node]
        # occu_y = [x[1] for x in occu_node]
        # occu_z = [x[2] for x in occu_node]
        #
        # free_x = [x[0] for x in occu_node]
        # free_y = [x[1] for x in occu_node]
        # free_z = [x[2] for x in occu_node]
        # ax = plt.figure().add_subplot(projection='3d')
        # ax.scatter(occu_x, occu_y, occu_z, c='r')
        # ax.scatter(free_x, free_y, free_z, c='g')

        plt.show()

    def test(self):
        cubem = None
        voxelarray = cubem
        ax = plt.figure().add_subplot(projection='3d')
        colors = np.empty(voxelarray.shape, dtype=object)
        m = [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        for i in range(3):
            cubem = (x >= m[i][0]) & (x < m[i][0] + 1) & (y >= m[i][1]) & (y < m[i][1] + 1) & (z >= m[i][2]) & (
                        z < m[i][2] + 1)
            voxelarray = cubem
            ax.voxels(voxelarray, facecolors=colors, edgecolor='k')
        colors[cubem] = 'blue'

        plt.show()

#
# def test():
#     cube = np.ones((3, 3, 3))
#     print(cube)
#
# if __name__=="__main__":
#    Visualization().show()
