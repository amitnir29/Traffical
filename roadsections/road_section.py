from typing import List, Tuple

from geometry.point import Point
from lanes.i_lane import ILane
from roadsections.i_road_section import IRoadSection


class RoadSection(IRoadSection):

    def __init__(self, new_lanes: List[ILane]):
        self.__lanes = new_lanes
        self.__coordinates: List[Tuple[Point, Point]]  # TODO
