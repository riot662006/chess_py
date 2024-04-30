from constants import *

class PieceException(Exception):
    pass


class Piece:
    def __init__(self, color=USR_WHITE):
        self.name = None
        self.short = None
        self.color = color

        if color not in [USR_WHITE, USR_BLACK]:
            raise PieceException("Invalid piece color, got " + str(color))


class Pawn(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "pawn"
        self.short = "p" if color == USR_WHITE else "P"


class Knight(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "knight"
        self.short = "n" if color == USR_WHITE else "N"


class Bishop(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "bishop"
        self.short = "b" if color == USR_WHITE else "B"


class Rook(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "rook"
        self.short = "r" if color == USR_WHITE else "R"


class Queen(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "queen"
        self.short = "q" if color == USR_WHITE else "Q"


class King(Piece):
    def __init__(self, color=USR_WHITE):
        super().__init__(color)
        self.name = "king"
        self.short = "k" if color == USR_WHITE else "K"
