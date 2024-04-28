class PieceException(Exception):
    pass


class Piece:
    def __init__(self, color="w"):
        self.name = None
        self.color = "white" if color == "w" else "black"


class Pawn(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "pawn"


class Knight(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "knight"


class Bishop(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "bishop"


class Rook(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "rook"


class Queen(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "queen"


class King(Piece):
    def __init__(self, color="w"):
        super().__init__(color)
        self.name = "king"
