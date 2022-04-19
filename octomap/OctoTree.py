import datetime
import math
import numpy as np
import xlwt

from datetime import datetime
from Config import FREE_LOGODDS, HIT_LOGODDS, OCCUPANY_LOGODDS, TREE_RESOLUTION, MISS_LOGODDS, LOGGER
from OctoNode import OctoNode


class OctoTree:
    """
    OctoMap to store 3D probabilistic occupancy information.
    """

    def __init__(self, center: tuple, resolution: int, max_depth: int):
        """
        Create a new OctoMap.
        The map will be created around the 'center' position.

        Args:
            center: the coordinate of the center --- (x,y,z): tuple
            resolution: maximal resolution --- int
            max_depth: maximun depth --- int
        
        Returns:
            a new OctoTree Map --- OctoTree
        """

        self._center = center
        self._resolution = resolution
        self._max_depth = max_depth

        self._root = OctoNode()

    @property
    def radius(self):
        """
        Returns:
            the radius of this tree (also width/2) --- int
        """
        radius: int = self._resolution * int(math.pow(2, self._max_depth - 1))

        return radius
    
    @property
    def width(self):
        """
        Returns:
            the width of this tree --- int
        """
        width: int = int(self._resolution * math.pow(2, self._max_depth))

        return width
    
    @property
    def origin(self):
        """
        Returns:
            the origin coordinate of this tree --- (x,y,z): tuple
        """
        origin: tuple = (self._center[0] - self.radius, self._center[1] - self.radius, self._center[2] - self.radius)
        
        return origin
    
    def insert_point(self, point: tuple, diff_logodds: float = HIT_LOGODDS):
        """
        Add an observation to the octo map.

        Args:
            point: the coordinate of the observation lidar point --- (x,y,z): tuple
            diff_logodds: the difference value of logodds
        """
        if not len(point) == 3:
            raise ValueError("Point should be tuple (x,y,z)")
        self._root.update(point, diff_logodds, self.origin, self.width, self._max_depth)

    def ray_casting(self, start_point: tuple, end_point: tuple, diff_logodds: float = MISS_LOGODDS):
        """
        Add the probability of the grid occupied by the ray path to the tree

        Args:
            start_point: the coordinate of the sensor --- (x,y,z): tuple
            end_point: the coordinate of the observation point  --- (x,y,z): tuple
            diff_logodds: the difference value of logodds
        """
        if len(start_point) != 3 or len(end_point) != 3:
            raise ValueError("Point should be tuple (x,y,z)")
        # insert occu node
        self.insert_point(end_point)
        # insert free node
        grid_path: list = self.bresenham3D(start_point, end_point)
        for point in grid_path:
            self._root.update(point, diff_logodds, self.origin, self.width, self._max_depth)

    @staticmethod
    def bresenham3D(startPoint, endPoint):
        """
        Use bresenham algorithm to return points on the ray's path
        """
        path = []

        startPoint = [int(startPoint[0]), int(startPoint[1]), int(startPoint[2])]
        endPoint = [int(endPoint[0]), int(endPoint[1]), int(endPoint[2])]
        endpoint_origin = [int(endPoint[0] / TREE_RESOLUTION) * TREE_RESOLUTION, 
                            int(endPoint[1] / TREE_RESOLUTION) * TREE_RESOLUTION, 
                            int(endPoint[2] / TREE_RESOLUTION) * TREE_RESOLUTION]

        steepXY = (np.abs(endPoint[1] - startPoint[1]) > np.abs(endPoint[0] - startPoint[0]))
        if steepXY:
            startPoint[0], startPoint[1] = startPoint[1], startPoint[0]
            endPoint[0], endPoint[1] = endPoint[1], endPoint[0]

        steepXZ = (np.abs(endPoint[2] - startPoint[2]) > np.abs(endPoint[0] - startPoint[0]))
        if steepXZ:
            startPoint[0], startPoint[2] = startPoint[2], startPoint[0]
            endPoint[0], endPoint[2] = endPoint[2], endPoint[0]

        delta = [np.abs(endPoint[0] - startPoint[0]), np.abs(endPoint[1] - startPoint[1]),
                 np.abs(endPoint[2] - startPoint[2])]

        errorXY = delta[0] / 2
        errorXZ = delta[0] / 2

        step = [
            -TREE_RESOLUTION if startPoint[0] > endPoint[0] else TREE_RESOLUTION,
            -TREE_RESOLUTION if startPoint[1] > endPoint[1] else TREE_RESOLUTION,
            -TREE_RESOLUTION if startPoint[2] > endPoint[2] else TREE_RESOLUTION
        ]

        y = startPoint[1]
        z = startPoint[2]

        for x in range(startPoint[0], endPoint[0], step[0]):
            point = [x, y, z]
            if steepXZ:
                point[0], point[2] = point[2], point[0]
            if steepXY:
                point[0], point[1] = point[1], point[0]
                
            errorXY -= delta[1]
            errorXZ -= delta[2]
            if errorXY < 0:
                y += step[1]
                errorXY += delta[0]
            if errorXZ < 0:
                z += step[2]
                errorXZ += delta[0]

            if (point != endpoint_origin):
                path.append(point)
        return path

    def contains(self, point: tuple):
        """
        Return whether the point is contained in this tree.

        Args:
            point: coordinate of the point to check --- (x,y,z): tuple
        Returns:
            whether the point is contained --- bool
        """
        if not len(point) == 3:
            raise ValueError("Point should be tuple (x,y,z)")

        res: bool = (self._center[0] - self.radius) <= point[0] < (self._center[0] + self.radius) and \
                    (self._center[1] - self.radius) <= point[1] < (self._center[1] + self.radius) and \
                    (self._center[2] - self.radius) <= point[2] < (self._center[2] + self.radius)
        return res
    
    def get_probability(self, point: tuple):
        """
        Return the occupancy probability of the voxel at a given point coordinate.

        Args:
            point: coordinate of some voxel to get probability --- (x,y,z): tuple
        Returns:
            occupancy probability of the corresponding voxel --- float
        """
        if not self.contains(point):
            raise ValueError("Invalid point.")
        
        probability: float = self._root.probability_at(point, self.origin, self.width)

        return probability
        
    def export_known_node(self):
        leaf_node_list: list = self.get_leaf_node_list()
        LOGGER.info("leaf_node_list: {}".format(len(leaf_node_list)))
        threshold_node_list: list = self.get_threshold_node_list(leaf_node_list)
        LOGGER.info("threshold_node_list: {}".format(len(threshold_node_list)))
        occu_node_list, free_node_list = self.get_classified_node_list(threshold_node_list)
        occu_node_coor_list, free_node_coor_list = self.get_classified_node_coor_list(occu_node_list, free_node_list)
        LOGGER.info("length of occu_node_coor_list: {}".format(len(occu_node_coor_list)))
        # LOGGER.info("occu_node_coor_list: {}".format(str(occu_node_coor_list)))
        LOGGER.info("length of free_node_coor_list: {}".format(len(free_node_coor_list)))
        # LOGGER.info("free_node_coor_list: {}",format(str(free_node_coor_list)))

        # Output points to xls file
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_occu_node = workbook.add_sheet('occu_node_coor_list')
        sheet_free_node = workbook.add_sheet('free_node_coor_list')
        value = datetime.today()
        date_value = datetime.strftime(value,'%H:%M:%S')
        sheet_occu_node.write(0, 0, label = 'x')
        sheet_occu_node.write(0, 1, label = 'y')
        sheet_occu_node.write(0, 2, label = 'z')
        sheet_occu_node.write(0, 3, label = date_value)
        sheet_occu_node.write(0, 4, label = len(occu_node_coor_list))

        sheet_free_node.write(0, 0, label = 'x')
        sheet_free_node.write(0, 1, label = 'y')
        sheet_free_node.write(0, 2, label = 'z')
        sheet_free_node.write(0, 3, label = date_value)
        sheet_occu_node.write(0, 4, label = len(free_node_coor_list))

        for i in range(len(occu_node_coor_list)):
            sheet_occu_node.write(i + 1, 0, occu_node_coor_list[i][0])
            sheet_occu_node.write(i + 1, 1, occu_node_coor_list[i][1])
            sheet_occu_node.write(i + 1, 2, occu_node_coor_list[i][2])
        for i in range(len(free_node_coor_list)):
            sheet_free_node.write(i + 1, 0, free_node_coor_list[i][0])
            sheet_free_node.write(i + 1, 1, free_node_coor_list[i][1])
            sheet_free_node.write(i + 1, 2, free_node_coor_list[i][2])
        workbook.save("./point_list.xls")


    def get_leaf_node_list(self):
        """
        Return leaf nodes for tree traversal
        """
        if not self._root:
            return []

        leaf_nodes = []
        queue = [self._root]
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
            node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), 
                        int(node.get_origin()[1] / TREE_RESOLUTION), 
                        int(node.get_origin()[2] / TREE_RESOLUTION))
            occu_node_coor_list.append(node_coor)
        for node in free_node_list:
            node_coor = (int(node.get_origin()[0] / TREE_RESOLUTION), 
                        int(node.get_origin()[1] / TREE_RESOLUTION), 
                        int(node.get_origin()[2] / TREE_RESOLUTION))
            free_node_coor_list.append(node_coor)

        return occu_node_coor_list, free_node_coor_list