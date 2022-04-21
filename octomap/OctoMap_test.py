import unittest
import math

from Config import TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH
from OctoTree import OctoTree

class TestOctoTree(unittest.TestCase):
    octotree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)

    def test_create_tree(self):
        self.assertEqual(self.octotree.get_center(), TREE_CENTER)
        self.assertEqual(self.octotree.get_resolution(), TREE_RESOLUTION)
        self.assertEqual(self.octotree.get_max_depth(), TREE_MAX_DEPTH)
    
    def test_tree_range(self):
        size = TREE_RESOLUTION * math.pow(2, TREE_MAX_DEPTH)
        corner_point = (size / 2, size / 2, size / 2)
        self.assertTrue(self.octotree.contains(TREE_CENTER))
        self.assertTrue(self.octotree.contains(corner_point))

if __name__ == '__main__':
    unittest.main()