import pygame

class Renderer():

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

        self.surface_cache = {}

    def render(self, forest, paused):
        self.surface.fill(pygame.Color(255, 255, 255))
        self._render_terrain(forest)

        for tree in forest.trees:
            self._render_tree(tree)

        pygame.display.update()

    def _render_terrain(self, forest):
        if forest.terrain in self.surface_cache.keys():
            surface = self.surface_cache[forest.terrain]
        else:
            surface = pygame.Surface((self.width, self.height))
            px_array = pygame.PixelArray(surface)

            try:
                for row in range(self.height):
                    for col in range(self.width):
                        if row >= forest.height or col >= forest.width:
                            px_array[col, row] = pygame.Color(0, 0, 0)
                        else:
                            t = int(forest.terrain.points[row][col] * 128.0 + 128.0)
                            px_array[col, row] = pygame.Color(t, t, t)
            finally:
                del px_array

            self.surface_cache[forest.terrain] = surface

        self.surface.blit(surface, (0, 0))

    def _render_tree(self, tree):
        color = self._get_tree_color(tree)
        pygame.draw.circle(self.surface, color, (tree.x, tree.y), round(tree.size), 0)

    def _get_tree_color(self, tree):
        r = tree.size / tree.species.max_size
        alpha = int(255 - 255 * r)

        if tree.species.name == "birch":
            return pygame.Color(255, 0, 0, alpha)
        elif tree.species.name == "oak":
            return pygame.Color(0, 255, 0, alpha)
        else:
            return pygame.Color(0, 0, 0, alpha)


class ImageCache():

    def __init__(self):
        self.cache = {}

    def get_image(self, image_location):
        if not image_location in self.cache.keys:
            self.cache[image_location] = pygame.image.load(image_location)

        return self.cache[image_location]
