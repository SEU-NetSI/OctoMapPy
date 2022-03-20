import math
import OctoNode
from Config import HIT_LOGODDS


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
            point: the coordinate of the ovservation lidar point --- (x,y,z): tuple
            diff_logodds: the difference value of logodds
        """
        if not len(point) == 3:
            raise ValueError("Point shoule be tuple (x,y,z)")

        self._root.update(point, diff_logodds, self.origin, self.width, self._max_depth)

    def ray_casting(self, point: tuple):
        """
        Add an observation to the treemap.

        Args:
            point: the coordinate of the ovservation lidar point --- (x,y,z): tuple
        """
        if not len(point) == 3:
            raise ValueError("Point shoule be tuple (x,y,z)")    

    def contains(self, point: tuple):
        """
        Return whether the point is contained in this tree.

        Args:
            point: coordinate of the point to check --- (x,y,z): tuple
        Returns:
            whether the point is contained --- bool
        """
        if not len(point) == 3:
            raise ValueError("Point shoule be tuple (x,y,z)")

        res: bool = (self._center[0] - self.radius) <= point[0] < (self._center[0] + self.radius) and \
                    (self._center[1] - self.radius <= point[1]) < (self._center[1] + self.radius) and \
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
        