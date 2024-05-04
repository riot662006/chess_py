import pygame
from helper import load_image, grid_board

from src.square import Square
from src.ui.board import Board
from constants import *
from src.ui.textbox import TextBox


class GameException(Exception):
    pass


class GameState(Enum):
    TURN = 0
    CHECKMATED = 1
    STALEMATE = 2

    def is_game_end(self):
        return self == GameState.CHECKMATED or self == GameState.STALEMATE


class Game:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        self.screen = screen
        self.is_running = True

        self.board = Board((600, 600), TEST_CONFIG)
        self.board.settings.side = USR_WHITE

        self.player_names = {USR_WHITE: "Rick1203", USR_BLACK: "3021kicR"}

        self.state = GameState.TURN
        self.player_txtBox = TextBox(f"{self.player_names[USR_WHITE]}'s turn",
                                     (200, 80), font=pygame.font.Font(None, 25),
                                     color="black", background_color="white")

    @property
    def current_player(self):
        return USR_WHITE if len(self.board.history) % 2 else USR_BLACK

    def update(self):
        needs_render = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return False

            elif event.type == pygame.KEYDOWN:
                self.handle_key(event)
                needs_render = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.handle_mouse(event)
                    needs_render = True

        return needs_render

    def render(self):
        self.set_highlights()

        self._draw_background()
        self.board.draw()
        self.player_txtBox.draw()

        self.screen.blit(self.board.surface, (0, 0))

        if self.state.is_game_end():
            end_txt1 = TextBox("GAME OVER", (200, 80), color="red")
            end_txt1.draw()

            if self.state == GameState.CHECKMATED:
                winner = USR_BLACK if self.current_player == USR_WHITE else USR_WHITE
                msg = self.player_names[winner] + " WINS!!!"
            else:
                msg = "STALEMATE"

            end_txt2 = TextBox(msg, (200, 80))
            end_txt2.draw()

            self.screen.blit(end_txt1.surface, (640, 200))
            self.screen.blit(end_txt2.surface, (640, 320))

        else:
            self.screen.blit(self.player_txtBox.surface, (640, 260))

    def _draw_background(self):
        background = load_image("assets/images/background.jpg")
        background = pygame.transform.scale(background, self.screen.get_size())

        self.screen.blit(background, (0, 0))

    def handle_mouse(self, event):
        if self.board.settings.get_rect().collidepoint(event.pos):
            self.handle_board_click(event.pos)

    def handle_key(self, event):
        if self.state != GameState.TURN:
            return

        if event.mod & pygame.KMOD_CTRL:
            match event.key:
                case pygame.K_z:
                    print("UNDO")
                    if self.board.undo():
                        self.toggle_current_turn()
                        self.board.selected_square = None
                case pygame.K_y:
                    print("REDO")
                    if self.board.redo():
                        self.toggle_current_turn()
                        self.board.selected_square = None

                case pygame.K_s:
                    print(str(self.board))

    def handle_board_click(self, pos: tuple[int, int]):
        if self.state != GameState.TURN:
            return

        old_square = self.board.selected_square
        new_square = self.board.get_clicked_square(pos)

        old_move_squares = []
        old_capture_squares = []

        if old_square is not None:
            old_move_squares = self.get_safe_move_squares(old_square)
            old_capture_squares = self.get_safe_capture_squares(old_square)
            self.board.selected_square = None

        if new_square in old_move_squares:
            self.move_board_piece(old_square, new_square)
            return

        if new_square in old_capture_squares:
            self.capture_board_piece(old_square, new_square)
            return

        piece = self.board[new_square]
        if piece is None or piece.color != self.current_player:
            return

        self.board.selected_square = new_square

    def move_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_player:
            raise GameException("Wait your turn!")

        self.board.move_piece(from_square, to_square)
        self.toggle_current_turn()
        self.set_highlights()

    def capture_board_piece(self, from_square: Square, to_square: Square):
        if self.board[from_square] is None:
            raise GameException("From square can not be empty")

        if self.board[from_square].color != self.current_player:
            raise GameException("Wait your turn!")

        self.board.capture_piece(from_square, to_square)
        self.toggle_current_turn()
        self.set_highlights()

    def toggle_current_turn(self):
        if self.state == GameState.TURN:
            self.player_txtBox.set(
                text=f"{self.player_names[self.current_player]}'s turn",
                color="black" if self.current_player == USR_WHITE else "white",
                background_color="white" if self.current_player == USR_WHITE else "black"
            )

            if not self.has_possible_move(self.current_player):
                self.state = GameState.CHECKMATED if self.on_check(self.current_player) else GameState.STALEMATE
        else:
            raise GameException("Invalid turn")

    def get_king_position(self, color):
        if color not in [USR_WHITE, USR_BLACK]:
            raise GameException("Invalid color type")

        return Square.from_board_str_index(str(self.board).index('k' if color == USR_WHITE else 'K'))

    def on_check(self, color):
        if color not in [USR_WHITE, USR_BLACK]:
            raise GameException("Invalid color type")

        king_square = self.get_king_position(color)
        return len(self.board.attackers(king_square, USR_BLACK if color == USR_WHITE else USR_WHITE)) > 0

    def get_safe_move_squares(self, square: Square):
        piece = self.board[square]

        if piece is None:
            raise GameException(f"Piece must be on square {square} to evaluate its safe moves")

        safe_moves = []

        for move in self.board.get_move_squares(square):
            self.board.move_piece(square, move, False)

            if not self.on_check(piece.color):
                safe_moves.append(move)
                print(grid_board(str(self.board)))

            self.board.undo(False)

        return safe_moves

    def get_safe_capture_squares(self, square: Square):
        piece = self.board[square]

        if piece is None:
            raise GameException(f"Piece must be on square {square} to evaluate its safe moves")

        safe_captures = []

        for move in self.board.get_capture_squares(square):
            self.board.capture_piece(square, move, False)

            if not self.on_check(piece.color):
                safe_captures.append(move)

            self.board.undo(False)

        return safe_captures

    def has_possible_move(self, color):
        for y in range(8):
            for x in range(8):
                if self.board[x, y] is None or self.board[x, y].color != color:
                    continue

                if len(self.get_safe_move_squares(Square(x, y))) > 0 \
                        or len(self.get_safe_capture_squares(Square(x, y))) > 0:
                    return Square(x, y), self.get_safe_move_squares(Square(x, y)), self.get_safe_capture_squares(
                        Square(x, y))

        return False

    def set_highlights(self):
        self.board.reset_highlight_color()

        if self.board.selected_square is not None:
            self.board.set_highlight_color(self.board.selected_square, Palette.SELECTED.value)

            for square in self.get_safe_move_squares(self.board.selected_square):
                self.board.set_highlight_color(square, Palette.MOVABLE.value)

            for square in self.get_safe_capture_squares(self.board.selected_square):
                self.board.set_highlight_color(square, Palette.CAPTURABLE.value)

        if self.on_check(self.current_player):
            self.board.set_highlight_color(self.get_king_position(self.current_player), Palette.CHECK.value)

        if self.state.is_game_end():
            winner = USR_BLACK if self.current_player == USR_WHITE else USR_WHITE
            king_square = self.get_king_position(self.current_player)

            attacked_squares = self.board.get_move_squares(king_square) + self.board.get_capture_squares(king_square)

            for square in [king_square, *attacked_squares]:
                for attacker in self.board.attackers(square, winner):
                    self.board.set_highlight_color(attacker, Palette.CAPTURABLE.value)

    def quit(self):
        self.is_running = False
