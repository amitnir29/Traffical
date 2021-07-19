from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List

import pygame
from pygame import Rect

from graphics.camera import Camera
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
        x, y = self.center.to_tuple()
        circle_radius = 70 * scale
        back_circle_radius = 95 * scale

        # COLORS
        color = GREEN if self.is_green else RED

        # DRAWING
        pygame.draw.circle(screen, GRAY, (x, y), back_circle_radius)
        pygame.draw.circle(screen, color, (x, y), circle_radius)

    @staticmethod
    def from_server_obj(obj: ITrafficLight) -> DrawableLight:
        return DrawableLight(deepcopy(obj.coordinate), obj.can_pass)

    def get_all_points(self) -> List[Point]:
        return [self.center]

    def is_inside_camera(self, camera: Camera):
        return camera.is_inside_camera(self.center)
