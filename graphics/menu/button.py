import pygame

from graphics.colors import GRAY, DARK_GRAY
from graphics.menu.screens.screen_activity import Screen
from server.geometry.point import Point


class Button:
    def __init__(self, top_left: Point, width, height, txt):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.txt = txt

    def draw(self, screen: Screen):
        pygame.draw.rect(screen.screen, DARK_GRAY, [self.top_left.x, self.top_left.y, self.width, self.height])
        screen.write_text(self.txt, self.top_left.x + self.width // 2, self.top_left.y + self.height // 2,
                          self.height // len(self.txt))

    def click_inside(self, p: Point):
        return self.top_left.x <= p.x <= self.top_left.x + self.width and \
               self.top_left.y <= p.y <= self.top_left.y + self.height
