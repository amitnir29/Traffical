from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

import pygame

from graphics.colors import *
from graphics.drawables.drawable import Drawable
from server.geometry.point import Point
from server.simulation_objects.roadsections.i_road_section import IRoadSection


@dataclass(init=True, repr=True)
class DrawableRoad(Drawable):
    border_coordinates: List[Tuple[Point, Point]]
    inner_lines: List[List[Point]]

    def draw(self, screen, scale):
        # DRAWS THE ROAD SECTION:
        coors = self.border_coordinates
        for i in range(len(coors) - 1):
            # yes, the order of [i+1] points is reversed on purpose
            current_points = (coors[i][0].to_tuple(), coors[i][1].to_tuple(),
                              coors[i + 1][1].to_tuple(), coors[i + 1][0].to_tuple())
            pygame.draw.polygon(screen, BLACK, current_points)

        # DRAWS THE LANES:
        for line in self.inner_lines:
            for i in range(len(line) - 1):
                pygame.draw.line(screen, WHITE, line[i].to_tuple(), line[i + 1].to_tuple())

    @staticmethod
    def from_server_obj(obj: IRoadSection) -> DrawableRoad:
        return DrawableRoad(obj.coordinates, obj.get_lines_between_lanes())

    def get_all_points(self) -> List[Point]:
        return [p for pair in self.border_coordinates for p in pair] + [p for line in self.inner_lines for p in line]
