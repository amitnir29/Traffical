from dataclasses import dataclass
from typing import Tuple, List

from db_dataclasses.road_lane import RoadLane
from geometry.point import Point


@dataclass(init=True, repr=True)
class JunctionData:
    idnum: int
    coordinates: List[Point]
    goes_to: List[Tuple[RoadLane, RoadLane]]
    traffic_lights: List[List[RoadLane]]
    num_traffic_lights: int
