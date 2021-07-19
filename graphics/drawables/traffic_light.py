from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from math import degrees, atan
from typing import List

import pygame

from graphics.camera import Camera
from graphics.drawables.drawable import Drawable
from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


@dataclass(init=True, repr=True)
class DrawableLight(Drawable):
    center: Point
    is_green: bool
    angle: float
    width: float = 160
    height: float = 330
    green_path: str = "graphics/images/green_light.png"
    red_path: str = "graphics/images/red_light.png"

    def draw(self, screen, scale):
        # # SETTING SIZES AND SCALES
        # w = 120 * scale
        # h = 200 * scale
        # x, y = self.center.to_tuple()
        # rect = Rect(x, y, w, h)
        # rect.center = x, y
        # circle_radius = 40 * scale
        #
        # # CENTERS
        # red_center = (x, y - 40 * scale)
        # green_center = (x, y + 40 * scale)
        #
        # # COLORS
        # red_color = RED if not self.is_green else DARK_GRAY
        # green_color = GREEN if self.is_green else DARK_GRAY
        #
        # # DRAWING
        # pygame.draw.rect(screen, GRAY, rect)
        # pygame.draw.circle(screen, red_color, red_center, circle_radius)
        # pygame.draw.circle(screen, green_color, green_center, circle_radius)
        path = self.green_path if self.is_green else self.red_path
        tl_img = pygame.image.load(path)
        img = pygame.transform.rotozoom(tl_img, self.angle, scale)
        rect = img.get_rect()
        rect.center = self.center.to_tuple()
        screen.blit(img, rect)

    @staticmethod
    def from_server_obj(obj: ITrafficLight) -> DrawableLight:
        right_lane_coors = obj.lanes[-1].coordinates
        line = Line(right_lane_coors[-2][1], right_lane_coors[-1][1])
        return DrawableLight(deepcopy(obj.coordinate), obj.can_pass, DrawableLight.__get_angle(line))

    def get_all_points(self) -> List[Point]:
        return [self.center]

    def is_inside_camera(self, camera: Camera):
        return camera.is_inside_camera(self.center)

    @staticmethod
    def __get_angle(line):
        # the line from the middle of the start of the current part, to the middle of the end of the current part
        x_diff = line.p2.x - line.p1.x
        y_diff = line.p1.y - line.p2.y  # y axis is upside down
        if x_diff == 0:
            if y_diff > 0:
                return 0
            else:
                return 180
        res = (90 - degrees(atan(y_diff / x_diff))) % 360
        if x_diff < 0:
            res = 180 - res
        if x_diff > 0:
            res = 360 - res
        return res
