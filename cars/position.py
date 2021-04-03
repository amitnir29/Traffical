from numbers import Real

from geometry.point import Point


class Position(Point):
    def __init__(self, x: Real, y: Real):
        super().__init__(x, y)
