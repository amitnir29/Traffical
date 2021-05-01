from dataclasses import dataclass
from typing import List, Tuple

import pygame
from pygame import Rect

from graphics.colors import *
from graphics.drawables.drawable import Drawable
from simulation_objects.geometry.point import Point


@dataclass(init=True, repr=True)
class DrawableLight(Drawable):
    center: Point
    is_green: bool
    width: float = 160
    height: float = 330

    def draw(self, window):
        # SETTING SIZES AND SCALES
        w = 160 * window.scale
        h = 330 * window.scale
        x, y = self.center.to_tuple()
        rect = Rect(x, y, w, h)
        rect.center = x, y
        circle_radius = 42 * window.scale

        # CENTERS
        red_center = (x, y - 96 * window.scale)
        yellow_center = (x, y)
        green_center = (x, y + 96 * window.scale)

        # COLORS
        red_color = RED if not self.is_green else DARK_GRAY
        yellow_color = DARK_GRAY
        green_color = GREEN if self.is_green else DARK_GRAY

        # DRAWING
        pygame.draw.rect(window.screen, GRAY, rect)
        pygame.draw.circle(window.screen, red_color, red_center, circle_radius)
        pygame.draw.circle(window.screen, yellow_color, yellow_center, circle_radius)
        pygame.draw.circle(window.screen, green_color, green_center, circle_radius)
