import pygame

from gui.utils.colors import DARK_GRAY, GREEN
from gui.screens.screen_activity import Screen
from server.geometry.point import Point


class CheckBox:
    def __init__(self, top_left: Point, width, height, init_val=None):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.is_checked = False if init_val is None else init_val

    def draw(self, screen: Screen):
        pygame.draw.rect(screen.screen, DARK_GRAY, [self.top_left.x, self.top_left.y, self.width, self.height], 5)
        if self.is_checked:
            pygame.draw.rect(screen.screen, GREEN,
                             [self.top_left.x + 5, self.top_left.y + 5, self.width - 10, self.height - 10])

    def is_click_inside(self, p: Point):
        return self.top_left.x <= p.x <= self.top_left.x + self.width and \
               self.top_left.y <= p.y <= self.top_left.y + self.height

    def was_clicked(self):
        self.is_checked = not self.is_checked

    @property
    def y(self):
        return self.top_left.y + self.height // 2
