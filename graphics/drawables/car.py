from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List

import pygame

from graphics.camera import Camera
from graphics.drawables.drawable import Drawable
from server.simulation_objects.cars.i_car import ICar
from server.geometry.point import Point


@dataclass(init=True, repr=True)
class DrawableCar(Drawable):
    center: Point
    angle: float
    path: str = "graphics/images/car.png"

    def draw(self, screen, scale):
        car_img = pygame.image.load(self.path)
        img = pygame.transform.rotozoom(car_img, self.angle, scale)
        rect = img.get_rect()
        rect.center = self.center.to_tuple()
        screen.blit(img, rect)

    @staticmethod
    def from_server_obj(obj: ICar) -> DrawableCar:
        return DrawableCar(deepcopy(obj.position), obj.get_angle())

    def get_all_points(self) -> List[Point]:
        return [self.center]

    def is_inside_camera(self, camera: Camera):
        return camera.is_inside_camera(self.center)
