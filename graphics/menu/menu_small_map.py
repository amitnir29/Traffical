from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import List, Any, Dict

import pygame

from db.load_map_data import get_db_road_sections
from graphics.camera import Camera
from graphics.colors import *
from graphics.drawables.drawable import Drawable
from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.roadsections.road_section import RoadSection


class MenuSmallMap:
    def __init__(self, screen: pygame.Surface, width: int, height: int, roads: List[IRoadSection], top_left=None):
        self.roads = [DrawableRoad.from_server_obj(road) for road in roads]
        self.all_points = [point for road in self.roads for point in road.get_all_points()]
        self.width = width
        self.height = height
        self.screen = screen
        self.curr_top_left = Point(0, 0) if top_left is None else top_left
        self.__normalize_points()

    def __normalize_points(self):
        norm_x = lambda x: x / self.width
        norm_y = lambda y: y / self.height
        # normalize the points:
        for point in self.all_points:
            point.normalize(norm_x, norm_y)

    def __shift_points(self, top_left: Point):
        if top_left == self.curr_top_left:
            return
        delta_x = top_left.x - self.curr_top_left.x
        delta_y = top_left.y - self.curr_top_left.y
        for point in self.all_points:
            point.shift(delta_x, delta_y)
        self.curr_top_left = top_left

    def draw(self, screen, top_left: Point):
        # draw rectangle of the map
        pygame.draw.rect(screen, GRAY, [top_left.x, top_left.y, self.width, self.height])
        # draw the roads
        for road in self.roads:
            road.draw(self.screen, with_lanes=False)


def load_small_map(path: str):
    roads = __get_roads(path)
    return CornerSmallMap()


def __get_roads(path: str) -> Dict[int, IRoadSection]:
    roads: Dict[int, IRoadSection] = dict()
    # create all roads
    for road_data in get_db_road_sections(path):
        roads[road_data.idnum] = RoadSection(road_data, set())
    return roads
