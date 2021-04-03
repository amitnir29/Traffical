from __future__ import annotations

from typing import NamedTuple, Optional, Union, NewType
from math import inf, sqrt
from numbers import Real


class Point:
    def __init__(self, x: Real, y: Real):
        self.__x: Real = x
        self.__y: Real = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def distance(self, other: Point):
        """
        :param other: other point
        :return: distance between self and other point
        """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
