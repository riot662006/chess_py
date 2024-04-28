import pygame
import sys

from constants import *
from game import Game

pygame.init()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)

    while game.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

            elif event.type == pygame.KEYDOWN:
                print(game.board[6, 4])

        game.update()
        game.render()
        pygame.display.flip()


if __name__ == '__main__':
    main()
