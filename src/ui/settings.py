import pygame

from ..helper import load_pieces
from ..constants import *


class SettingsException(Exception):
    pass


class SettingsElement:
    def __init__(self, surface: pygame.Surface | pygame.SurfaceType):
        self.surface = surface

        self.padding: None | int = None
        self.font: None | pygame.font.Font = None
        self.outline_width: None | int = None

    def get_rect(self):
        pass


class BoardSettings(SettingsElement):
    def __init__(self, surface: pygame.Surface | pygame.SurfaceType):
        super().__init__(surface)

        self.padding = 30
        self.outline_width = 6

        self.piece_sprites = load_pieces("assets/images/pieces.png")
        self.piece_outline_width = 5

        self.side = USR_SPECTATOR

    def get_length(self, with_outline=False):
        w, h = self.surface.get_size()

        if with_outline:
            w, h = w - self.padding * 2, h - self.padding * 2
        else:
            w, h = w - (self.padding + self.outline_width) * 2, h - (
                    self.padding + self.outline_width) * 2

        return min(w, h)

    def get_pos(self, with_outline=False):
        w, h = self.surface.get_size()
        length = self.get_length(with_outline)

        x, y = (w - length) // 2, (h - length) // 2

        return x, y

    def get_rect(self, with_outline=False):
        length = self.get_length(with_outline)
        return pygame.Rect(*self.get_pos(with_outline), length, length)

    def get_square_length(self):
        length = self.get_length()
        length /= 8

        return length

    def get_piece_sprite(self, color, piece):
        if color == USR_WHITE:
            color = "white"
        elif color == USR_BLACK:
            color = "black"
        else:
            raise SettingsException("Could not get piece sprite")

        square_len = self.get_square_length()
        return pygame.transform.smoothscale(self.piece_sprites[color][piece], (square_len, square_len))

    def get_piece_outline_sprite(self, color, piece):
        if color == USR_WHITE:
            color = "white"
        elif color == USR_BLACK:
            color = "black"
        else:
            raise SettingsException("Could not get piece sprite")

        square_len = self.get_square_length()
        surf = self.piece_sprites[color][piece]

        outline_width = self.piece_outline_width * surf.get_size()[0] / square_len

        piece_mask = pygame.mask.from_surface(surf)
        piece_outline = piece_mask.outline()

        outline_surface = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
        outline_surface.blit(piece_mask.to_surface(unsetcolor=None, unsetsurface=None, setcolor=BLACK), (0, 0))

        for points in piece_outline:
            pygame.draw.circle(outline_surface, BLACK, points, outline_width)

        return pygame.transform.smoothscale(outline_surface, (square_len, square_len))


class TextBoxSettings(SettingsElement):
    def __init__(self, surface: pygame.Surface | pygame.SurfaceType):
        super().__init__(surface)
        self.text_align = Align.LEFT
        self.font = pygame.font.Font(None, 30)
        self.color = "black"
        self.padding = 30

        self.background_color = "#00000000"
        self.outline_width = 5
        self.outline_color = "black"

        self.text = ""

    def get_rect(self):
        temp_text = self.font.render(self.text, True, self.color)
        dimensions = temp_text.get_rect()

        self_w, self_h = self.surface.get_size()
        text_w, text_h = dimensions.size

        dimensions = dimensions.move((0, (self_h - text_h) // 2))

        if self.text_align == Align.LEFT:
            return dimensions.move((self.padding, 0))

        elif self.text_align == Align.CENTER:
            self_w, self_h = self.surface.get_size()

            return pygame.Rect((self_w - text_w) // 2, (self_h - text_h) // 2, text_w, text_h)

        elif self.text_align == Align.RIGHT:
            return dimensions.move(self_w - dimensions.right - self.padding, 0)

        raise SettingsException("Invalid text_align value")

    def render_text(self):
        return self.font.render(self.text, True, self.color)
