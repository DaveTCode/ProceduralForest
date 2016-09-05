import pygame
from pygame.locals import *

HEIGHTMAP_MODE = 0
SLOPE_MODE = 1


class Renderer:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.mode = HEIGHTMAP_MODE

    def handle_event(self, event):
        if event.type == KEYUP:
            if event.key == K_s:
                self.mode = SLOPE_MODE
            elif event.key == K_h:
                self.mode = HEIGHTMAP_MODE

    def render(self, forest, paused):
        self.surface.fill(pygame.Color(255, 255, 255))

        if self.mode == HEIGHTMAP_MODE:
            self._render_terrain(forest)
        elif self.mode == SLOPE_MODE:
            self._render_slopes(forest)

        for tree in forest.trees:
            self._render_tree(tree)

        pygame.display.update()

    def _create_surface_from_2d_array(self, arr, f):
        """
            Utility function to create a grey map from a 2d array of values between 0 and 1.
        """
        surface = pygame.Surface((self.width, self.height))
        px_array = pygame.PixelArray(surface)

        try:
            for row in range(self.height):
                for col in range(self.width):
                    if row >= len(arr) or col >= len(arr[0]):
                        px_array[col, row] = pygame.Color(0, 0, 0)
                    else:
                        t = f(arr[row][col])

                        px_array[col, row] = pygame.Color(t, t, t)
        finally:
            del px_array

        return surface

    def _render_slopes(self, forest):
        try:
            surface = forest.terrain.cached_slope_map_surface
        except AttributeError:
            def f(x):
                return int(min(255, x * 255 / 0.04))

            surface = self._create_surface_from_2d_array(forest.terrain.max_slope, f)
            forest.terrain.cached_slope_map_surface = surface

        self.surface.blit(surface, (0, 0))

    def _render_terrain(self, forest):
        try:
            surface = forest.terrain.cached_normalized_points_surface
        except AttributeError:
            def f(x):
                return int(x * 255)

            surface = self._create_surface_from_2d_array(forest.terrain.normalized_points, f)
            forest.terrain.cached_normalized_points_surface = surface

        self.surface.blit(surface, (0, 0))

    def _render_tree(self, tree):
        color = Renderer._get_tree_color(tree)
        pygame.draw.circle(self.surface, color, (tree.x, tree.y), round(tree.size), 0)

    @staticmethod
    def _get_tree_color(tree):
        r = tree.size / tree.species.max_size
        alpha = int(255 - 255 * r)

        if tree.species.name == "birch":
            return pygame.Color(255, 0, 0, alpha)
        elif tree.species.name == "oak":
            return pygame.Color(0, 255, 0, alpha)
        else:
            return pygame.Color(0, 0, 0, alpha)


class ImageCache:
    def __init__(self):
        self.cache = {}

    def get_image(self, image_location):
        if image_location not in self.cache.keys:
            self.cache[image_location] = pygame.image.load(image_location)

        return self.cache[image_location]
