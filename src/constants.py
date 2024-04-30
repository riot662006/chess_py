SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

USR_WHITE = 0
USR_BLACK = 1
USR_SPECTATOR = 2

CLR_CHECK = "#FF0000"
CLR_CHECKMATE = "#CC0000AA"
CLR_CAPTURABLE = "#FC716B"
CLR_SELECTED = "#ADF9A1"
CLR_LAST_MOVE = "#F1EBBE"

BISHOP_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ROOK_DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
KNIGHT_MOVES = ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))
QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + ROOK_DIRECTIONS

START_CONFIG = "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR"
TEST_CONFIG = ".............................r.................................."
