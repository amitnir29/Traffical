from abc import ABC, abstractmethod
from numbers import Real
from typing import List, Tuple

from geometry.point import Point
from lanes.i_lane import ILane


class IRoadSection(ABC):
    @abstractmethod
    def get_left_lane(self, curr: ILane) -> ILane:
        """
        :param curr: a lane in the road section
        :return: the lane to the left of curr
        """
        pass

    @abstractmethod
    def get_right_lane(self, curr: ILane) -> ILane:
        """
        :param curr: a lane in the road section
        :return: the lane to the right of curr
        """
        pass

    @abstractmethod
    def get_lane_from_right(self, index: int) -> ILane:
        pass

    @property
    @abstractmethod
    def max_speed(self) -> Real:
        """
        :return: the max allowed speed of the road
        """
        pass

    @property
    @abstractmethod
    def points_pairs(self)->List[Tuple[Point, Point]]:
        pass
