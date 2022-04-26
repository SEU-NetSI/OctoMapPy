
from matplotlib import pyplot as plt
import random
import math
import copy

show_animation = True


class Node(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None


class RRT(object):

    def __init__(self, start, goal, obstacle_list, rand_area):
        """
        Parameter:
        start:Start Position [x,y,z]
        goal:Goal Position [x,y,z]
        obstacleList:obstacle Positions [[x,y,z,size]]
        randArea:random sampling Area [min,max]
        """
        self.start = Node(start[0], start[1], start[2])
        self.end = Node(goal[0], goal[1], goal[2])
        self.min_rand = rand_area[0]
        self.max_rand = rand_area[1]
        self.expandDis = 4  
        self.goalSampleRate = 0.05  
        self.maxIter = 500
        self.obstacleList = obstacle_list
        self.nodeList = [self.start]

    def random_node(self):
        """
        :return:
        """
        node_x = random.uniform(self.min_rand, self.max_rand)
        node_y = random.uniform(self.min_rand, self.max_rand)
        node_z = random.uniform(self.min_rand, self.max_rand)
        node = [node_x, node_y, node_z]

        return node

    @staticmethod
    def get_nearest_list_index(node_list, rnd):
        """
        :param node_list:
        :param rnd:
        :return:
        """
        d_list = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1]) ** 2 + (node.y - rnd[1]) ** 2 for node in node_list]
        min_index = d_list.index(min(d_list))
        return min_index

    @staticmethod
    def collision_check(new_node, obstacle_list):
        a = 1
        for (ox, oy, oz, size) in obstacle_list:
            dx = ox - new_node.x
            dy = oy - new_node.y
            dz = oz - new_node.z
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            if d <= size:
                a = 0  # collision

        return a  # safe

    def planning(self):
        """
        Path planning
        animation: flag for animation on or off
        """

        while True:
            # Random Sampling
            if random.random() > self.goalSampleRate:
                rnd = self.random_node()
            else:
                rnd = [self.end.x, self.end.y, self.end.z]

            # Find nearest node
            min_index = self.get_nearest_list_index(self.nodeList, rnd)
            # print(min_index)

            # expand tree
            nearest_node = self.nodeList[min_index]

            # 返回弧度制
            # theta = len(rnd[1] - nearest_node.y, rnd[0] - nearest_node.x)
            path_len = math.sqrt((rnd[2] - nearest_node.z) ** 2 +
                            (rnd[1] - nearest_node.y) ** 2 +
                            (rnd[0] - nearest_node.x) ** 2)
            path_x = (rnd[0] - nearest_node.x) / path_len
            path_y = (rnd[1] - nearest_node.y) / path_len
            path_z = (rnd[2] - nearest_node.z) / path_len
            new_node = copy.deepcopy(nearest_node)
            new_node.x += self.expandDis * path_x
            new_node.y += self.expandDis * path_y
            new_node.z += self.expandDis * path_z
            new_node.parent = min_index

            if not self.collision_check(new_node, self.obstacleList):
                continue

            self.nodeList.append(new_node)

            # check goal
            dx = new_node.x - self.end.x
            dy = new_node.y - self.end.y
            dz = new_node.z - self.end.z
            d = math.sqrt(dx * dx + dy * dy + dz * dz)
            if d <= self.expandDis:
                break
            if show_animation:
                self.draw_graph(rnd)

        path = [[self.end.x, self.end.y, self.end.z]]
        last_index = len(self.nodeList) - 1
        while self.nodeList[last_index].parent is not None:
            node = self.nodeList[last_index]
            path.append([node.x, node.y,node.z])
            last_index = node.parent
        path.append([self.start.x, self.start.y, self.start.z])

        return path

    def draw_graph(self, rnd=None):
        """
        Draw Graph
        """
        plt.clf()  # 清除上次画的图
        # fig = plt.figure()
        ax = plt.gca(projection='3d')

        if rnd is not None:
            ax.plot(rnd[0], rnd[1], rnd[2], "^g")
        for node in self.nodeList:
            if node.parent is not None:
                ax.plot([node.x, self.nodeList[node.parent].x], [
                    node.y, self.nodeList[node.parent].y], [node.z, self.nodeList[node.parent].z], "-g")

        for (ox, oy, oz, size) in self.obstacleList:
            ax.plot(ox, oy, oz, "sk", ms=10 * size)

        ax.plot(self.start.x, self.start.y, self.start.z, "^r")
        ax.plot(self.end.x, self.end.y, self.end.z, "^b")
        # plt.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand])
        ax.set_xlim(self.min_rand, self.max_rand)
        ax.set_ylim(self.min_rand, self.max_rand)
        ax.set_zlim(self.min_rand, self.max_rand)
        plt.grid(True)
        plt.pause(0.01)

    def draw_static(self, path):
        """
        画出静态图像
        :return:
        """
        # plt.clf()  # 清除上次画的图
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for node in self.nodeList:
            if node.parent is not None:
                ax.plot([node.x, self.nodeList[node.parent].x], [
                    node.y, self.nodeList[node.parent].y],[node.z, self.nodeList[node.parent].z], "-g")

        for (ox, oy, oz, size) in self.obstacleList:
            ax.plot(ox, oy, oz, "sk", ms=10 * size)

        ax.plot(self.start.x, self.start.y, self.start.z, "^r")
        ax.plot(self.end.x, self.end.y, self.end.z, "^b")
        # ax.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand, self.min_rand, self.max_rand])
        ax.set_xlim(self.min_rand, self.max_rand)
        ax.set_ylim(self.min_rand, self.max_rand)
        ax.set_zlim(self.min_rand, self.max_rand)
        ax.plot([data[0] for data in path], [data[1] for data in path], [data[2] for data in path], '-r')
        plt.grid(True)
        plt.show()


def main():
    print("start RRT path planning")

    obstacle_list = [
        (5, 1, 5, 1),
        (3, 6, 6, 1),
        (3, 8, 1, 1),
        (1, 1, 6, 1),
        (3, 5, 3, 1),
        (9, 5, 6, 1)]

    # Set Initial parameters
    rrt = RRT(start=[0, 0, 0], goal=[25, 17, 29], rand_area=[-32, 32], obstacle_list=obstacle_list)
    path = rrt.planning()
    print(path)

    # Draw final path
    plt.close()
    rrt.draw_static(path)


if __name__ == '__main__':
    main()
