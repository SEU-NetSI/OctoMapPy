import math


class OctoNode:
    def __init__(self, prior_prob=0.5):
        """
        Initiates a new OctoNode
        prior_prob: the prior probability of this node being occupied
        """
        self._children = None
        self._log_odds = math.log(prior_prob/1-prior_prob)

    def is_leaf(self):
        """
        Returns whether this is a leaf node
        """
        return self._children is None

    def _split(self):
        """
        Splits the node into 8 child nodes
        """
        if not self.is_leaf():
            return
        """
        Child nodes are given the occupancy of this parent node as the initial probability of occupancy
        """
        self._children = (
            OctoNode(self.probability), OctoNode(self.probability), OctoNode(self.probability),
            OctoNode(self.probability), OctoNode(self.probability), OctoNode(self.probability),
            OctoNode(self.probability), OctoNode(self.probability),
        )

    def index(self, point, origin, width):
        """
        Calculates the index of the child containing point
        """
        if not self.contains(point, origin, width):
            raise ValueError('Point is not contained in node')

        return (1 if point[0] >= origin[0] + width / 2 else 0) +\
               (2 if point[1] >= origin[1] + width / 2 else 0) +\
               (4 if point[2] >= origin[2] + width / 2 else 0)

    def contains(self, point, origin, width):
        """
        Returns whether the point is contained by this node
        """
        return origin[0] <= point[0] < origin[0] + width and \
               origin[1] <= point[1] < origin[1] + width and \
               origin[2] <= point[2] < origin[2] + width

    def origin(self, index, origin, width):
        """
        Calculates the origin of the node with given index
        """
        hwidth = width / 2
        return (origin[0] + (hwidth if index & 1 else 0),
                origin[1] + (hwidth if index & 2 else 0),
                origin[2] + (hwidth if index & 4 else 0))

    def update(self, point, probability, origin, width, max_depth):
        """
        Updates the node with a new observation.

            Args:
                point: the point of the observation
                probability: probability of occupancy
                origin: origin of this node
                width: width of this node
                max_depth: maximum depth this node can be branched
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
        Updates the probability of occupancy
        """
        self._log_odds += math.log(probability / (1 - probability))

    @property
    def probability(self):
        """
        Returns probability of occupancy
        """
        odds = math.pow(math.e, self._log_odds)
        return odds / (odds + 1)

    def probability_at(self, point, origin, width):
        """
        Returns probability of occupancy at a given point.
        Args:
            point: point at which the occupancy needs to be calculated
            origin: origin of this node
            width: width of this node
        """
        if self.is_leaf():
            return self.probability
        else:
            child_index = self.index(point, origin, width)
            return self._children[child_index].probability_at(point, self.origin(child_index, origin, width), width / 2)










