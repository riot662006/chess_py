import pygame
from typing import Type, TypeVar

from .settings import SettingsElement


class UIException(Exception):
    pass


class UIElement:
    def __init__(self, surface_size: tuple[int, int]):
        self.surface = pygame.Surface(surface_size, flags=pygame.SRCALPHA)
        self.settings: SettingsElement | None = None

    def draw(self):
        pass

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def set(self, **kwargs):
        for arg, value in kwargs.items():
            if arg in vars(self.settings):
                self.settings.__dict__[arg] = value
            else:
                raise UIException(f"Invalid option - {arg}")
