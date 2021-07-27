from abc import ABC

import pygame

from gui.screens.screen_activity import Screen
from gui.utils.colors import LIGHT_BLUE


class HelpScreen(Screen, ABC):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, background=LIGHT_BLUE)
