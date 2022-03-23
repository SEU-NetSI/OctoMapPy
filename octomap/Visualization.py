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
            occu_node[i,:,:] = node.get_origin()[0]/5
            occu_node[:,:,i] = node.get_origin()[1]/5
            occu_node[:,i,:] = node.get_origin()[2]/5
        for node in free_origin_to_coordinate:
            free_node[i,:,:] = node.get_origin()[0]/5
            free_node[:,:,i] = node.get_origin()[1]/5
            free_node[:,i,:] = node.get_origin()[2]/5
        occu_x = [x[0] for x in occu_node]
        occu_y = [x[1] for x in occu_node]
        occu_z = [x[2] for x in occu_node]

        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter(occu_x, occu_y, occu_z, c='r')






        plt.show()

def test():
    cube = np.ones((3, 3, 3))
    print(cube)

if __name__=="__main__":
   Visualization().show()
