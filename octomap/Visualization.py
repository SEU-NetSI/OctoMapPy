import matplotlib.pyplot as plt
import numpy as np

from Config import OCCUPANY_LOGODDS, FREE_LOGODDS
from OctoNode import OctoNode


class Visualization:
    def __init__(self) -> None:
        pass

    @staticmethod
    def display():
        """
        Official Reference Visualization Module
        """
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

    def get_leaf_nodes(self, root: OctoNode):
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

        print("leaf_nodes: ", len(leaf_nodes))
        require_nodes = self.req_leaf_node(leaf_nodes)
        print("require_nodes", len(require_nodes))
        self.show(require_nodes)

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
        """
        visualize the occupied/free points
        """
        occu_origin_to_coordinate = []
        free_origin_to_coordinate = []
        """
        Separating occupied and free points 
        """
        for node in require_nodes:
            if node.get_log_odds() == OCCUPANY_LOGODDS:
                occu_origin_to_coordinate.append(node)
            if node.get_log_odds() == FREE_LOGODDS:
                free_origin_to_coordinate.append(node)
        print("occu_origin_to_coordinate:", len(occu_origin_to_coordinate))
        occu_node = []
        free_node = []
        """
        Use list to store the corresponding coordinates 
        """
        for node in occu_origin_to_coordinate:
            # print(node.get_origin())
            new_node = (int(node.origin[0] / 4), int(node.origin[1] / 4), int(node.origin[2] / 4))
            occu_node.append(new_node)
        for node in free_origin_to_coordinate:
            new_node = (int(node.get_origin()[0] / 4), int(node.get_origin()[1] / 4), int(node.get_origin()[2] / 4))
            free_node.append(new_node)
        print("occu_node_list:", occu_node)
        """
        Draw a 3D occupancy grid 
        """
        x, y, z = np.indices((128, 128, 128))
        ax = plt.figure().add_subplot(projection='3d')
        for i in range(len(occu_node)):
            occu = (x >= occu_node[i][0]) & (x < occu_node[i][0] + 1) & (y >= occu_node[i][1]) & (y < occu_node[i][1] + 1) & (z >= occu_node[i][2]) & (z < occu_node[i][2] + 1)
            # voxel = occu
            colors = np.empty(occu.shape, dtype=object)
            colors[occu] = 'red'
            ax.voxels(occu, facecolors=colors, edgecolor='k')
        # for i in range(len(free_node)):
        #     free = (x >= x[0]) & (x < x[0]+1) & (y >= x[1]) & (y < x[1]+1) & (z >= x[3]) & (z < x[3]+1)
        #     voxel = free
        #     colors = np.empty(voxel.shape, dtype=object)
        #     colors[free] = 'green'
        #     ax.voxels(voxel, facecolors=colors, edgecolor='k')
        plt.show()

    @staticmethod
    def test():
        """
        test function
        """
        x, y, z = np.indices((11, 11, 11))
        ax = plt.figure().add_subplot(projection='3d')
        m = [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        print(len(m))
        for i in range(len(m)):
            cubem = (x >= m[i][0]) & (x < m[i][0] + 1) & (y >= m[i][1]) & (y < m[i][1] + 1) & (z >= m[i][2]) & (
                        z < m[i][2] + 1)
            voxelarray = cubem
            colors = np.empty(voxelarray.shape, dtype=object)
            colors[cubem] = 'blue'
            ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        # plt.show()


if __name__ == "__main__":
    Visualization().test()
