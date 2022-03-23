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
                else:
                    childNodes.extend(node.children())
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


if __name__=="__main__":
    Visualization().display()
