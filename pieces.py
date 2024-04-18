from utils import *
from board import Board, Square

from collections import defaultdict


class BoardManager:
    def __init__(self, _screen: pygame.Surface | pygame.SurfaceType):
        self.screen = _screen
        self.board = Board(_screen)
        self.pieces = defaultdict(lambda: Piece())

        self.selected_square = None
        self.move_squares = None

    def setup(self):
        p = {"pawn": Pawn, "knight": Knight, "bishop": Bishop, "rook": Rook, "queen": Queen, "king": King}
        s = {"w": Piece.WHITE, "b": Piece.BLACK}

        for square, piece in START_POS.items():
            self.pieces[square] = p[piece[:-2]](s[piece[-1]])

        self.selected_square = "a1"

    def piece_surface(self, piece):
        square_to_draw = pygame.Surface(self.board.square_rect.size, pygame.SRCALPHA)

        square_to_draw.blit(resize(piece.sprite,
                                   self.board.square_rect.size),
                            (0, 0))

        return square_to_draw

    def draw(self):
        resources = load_resources()

        board_txt = pygame.Surface(self.board.board_rect.size, pygame.SRCALPHA)
        board_surf = pygame.Surface(self.board.board_rect.size, pygame.SRCALPHA)

        board_txt.blit(resources["board_texture"], (0, 0), self.board.board_rect)

        if self.selected_square:
            board_surf.fill((200, 0, 0, 100),
                            self.board.get_square(self.selected_square),
                            special_flags=pygame.BLEND_RGBA_MAX)

        board_surf.blit(resize(resources["board_outline"], self.board.board_rect.size), (0, 0))

        for square, piece in self.pieces.items():
            if square == self.selected_square or Square(square).is_black():
                board_surf.blit(resize(piece.outline_sprite,
                                       self.board.square_rect.size),
                                self.board.get_square(square).topleft,
                                special_flags=pygame.BLEND_RGBA_SUB)

            piece_surf = self.piece_surface(piece)

            board_surf.blit(piece_surf, self.board.get_square(square).topleft)

        if self.move_squares is not None:
            for move_square in self.move_squares:
                if Square(move_square).is_black():
                    board_surf.blit(resize(resources['pieces']['move_out'],
                                           self.board.square_rect.size),
                                    self.board.get_square(move_square).topleft,
                                    special_flags=pygame.BLEND_RGBA_SUB)
                piece_surf = resources['pieces']['move']

                board_surf.blit(resize(piece_surf,
                                       self.board.square_rect.size),
                                self.board.get_square(move_square).topleft)

        board_txt.blit(board_surf, (0, 0))

        self.screen.blit(board_txt, (self.board.margin, self.board.margin))

    def handle_mouse_click(self, pos):
        if self.board.is_pos_on_board(pos):
            self.selected_square = self.board.get_square_from_pos(pos)
            self.move_squares = self.possible_piece_moves(self.selected_square)
            return True
        return False

    def possible_piece_moves(self, notation):
        if notation not in self.pieces:
            return None

        piece = self.pieces[notation]
        position = self.board.get_square(notation)

        match piece:
            case Pawn():
                forward_move = str(Square(notation).add(0, 1 if piece.is_white() else -1))

                if piece.moves == 0:
                    return [forward_move, str(Square(notation).add(0, 2 if piece.is_white() else -2))]

                return [forward_move]

        return None


class Piece:
    WHITE = False
    BLACK = True

    def __init__(self, side: bool | None = None):
        self.resources = [None, None, None, None]
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
