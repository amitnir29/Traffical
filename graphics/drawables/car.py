from dataclasses import dataclass
from typing import List, Tuple

import pygame

from graphics.drawables.drawable import Drawable
from simulation_objects.geometry.point import Point


@dataclass(init=True, repr=True)
class DrawableCar(Drawable):
    center: Point
    angle: float
    path: str = "graphics/images/car.png"

    def draw(self, window):
        car_img = pygame.image.load(self.path)
        img = pygame.transform.rotozoom(car_img, self.angle, window.scale)
        rect = img.get_rect()
        rect.center = self.center.to_tuple()
        window.screen.blit(img, rect)