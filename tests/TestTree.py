import math
import unittest
from forest.treespecies import TreeSpecies
from forest.tree import Tree


class TestTree(unittest.TestCase):

    def setUp(self):
        self.species = TreeSpecies("birch", 0.1, 10, 3, 0.8, 79, 2)

    def test_create(self):
        t = Tree(self.species, 100, 200)

        self.assertEqual(self.species, t.species)
        self.assertEqual(3, t.size)
        self.assertEqual(100, t.x)
        self.assertEqual(200, t.y)


    def test_grow_before_max(self):
        t = Tree(self.species, 100, 200)

        t.grow()
        self.assertEqual(3.1, t.size)

    def test_grow_past_max(self):
        t = Tree(self.species, 100, 200)

        for i in range(10000):
            t.grow()

        self.assertEqual(self.species.max_size, t.size)

    def test_is_mature_no(self):
        t = Tree(self.species, 100, 200)
        self.assertFalse(t.is_mature())

    def test_is_mature_yes(self):
        t = Tree(self.species, 100, 200)
        for i in range(10000):
            t.grow()

        self.assertTrue(t.is_mature())

    def test_overlapping_various(self):
        t1 = Tree(self.species, 100, 200)
        t2 = Tree(self.species, 100, 201)

        self.assertTrue(t1.overlapping(t2))
        self.assertTrue(t2.overlapping(t1))

        t1 = Tree(self.species, 100, 200)
        t2 = Tree(self.species, 101, 200)

        self.assertTrue(t1.overlapping(t2))
        self.assertTrue(t2.overlapping(t1))

        t1 = Tree(self.species, 99, 200)
        t2 = Tree(self.species, 100, 201)

        self.assertTrue(t1.overlapping(t2))
        self.assertTrue(t2.overlapping(t1))

        t1 = Tree(self.species, 100, 2)
        t2 = Tree(self.species, 100, 201)

        self.assertFalse(t1.overlapping(t2))
        self.assertFalse(t2.overlapping(t1))

        t1 = Tree(self.species, 0, 0)
        t2 = Tree(self.species, math.sqrt(18), math.sqrt(18))

        self.assertTrue(t1.overlapping(t2))
        self.assertTrue(t2.overlapping(t1))

        t1 = Tree(self.species, 0, 0)
        t2 = Tree(self.species, math.sqrt(18) + 0.1, math.sqrt(18) + 0.1)

        self.assertFalse(t1.overlapping(t2))
        self.assertFalse(t2.overlapping(t1))

    def test_contains_point(self):
        t = Tree(self.species, 0, 0)
        self.assertTrue(t.contains_point(0, 0))
        self.assertTrue(t.contains_point(math.sqrt(4.5), math.sqrt(4.5)))
        self.assertFalse(t.contains_point(math.sqrt(4.5) + 0.01, math.sqrt(4.5) + 0.01))

        t = Tree(self.species, 100, 100)
        self.assertTrue(t.contains_point(100, 100))
        self.assertTrue(t.contains_point(100 + math.sqrt(4.5) - 0.1, 100 + math.sqrt(4.5) - 0.1))
        self.assertFalse(t.contains_point(100 + math.sqrt(4.5) + 0.01, 100 + math.sqrt(4.5) + 0.01))


    def test_smaller_than(self):
        t1 = Tree(self.species, 100, 100)
        t2 = Tree(self.species, 100, 100)
        t2.grow()

        self.assertTrue(t1.smaller_than(t2))
        self.assertFalse(t2.smaller_than(t1))

    def test_absorb(self):
        t1 = Tree(self.species, 100, 100)
        t2 = Tree(self.species, 100, 100)
        t1.absorb(t2)

        self.assertEqual(6, t1.size)
