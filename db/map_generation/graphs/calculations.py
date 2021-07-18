from math import sqrt, degrees, pi, sin, radians
from typing import List, Optional, Tuple

from server.geometry.point import Point
from server.geometry.triangle import area_by_3_sides, law_of_cosines_angle, law_of_cosines, is_valid_triangle

ROUND_FAC = 5
EPSILON = 10 ** (-ROUND_FAC)


def get_diagonals(x1, x2, x3, x4, angle_12) -> Optional[Tuple[float, float]]:
    """
    get diagonals of a quadrilateral based on the length of the 4 sides and an angle.
    :param angle_12: the angle between x1 and x2
    :return: the length of the diagonals: (p(x2,x3)<->p(x4,x1)), (p(x1,x2)<->p(x3,x4)). None if impossible
    """
    # law of cosines
    d1 = law_of_cosines(x1, x2, angle_12)
    if not is_valid_triangle(x1, x2, d1):
        # raise Exception(f"x1: {x1}, x2: {x2}, d1: {d1} do not create a valid triangle")
        return None
    if not is_valid_triangle(x3, x4, d1):
        # raise Exception(f"x3: {x3}, x4: {x4}, d1: {d1} do not create a valid triangle")
        return None
    angle_x2d1 = law_of_cosines_angle(x1, x2, d1)
    angle_x3d1 = law_of_cosines_angle(x4, x3, d1)
    d2 = law_of_cosines(x2, x3, angle_x2d1 + angle_x3d1)
    if not is_valid_triangle(x2, x3, d2):
        # raise Exception(f"x2: {x2}, x3: {x3}, d2: {d2} do not create a valid triangle")
        return None
    if not is_valid_triangle(x1, x4, d2):
        # raise Exception(f"x1: {x1}, x4: {x4}, d2: {d2} do not create a valid triangle")
        return None
    return d1, d2


