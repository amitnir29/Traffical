from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple

from simulation_objects.geometry.line import Line
from simulation_objects.geometry.point import Point

import simulation_objects.lanes.i_lane as il


class IRoadSection(ABC):
    @abstractmethod
    def get_left_lane(self, curr: il.ILane) -> il.ILane:
        """
        :param curr: a lane in the road section
        :return: the lane to the left of curr
        """
        pass

    @abstractmethod
    def get_right_lane(self, curr: il.ILane) -> il.ILane:
        """
        :param curr: a lane in the road section
        :return: the lane to the right of curr
        """
        pass

    @abstractmethod
    def get_lane(self, index: int) -> il.ILane:
        """
        :param index: index of lane from left, 0 based.
        :return: the lane in that index
        """
        pass

    @abstractmethod
    def get_most_right_lane_index(self) -> int:
        """
        :return: The index of the most right lane in the road section.
        """
        pass

    @property
    @abstractmethod
    def max_speed(self) -> float:
        """
        :return: the max allowed speed of the road
        """
        pass

    @property
    @abstractmethod
    def coordinates(self) -> List[Tuple[Point, Point]]:
        pass

    @property
    @abstractmethod
    def lanes(self)->List[il.ILane]:
        pass

    @abstractmethod
    def get_lines_between_lanes(self) -> List[List[Point]]:
        """
        :return: for each seperating line (number_of_lanes - 1),
                a list of points that represent the seperating line coordinates
        """
        pass
