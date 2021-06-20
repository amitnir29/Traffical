from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

import pygame

from graphics.colors import *
from graphics.drawables.drawable import Drawable
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection


@dataclass(init=True, repr=True)
class DrawableJunction(Drawable):
    coordinates: List[Point]

    def draw(self, screen, scale=None):
        polygon_points = [p.to_tuple() for p in self.coordinates]
        pygame.draw.polygon(screen, BLACK, polygon_points)

    @staticmethod
    def from_server_obj(obj: IJunction) -> DrawableJunction:
        return DrawableJunction(obj.coordinates)

    def get_all_points(self) -> List[Point]:
        return self.coordinates
