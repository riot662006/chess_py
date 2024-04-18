import pygame

from utils import *
from board import Board
from pieces import BoardManager

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 650))
        load_resources()

        self.board_man = BoardManager(self.screen)
        self.board_man.test_setup()

        self.clock = pygame.time.Clock()
        self.fps = 50

    def next_frame(self):
        w, h = self.screen.get_size()
        pygame.draw.rect(self.screen, GREY, (0, 0, w, h))
        self.board_man.draw()

        pygame.display.flip()

    def mainloop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.board_man.handle_mouse_click(event.pos)

            self.next_frame()
            self.clock.tick(self.fps)
