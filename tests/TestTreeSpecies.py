import math
import unittest
from forest.treespecies import TreeSpecies


class TestTreeSpecies(unittest.TestCase):

    def test_create(self):
        s = TreeSpecies("birch", 0.1, 10, 3, 0.8, 79, 2)
        self.assertEqual("birch", s.name)
        self.assertEqual(0.1, s.growth_rate)
        self.assertEqual(10, s.max_size)
        self.assertEqual(3, s.initial_size)
        self.assertEqual(0.8, s.seed_survivability)
        self.assertEqual(79, s.seed_spread_distance)
        self.assertEqual(2, s.seed_rate)
