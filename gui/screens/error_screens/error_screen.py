from abc import ABC

import pygame

from gui.screens.screen_activity import Screen
from gui.utils.colors import RED


class ErrorScreen(Screen, ABC):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, background=RED)
