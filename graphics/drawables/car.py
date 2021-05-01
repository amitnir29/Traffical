from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

import pygame

from graphics.drawables.drawable import Drawable
from simulation_objects.cars.i_car import ICar
from simulation_objects.geometry.point import Point


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
        # TODO
        pass

    def get_all_points(self) -> List[Point]:
        return [self.center]
