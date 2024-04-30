import pygame
from helper import load_image

from board import Board
from constants import *


class Game:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.is_running = True

        self.board = Board(self.screen)
        self.board.settings.side = "w"

    def update(self):
        needs_render = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return False

            elif event.type == pygame.KEYDOWN:
                print(str(self.board))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.handle_board_clicks(event.pos)
                    needs_render = True

        return needs_render

    def render(self):
        self._draw_background()
        self._draw_board()

    def _draw_background(self):
        background = load_image("assets/images/background.jpg")
        background = pygame.transform.scale(background, self.screen.get_size())

        self.screen.blit(background, (0, 0))

    def _draw_board(self):
        self.board.draw()

    def handle_board_clicks(self, pos):
        if self.board.settings.get_board_rect().collidepoint(pos):
            self.board.handle_click(pos)

    def quit(self):
        self.is_running = False
