import pygame

from constants import *
from helper import load_image
from settings import BoardSettings
from square import Square
from pieces import King, Queen, Knight, Bishop, Rook, Pawn, Piece


class BoardException(Exception):
    pass


class Board:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen

        self._squares = [[None for j in range(8)] for i in range(8)]

        self.settings = BoardSettings(self.screen)
        self.str_to_pieces(start_config)

    def at(self, pos_or_square: Square | tuple[int, int]):
        if isinstance(pos_or_square, Square):
            return self._squares[pos_or_square.x][pos_or_square.y]

        if isinstance(pos_or_square, tuple):
            if len(pos_or_square) == 2 and Square.is_valid(*pos_or_square):
                return self._squares[pos_or_square[0]][pos_or_square[1]]

        raise BoardException("Invalid square position. got", pos_or_square)

    def draw(self, side='w'):
        pygame.draw.rect(self.screen, "black", self.settings.get_board_rect(True), self.settings.board_outline_width)
        rect = self.settings.get_board_rect()

        # board background
        background = load_image("assets/images/board.png").convert_alpha()
        background = pygame.transform.smoothscale(background, rect.size)
        self._draw_pieces(background, side)

        self.screen.blit(background, rect.topleft)

    def _draw_pieces(self, surf: pygame.Surface | pygame.SurfaceType, side='w'):
        square_length = self.settings.get_board_square_length()

        for y in range(8):
            for x in range(8):
                if self[x, y] is None:
                    continue

                color, name = self[x, y].color, self[x, y].name

                if side == 'w':
                    pos_x, pos_y = (8 - x - 1) * square_length, (8 - y - 1) * square_length
                else:
                    pos_x, pos_y = x * square_length, y * square_length

                surf.blit(self.settings.get_piece_outline_sprite(color, name),
                          (pos_x, pos_y), special_flags=pygame.BLEND_RGBA_SUB)
                surf.blit(self.settings.get_piece_sprite(color, name),
                          (pos_x, pos_y))

    def str_to_pieces(self, brd):
        if len(brd) != 64:
            raise BoardException("Invalid string to board conversion, got len = " + str(len(brd)))

        for j in range(8):
            for i in range(8):
                piece = None

                side = 'w' if brd[j * 8 + i].islower() else 'b'

                match str(brd[j * 8 + i]).lower():
                    case 'p':
                        piece = Pawn(side)
                    case 'r':
                        piece = Rook(side)
                    case 'n':
                        piece = Knight(side)
                    case 'b':
                        piece = Bishop(side)
                    case 'q':
                        piece = Queen(side)
                    case 'k':
                        piece = King(side)
                    case _:
                        pass

                self._squares[i][j] = piece
        print(self._squares)

    def __getitem__(self, item: tuple[int, int]) -> None | Piece:
        if isinstance(item, tuple):
            return self.at(item)

        raise BoardException("Invalid square position. got", item)

