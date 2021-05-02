from typing import List, Tuple

from server.geometry.point import Point
import server.simulation_objects.lanes.lane as lane
import server.simulation_objects.roadsections.i_road_section as irs


class UnnotifiedLane(lane.Lane):
    def __init__(self, road: irs.IRoadSection, coordinates: List[Tuple[Point, Point]]):
        super().__init__(road, coordinates)
