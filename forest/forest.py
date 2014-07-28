import math
import random
from forest.tree import Tree

class Forest:

    def __init__(self, random_seed, terrain, width, height):
        self.terrain = terrain
        self.trees = []
        self.width = width
        self.height = height
        random.seed(random_seed)
        self.cell_size = 10
        self.cells = [[] for _ in range(int(math.ceil(self.height / self.cell_size)))]
        for row in range(len(self.cells)):
            self.cells[row] = [[] for _ in range(int(math.ceil(self.width / self.cell_size)))]

    def add_tree(self, tree):
        '''
            Used to add trees so that they are maintained correctly in the space partitioned cells.
        '''
        self.trees.append(tree)
        self.get_cell(tree).append(tree)

    def remove_tree(self, tree):
        '''
            Used to remove trees so that they are maintained correctly in the space partitioned
            cells.
        '''
        self.trees.remove(tree)
        self.get_cell(tree).remove(tree)

    def get_cell(self, tree):
        '''
            Get the cell in which a tree begins - a tree may overlap into another cell.
        '''
        return self.get_cell_from_point(tree.x, tree.y)

    def get_all_nboring_cells_by_tree(self, tree):
        '''
            For a given tree we need to know which are the 9 cells with which it might interact.
        '''
        return self.get_all_nboring_cells_by_point(tree.x, tree.y)

    def get_cell_from_point(self, x, y):
        '''
            Get the cell that a single point lives in.
        '''
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)

        return self.cells[row][col]

    def get_all_nboring_cells_by_point(self, x, y):
        '''
            Get a list of all [at most] 9 cells that are neighboring the one containing a point.

            This allows us to check if any of the 9 cells contain a tree which will overlap this
            point.
        '''
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)

        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if row + i >= 0 and row + i < len(self.cells) and col + j >= 0 and col + j < len(self.cells[0]):
                    cells.append(self.cells[row + i][col + j])

        return cells

    def absorb_tree(self, tree, victim):
        '''
            Absorb one tree into another by increasing the size of one and removing the other from
            the forest.
        '''
        self.remove_tree(victim)
        tree.absorb(victim)

    def _is_point_in_tree(self, x, y):
        '''
            Check if a given point is contained within a tree. Only need to check current cell plus
            neighboring.
        '''
        for cell in self.get_all_nboring_cells_by_point(x, y):
            for tree in cell:
                if tree.contains_point(x, y):
                    return True

        return False

    def spread_tree_seed(self, tree):
        '''
            At each iteration, once a tree is mature, it spreads seeds based on some constants
            defined in the species.

            This function performs that and is therefore responsible for attempting to grow new
            trees.
        '''
        for i in range(tree.species.seed_rate):
            if random.random() * self.terrain.normalized_points[tree.y][tree.x] < tree.species.seed_survivability:
                d = random.uniform(tree.size, tree.species.seed_spread_distance)
                direction = random.uniform(0, 2 * math.pi)

                x = tree.x + round(d * math.cos(direction))
                y = tree.y + round(d * math.sin(direction))

                if x >= 0 and x < self.width and y >= 0 and y < self.height and not self._is_point_in_tree(x, y):
                    self.add_tree(Tree(tree.species, x, y))

    def iterate(self):
        '''
            Perform a single iteration of the forest generation routine.

            This acts on each tree in turn growing, handling collisions post growth and then
            spreading the trees seeds.
        '''
        to_be_removed = set()

        for tree in list(self.trees):
            if tree not in to_be_removed:
                tree.grow()

                # Complex - only care about the adjacent cells for collision purposes so flatten trees
                # from those into a list to iterate over.
                for collide_tree in [t for cell in self.get_all_nboring_cells_by_tree(tree) for t in cell]:
                    if collide_tree not in to_be_removed and collide_tree != tree and collide_tree.overlapping(tree):
                        if collide_tree.smaller_than(tree):
                            tree.absorb(collide_tree)
                            to_be_removed.add(collide_tree)
                        else:
                            collide_tree.absorb(tree)
                            to_be_removed.add(tree)

                if tree.is_mature() and tree not in to_be_removed:
                    self.spread_tree_seed(tree)

        for tree in to_be_removed:
            self.remove_tree(tree)
