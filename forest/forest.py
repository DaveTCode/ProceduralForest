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

    def _is_point_too_close_to_tree(self, x, y, species):
        '''
            When seeding a new tree we need to check whether there is space for it.

            This is based on the slope of the terrain at that point (hence the magic numbers) in
            this function.
        '''
        s = self.terrain.max_slope[y][x]
        d = int(10 * s / 0.05)

        for tree in [t for cell in self.get_all_nboring_cells_by_point(x, y) for t in cell]:
            if abs(tree.x - x) < tree.size + species.initial_size + d:
                return True

        return False

    def spread_tree_seed(self, tree):
        '''
            At each iteration, once a tree is mature, it spreads seeds based on some constants
            defined in the species.

            This function performs that and is therefore responsible for attempting to grow new
            trees.
        '''
        to_be_added = set()

        for i in range(tree.species.seed_rate):

            if random.random() < tree.species.seed_survivability:
                d = random.uniform(tree.size, tree.species.seed_spread_distance)
                direction = random.uniform(0, 2 * math.pi)

                x = tree.x + round(d * math.cos(direction))
                y = tree.y + round(d * math.sin(direction))

                if self._can_plant_seed(x, y, tree.species):
                    to_be_added.add(Tree(tree.species, x, y))

        return to_be_added

    def _can_plant_seed(self, x, y, species):
        '''
            Returns true if this location is a valid seed point and false otherwise.
        '''
        if x < 0 or x >= self.width or y < 0 or y >= self.height: # Outside of the forest
            return False

        if self.terrain.max_slope[y][x] > species.slope_threshhold: # Slope too steep for this tree type
            return False

        if self._is_point_too_close_to_tree(x, y, species): # Don't seed a tree too close to another tree
            return False

        return True

    def iterate(self):
        '''
            Perform a single iteration of the forest generation routine.

            This acts on each tree in turn; growing, handling collisions post growth and then
            spreading the trees seeds.
        '''
        to_be_removed = set()
        to_be_added = set()

        for tree in self.trees:
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
                            break

                if tree.is_mature() and tree not in to_be_removed:
                    to_be_added |= self.spread_tree_seed(tree)

        for tree in to_be_removed:
            self.remove_tree(tree)

        for tree in to_be_added:
            self.add_tree(tree)
