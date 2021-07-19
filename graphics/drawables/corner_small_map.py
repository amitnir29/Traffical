from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List, Any

import pygame

from graphics.camera import Camera
from graphics.colors import *
from graphics.drawables.drawable import Drawable
from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection


@dataclass(init=True, repr=True)
class CornerSmallMap(Drawable):
    width: int
    height: int
    screen_width: int
    screen_height: int
    roads: List[DrawableRoad]
    screen: pygame.Surface
    camera: Camera

    def draw(self, screen, scale=None):
        # draw rectangle of the map
        pygame.draw.rect(screen, GRAY, [0, 0, self.width, self.height])
        # draw the objects
        for road in self.roads:
            road.draw(self.screen, with_lanes=False)
        # draw the red rectangle of the camera
        rect_sizes = (
            int(self.camera.min_x * self.width / self.screen_width),
            int(self.camera.min_y * self.height / self.screen_height),
            int(self.camera.delta_x * self.width / self.screen_width),
            int(self.camera.delta_y * self.height / self.screen_height)
        )
        pygame.draw.rect(self.screen, RED, rect_sizes, width=3)

    @staticmethod
    def from_server_obj(obj: (int, int, int, int, List[IRoadSection], pygame.Surface, Camera)) -> CornerSmallMap:
        width, height, screen_width, screen_height, roads, screen, camera = obj
        roads = [DrawableRoad.from_server_obj(road) for road in roads]
        # now normalize the points:
        all_points = [point for road in roads for point in road.get_all_points()]
        norm_x = lambda x: x * width / screen_width
        norm_y = lambda y: y * height / screen_height
        # part 3
        for point in all_points:
            point.normalize(norm_x, norm_y)
        # finally, set the small map to a field
        return CornerSmallMap(width, height, screen_width, screen_height, roads, screen, camera)

    def get_all_points(self) -> List[Point]:
        return [point for road in self.roads for point in road.get_all_points()]

    def is_inside_camera(self, camera: Camera):
        return True