def get_diagonal_parts(x1, x2, x3, x4, d1, d2) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    calculate the length of each part of each diagonal
    :return: (d1_px1x4 part, d1_px2x3 part),(d2_px1x2 part, d2_px3x4 part)
    """
    a_x1d1 = law_of_cosines_angle(x2, x1, d1)
    a_x1d2 = law_of_cosines_angle(x4, x1, d2)
    a_d1d2 = pi - a_x1d1 - a_x1d2

    d1_px1x4 = x1 * sin(a_x1d2) / sin(a_d1d2)
    d2_px1x2 = x1 * sin(a_x1d1) / sin(a_d1d2)
    if d1_px1x4 > d1 or d1_px1x4 < 0:
        raise Exception(f"error in get_diagonal_parts: d1={d1}, but d1_px1x4={d1_px1x4}")
    if d2_px1x2 > d2 or d2_px1x2 < 0:
        raise Exception(f"error in get_diagonal_parts: d2={d2}, but d2_px1x2={d2_px1x2}")
    return (d1_px1x4, d1 - d1_px1x4), (d2_px1x2, d2 - d2_px1x2)


def calc_junc_points_from_lengths(x1, x2, x3, x4, d1, d2, center) -> List[Point]:
    """
    calculate the 4 junction coordinates from the length of the junction sides and diagonals.
    :return: 4 junction points
    """
    # set x1 parallel to y axis
    diagonals_parts = get_diagonal_parts(x1, x2, x3, x4, d1, d2)
    d1_px1x4, d1_px2x3, d2_px1x2, d2_px3x4 \
        = diagonals_parts[0][0], diagonals_parts[0][1], diagonals_parts[1][0], diagonals_parts[1][1]
    # get area of the triangle created by center and two x1 points
    s_x1d1d2 = area_by_3_sides(x1, d1_px1x4, d2_px1x2)
    # now get the height to x1
    x1_delta_x = round(2 * s_x1d1d2 / x1, ROUND_FAC)
    # get height of p1:
    p1_delta_y = round(sqrt(round(d2_px1x2 ** 2 - x1_delta_x ** 2, ROUND_FAC)), ROUND_FAC)
    # get height (down) of p4:
    p4_delta_y = round(sqrt(round(d1_px1x4 ** 2 - x1_delta_x ** 2, ROUND_FAC)), ROUND_FAC)
    # now we have p1, p4:
    p1 = Point(center.x - x1_delta_x, center.y - p1_delta_y)
    p4 = Point(center.x - x1_delta_x, center.y + p4_delta_y)
    # now get p2,p3 using calculation of s_x1x2d1->p2, s_x1x4d2->p3
    # p2.x:
    s_x1x2d1 = round(area_by_3_sides(x1, x2, d1), ROUND_FAC)
    p2_delta_x_from_p1 = round(2 * s_x1x2d1 / x1, ROUND_FAC)
    # p2.y:
    p2_delta_y_from_p1 = round(sqrt(round(x2 ** 2 - p2_delta_x_from_p1 ** 2, ROUND_FAC)), ROUND_FAC)
    angle_12 = round(degrees(law_of_cosines_angle(d1, x1, x2)), ROUND_FAC)
    if angle_12 > 90:
        p2_delta_y_from_p1 = -p2_delta_y_from_p1  # p2 is above p1
    p2 = Point(p1.x + p2_delta_x_from_p1, p1.y + p2_delta_y_from_p1)
    # p3.x:
    s_x1x4d2 = round(area_by_3_sides(x1, x4, d2), ROUND_FAC)
    p3_delta_x_from_p4 = round(2 * s_x1x4d2 / x1, ROUND_FAC)
    # p3.y:
    p3_delta_y_from_p4 = round(sqrt(round(x4 ** 2 - p3_delta_x_from_p4 ** 2, ROUND_FAC)), ROUND_FAC)
    angle_14 = round(degrees(law_of_cosines_angle(d2, x1, x4)), ROUND_FAC)
    if angle_14 < 90:
        p3_delta_y_from_p4 = -p3_delta_y_from_p4  # p3 is above p4
    p3 = Point(p4.x + p3_delta_x_from_p4, p4.y + p3_delta_y_from_p4)

    return [p1, p2, p3, p4]


def all_degrees_limited(x1, x2, x3, x4, a_12, max_degree=radians(180)) -> bool:
    """
    :return: True if all degrees are less than the input max_degree
    """
    diagonals = get_diagonals(x1, x2, x3, x4, a_12)
    if diagonals is None:
        return False
    d1, d2 = diagonals
    if not is_valid_triangle(x1, x2, d1) or not is_valid_triangle(x3, x4, d1) \
            or not is_valid_triangle(x2, x3, d2) or not is_valid_triangle(x1, x4, d2):
        return False
    """
    look at each angle as the sum of its 2 parts - there is a diagonal that splits it.
    if not convex, the calculations do not make sense:
        we get more than 360 deg total, 
        we get angles>180,
    because the triangles do not match, some of them will have a diagonal as main in law_of_cosines_angle
    """
    p1a1 = law_of_cosines_angle(x4, x1, d2)
    p1a2 = law_of_cosines_angle(x3, x2, d2)
    if p1a1 + p1a2 > max_degree:
        return False
    p2a1 = law_of_cosines_angle(x1, x2, d1)
    p2a2 = law_of_cosines_angle(x4, x3, d1)
    if p2a1 + p2a2 > max_degree:
        return False
    p3a1 = law_of_cosines_angle(x2, x3, d2)
    p3a2 = law_of_cosines_angle(x1, x4, d2)
    if p3a1 + p3a2 > max_degree:
        return False
    p4a1 = law_of_cosines_angle(x3, x4, d1)
    p4a2 = law_of_cosines_angle(x2, x1, d1)
    if p4a1 + p4a2 > max_degree:
        return False
    return True
