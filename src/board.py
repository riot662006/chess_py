import pygame

from constants import *
from helper import load_image, get_moves_in_direction
from settings import BoardSettings
from square import Square
from pieces import King, Queen, Knight, Bishop, Rook, Pawn, Piece


class BoardException(Exception):
    pass


class Board:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen

        self._squares: list[list[None | Piece]] = [[None for _ in range(8)] for _ in range(8)]
        self._square_highlight: list[list[None | pygame.Color]] = [[None for _ in range(8)] for _ in
                                                                   range(8)]
        self.selected_square = None

        self.settings = BoardSettings(self.screen)
        self.str_to_board(START_CONFIG)

        # for testing
        # self.str_to_board(TEST_CONFIG)

        self.history = [str(self)]

    def __str__(self):
        res = ""

        for y in range(8):
            for x in range(8):
                if self._squares[x][y] is not None:
                    res += self._squares[x][y].short
                else:
                    res += "."

        return res

    def __getitem__(self, item: tuple[int, int] | Square) -> None | Piece:
        if isinstance(item, (tuple, Square)):
            return self.at(item)

        raise BoardException("Invalid square position. got", item)

    def at(self, pos_or_square: Square | tuple[int, int]):
        if isinstance(pos_or_square, Square):
            return self._squares[pos_or_square.x][pos_or_square.y]

        if isinstance(pos_or_square, tuple):
            if len(pos_or_square) == 2 and Square.is_valid(*pos_or_square):
                return self._squares[pos_or_square[0]][pos_or_square[1]]

        raise BoardException("Invalid square position. got", pos_or_square)

    def grid_to_board_square(self, x, y):
        if self.settings.side == USR_WHITE:  # white player
            return x, (8 - y - 1)
        if self.settings.side == USR_BLACK:  # black player
            return (8 - x - 1), y
        if self.settings.side == USR_SPECTATOR:  # spectator - TODO: fix later
            return x, (8 - y - 1)

        raise BoardException("Invalid settings for board side, got " + str(self.settings.side))

    def draw(self):
        pygame.draw.rect(self.screen, "black", self.settings.get_board_rect(True), self.settings.board_outline_width)
        rect = self.settings.get_board_rect()

        # board background
        background = load_image("assets/images/board.png").convert_alpha()
        background = pygame.transform.smoothscale(background, rect.size)
        self._draw_pieces(background)

        highlight_grid = self._draw_square_highlights()

        self.screen.blit(highlight_grid, rect.topleft)
        self.screen.blit(background, rect.topleft)

    def _draw_pieces(self, surf: pygame.Surface | pygame.SurfaceType):
        square_length = self.settings.get_board_square_length()

        for y in range(8):
            for x in range(8):
                if self[x, y] is None:
                    continue

                color, name = self[x, y].color, self[x, y].name

                pos_x, pos_y = [pos * square_length for pos in self.grid_to_board_square(x, y)]

                surf.blit(self.settings.get_piece_outline_sprite(color, name),
                          (pos_x, pos_y), special_flags=pygame.BLEND_RGBA_SUB)
                surf.blit(self.settings.get_piece_sprite(color, name),
                          (pos_x, pos_y))

    def _draw_square_highlights(self):
        surf = pygame.Surface(self.settings.get_board_rect().size, flags=pygame.SRCALPHA)
        square_length = self.settings.get_board_square_length()

        for y in range(8):
            for x in range(8):
                if self._square_highlight[x][y] is None:
                    continue

                pos_x, pos_y = [pos * square_length for pos in self.grid_to_board_square(x, y)]

                surf.fill(self._square_highlight[x][y],
                          (pos_x, pos_y, square_length, square_length),
                          special_flags=pygame.BLEND_RGBA_ADD)

        return surf

    def str_to_board(self, brd):
        if len(brd) != 64:
            raise BoardException("Invalid string to board conversion, got len = " + str(len(brd)))

        for j in range(8):
            for i in range(8):
                piece = None

                side = USR_WHITE if brd[j * 8 + i].islower() else USR_BLACK

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

    def get_clicked_square(self, pos: tuple[int, int]):
        board_rect = self.settings.get_board_rect()

        if board_rect.collidepoint(*pos):
            rel_pos = pygame.Vector2(pos[0] - board_rect.x, pos[1] - board_rect.y)
            rel_pos //= self.settings.get_board_square_length()

            pos_x, pos_y = self.grid_to_board_square(int(rel_pos.x), int(rel_pos.y))

            return Square(pos_x, pos_y)

        return None

    def set_highlight_color(self, square: Square, to: str | pygame.Color | None):
        if isinstance(to, str):
            to = pygame.Color(to)

        self._square_highlight[square.x][square.y] = to

    def has_been_moved(self, square: Square):
        start_piece = self.history[0][square.to_board_str_index()]

        for board_state in self.history:
            if start_piece != board_state[square.to_board_str_index()]:
                return True

        return False

    def get_move_squares(self, square: Square):
        piece = self[square]

        match piece:
            case None:
                return []

            case Pawn():
                if piece.color == USR_WHITE:
                    direction = 1
                elif piece.color == USR_BLACK:
                    direction = -1
                else:
                    raise BoardException("Invalid piece color, got " + str(piece.color))

                if Square.is_valid(square.x, square.y + direction) and self[square.x, square.y + direction] is None:
                    if Square.is_valid(square.x, square.y + 2 * direction) \
                            and self[square.x, square.y + 2 * direction] is None\
                            and not(self.has_been_moved(square)):
                        return [Square(square.x, square.y + direction), Square(square.x, square.y + 2 * direction)]
                    return [Square(square.x, square.y + direction)]
                return []

            case Bishop() | Rook() | Queen():
                moves = []

                if isinstance(piece, Bishop):
                    move_directions = BISHOP_DIRECTIONS
                elif isinstance(piece, Rook):
                    move_directions = ROOK_DIRECTIONS
                else:
                    move_directions = QUEEN_DIRECTIONS

                for move_dir in move_directions:
                    for move_square in get_moves_in_direction(square, move_dir):
                        if self[move_square] is not None:
                            break
                        moves.append(move_square)

                return moves

            case Knight():
                moves = []

                for move in KNIGHT_MOVES:
                    if Square.is_valid(square.x + move[0], square.y + move[1]) \
                            and self[square.x + move[0], square.y + move[1]] is None:
                        moves.append(Square(square.x + move[0], square.y + move[1]))

                return moves

            case Piece():
                return []
            case _:
                raise BoardException("Invalid piece on square. Cannot compute moves.")

    def move_piece(self, from_square: Square, to_square: Square):
        if self[from_square] is None:
            raise BoardException(f"No piece to move on {from_square}")

        if self[to_square] is not None:
            raise BoardException(f"Piece on {to_square}. Cannot move to occupied square")

        self._squares[to_square.x][to_square.y] = self[from_square]
        self._squares[from_square.x][from_square.y] = None

        self.history.append(str(self))
