from typing import List, Tuple

from geometry.point import Point
import lanes.lane as lane
import roadsections.i_road_section as irs


class UnnotifiedLane(lane.Lane):
    def __init__(self, road: irs.IRoadSection, coordinates: List[Tuple[Point, Point]]):
        super().__init__(road, coordinates)
