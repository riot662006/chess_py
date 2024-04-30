class PieceException(Exception):
    pass


class Piece:
    def __init__(self, color="w"):
        self.name = None
        self.short = None
        self.color = "white" if color == "w" else "black"


class Pawn(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "pawn"
        self.short = "p" if color == "w" else "P"


class Knight(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "knight"
        self.short = "n" if color == "w" else "N"


class Bishop(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "bishop"
        self.short = "b" if color == "w" else "B"


class Rook(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "rook"
        self.short = "r" if color == "w" else "R"


class Queen(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "queen"
        self.short = "q" if color == "w" else "Q"


class King(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "king"
        self.short = "k" if color == "w" else "K"
