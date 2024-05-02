import pygame
from helper import load_image

from square import Square
from src.ui.board import Board
from constants import *
from src.ui.textbox import TextBox


class GameException(Exception):
    pass


class Game:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.is_running = True

        self.board = Board((600, 600))
        self.board.settings.side = USR_WHITE

        self.white_player_name = "Rick1203"
        self.black_player_name = "3021kicR"

        self.current_turn = USR_WHITE
        self.current_turn_txtBox = TextBox(f"{self.white_player_name}'s turn",
                                           (200, 80), font=pygame.font.Font(None, 25),
                                           color="black", background_color="white")

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
        self._draw_background()
        self.board.draw()
        self.current_turn_txtBox.draw()

        self.screen.blit(self.board.surface, (0, 0))
        self.screen.blit(self.current_turn_txtBox.surface, (640, 260))

    def _draw_background(self):
        background = load_image("assets/images/background.jpg")
        background = pygame.transform.scale(background, self.screen.get_size())

        self.screen.blit(background, (0, 0))

    def handle_mouse(self, pos):
        if self.board.settings.get_rect().collidepoint(pos):
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
            self.board.set_highlight_color(self.board.selected_square, Palette.SELECTED.value)

        # FOR TESTING
        for square in self.board.get_move_squares(self.board.selected_square):
            self.board.set_highlight_color(square, Palette.MOVABLE.value)

        for square in self.board.get_capture_squares(self.board.selected_square):
            self.board.set_highlight_color(square, Palette.CAPTURABLE.value)

    def move_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_turn:
            raise GameException("Wait your turn!")

        self.toggle_current_turn()

        self.board.move_piece(from_square, to_square)

        print(self.board.history)

    def capture_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_turn:
            raise GameException("Wait your turn!")

        self.toggle_current_turn()

        self.board.capture_piece(from_square, to_square)

        print(self.board.history)

    def toggle_current_turn(self):
        if self.current_turn == USR_WHITE:
            self.current_turn = USR_BLACK
            self.current_turn_txtBox.set(
                text=f"{self.black_player_name}'s turn",
                color="white",
                background_color="black"
            )

        elif self.current_turn == USR_BLACK:
            self.current_turn = USR_WHITE
            self.current_turn_txtBox.set(
                text=f"{self.white_player_name}'s turn",
                color="black",
                background_color="white"
            )
        else:
            raise GameException("Invalid turn")

    def quit(self):
        self.is_running = False
