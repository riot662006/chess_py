from enum import Enum

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

USR_WHITE = 0
USR_BLACK = 1
USR_SPECTATOR = 2


class Palette(Enum):
    CHECK = "#FF0000"
    CHECKMATE = "#CC0000AA"
    CAPTURABLE = "#FC716B"
    MOVABLE = "#E5FFE5"
    SELECTED = "#ADF9A1"
    LAST_MOVE = "#F1EBBE"


BISHOP_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ROOK_DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
KNIGHT_MOVES = ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))

KING_MOVES = BISHOP_DIRECTIONS + ROOK_DIRECTIONS
QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + ROOK_DIRECTIONS

START_CONFIG = "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR"
TEST_CONFIG = "rnbqk..rppp..ppp...P.n....b.p..............B....PPPP.PPPRNBQK.NR"


class Align(Enum):
    LEFT = -1
    CENTER = 0
    RIGHT = 1
