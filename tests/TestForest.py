import math
import unittest
from forest.generator import TreeSpecies, Tree, Forest

class TestForest(unittest.TestCase):

    def setUp(self):
        self.species = TreeSpecies("birch", 0.1, 10, 3, 0.8, 79, 2)

    def test_create(self):
        f = Forest(1, 100, 200)
        self.assertEqual([], f.trees)
        self.assertEqual(100, f.width)
        self.assertEqual(200, f.height)
        self.assertEqual(10, f.cell_size)
        self.assertEqual(20, len(f.cells))
        self.assertEqual(10, len(f.cells[0]))

    def test_create_irregular_size(self):
        f = Forest(1, 17, 29)
        self.assertEqual(3, len(f.cells))
        self.assertEqual(2, len(f.cells[0]))

    def test_add_tree(self):
        f = Forest(1, 17, 29)
        t = Tree(self.species, 0, 0)
        f.add_tree(t)

        self.assertEqual([t], f.trees)
        self.assertEqual([t], f.cells[0][0])

        for row in range(1, len(f.cells)):
            for col in range(1, len(f.cells[0])):
                self.assertEqual([], f.cells[row][col])


    def test_add_tree_2(self):
        f = Forest(1, 17, 29)
        t = Tree(self.species, 16, 23)
        f.add_tree(t)

        self.assertEqual([t], f.trees)
        self.assertEqual([t], f.cells[2][1])

        for row in range(len(f.cells)):
            for col in range(len(f.cells[0])):
                if row == 2 and col == 1:
                    self.assertEqual([t], f.cells[row][col])
                else:
                    self.assertEqual([], f.cells[row][col])


    def test_remove_tree(self):
        f = Forest(1, 17, 29)
        t = Tree(self.species, 0, 0)
        f.add_tree(t)
        f.remove_tree(t)

        for row in range(len(f.cells)):
            for col in range(len(f.cells[0])):
                self.assertEqual([], f.cells[row][col])

    def test_get_all_nboring_cells_by_tree(self):
        f = Forest(1, 17, 29)
        t = Tree(self.species, 0, 0)
        f.add_tree(t)

        cells = f.get_all_nboring_cells_by_tree(t)
        self.assertEqual(4, len(cells))
        self.assertEqual(sorted([f.cells[0][0], f.cells[0][1], f.cells[1][0], f.cells[1][1]]), sorted(cells))

        t1 = Tree(self.species, 9, 11)
        cells = f.get_all_nboring_cells_by_tree(t1)
        self.assertEqual(6, len(cells))
        self.assertEqual(sorted([cell for row in f.cells for cell in row]), sorted(cells))
