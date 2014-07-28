import math
import random


grad = [(1, 1, 0),(-1, 1, 0),(1,-1, 0),(-1,-1, 0),
        (1, 0, 1),(-1, 0, 1),(1, 0,-1),(-1, 0,-1),
        (0, 1, 1),( 0,-1, 1),(0, 1,-1),( 0,-1,-1)]
F = 0.5 * (math.sqrt(3) - 1.0)
G = (3.0 - math.sqrt(3)) / 6.0

class Terrain():

    def __init__(self, points):
        self.points = points
        self.normalized_points = [[1.0 - (x + 1.0) / 2.0 for x in row] for row in self.points]

class TerrainGenerator():
    '''
        This is a basic Simplex Noise generation algorithm based on the reference implementation
        at http://www.itn.liu.se/~stegu/simplexnoise/SimplexNoise.java by Peter Eastman and Stefan
        Gustavson.

        Rewritten in pure python to remove dependency on c++ compiler required when attempting to
        install the noise library.
    '''

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)
        self._randomize_permutation_table()

    def generate(self, width, height):
        '''
            Generate an entire 2d map of simplex noise based on the permutation table which was
            created when the class was instantiated.
        '''
        r = [[0.0 for _ in range(width)] for _ in range(height)]
        f = 3.0 / max(height, width)
        for row in range(height):
            for col in range(width):
                r[row][col] = self._generate_point(col * f, row * f)

        return Terrain(r)

    def _generate_point(self, x, y):
        '''
            Generates a single point of simplex noise at the given x,y coordinates using the
            permutation table calculated when this class was instantiated.
        '''
        s = (x + y) * F
        i, j = int(x + s), int(y + s)

        t = (i + j) * G
        x0, y0 = x - i + t, y - j + t

        if x0 > y0:
            i1, j1 = 1, 0
        else:
            i1, j1 = 0, 1

        x1 = x0 - i1 + G
        y1 = y0 - j1 + G
        x2 = x0 - 1.0 + 2.0 * G
        y2 = y0 - 1.0 + 2.0 * G

        ii, jj = i & 255, j & 255
        gi0 = self.permutation_table_mod_12[ii + self.permutation_table[jj]]
        gi1 = self.permutation_table_mod_12[ii + i1 + self.permutation_table[jj + j1]]
        gi2 = self.permutation_table_mod_12[ii + 1 + self.permutation_table[jj + 1]]

        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 < 0:
            n0 = 0.0
        else:
            t0 *= t0
            n0 = t0 * t0 * (grad[gi0][0] * x0 + grad[gi0][1] * y0)

        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 < 0:
            n1 = 0.0
        else:
            t1 *= t1
            n1 = t1 * t1 * (grad[gi1][0] * x1 + grad[gi1][1] * y1)

        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 < 0:
            n2 = 0.0
        else:
            t2 *= t2
            n2 = t2 * t2 * (grad[gi2][0] * x2 + grad[gi2][1] * y2)

        return 70.0 * (n0 + n1 + n2)

    def _randomize_permutation_table(self):
        '''
            The only random element to the algorithm for generating the terrain is the permutation
            table. This function randomizes the table given the passed in seed.
        '''
        p = list(range(256))
        random.shuffle(p)
        self.permutation_table = p * 2
        self.permutation_table_mod_12 = [x % 12 for x in self.permutation_table]
