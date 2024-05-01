import pygame
from helper import load_image

from square import Square
from src.ui.board import Board
from constants import *

class GameException(Exception):
    pass


class Game:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.is_running = True

        self.board_surface = pygame.Surface((600, 600), flags=pygame.SRCALPHA)

        self.board = Board(self.board_surface)
        self.board.settings.side = USR_WHITE

        self.current_turn = USR_WHITE

    def update(self):
        needs_render = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return False

            elif event.type == pygame.KEYDOWN:
                print(str(self.board))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.handle_mouse(event.pos)
                    needs_render = True

        return needs_render

    def render(self):
        self.board_surface.fill((0, 0, 0, 0))

        self._draw_background()
        self._draw_board()

        self.screen.blit(self.board_surface, (0, 0))

    def _draw_background(self):
        background = load_image("assets/images/background.jpg")
        background = pygame.transform.scale(background, self.screen.get_size())

        self.screen.blit(background, (0, 0))

    def _draw_board(self):
        self.board.draw()

    def handle_mouse(self, pos):
        if self.board.settings.get_board_rect().collidepoint(pos):
            self.handle_board_click(pos)

    def handle_board_click(self, pos: tuple[int, int]):
        old_square = self.board.selected_square
        new_square = self.board.get_clicked_square(pos)

        if old_square is None:
            old_move_squares = []
            old_capture_squares = []
        else:
            self.board.set_highlight_color(old_square, None)
            old_move_squares = self.board.get_move_squares(old_square)
            old_capture_squares = self.board.get_capture_squares(old_square)
            self.board.selected_square = None

        for square in old_move_squares:
            self.board.set_highlight_color(square, None)

        for square in old_capture_squares:
            self.board.set_highlight_color(square, None)

        if new_square in old_move_squares:
            self.move_board_piece(old_square, new_square)
            return

        if new_square in old_capture_squares:
            self.capture_board_piece(old_square, new_square)
            return

        piece = self.board[new_square]
        if piece is None or piece.color != self.current_turn:
            return

        self.board.selected_square = new_square

        if self.board.selected_square is not None:
            self.board.set_highlight_color(self.board.selected_square, CLR_SELECTED)

        # FOR TESTING
        for square in self.board.get_move_squares(self.board.selected_square):
            self.board.set_highlight_color(square, CLR_MOVABLE)

        for square in self.board.get_capture_squares(self.board.selected_square):
            self.board.set_highlight_color(square, CLR_CAPTURABLE)

    def move_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_turn:
            raise GameException("Wait your turn!")

        self.board.move_piece(from_square, to_square)

        if self.current_turn == USR_WHITE:
            self.current_turn = USR_BLACK
        elif self.current_turn == USR_BLACK:
            self.current_turn = USR_WHITE
        else:
            raise GameException("Invalid turn")

        print(self.board.history)

    def capture_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_turn:
            raise GameException("Wait your turn!")

        self.board.capture_piece(from_square, to_square)

        print(self.board.history)

    def quit(self):
        self.is_running = False
