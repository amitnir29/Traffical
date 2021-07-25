from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

import pygame

from gui.simulation_graphics.camera import Camera
from gui.simulation_graphics.colors import *
from gui.simulation_graphics.drawables.drawable import Drawable
from server.geometry.point import Point
from server.simulation_objects.roadsections.i_road_section import IRoadSection


@dataclass(init=True, repr=True)
class DrawableRoad(Drawable):
    border_coordinates: List[Tuple[Point, Point]]
    inner_lines: List[List[Point]]

    def draw(self, screen, scale=None, with_lanes=True):
        # DRAWS THE ROAD SECTION:
        coors = self.border_coordinates
        polygon_points = [pair[0].to_tuple() for pair in coors] + [pair[1].to_tuple() for pair in reversed(coors)]
        pygame.draw.polygon(screen, BLACK, polygon_points)

        # DRAWS THE LANES:
        if with_lanes:
            for line in self.inner_lines:
                for i in range(len(line) - 1):
                    pygame.draw.line(screen, WHITE, line[i].to_tuple(), line[i + 1].to_tuple())

    @staticmethod
    def from_server_obj(obj: IRoadSection) -> DrawableRoad:
        return DrawableRoad(deepcopy(obj.coordinates), deepcopy(obj.get_lines_between_lanes()))

    def get_all_points(self) -> List[Point]:
        return [p for pair in self.border_coordinates for p in pair] + [p for line in self.inner_lines for p in line]

    def is_inside_camera(self, camera: Camera):
        for pair in self.border_coordinates:
            for coor in pair:
                if camera.is_inside_camera(coor):
                    return True
        return False
