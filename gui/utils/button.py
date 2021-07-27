import pygame

from gui.utils.colors import DARK_GRAY, DARKER_GRAY
from gui.screens.screen_activity import Screen
from server.geometry.point import Point


class Button:
    def __init__(self, top_left: Point, width, height, txt, font_size=None):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.txt = txt
        self.font_size = max(self.height // len(self.txt),
                             self.width // len(self.txt)) if font_size is None else font_size

    def draw(self, screen: Screen):
        margin = 3
        pygame.draw.rect(screen.screen, DARK_GRAY, [self.top_left.x - margin, self.top_left.y - margin,
                                                    self.width + 2 * margin, self.height + 2 * margin], border_radius=8)
        pygame.draw.rect(screen.screen, DARKER_GRAY, [self.top_left.x, self.top_left.y, self.width, self.height],
                         border_radius=8)
        screen.write_text(self.txt, self.top_left.x + self.width // 2, self.top_left.y + self.height // 2,
                          size=self.font_size)

    def click_inside(self, p: Point):
        return self.top_left.x <= p.x <= self.top_left.x + self.width and \
               self.top_left.y <= p.y <= self.top_left.y + self.height
