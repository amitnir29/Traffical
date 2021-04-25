from typing import List, Tuple

from geometry.point import Point
from lanes.lane import Lane
from roadsections.i_road_section import IRoadSection


class UnnotifiedLane(Lane):
    def __init__(self, road: IRoadSection, coordinates: List[Tuple[Point, Point]], vertical: bool = False):
        super().__init__(road, coordinates, vertical)
