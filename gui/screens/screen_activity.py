from abc import ABC, abstractmethod

import pygame

from gui.utils.colors import WHITE

TITLES_SCREEN_PORTION = 4


class Screen(ABC):
    def __init__(self, screen: pygame.Surface, background):
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

    def default_click_disappear(self):
        """
        keep the screen open until it is clicked on
        """
        # block until click
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        running = False
                        break
