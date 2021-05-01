from dataclasses import dataclass
from typing import List, Tuple

import pygame

from graphics.colors import *
from graphics.drawables.drawable import Drawable
from simulation_objects.geometry.point import Point


@dataclass(init=True, repr=True)
class DrawableRoad(Drawable):
    border_coordinates: List[Tuple[Point, Point]]
    inner_lines: List[List[Point]]

    def draw(self, window):
        # DRAWS THE ROAD SECTION:
        coors = self.border_coordinates
        for i in range(len(coors) - 1):
            # yes, the order of [i+1] points is reversed on purpose
            current_points = (coors[i][0].to_tuple(), coors[i][1].to_tuple(),
                              coors[i + 1][1].to_tuple(), coors[i + 1][0].to_tuple())
            pygame.draw.polygon(window.screen, BLACK, current_points)

        # DRAWS THE LANES:
        for line in self.inner_lines:
            for i in range(len(line) - 1):
                pygame.draw.line(window.screen, WHITE, line[i].to_tuple(), line[i + 1].to_tuple())
