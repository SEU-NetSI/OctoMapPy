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

    def get_leaf_nodes(self, root: OctoNode):
        """

        """
        if not root:
            return []
      
        leaf_nodes = []
        que = []
        
        que.append(root)
        que_l = len(que)
            
        sub = []

        for node in que:
            if node.has_children:

        for i in range(l):
            current = que.pop(0)
            sub.append(current.val)
            for child in current.children:
                que.append(child)

            res.append(sub)
        return res


if __name__=="__main__":
    Visualization().display()
