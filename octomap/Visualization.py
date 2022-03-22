import matplotlib.pyplot as plt
import numpy as np


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

    def levelOrder(self, root):
        """

        """
        if not root:
            return []
        # 保存节点的队列
        que = []
        # 保存结果的列表
        res = []
        # 根元素入队列
        que.append(root)
        while len(que):
            l = len(que)
        sub = []

        for i in range(l):
            current = que.pop(0)
            sub.append(current.val)
            for child in current.children:
                que.append(child)

        res.append(sub)
        return res


if __name__=="__main__":
    Visualization().display()
