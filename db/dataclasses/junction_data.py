from dataclasses import dataclass, field
from typing import Tuple, List

from db.dataclasses.road_lane import RoadLane
from server.geometry.point import Point


@dataclass(init=True, repr=True)
class JunctionData:
    idnum: int
    coordinates: List[Point]
    goes_to: List[Tuple[RoadLane, RoadLane]]
    traffic_lights: List[List[RoadLane]] = field(default_factory=list)
    traffic_lights_coords: List[Point] = field(default_factory=list)
    num_traffic_lights: int = 0
