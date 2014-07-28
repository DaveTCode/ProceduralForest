import argparse
import pygame
from pygame.locals import *
import sys
import random
from forest.renderer import Renderer
from forest.treespecies import TreeSpecies
from forest.tree import Tree
from forest.forest import Forest
from forest.terrain import TerrainGenerator

WIDTH = 800
HEIGHT = 600

def run(seed):
    pygame.init()
    fps_clock = pygame.time.Clock()

    running = True

    renderer = Renderer(WIDTH, HEIGHT)
    forest = create_base_forest(seed, WIDTH, HEIGHT)
    ticks_since_iterate = 0

    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    paused = not paused

        ticks_since_iterate += 1
        if ticks_since_iterate == 6 and not paused:
            forest.iterate()
            ticks_since_iterate = 0

        renderer.render(forest, paused)

        fps_clock.tick(60)

    pygame.quit()
    return 0

def create_base_forest(seed, width, height):
    '''
        Placeholder for creating the base forest until I decide how to tie that in.
    '''
    terrain_gen = TerrainGenerator(seed)
    terrain = terrain_gen.generate(width, height)
    forest = Forest(seed, terrain, width, height)

    oak = TreeSpecies("oak", 0.1, 10, 1, 0.2, 100, 5)
    birch = TreeSpecies("birch", 0.3, 5, 1, 0.2, 30, 5)
    for i in range(0, 6):
        forest.trees.append(Tree(birch, random.randint(0, width), random.randint(0, height)))

    for i in range(0, 4):
        forest.trees.append(Tree(oak, random.randint(0, width), random.randint(0, height)))

    return forest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a procedural forest')
    parser.add_argument('--seed', '-s', type=int, help='The seed for the random number generator. Two forests with the same seed will be identical')
    args = parser.parse_args()

    sys.exit(run(args.seed))
