import pygame
import sys

from constants import *
from game import Game

pygame.init()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    game.render()

    while game.is_running:
        needs_render = game.update()
        if needs_render:
            game.render()
        pygame.display.flip()


if __name__ == '__main__':
    main()
