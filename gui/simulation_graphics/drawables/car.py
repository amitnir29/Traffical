from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List

import pygame

from gui.simulation_graphics.camera import Camera
from gui.simulation_graphics.drawables.drawable import Drawable
from server.simulation_objects.cars.i_car import ICar
from server.geometry.point import Point


@dataclass(init=True, repr=True)
class DrawableCar(Drawable):
    center: Point
    angle: float
    reached_target = False
    is_done = False
    fade_range = 255
    path: str = "gui/simulation_graphics/images/car.png"

    def draw(self, screen, scale):
        car_img = pygame.image.load(self.path)
        img = pygame.transform.rotozoom(car_img, self.angle, scale)
        rect = img.get_rect()
        rect.center = self.center.to_tuple()
        img.set_alpha(self.fade_range)
        if self.reached_target:
            self.fade_range -= 50
        if self.fade_range <= 0:
            self.is_done = True
        screen.blit(img, rect)

    @staticmethod
    def from_server_obj(obj: ICar) -> DrawableCar:
        return DrawableCar(deepcopy(obj.position), obj.get_angle())

    def get_all_points(self) -> List[Point]:
        return [self.center]

    def is_inside_camera(self, camera: Camera):
        return 0 <= self.center.x <= camera.width and 0 <= self.center.y <= camera.height
