import pygame

class Renderer():

    def __init__(self, width=800, height=600):
        self.surface = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

    def render(self, forest):
        self.surface.fill(pygame.Color(255, 255, 255))

        for tree in forest.trees:
            self._render_tree(tree)

        pygame.display.update()

    def _render_tree(self, tree):
        color = self._get_tree_color(tree)
        pygame.draw.circle(self.surface, color, (tree.x, tree.y), round(tree.size), 0)

    def _get_tree_color(self, tree):
        r = tree.size / tree.species.max_size
        alpha = int(255 - 255 * r)

        if tree.species.name == "birch":
            return pygame.Color(0, 0, 0, alpha)
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
