from abc import ABC, abstractmethod
from typing import List

import pygame

from graphics.camera import Camera
from graphics.colors import DARK_BLUE, WHITE
from server.geometry.point import Point

TITLES_SCREEN_PORTION = 4


class Screen(ABC):
    def __init__(self, screen: pygame.Surface, background=DARK_BLUE):
        self.screen = screen
        self.background = background

    @abstractmethod
    def display(self):
        pass

    def write_text(self, txt, x, y, size, color=WHITE, font='freesansbold.ttf'):
        """
        write text on the screen
        :param txt: text to write
        :param x: middle x of the text position
        :param y: middle y of the text position
        :param size: font size
        :param color: color of the text
        :param font: font of the text
        :return:
        """
        font = pygame.font.Font(font, size)
        # create a text surface object, on which text is drawn on it.
        text = font.render(txt, True, color)
        # create a rectangular object for the text surface object
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (x, y)
        # write the text
        self.screen.blit(text, textRect)