import pygame
from .settings import SettingsElement


class UIElement:
    def __init__(self, settings_class, surface: pygame.Surface | pygame.SurfaceType):
        self.settings = settings_class(surface)

    def __draw__(self):
        pass
