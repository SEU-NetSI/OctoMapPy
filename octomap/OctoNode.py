import math


class OctoNode:
    def __init__(self, default_probability: float=0.5):
        """
        Initiates a new OctoNode.

        Args:
            default_probability: the default probability of this node being occupied, 
            the probability of non-leaf will be set as 0.
        """
        self._children = None
        self._log_odds = math.log(default_probability / (1 - default_probability))

    def is_leaf(self):
        """
        Returns:
            whether this is a leaf node --- bool
        """
        return self._children is None

    def _split(self):
        """
        Splits the node into 8 child nodes.
        Child nodes are given the occupancy probability of this parent node as the initial probability
        """
        if not self.is_leaf():
            return
        
        self._children = (
            OctoNode(self.probability), OctoNode(self.probability), OctoNode(self.probability),
            OctoNode(self.probability), OctoNode(self.probability), OctoNode(self.probability),
            OctoNode(self.probability), OctoNode(self.probability),
        )

    def index(self, point, origin, width):
        """
        Calculates the index of the child containing point.

        Args:
            point: the coornidate of the child node --- (x,y,z): tuple
            origin: the origin coornidate of the parent node -- (x,y,z): tuple
            width: the width of the parent node --- int

        Returns:
            the index of the child --- int
        """
        if not self.contains(point, origin, width):
            raise ValueError('Point is not contained in node.')

        return (1 if point[0] >= origin[0] + width / 2 else 0) + \
               (2 if point[1] >= origin[1] + width / 2 else 0) + \
               (4 if point[2] >= origin[2] + width / 2 else 0)

    def contains(self, point, origin, width):
        """
        Returns:
            whether the point is contained by this node --- bool
        """
        return origin[0] <= point[0] < origin[0] + width and \
               origin[1] <= point[1] < origin[1] + width and \
               origin[2] <= point[2] < origin[2] + width

    def origin(self, index: int, origin: tuple, width: int):
        """
        Calculates the origin of the node with given index.

        Args:
            index: the index of the child node --- int
            origin: the origin coordinate of the parent node --- (x,y,z): tuple
            width: the width of the parent node --- int
        """
        hwidth: int = width / 2

        return (origin[0] + (hwidth if index & 1 else 0),
                origin[1] + (hwidth if index & 2 else 0),
                origin[2] + (hwidth if index & 4 else 0))

    def update(self, point, probability, origin, width, max_depth):
        """
        Updates the node with a new observation.

        Args:
            point: the point coornidate of the observation --- (x,y,z): tuple
            probability: probability of occupancy --- float
            origin: origin of this node --- (x,y,z): tuple
            width: width of this node --- int
            max_depth: maximum depth this node can be branched --- int
        """
        if max_depth == 0:
            self._update_probability(probability)
        else:
            if self.is_leaf():
                self._split()
                child_index = self.index(point, origin, width)
                child_index = self.index(point, origin, width)
                self._children[child_index].update(point, probability, self.origin(child_index, origin, width),
                                                   width / 2, max_depth - 1)

    def _update_probability(self, probability):
        """
        Updates the occupancy probability of the leaf node.

        Args:
            probability: pre-defined probability --- float
        """
        self._log_odds += math.log(probability / (1 - probability))

    @property
    def probability(self):
        """
        Returns:
            occupancy probability of node --- float
        """
        odds = math.pow(math.e, self._log_odds)
        return odds / (odds + 1)

    def probability_at(self, point, origin, width):
        """
        Args:
            point: point at which the occupancy needs to be calculated --- (x,y,z): tuple
            origin: origin of this node --- (x,y,z): tuple
            width: width of this node --- int

        Returns:
            occupancy probability of a given point.
        """
        if self.is_leaf():
            return self.probability
        else:
            child_index = self.index(point, origin, width)
            return self._children[child_index].probability_at(point, self.origin(child_index, origin, width), width / 2)
