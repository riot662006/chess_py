import pygame
from helper import load_image

from board import Board


class Game:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.is_running = True

        self.board = Board(self.screen)
        self.is_white = True

    def update(self):
        pass

    def render(self):
        self._draw_background()
        self._draw_board()

    def _draw_background(self):
        background = load_image("assets/images/background.jpg")
        background = pygame.transform.scale(background, self.screen.get_size())

        self.screen.blit(background, (0, 0))

    def _draw_board(self):
        self.board.draw(side='w' if self.is_white else 'b')

    def quit(self):
        self.is_running = False
