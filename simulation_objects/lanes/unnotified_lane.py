from typing import List, Tuple

from simulation_objects.geometry.point import Point
import simulation_objects.lanes.lane as lane
import simulation_objects.roadsections.i_road_section as irs


class UnnotifiedLane(lane.Lane):
    def __init__(self, road: irs.IRoadSection, coordinates: List[Tuple[Point, Point]]):
        super().__init__(road, coordinates)
