import pygame

from utils import *


class Square:
    def __init__(self, notation):
        self.file = None
        self.rank = None

        if isinstance(notation, str):
            if len(notation) != 2 or notation[0] not in "abcdefgh" or notation[1] not in "12345678":
                raise AttributeError("Invalid square")
            self.file = "abcdefgh".index(notation[0]) + 1
            self.rank = int(notation[1])
        elif isinstance(notation, (tuple, list)):
            if len(notation) != 2 or not(1 <= notation[0] <= 8 and 1 <= notation[1] <= 8):
                raise AttributeError("Invalid square")
            self.file, self.rank = notation

    def __str__(self):
        return "abcdefgh"[self.file - 1] + str(self.rank)

    def __repr__(self):
        return f"Square <{str(self)}>"

    def add(self, f, r):
        try:
            return Square((self.file + f, self.rank + r))
        except AttributeError:
            return None

    def is_black(self):
        return (self.file + self.rank) % 2 == 0


class Board:
    def __init__(self, _screen: pygame.Surface | pygame.SurfaceType):
        self.screen = _screen
        self.length = 400
        self.margin = 10

        self.side = 0

    @property
    def square_length(self):
        return self.length / 8

    @property
    def square_rect(self):
        return pygame.Rect(0, 0, self.length / 8, self.length / 8)

    @property
    def board_rect(self):
        return pygame.Rect(0, 0, self.length, self.length)

    def get_square(self, name):
        if len(name) == 2 and name[0] in "abcdefgh" and name[1] in "12345678":
            file = "abcdefgh".index(name[0]) + 1
            rank = int(name[1])

            x = file
            y = rank

            if self.side == 0:
                x = x - 1
                y = 8 - y

            elif self.side == 1:
                x = 8 - x
                y = y - 1

            return self.square_rect.move((x * self.square_length, y * self.square_length))

        raise AttributeError("Invalid square")

    def is_pos_on_board(self, pos):
        return self.board_rect.move(self.margin, self.margin).collidepoint(pos)

    def get_square_from_pos(self, pos):
        if not(self.is_pos_on_board(pos)):
            return None

        file, rank = ((pos[0] - self.margin) // self.square_length) + 1, \
            ((pos[1] - self.margin) // self.square_length) + 1
        if self.side == 0:
            rank = 8 - rank + 1
        elif self.side == 1:
            file = 8 - file + 1

        print(file, rank)

        return "abcdefgh"[int(file) - 1] + str(int(rank))

    def __getattr__(self, name):
        if not isinstance(name, str):
            raise AttributeError("Invalid attribute name.")

        if len(name) == 2 and name[0] in "abcdefgh" and name[1] in "12345678":
            return self.get_square(name)

        if name not in self.__dict__:
            raise AttributeError(f"Attribute '{name}' not found.")
        return getattr(self, name)
