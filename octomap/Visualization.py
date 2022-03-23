import matplotlib.pyplot as plt
import numpy as np
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
            for node in queue:
                if node.is_leaf():
                    leaf_nodes.append(node.log_odds)
            # 存储当前层的孩子节点列表
            childNodes = []
            for node in queue:
                # 若节点存在子节点，入队
                if node.children:
                    childNodes.extend(node.children)
            # 更新队列为下一层的节点，继续遍历
            queue = childNodes
        return leaf_nodes



if __name__=="__main__":
    Visualization().display()
