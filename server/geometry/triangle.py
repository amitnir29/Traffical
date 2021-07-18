from math import sqrt, cos, acos


def law_of_cosines(a, b, alpha):
    """
    implementation of law of cosines
    alpha is in radians
    """
    inside_sqrt = a ** 2 + b ** 2 - 2 * a * b * cos(alpha)
    if inside_sqrt < 0:
        raise Exception(f"law of cosines error, inside_sqrt<0. a:{a}, b:{b}, alpha:{alpha}, inside_sqrt: {inside_sqrt}")
    return sqrt(inside_sqrt)


def law_of_cosines_angle(main, r1, r2):
    """
    implementation of law of cosines to get angle.
    angle returned is in radians
    """
    return acos((r1 ** 2 + r2 ** 2 - main ** 2) / (2 * r1 * r2))


def is_valid_triangle(a, b, c):
    """
    :return: True if a triangle can be built from these length
    """
    return a > 0 and b > 0 and c > 0 and a + b > c and a + c > b and b + c > a


def area_by_3_sides(a, b, c) -> float:
    """
    :return: area of a triangle
    """
    # calculate the semi-perimeter
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))
