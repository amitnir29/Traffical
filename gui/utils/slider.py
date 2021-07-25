import pygame

from gui.simulation_graphics.colors import GRAY, DARK_GRAY
from gui.screens.screen_activity import Screen
from server.geometry.point import Point

SLIDER_LINE_HEIGHT = 10
BUTTON_SIZE = 20
TEXT_SIZE = 20


class Slider:
    def __init__(self, left_x, y, width, min_val, max_val, init_val=None):
        self.left_x = left_x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.curr_value = min_val if init_val is None else init_val

    @property
    def txt(self):
        return str(self.curr_value)

    @property
    def vals_range(self):
        return self.max_val - self.min_val

    @property
    def right_x(self):
        return self.left_x + self.width

    def curr_value_to_x_center(self):
        return self.left_x + (self.curr_value - self.min_val) * self.width // self.vals_range

    def draw(self, screen: Screen):
        # line
        pygame.draw.rect(screen.screen, DARK_GRAY,
                         [self.left_x, self.y - SLIDER_LINE_HEIGHT // 2, self.width, SLIDER_LINE_HEIGHT])
        # button
        pygame.draw.rect(screen.screen, GRAY,
                         [self.curr_value_to_x_center() - BUTTON_SIZE // 2, self.y - BUTTON_SIZE // 2, BUTTON_SIZE,
                          BUTTON_SIZE])
        screen.write_text(self.txt, self.left_x + self.width + TEXT_SIZE * 2, self.y, TEXT_SIZE)

    def click_on_slider(self, p: Point):
        return self.curr_value_to_x_center() - BUTTON_SIZE // 2 <= p.x <= \
               self.curr_value_to_x_center() + BUTTON_SIZE // 2 and \
               self.y - BUTTON_SIZE // 2 <= p.y <= self.y + BUTTON_SIZE // 2

    def update_position(self, pos: Point):
        """
        move the button's center to where the x value is set
        :param pos: new mouse position
        """
        new_val = int(((pos.x - self.left_x) / self.width) * self.vals_range + self.min_val)
        if new_val > self.max_val:
            new_val = self.max_val
        elif new_val < self.min_val:
            new_val = self.min_val
        self.curr_value = new_val
