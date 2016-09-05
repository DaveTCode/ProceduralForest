import math


class Tree:

    def __init__(self, species, x, y):
        self.species = species
        self.size = species.initial_size
        self.x = x
        self.y = y

    def absorb(self, victim):
        """
            Absorb one tree into another - note that this can't exceed the maximum size of the
            species.
        """
        self.size = min(self.size + victim.size, self.species.max_size)

    def grow(self):
        """
            Increase the size of the tree by the amount specified in the species.
        """
        self.size = min(self.size + self.species.growth_rate, self.species.max_size)

    def is_mature(self):
        """
            Some actions only occur when a tree is fully mature. This checks for that by comparing
            the size to the species maximum size.
        """
        return self.size == self.species.max_size

    def overlapping(self, tree):
        """
            Check whether this tree overlaps another tree - assumes circular tree.
        """
        d = math.sqrt(math.pow(tree.x - self.x, 2) + math.pow(tree.y - self.y, 2))

        return d <= tree.size + self.size

    def contains_point(self, x, y):
        """
            Check whether a point is within this tree.
        """
        d = math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))

        return d <= self.size

    def smaller_than(self, tree):
        return self.size < tree.size
