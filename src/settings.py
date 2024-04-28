import pygame

from helper import load_pieces
from constants import *


class BoardSettings:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.board_padding = 30
        self.board_outline_width = 5

        self.piece_sprites = load_pieces("assets/images/pieces.png")
        self.piece_outline_width = 5

        print(self.piece_sprites)

    def get_board_length(self, with_outline=False):
        w, h = self.screen.get_size()

        if with_outline:
            w, h = w - self.board_padding * 2, h - self.board_padding * 2
        else:
            w, h = w - (self.board_padding + self.board_outline_width) * 2, h - (self.board_padding + self.board_outline_width) * 2

        return min(w, h)

    def get_board_pos(self, with_outline=False):
        w, h = self.screen.get_size()
        length = self.get_board_length(with_outline)

        x, y = (w - length) // 2, (h - length) // 2

        return x, y

    def get_board_rect(self, with_outline=False):
        length = self.get_board_length(with_outline)
        return pygame.Rect(*self.get_board_pos(with_outline), length, length)

    def get_board_square_length(self):
        length = self.get_board_length()
        length /= 8

        return length

    def get_piece_sprite(self, color, piece):
        square_len = self.get_board_square_length()
        return pygame.transform.smoothscale(self.piece_sprites[color][piece], (square_len, square_len))

    def get_piece_outline_sprite(self, color, piece):
        square_len = self.get_board_square_length()
        surf = self.piece_sprites[color][piece]

        outline_width = self.piece_outline_width * surf.get_size()[0] / square_len

        piece_mask = pygame.mask.from_surface(surf)
        piece_outline = piece_mask.outline()

        outline_surface = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
        outline_surface.blit(piece_mask.to_surface(unsetcolor=None, unsetsurface=None, setcolor=BLACK), (0, 0))

        for points in piece_outline:
            pygame.draw.circle(outline_surface, BLACK, points, outline_width)

        return pygame.transform.smoothscale(outline_surface, (square_len, square_len))
