from __future__ import annotations

from math import inf, sqrt
from typing import Optional, Tuple

from server.geometry.point import Point

EPSILON = 1e-6


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.__p1: Point = p1
        self.__p2: Point = p2
        m, b = self.__calc_mb()
        self.__m = m
        self.__b = b
        self.__min_x = min(p1.x, p2.x)
        self.__max_x = max(p1.x, p2.x)
        self.__min_y = min(p1.y, p2.y)
        self.__max_y = max(p1.y, p2.y)

    @property
    def p1(self) -> Point:
        return self.__p1

    @property
    def p2(self) -> Point:
        return self.__p2

    @property
    def m(self) -> float:
        return self.__m

    @property
    def b(self):
        return self.__b

    def value_at_x(self, x):
        return self.m * x + self.b

    def __calc_mb(self) -> (float, float):
        """
        :return: m,b values for the line equation, such that y=mx+b
        """
        if self.p1.x == self.p2.x:
            m = inf
        else:
            m = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
        b = (self.p1.y - self.p1.x * m)
        return m, b

    def __is_in_y_range(self, y: float):
        """
        :param y: input y value
        :return: True if y is between the min y and max y of the line
        """
        return self.__min_y - EPSILON <= y <= self.__max_y + EPSILON

    def __is_in_x_range(self, x: float):
        """
        :param x: input y value
        :return: True if x is between the min x and max x of the line
        """
        return self.__min_x - EPSILON <= x <= self.__max_x + EPSILON

    def __is_in_range(self, x: float, y: float):
        """
        :param x: input x value
        :param y: input y value
        :return: True if the point represented by (x,y) is in the range of the line
        """
        return self.__is_in_x_range(x) and self.__is_in_y_range(y)

    def contains_point(self, p: Point):
        """
        :param p: a point
        :return: True if the point is on the line
        """
        if not self.__is_in_range(p.x, p.y):
            return False
        if self.m == inf:
            return True
        return p.y == self.value_at_x(p.x)

    def is_intersecting(self, other: Line) -> bool:
        """
        :param other: another line
        :return: True if the lines intersect
        """
        if self.m == other.m:
            # they are parallel, so they are either no connected at all, or have a certain overlap
            return self.contains_point(other.p1) or self.contains_point(other.p2) \
                   or other.contains_point(self.p1) or other.contains_point(self.p2)
        # else, they are not parallel, they either intersect in a single point, or do not intersect
        # if self is parallel to the y axis. we know other is for sure not, because they are not parallel
        if self.m == inf:
            # get the y of the other line at the x value of the inf line
            line1_x = self.p1.x
            inter_y = other.m * line1_x + other.b
            return self.__is_in_range(line1_x, inter_y) and other.__is_in_range(line1_x, inter_y)
        # if other is parallel to the y axis. we know self is for sure not, because they are not parallel
        elif other.m == inf:
            # get the y of the other line at the x value of the inf line
            line2_x = other.p1.x
            inter_y = self.value_at_x(line2_x)
            return self.__is_in_range(line2_x, inter_y) and other.__is_in_range(line2_x, inter_y)
        # calculate the x,y of the intersection based on the known formula, but the point may be anywhere in the grid
        inter_x: float = (other.b - self.b) / (self.m - other.m)
        inter_y: float = self.value_at_x(inter_x)
        # return True if the point of intersection is exactly on the line cuts that are self and other
        return self.__is_in_range(inter_x, inter_y) and other.__is_in_range(inter_x, inter_y)

    def intersection_point(self, other: Line) -> Optional[Point]:
        """
        intersecting point between lines.
        :param other: other line
        :return: intersecting point of the lines. None if no intersection
        """
        if not self.is_intersecting(other):
            return None
        if self.m == other.m:
            # return a point only if the line match at exactly one end, no overlapping allowed
            if self.p1 == other.p1:
                if self.p2 != other.p2:
                    return self.p1
                else:
                    return None
            if self.p2 != other.p2:
                return None
            else:
                return self.p2
        # else, regular calculation
        inter_x = (other.b - self.b) / (other.m - self.m)
        inter_y = self.value_at_x(inter_x)
        return Point(inter_x, inter_y)

    def intersection_point_infinite(self, other: Line) -> Optional[Point]:
        """
        intersecting point between lines, but do not treat the length of the lines, just the (m,b).
        returned point may not be on the lines.
        :param other: the other line
        :return: intersetion point if lines were infinite to both sides
        """
        if self.m == other.m:
            # parallel lines never meet
            return None
        # m1x+b1=m2x+b2 -> x = (m1-m2)/(b2-b1)
        x = (self.m - other.m) / (other.b - self.b)
        return Point(x, self.m * x + self.b)

    def length(self) -> float:
        """
        :return: length of the line
        """
        return self.p1.distance(self.p2)

    def __repr__(self):
        return repr(self.p1) + "<->" + repr(self.p2)

    def split_by_ratio(self, r):
        """
        get a point s.t. the distance between it to p1, divided by the total line length, is r
        :param r: the ratio
        :return: the point
        """
        new_x = r * self.p2.x + (1 - r) * self.p1.x
        new_y = r * self.p2.y + (1 - r) * self.p1.y
        return Point(new_x, new_y)

    def middle(self) -> Point:
        """
        :return: middle Point of the line
        """
        return self.split_by_ratio(1 / 2)

    def distance_of_point(self, p: Point):
        """
        :param p: input point
        :return: distance of the point from self
        """
        if self.contains_point(p):
            return 0
        # else, get the formula
        new_line_m = -1 / self.m
        new_line = Line(p, Point(p.x + 1, p.y + new_line_m))
        cross_point = self.intersection_point_infinite(new_line)
        return p.distance(cross_point)

    def point_at_distance_from_point(self, source: Point, distance: float) -> Optional[Tuple[Point, Point]]:
        """
        return the 2 points that are on the line and also with input distance from input point
        :param source: input point
        :param distance: input distance
        :return: the 2 result points
        """
        """
        x^2*(1+m^2)+x*(2mb-2*s.x*-2*m*s.y)+(s.x^2+s.y^2+b^2-d^2-2*b*s.y)=0
        """
        if distance < self.distance_of_point(source):
            return None
        ns_a = 1 + self.m ** 2
        ns_b = 2 * self.m * self.b - 2 * source.x - 2 * self.m * source.y
        ns_c = source.x ** 2 + source.y ** 2 + self.b ** 2 - distance ** 2 - 2 * self.b * source.y

        delta = ns_b ** 2 - 4 * ns_a * ns_c
        x1 = (-ns_b + sqrt(delta)) / (2 * ns_a)
        x2 = (-ns_b - sqrt(delta)) / (2 * ns_a)
        return Point(x1, self.value_at_x(x1)), Point(x2, self.value_at_x(x2))
