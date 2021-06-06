from dataclasses import dataclass
from typing import Tuple, List

from server.geometry.point import Point


@dataclass(init=True, repr=True)
class RoadData:
    idnum: int
    coordinates: List[Tuple[Point, Point]]
    num_lanes: int
    max_speed: float
