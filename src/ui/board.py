import pygame
from .ui_element import UIElement

from ..constants import *
from ..helper import load_image, get_moves_in_direction
from .settings import BoardSettings
from ..square import Square
from ..pieces import King, Queen, Knight, Bishop, Rook, Pawn, Piece


class BoardException(Exception):
    pass


class Board(UIElement):
    def __init__(self, surface_size: tuple[int, int], config=START_CONFIG):
        super().__init__(surface_size)
        self.settings = BoardSettings(self.surface)

        self._squares: list[list[None | Piece]] = [[None for _ in range(8)] for _ in range(8)]
        self._square_highlight: list[list[None | pygame.Color]] = [[None for _ in range(8)] for _ in
                                                                   range(8)]
        self.selected_square = None

        self.str_to_board(config)

        self.history = [[str(self), (None, None)]]
        self.redo_history = []

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
        self.clear()

        pygame.draw.rect(self.settings.surface, "black", self.settings.get_rect(True), self.settings.outline_width)
        rect = self.settings.get_rect()

        # board background
        background = load_image("assets/images/board.png").convert_alpha()
        background = pygame.transform.smoothscale(background, rect.size)
        self._draw_pieces(background)

        highlight_grid = self._draw_square_highlights()

        self.settings.surface.blit(highlight_grid, rect.topleft)
        self.settings.surface.blit(background, rect.topleft)

    def _draw_pieces(self, surf: pygame.Surface | pygame.SurfaceType):
        square_length = self.settings.get_square_length()

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
        surf = pygame.Surface(self.settings.get_rect().size, flags=pygame.SRCALPHA)
        square_length = self.settings.get_square_length()

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
        board_rect = self.settings.get_rect()

        if board_rect.collidepoint(*pos):
            rel_pos = pygame.Vector2(pos[0] - board_rect.x, pos[1] - board_rect.y)
            rel_pos //= self.settings.get_square_length()

            pos_x, pos_y = self.grid_to_board_square(int(rel_pos.x), int(rel_pos.y))

            return Square(pos_x, pos_y)

        return None

    def set_highlight_color(self, square: Square, to: str | pygame.Color | None):
        if isinstance(to, str):
            to = pygame.Color(to)

        self._square_highlight[square.x][square.y] = to

    def reset_highlight_color(self, colors: tuple | list | None = None):
        if colors is not None:
            colors = [pygame.Color(color) for color in colors]

        for y in range(8):
            for x in range(8):
                if colors is None or self._square_highlight[x][y] in colors:
                    self.set_highlight_color(Square(x, y), None)

    def has_been_moved(self, square: Square):
        start_piece = self.history[0][0][square.to_board_str_index()]

        for board_state, _ in self.history:
            if start_piece != board_state[square.to_board_str_index()]:
                return True

        return False

    def attackers(self, square: Square, by):
        attackers = []

        if by not in [USR_WHITE, USR_BLACK]:
            raise BoardException("Invalid attacking user")

        # check pawn
        pawn_pos = [(square.x + x, square.y + (-1 if by == USR_WHITE else 1)) for x in (-1, 1)]
        for pos in pawn_pos:
            if Square.is_valid(*pos) and isinstance(self[*pos], Pawn) and self[*pos].color == by:
                attackers.append(Square(*pos))

        # check king
        for x, y in KING_MOVES:
            if Square.is_valid(square.x + x, square.y + y):
                pos_square = square + (x, y)
                if isinstance(self[pos_square], King) and self[pos_square].color == by:
                    attackers.append(pos_square)

        # check knight
        for x, y in KNIGHT_MOVES:
            if Square.is_valid(square.x + x, square.y + y):
                pos_square = square + (x, y)
                if isinstance(self[pos_square], Knight) and self[pos_square].color == by:
                    attackers.append(pos_square)

        # check bishop (and queen diagonals)
        for move_dir in BISHOP_DIRECTIONS:
            for move_square in get_moves_in_direction(square, move_dir):
                if self[move_square] is None:
                    continue

                if isinstance(self[move_square], (Bishop, Queen)) and self[move_square].color == by:
                    attackers.append(move_square)

                break

        # check rook (and queen straights)
        for move_dir in ROOK_DIRECTIONS:
            for move_square in get_moves_in_direction(square, move_dir):
                if self[move_square] is None:
                    continue

                if isinstance(self[move_square], (Rook, Queen)) and self[move_square].color == by:
                    attackers.append(move_square)

                break

        return attackers

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
                            and self[square.x, square.y + 2 * direction] is None \
                            and not (self.has_been_moved(square)):
                        return [square + (0, direction), square + (0, 2 * direction)]
                    return [square + (0, direction)]
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

            case Knight() | King():
                moves = []

                if isinstance(piece, King):
                    p_moves = KING_MOVES

                    if self.is_castle_move(square, (2, 0)):
                        moves.append(square + (2, 0))
                    if self.is_castle_move(square, (-2, 0)):
                        moves.append(square + (-2, 0))
                else:
                    p_moves = KNIGHT_MOVES

                for move in p_moves:
                    if Square.is_valid(square.x + move[0], square.y + move[1]) \
                            and self[square.x + move[0], square.y + move[1]] is None:
                        moves.append(square + move)

                return moves

            case Piece():
                return []
            case _:
                raise BoardException("Invalid piece on square. Cannot compute moves.")

    def get_capture_squares(self, square: Square):
        piece = self[square]

        match piece:
            case None:
                return []

            case Pawn():
                captures = []

                if piece.color == USR_WHITE:
                    direction = 1
                elif piece.color == USR_BLACK:
                    direction = -1
                else:
                    raise BoardException("Invalid piece color, got " + str(piece.color))

                for move in [(-1, direction), (1, direction)]:
                    if Square.is_valid(square.x + move[0], square.y + move[1]):
                        capture_square = square + (move[0], move[1])
                        # normal capture
                        if (self[capture_square] is not None and self[capture_square].color != piece.color) \
                                or self.is_en_passant_move(square, move):
                            captures.append(capture_square)

                return captures

            case Bishop() | Rook() | Queen():
                captures = []

                if isinstance(piece, Bishop):
                    move_directions = BISHOP_DIRECTIONS
                elif isinstance(piece, Rook):
                    move_directions = ROOK_DIRECTIONS
                else:
                    move_directions = QUEEN_DIRECTIONS

                for move_dir in move_directions:
                    for move_square in get_moves_in_direction(square, move_dir):
                        if self[move_square] is not None:
                            if self[move_square].color != piece.color:
                                captures.append(move_square)
                            break

                return captures

            case Knight() | King():
                captures = []

                if isinstance(piece, King):
                    p_moves = KING_MOVES
                else:
                    p_moves = KNIGHT_MOVES

                for move in p_moves:
                    if Square.is_valid(square.x + move[0], square.y + move[1]) \
                            and self[square.x + move[0], square.y + move[1]] is not None \
                            and self[square.x + move[0], square.y + move[1]].color != piece.color:
                        captures.append(square + move)

                return captures

            case _:
                raise BoardException("Invalid piece on square. Cannot compute moves.")

    def move_piece(self, from_square: Square, to_square: Square, reset_redo_history=True):
        if self[from_square] is None:
            raise BoardException(f"No piece to move on {from_square}")

        if self[to_square] is not None:
            raise BoardException(f"Piece on {to_square}. Cannot move to occupied square")

        if isinstance(self[from_square], King):
            if self.is_castle_move(from_square, to_square - from_square):
                direction = (to_square - from_square)[0] // 2

                for square in get_moves_in_direction(from_square, (direction, 0)):
                    if isinstance(self[square], Rook):
                        rook_to_square = to_square + (-direction, 0)
                        self._squares[rook_to_square.x][rook_to_square.y] = self[square]
                    self._squares[square.x][square.y] = None

        self._squares[to_square.x][to_square.y] = self[from_square]
        self._squares[from_square.x][from_square.y] = None

        self.history.append([str(self), (from_square, to_square)])

        if reset_redo_history:
            self.redo_history = []

    def capture_piece(self, from_square, to_square, reset_redo_history=True):
        if self[from_square] is None:
            raise BoardException(f"No piece to move on {from_square}")

        if self[to_square] is None:
            if isinstance(self[from_square], Pawn):
                # check for en-passant
                if self.is_en_passant_move(from_square, to_square - from_square):
                    self._squares[to_square.x][from_square.y] = None
                    self.move_piece(from_square, to_square, reset_redo_history)
                else:
                    raise BoardException(f"Invalid capture on {to_square}")
            else:
                raise BoardException(f"Invalid capture on {to_square}")

        else:
            self._squares[to_square.x][to_square.y] = None
            self.move_piece(from_square, to_square, reset_redo_history)

    def undo(self, redoable=True):
        if len(self.history) > 1:
            self.str_to_board(self.history[-2][0])
            redo_data = self.history.pop()
            if redoable:
                self.redo_history.append(redo_data)
            return True
        return False

    def redo(self):
        if len(self.redo_history) > 0:
            self.str_to_board(self.redo_history[-1][0])
            self.history.append(self.redo_history.pop())
            return True
        return False

    def is_en_passant_move(self, square: Square, move: tuple[int, int]):
        piece = self[square]

        if piece is None or not isinstance(piece, Pawn):
            return False

        if abs(move[0]) != 1:
            return False

        if piece.color == USR_WHITE:
            if move[1] != 1:
                return False
        elif piece.color == USR_BLACK:
            if move[1] != -1:
                return False
        else:
            raise BoardException("Invalid piece color, got " + str(piece.color))

        if not Square.is_valid(square.x + move[0], square.y + move[1]) \
                or self[square + move] is not None:
            return False

        if not Square.is_valid(square.x + move[0], square.y + 2 * move[1]):
            return False
        if not Square.is_valid(square.x + move[0], square.y):
            return False

        # opposing player must have moved the pawn double last move
        pass_square_out = square + (move[0], 2 * move[1])
        pass_square_in = square + (move[0], 0)

        if self[pass_square_out] is not None or not isinstance(self[pass_square_in], Pawn):
            return False

        if self[pass_square_in].color == piece.color:
            return False

        if len(self.history) < 2:
            return False

        if self.history[-2][0][pass_square_out.to_board_str_index()] != self[pass_square_in].short:
            return False

        if self.history[-2][0][pass_square_in.to_board_str_index()] != ".":
            return False

        return True

    def is_castle_move(self, square: Square, move: tuple[int, int]):
        piece = self[square]

        if piece is None or not isinstance(piece, King):
            return False

        if self.has_been_moved(square):
            return False

        if abs(move[0]) != 2:
            return False

        if move[1] != 0:
            return False

        if not Square.is_valid(square.x + move[0], square.y):
            return False

        opponent = USR_BLACK if piece.color == USR_WHITE else USR_WHITE

        if len(self.attackers(square, opponent)) > 0:
            return False

        for over_squares in get_moves_in_direction(square, (move[0] // 2, 0)):
            if self[over_squares] is None and len(self.attackers(over_squares, opponent)) == 0:
                continue
            if isinstance(self[over_squares], Rook) and self[over_squares].color == piece.color:
                if not self.has_been_moved(over_squares) and (square + move) != over_squares:
                    return True

            return False
        return False
