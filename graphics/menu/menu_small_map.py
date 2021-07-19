from __future__ import annotations

import os
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
        x_values = [p.x for p in self.all_points]
        y_values = [p.y for p in self.all_points]
        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        norm_x = lambda x: self.width * (x - min_x) / (max_x - min_x)
        norm_y = lambda y: self.height * (y - min_y) / (max_y - min_y)
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
        self.__shift_points(top_left)
        # draw rectangle of the map
        pygame.draw.rect(screen, GRAY, [top_left.x, top_left.y, self.width, self.height])
        # draw the roads
        for road in self.roads:
            road.draw(self.screen, with_lanes=False)
