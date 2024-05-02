import pygame
from .ui_element import UIElement

from .settings import TextBoxSettings
from ..constants import *


class TextBox(UIElement):
    def __init__(self, text: str, surface_size: tuple[int, int], **kwargs):
        super().__init__(surface_size)

        self.settings = TextBoxSettings(self.surface)
        self.settings.text = text
        self.settings.text_align = Align.CENTER

        self.set(**kwargs)

    def draw(self):
        self.clear()

        rect = self.settings.get_rect()
        text_graphic = self.settings.render_text()

        self.settings.surface.fill(self.settings.background_color)

        if self.settings.outline_width > 0:
            pygame.draw.rect(self.settings.surface,
                             self.settings.outline_color,
                             self.settings.surface.get_rect(),
                             self.settings.outline_width)
        self.settings.surface.blit(text_graphic, rect)
