from __future__ import annotations

from math import sqrt


class Point:
    def __init__(self, x: float, y: float):
        self.__x: float = x
        self.__y: float = y

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
