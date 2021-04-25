from abc import ABC, abstractmethod
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
    def get_lane(self, index: int) -> ILane:
        """
        :param index: index of lane from left, 0 based.
        :return: the lane in that index
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
