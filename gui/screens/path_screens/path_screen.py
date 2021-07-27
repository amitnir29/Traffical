from abc import ABC

from gui.screens.screen_activity import Screen
from gui.utils.colors import BLUE


class PathScreen(Screen, ABC):

    def __init__(self, screen):
        super().__init__(screen, background=BLUE)
