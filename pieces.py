from utils import *
from board import Board, Square

from collections import defaultdict


class BoardManager:
    def __init__(self, _screen: pygame.Surface | pygame.SurfaceType):
        self.screen = _screen
        self.board = Board(_screen)
        self.pieces = defaultdict(lambda: Piece())

        self.player_turn = Piece.WHITE

        self.selected_square = None
        self.capture_squares = []
        self.move_squares = []

        self.move_history = []

    def setup(self):
        p = {"pawn": Pawn, "knight": Knight, "bishop": Bishop, "rook": Rook, "queen": Queen, "king": King}
        s = {"w": Piece.WHITE, "b": Piece.BLACK}

        for square, piece in START_POS.items():
            self.pieces[square] = p[piece[:-2]](s[piece[-1]])

    def test_setup(self):
        self.pieces['e5'] = Knight(Piece.WHITE)
        self.pieces['g6'] = Pawn(Piece.WHITE)
        self.pieces['d5'] = King(Piece.BLACK)
        self.pieces['d4'] = Queen(Piece.BLACK)
        self.pieces['f7'] = Bishop(Piece.BLACK)
        self.pieces['g1'] = Bishop(Piece.WHITE)

    def piece_surface(self, piece):
        square_to_draw = pygame.Surface(self.board.square_rect.size, pygame.SRCALPHA)

        square_to_draw.blit(resize(piece.sprite,
                                   self.board.square_rect.size),
                            (0, 0))

        return square_to_draw

    def undo(self):
        if len(self.move_history) > 0:
            from_notation, piece_from, to_notation, piece_to = self.move_history.pop()

            del self.pieces[to_notation]

            if piece_to is not None:
                self.pieces[to_notation] = piece_to

            self.pieces[from_notation] = piece_from
            piece_from.moves -= 1

            return True
        return False

    def draw(self):
        resources = load_resources()

        board_txt = pygame.Surface(self.board.board_rect.size, pygame.SRCALPHA)
        board_surf = pygame.Surface(self.board.board_rect.size, pygame.SRCALPHA)

        board_txt.blit(resources["board_texture"], (0, 0), self.board.board_rect)

        if self.selected_square is not None:
            board_surf.fill((200, 0, 0, 100),
                            self.board.get_square(self.selected_square),
                            special_flags=pygame.BLEND_RGBA_MAX)

        for square in self.capture_squares:
            board_surf.fill((0, 200, 0, 100),
                            self.board.get_square(str(square)),
                            special_flags=pygame.BLEND_RGBA_MAX)

        board_surf.blit(resize(resources["board_outline"], self.board.board_rect.size), (0, 0))

        for square, piece in self.pieces.items():
            if square == self.selected_square or Square(square).is_black() or square in self.capture_squares:
                board_surf.blit(resize(piece.outline_sprite,
                                       self.board.square_rect.size),
                                self.board.get_square(square).topleft,
                                special_flags=pygame.BLEND_RGBA_SUB)

            piece_surf = self.piece_surface(piece)

            board_surf.blit(piece_surf, self.board.get_square(square).topleft)

        for move_square in self.move_squares:
            notation = str(move_square)
            if Square(notation).is_black():
                board_surf.blit(resize(resources['pieces']['move_out'],
                                       self.board.square_rect.size),
                                self.board.get_square(notation).topleft,
                                special_flags=pygame.BLEND_RGBA_SUB)
            piece_surf = resources['pieces']['move']

            board_surf.blit(resize(piece_surf,
                                   self.board.square_rect.size),
                            self.board.get_square(notation).topleft)

        board_txt.blit(board_surf, (0, 0))

        self.screen.blit(board_txt, (self.board.margin, self.board.margin))

    def handle_mouse_click(self, pos):
        if self.board.is_pos_on_board(pos):
            cur_square = self.board.get_square_from_pos(pos)
            cur_move_square = self.piece_moves(cur_square)
            cur_capture_square = self.piece_captures(cur_square)

            if self.selected_square is not None and cur_square in [*self.move_squares, *self.capture_squares]:
                self.move_piece(self.selected_square, str(cur_square))

                self.selected_square = None
                self.move_squares = []
                self.capture_squares = []

                return False

            self.selected_square = cur_square
            self.move_squares = cur_move_square
            self.capture_squares = cur_capture_square
            return True

        self.selected_square = None
        self.move_squares = []
        self.capture_squares = []
        return False

    def handle_key_press(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                self.undo()

    def move_piece(self, from_notation, to_notation):
        if from_notation not in self.pieces:
            raise AttributeError("This square is empty. No piece to move")

        return_val = None

        print(str(self.pieces[from_notation]), "to", to_notation)

        if to_notation in self.pieces:
            return_val = self.pieces[to_notation]
            print(str(self.pieces[from_notation]), "eats", str(return_val))

        self.pieces[to_notation] = self.pieces[from_notation]
        del self.pieces[from_notation]

        self.pieces[to_notation].moves += 1
        self.move_history.append((from_notation, self.pieces[to_notation], to_notation, return_val))

        return return_val

    def piece_moves(self, notation):
        if notation not in self.pieces:
            return []

        piece = self.pieces[notation]

        def moves_from_directions(dirs):
            _moves = []

            for direction in dirs:
                _loc = Square(notation).add(*direction)

                while _loc is not None and str(_loc) not in self.pieces:
                    _moves.append(_loc)
                    _loc = _loc.add(*direction)

            return _moves

        match piece:
            case Pawn():
                forward_move = Square(notation).add(0, 1 if piece.is_white() else -1)

                if forward_move is None or str(forward_move) in self.pieces:
                    return []

                if piece.moves == 0:
                    double_move = Square(notation).add(0, 2 if piece.is_white() else -2)
                    if double_move is None or str(double_move) in self.pieces:
                        return [forward_move]
                    return [forward_move, double_move]

                return [forward_move]

            case Knight():
                moves = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                         (2, 1), (2, -1), (-2, 1), (-2, -1)]
                _squares = [Square(notation).add(*move) for move in moves]
                return [square for square in _squares
                        if square is not None and str(square) not in self.pieces]

            case Bishop():
                directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

                return moves_from_directions(directions)

            case Rook():
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

                return moves_from_directions(directions)

            case Queen():
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1),
                              (1, 1), (-1, 1), (1, -1), (-1, -1)]

                return moves_from_directions(directions)

            case King():
                moves = []
                loc = Square(notation)

                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x == y == 0:
                            continue
                        pos_move = loc.add(x, y)
                        if pos_move is None or str(pos_move) in self.pieces:
                            continue
                        moves.append(pos_move)

                return moves

        return []

    def piece_captures(self, notation):
        if notation not in self.pieces:
            return []

        piece = self.pieces[notation]

        def captures_from_directions(dirs):
            _captures = []

            for direction in dirs:
                _loc = Square(notation).add(*direction)

                while _loc is not None and str(_loc) not in self.pieces:
                    _loc = _loc.add(*direction)

                if _loc is not None and self.pieces[str(_loc)].is_white() != piece.is_white():
                    _captures.append(_loc)

            return _captures

        match piece:
            case Pawn():
                basic_captures = [
                    Square(notation).add(-1, 1 if piece.is_white() else -1),
                    Square(notation).add(1, 1 if piece.is_white() else -1)
                ]

                # will add en-passant later

                return [cap for cap in basic_captures
                            if cap is not None
                        and str(cap) in self.pieces
                        and self.pieces[str(cap)].is_white() != piece.is_white()]

            case Knight():
                moves = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                         (2, 1), (2, -1), (-2, 1), (-2, -1)]
                captures = [Square(notation).add(*move) for move in moves]
                return [cap for cap in captures
                        if cap is not None
                        and str(cap) in self.pieces
                        and self.pieces[str(cap)].is_white() != piece.is_white()]

            case Bishop():
                directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

                return captures_from_directions(directions)

            case Rook():
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

                return captures_from_directions(directions)

            case Queen():
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1),
                              (1, 1), (-1, 1), (1, -1), (-1, -1)]

                return captures_from_directions(directions)

            case King():
                captures = []
                loc = Square(notation)

                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x == y == 0:
                            continue
                        pos_move = loc.add(x, y)
                        if pos_move is None:
                            continue
                        if str(pos_move) in self.pieces and self.pieces[str(pos_move)].is_white() != piece.is_white():
                            captures.append(pos_move)

                return captures

        return []


    def is_pinned(self, notation):
        # not complete
        if notation not in self.pieces:
            return False

        if isinstance(notation, King):
            return False

        my_piece = self.pieces[notation]
        del self.pieces[notation]

        for other_notation, other_piece in self.pieces.items():
            if not isinstance(other_piece, (Rook, Queen, Bishop)):
                pass



class Piece:
    WHITE = False
    BLACK = True

    def __init__(self, side: bool | None = None):
        self.resources: list[pygame.Surface | pygame.SurfaceType | None] = [None, None, None, None]

        self.side = side  # false - white; true - black
        self.moves = 0

    @property
    def sprite(self):
        return self.resources[int(self.side)]

    @property
    def outline_sprite(self):
        return self.resources[int(self.side) + 2]

    def is_white(self):
        return not self.side


class King(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["king_w", "king_b", "king_w_out", "king_b_out"]]


class Queen(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["queen_w", "queen_b", "queen_w_out", "queen_b_out"]]


class Bishop(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["bishop_w", "bishop_b", "bishop_w_out", "bishop_b_out"]]


class Knight(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["knight_w", "knight_b", "knight_w_out", "knight_b_out"]]


class Rook(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["rook_w", "rook_b", "rook_w_out", "rook_b_out"]]


class Pawn(Piece):
    def __init__(self, side: bool):
        super().__init__(side)
        self.resources = [load_resources()["pieces"][p]
                          for p in ["pawn_w", "pawn_b", "pawn_w_out", "pawn_b_out"]]
