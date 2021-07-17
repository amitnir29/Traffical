from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List

import pygame
from pygame import Rect

from graphics.colors import *
from graphics.drawables.drawable import Drawable
from server.geometry.point import Point
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


@dataclass(init=True, repr=True)
class DrawableLight(Drawable):
    center: Point
    is_green: bool
    width: float = 160
    height: float = 330

    def draw(self, screen, scale):
        # SETTING SIZES AND SCALES
        w = 160 * scale
        h = 330 * scale
        x, y = self.center.to_tuple()
        rect = Rect(x, y, w, h)
        rect.center = x, y
        circle_radius = 42 * scale

        # CENTERS
        red_center = (x, y - 96 * scale)
        yellow_center = (x, y)
        green_center = (x, y + 96 * scale)

        # COLORS
        red_color = RED if not self.is_green else DARK_GRAY
        yellow_color = DARK_GRAY
        green_color = GREEN if self.is_green else DARK_GRAY

        # DRAWING
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.circle(screen, red_color, red_center, circle_radius)
        pygame.draw.circle(screen, yellow_color, yellow_center, circle_radius)
        pygame.draw.circle(screen, green_color, green_center, circle_radius)

    @staticmethod
    def from_server_obj(obj: ITrafficLight) -> DrawableLight:
        return DrawableLight(deepcopy(obj.coordinate), obj.can_pass)

    def get_all_points(self) -> List[Point]:
        return [self.center]
